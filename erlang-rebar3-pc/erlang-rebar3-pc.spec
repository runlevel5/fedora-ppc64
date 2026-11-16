%global realname pc

Name:		erlang-rebar3-%{realname}
Version:	1.15.0
Release:	10%{?dist}
Summary:	A port compiler for Rebar3
License:	MIT
URL:		https://github.com/blt/port_compiler
VCS:		git:%{url}.git
Source:		%{url}/archive/v%{version}/port_compiler-%{version}.tar.gz
BuildArch:	noarch
BuildSystem:	rebar3
# Required for port compiling but cannot be picked up automatically yet
Requires:	erlang-erl_interface

%description
This plugin is intended to replicate the Rebar2 support for compiling native
code. It is not a drop-in replacement in terms of command-line interface but
the exact configuration interface in projects' rebar.configs have been
preserved.

%files
%license LICENSE
%doc README.md
%{erlang_appdir}

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 1.15.0-10
- Rebuild for Erlang/OTP 29

* Mon Oct 19 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.15.0-10
- Switch to declarative build (f44+)

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 07 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.15.0-5
- Cosmetic changes

* Mon Jul 29 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.15.0-4
- Add requires

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 06 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.15.0-2
- Typo

* Thu Jun 06 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.15.0-1
- port_compiler ver. 1.15.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 06 2022 Peter Lemenkov <lemenkov@gmail.com> - 1.14.0-1
- Initial commit
