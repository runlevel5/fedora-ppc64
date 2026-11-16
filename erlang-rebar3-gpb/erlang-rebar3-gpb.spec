%global realname rebar3_gpb_plugin

Name:		erlang-rebar3-gpb
Version:	3.0.1
Release:	2%{?dist}
Summary:	A protobuf compiler for Rebar3
License:	MIT
URL:		https://github.com/lrascao/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	erlang-gpb
BuildRequires:	erlang-rebar3

%description
A Rebar3 plugin for automatically compiling .proto files using the gpb protobuf
compiler.

%prep
%autosetup -p1 -n %{realname}-%{version}

%build
%{erlang3_compile}

%check
%{erlang3_test}

%install
%{erlang3_install}

%files
%license LICENSE
%doc README.md
%{erlang_appdir}

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 3.0.1-2
- Rebuild for Erlang/OTP 29

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Tue Jun 02 2026 Peter Lemenkov <lemenkov@gmail.com> - 3.0.1-1
- rebar3_gpb ver. 3.0.1

* Sat May 30 2026 Peter Lemenkov <lemenkov@gmail.com> - 3.0.0-1
- rebar3_gpb ver. 3.0.0

* Sun Feb 15 2026 Peter Lemenkov <lemenkov@gmail.com> - 2.23.8-1
- rebar3_gpb ver. 2.33.8

* Fri Feb 06 2026 Peter Lemenkov <lemenkov@gmail.com> - 2.23.6-1
- rebar3_gpb ver. 2.33.6

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 07 2024 Peter Lemenkov <lemenkov@gmail.com> - 2.23.2-2
- Cosmetic changes

* Tue Nov 05 2024 Peter Lemenkov <lemenkov@gmail.com> - 2.23.2-1
- Initial build
