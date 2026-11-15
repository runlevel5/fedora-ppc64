%global realname riak_ensemble

Name:		erlang-%{realname}
Version:	3.0.10
Release:	18%{?dist}
Summary:	Multi-Paxos framework in Erlang
License:	Apache-2.0
URL:		https://github.com/basho/%{realname}
VCS:		git:%{url}.git
Source:		%{url}/archive/riak_kv-%{version}/%{realname}-%{version}.tar.gz
Patch:		erlang-riak_ensemble-0001-We-do-not-have-eqc-rebar3-plugin-yet.patch
Patch:		erlang-riak_ensemble-0002-Do-not-use-a-keyword-reserved-in-Erlang-27.patch
# Builds with OTP 29
Patch:		erlang-riak_ensemble-0003-Do-not-warn-about-catch-and-gen_fsm-deprecated-in-OTP-29.patch
BuildRequires:	erlang-eleveldb
BuildRequires:	erlang-lager
BuildRequires:	erlang-rebar3
BuildRequires:	erlang-rebar3-pc
BuildRequires:	gcc

%description
A consensus library that supports creating multiple consensus groups
(ensembles). Each ensemble is a separate Multi-Paxos instance with its own
leader, set of members, and state.

Each ensemble also supports an extended API that provides consistent key/value
operations. Conceptually, this is identical to treating each key as a separate
Paxos entity. However, this isn't accomplished by having each key maintain its
own Paxos group. Instead, an ensemble emulates per-key consensus through a
combination of per-key and per-ensemble state.

%prep
%autosetup -p1 -n %{realname}-riak_kv-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE
%doc doc/ README.md
%{erlang_appdir}/

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 3.0.10-18
- Do not warn about catch and the callbacks of gen_fsm, which OTP 29
  deprecates, as warnings are errors

* Fri Aug 07 2026 Peter Lemenkov <lemenkov@gmail.com> - 3.0.10-18
- Fix FTBFS with Erlang 27

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Fri Feb 27 2026 Peter Lemenkov <lemenkov@gmail.com> - 3.0.10-16
- Shorten gitignore

* Fri Feb 27 2026 Peter Lemenkov <lemenkov@gmail.com> - 3.0.10-15
- Rebuild with fixed Rebar3

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 17 2024 Peter Lemenkov <lemenkov@gmail.com> - 3.0.10-10
- Add ppc64le to ExcludeArch

* Tue May 07 2024 Peter Lemenkov <lemenkov@gmail.com> - 3.0.10-9
- USe SPDX tag

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.0.10-2
- Rebuild for Erlang 25

* Thu Jun 23 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.0.10-1
- Ver. 3.0.10

* Thu Apr  7 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.0.0-1
- Ver. 3.0.0
- Switch to rebar3
- Enable tests

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Peter Lemenkov <lemenkov@gmail.com> - 2.1.9-5
- Rebuild for Erlang 22

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 21 2019 Peter Lemenkov <lemenkov@gmail.com> - 2.1.9-3
- Rebuild for Erlang 21

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 06 2018 Peter Lemenkov <lemenkov@gmail.com> - 2.1.9-1
- Ver. 2.1.9

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.1.8-6
- Rebuild against the noarch lager (#1589611).
- BuildRequire gcc.

* Wed Mar 21 2018 Peter Lemenkov <lemenkov@gmail.com> - 2.1.8-5
- Rebuild for Erlang 20 (with proper builddeps)

* Tue Mar 06 2018 Peter Lemenkov <lemenkov@gmail.com> - 2.1.8-4
- Fix FTBFS with Erlang 20

* Fri Feb 23 2018 Peter Lemenkov <lemenkov@gmail.com> - 2.1.8-3
- Rebuild for Erlang 20

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 21 2017 Peter Lemenkov <lemenkov@gmail.com> - 2.1.7-1
- Ver. 2.1.7

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 17 2016 Peter Lemenkov <lemenkov@gmail.com> - 2.1.2-4
- Fix FTBFS with Erlang 19

* Sun Aug 07 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.1.2-3
- Rebuild for Erlang 19

* Thu Jun  2 2016 Peter Lemenkov <lemenkov@gmail.com> - 2.1.2-2
- Re-enable debuginfo generation disabled by mistake

* Wed Mar 16 2016 Peter Lemenkov <lemenkov@gmail.com> - 2.1.2-1
- Ver. 2.1.2

