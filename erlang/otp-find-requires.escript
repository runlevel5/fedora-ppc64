#!/usr/bin/env escript
%% -*- erlang -*-

%% SPDX-FileCopyrightText: © 2026 Peter Lemenkov
%% SPDX-License-Identifier: MIT

%% RPM dependency generator for the subpackages of Erlang/OTP itself, using
%% the multifile protocol. Every BEAM file of a subpackage requires the
%% subpackages of the other OTP applications whose exported functions it
%% calls, resolved against the buildroot:
%%
%%   erlang-APP(ISA) = VERSION-RELEASE
%%
%% Calls the compiler can't see (apply/3, rpc, module names computed at
%% runtime) are deliberately not followed: OTP uses them for optional
%% dependencies.
%%
%% Usage: otp-find-requires.escript LIBDIR NAME VERSION-RELEASE [ISA]
%%        otp-find-requires.escript --spec ROOT
%%        otp-find-requires.escript --abi
%%        otp-find-requires.escript --app
%% The second form prints the Requires lines for the spec file, from an
%% unpacked tree (a buildroot, or the RPMs extracted into ROOT).
%%   LIBDIR is %{_libdir}/erlang/lib, NAME is %{name}, ISA is %{?_isa}
%% The third form is a Provides generator for the emulator binary: it prints
%% the driver and NIF API versions of the runtime it runs on, which during the
%% build is the emulator being packaged, and every older minor version of
%% them, as the emulator loads drivers and NIF libraries built for the same
%% major version and an older minor one.
%% The fourth form is a multifile Provides generator: every application
%% resource file APP/ebin/NAME.app provides erlang(NAME) = VSN, in the same
%% form as erlang-find-provides of erlang-rpm-macros.

-mode(compile).

main(["--app"]) ->
    app_provides();
main(["--abi"]) ->
    drain(),
    abi_provides("erl_drv_version", erlang:system_info(driver_version)),
    abi_provides("erl_nif_version", erlang:system_info(nif_version));
main(["--spec", Root]) ->
    [LibDir | _] = filelib:wildcard(Root ++ "/usr/lib*/erlang/lib"),
    Modules = index(LibDir),
    Apps = maps:fold(
             fun(_, Beam, Acc) ->
                     Deps = requires(Modules, Beam),
                     maps:update_with(application(Beam),
                                      fun(S) -> sets:union(S, Deps) end, Deps, Acc)
             end, #{}, Modules),
    lists:foreach(
      fun(App) ->
              io:format("%package ~s~n", [App]),
              [io:format("Requires: %{name}-~s%{?_isa} = %{version}-%{release}~n", [Dep])
               || Dep <- lists:sort(sets:to_list(maps:get(App, Apps)))]
      end, lists:sort(maps:keys(Apps)));
main([LibDir, Name, EVR | Rest]) ->
    ISA = case Rest of [I | _] -> I; [] -> "" end,
    Root = string:trim(os:getenv("RPM_BUILD_ROOT", ""), trailing, "/"),
    generate(index(Root ++ LibDir), Name, EVR, ISA);
main(_) ->
    Self = escript:script_name(),
    io:format(standard_error,
              "Usage: ~s LIBDIR NAME VERSION-RELEASE [ISA]~n"
              "       ~s --spec ROOT~n"
              "       ~s --abi~n"
              "       ~s --app~n", [Self, Self, Self, Self]),
    halt(1).

abi_provides(Name, Version) ->
    [Major, Minor] = string:split(Version, "."),
    [io:format("erlang(~s) = ~s.~b~n", [Name, Major, M])
     || M <- lists:seq(0, list_to_integer(Minor))].

app_provides() ->
    case io:get_line(standard_io, "") of
        eof ->
            ok;
        Line ->
            File = string:trim(Line, trailing, "\n"),
            case lists:reverse(filename:split(File)) of
                [AppFile, "ebin" | _] when length(AppFile) > 4 ->
                    case filename:extension(AppFile) of
                        ".app" ->
                            Name = filename:basename(AppFile, ".app"),
                            {ok, [{application, _, Props}]} = file:consult(File),
                            io:format(";~s~n", [File]),
                            case proplists:get_value(vsn, Props) of
                                undefined -> io:format("erlang(~s)~n", [Name]);
                                Vsn -> io:format("erlang(~s) = ~s~n", [Name, rpm_version(Vsn)])
                            end;
                        _ ->
                            ok
                    end;
                _ ->
                    ok
            end,
            app_provides()
    end.

%% An application version as an RPM version, as erlang-find-provides does:
%% '-' starts a pre-release in semantic versioning and '~' sorts the same way
%% in RPM; other characters RPM doesn't allow become '_'.
rpm_version(Vsn) ->
    [case C of
         $- -> $~;
         _ when C >= $a, C =< $z; C >= $A, C =< $Z; C >= $0, C =< $9 -> C;
         _ -> case lists:member(C, "._+~^") of true -> C; false -> $_ end
     end || C <- Vsn].

%% rpm writes the file name to the generator's stdin, so read it all.
drain() ->
    case io:get_line(standard_io, "") of
        eof -> ok;
        _ -> drain()
    end.

generate(Modules, Name, EVR, ISA) ->
    case io:get_line(standard_io, "") of
        eof ->
            ok;
        Line ->
            File = string:trim(Line, trailing, "\n"),
            case filename:extension(File) of
                ".beam" ->
                    case lists:sort(sets:to_list(requires(Modules, File))) of
                        [] ->
                            ok;
                        Deps ->
                            io:format(";~s~n", [File]),
                            [io:format("~s-~s~s = ~s~n", [Name, App, ISA, EVR]) || App <- Deps]
                    end;
                _ ->
                    ok
            end,
            generate(Modules, Name, EVR, ISA)
    end.

%% Module name -> BEAM file, for every application under LIBDIR.
index(LibDir) ->
    maps:from_list([{list_to_atom(filename:basename(B, ".beam")), B}
                    || B <- filelib:wildcard(LibDir ++ "/*/ebin/*.beam")]).

%% The application a BEAM file belongs to: lib/APP-VSN/ebin/MOD.beam.
application(Beam) ->
    AppVsn = filename:basename(filename:dirname(filename:dirname(Beam))),
    string:join(lists:droplast(string:split(AppVsn, "-", all)), "-").

%% The other applications whose exported functions a BEAM file calls.
requires(Modules, File) ->
    Own = application(File),
    sets:from_list(
      [App || {M, F, A} <- chunk(File, imports),
              Beam <- [maps:get(M, Modules, undefined)],
              Beam =/= undefined,
              App <- [application(Beam)],
              App =/= Own,
              lists:member({F, A}, exports(Beam))]).

exports(Beam) ->
    case get({exports, Beam}) of
        undefined ->
            E = chunk(Beam, exports),
            put({exports, Beam}, E),
            E;
        E ->
            E
    end.

%% An unreadable BEAM file fails the build rather than losing its Requires.
chunk(File, Name) ->
    {ok, {_, [{Name, List}]}} = beam_lib:chunks(File, [Name]),
    List.
