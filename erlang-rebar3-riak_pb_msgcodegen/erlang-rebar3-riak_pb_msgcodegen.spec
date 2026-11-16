%global realname riak_pb_msgcodegen

Name:		erlang-rebar3-%{realname}
Version:	1.0.0
Release:	8%{?dist}
Summary:	A riak_pb message compiler for Rebar3
License:	BSD-3-Clause
URL:		https://github.com/basho/%{realname}
VCS:		git:%{url}.git
Source:		%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildArch:	noarch
BuildSystem:	rebar3

%description
%{summary}.

%files
%license LICENSE
%doc README.md
%{erlang_appdir}

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 1.0.0-8
- Rebuild for Erlang/OTP 29

* Mon Oct 19 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-8
- Mostly cosmetic fix

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Fri Mar 13 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-6
- Switch to declarative build (f45+)

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 07 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-2
- Cosmetic changes

* Thu Nov 07 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-1
- Initial build
