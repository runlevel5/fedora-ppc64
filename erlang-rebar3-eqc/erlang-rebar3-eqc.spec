%global realname eqc_rebar

Name:		erlang-rebar3-eqc
Version:	1.1.0
Release:	1%{?dist}
Summary:	Rebar3 plugin for Quviq's QuickCheck
License:	Apache-2.0
URL:		https://github.com/Quviq/eqc-rebar
VCS:		git:%{url}.git
Source:		%{url}/archive/%{version}/eqc-rebar-%{version}.tar.gz
Patch:		erlang-rebar3-eqc-0001-Fix-version.patch
Patch:		erlang-rebar3-eqc-0002-We-don-t-have-rebar_api-warn-1.patch
BuildArch:	noarch
BuildRequires:	erlang-rebar3

%description
A Rebar3 plugin for using Quviq's Erlang QuickCheck (eqc) in rebar3 projects.

%prep
%autosetup -p1 -n eqc-rebar-%{version}

%build
%{erlang3_compile}

%check
%{erlang3_test}

%install
%{erlang3_install}

%files
%license LICENSE
%doc README.md
## These messages can be ignored. They just calls to a EQC API.
# ERROR: Cant find eqc:version/0 while processing '.../ebin/eqc_rebar_prv.beam'
# ERROR: Cant find eqc:start/0 while processing '.../ebin/eqc_rebar_prv.beam'
# ERROR: Cant find eqc:module/2 while processing '.../ebin/eqc_rebar_prv.beam'
# ERROR: Cant find eqc:force_registration/1 while processing '.../ebin/eqc_rebar_prv.beam'
%{erlang_appdir}

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 1.1.0-1
- Rebuild for Erlang/OTP 29

* Wed Sep 02 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.1.0-1
- Initial package
