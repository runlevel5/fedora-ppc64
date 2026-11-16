%global srcname iconv
%global p1_utils_ver 1.0.19

Name:       erlang-%{srcname}
Version:    1.0.13
Release:    14%{?dist}
Summary:    Fast encoding conversion library for Erlang / Elixir
License:    Apache-2.0
URL:        https://github.com/processone/%{srcname}
VCS:        scm:git:%{url}.git
Source0:    %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
Provides:   erlang-p1_iconv = %{version}-%{release}
Obsoletes:  erlang-p1_iconv <= 1.0.0-2
BuildRequires: gcc
BuildRequires: erlang-p1_utils >= %{p1_utils_ver}
BuildRequires: erlang-rebar3
BuildRequires: erlang-rebar3-pc
Requires: erlang-p1_utils >= %{p1_utils_ver}

%description
Erlang bindings for libiconv. This is used by ejabberd.

%prep
%autosetup -n %{srcname}-%{version}

%build
%configure --enable-nif
%{erlang3_compile}

%install
%{erlang3_install}

install -d $RPM_BUILD_ROOT%{_erllibdir}/%{srcname}-%{version}/priv/lib
install -pm755 priv/lib/iconv.so $RPM_BUILD_ROOT%{_erllibdir}/%{srcname}-%{version}/priv/lib/

%check
%{erlang3_test}

%files
%license LICENSE.txt
%doc README.md
%{erlang_appdir}

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 1.0.13-14
- Rebuild for Erlang/OTP 29

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Wed Mar 18 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.0.13-13
- Rebuild with fixed rebar3

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 19 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.0.13-8
- Rebuild with a fixed Erlang macros

* Wed Apr 17 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.0.13-7
- Switch to SPDX tag

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Peter Lemenkov <lemenkov@gmail.com> - 1.0.13-1
- Update to 1.0.13

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 05 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.11-1
- Update to 1.0.11 (#1858904).
- Fix FTBFS (#1863504).
- https://github.com/processone/iconv/blob/1.0.11/CHANGELOG.md

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 22 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.10-5
- Rebuild for Erlang 22 (#1775733).

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 21 2019 Peter Lemenkov <lemenkov@gmail.com> - 1.0.10-3
- Rebuild for Erlang 21

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

