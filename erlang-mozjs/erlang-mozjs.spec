%global realname mozjs

Name: erlang-%{realname}
Version: 2.0.1
Release: 5%{?dist}
License: Apache-2.0
Summary: A NIF module for Erlang to Mozilla's Spidermonkey Javascript runtime
URL:     https://github.com/erlang-mozjs/erlang-mozjs
VCS:     git:%{url}.git
Source0: %{url}/archive/%{version}/erlang-%{realname}-%{version}.tar.gz
# Builds with OTP 29
Patch: erlang-mozjs-0001-Do-not-warn-about-catch-deprecated-in-OTP-29.patch
BuildRequires: erlang-jsx
BuildRequires: erlang-rebar3
BuildRequires: erlang-rebar3-pc
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: mozjs140-devel
Obsoletes: erlang-js < 2.0.0
Provides: erlang-js%{?_isa} = %{version}-%{release}

%description
A NIF library that embeds Mozilla's SpiderMonkey JavaScript engine in Erlang.
Originally created to facilitate usage of Riak's MapReduce by non-Erlang
programmers, it supports multiple concurrent JavaScript VMs, runtime evaluation
of JavaScript code, and invocation of JavaScript functions.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE
%doc README.md
%{erlang_appdir}

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 2.0.1-5
- Do not warn about catch, which OTP 29 deprecates, as warnings are errors

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Sat Apr 18 2026 Peter Lemenkov <lemenkov@gmail.com> - 2.0.1-4
- Allowed committers

* Sat Apr 18 2026 Peter Lemenkov <lemenkov@gmail.com> - 2.0.1-3
- Do a fast-forward

* Tue Apr 14 2026 Peter Lemenkov <lemenkov@gmail.com> - 2.0.1-2
- Use PackIt integration

* Tue Apr 14 2026 Peter Lemenkov <lemenkov@gmail.com> - 2.0.1-1
- initial build
