%global srcname esip
%global fast_tls_ver 1.1.26
%global p1_utils_ver 1.0.29
%global stun_ver 1.2.23

Name: erlang-%{srcname}
Version: 1.0.61
Release: 1%{?dist}
License: Apache-2.0
Summary: ProcessOne SIP server component in Erlang
URL: https://github.com/processone/%{srcname}
VCS: git:%{url}.git
Source0: %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
BuildRequires: erlang-fast_tls >= %{fast_tls_ver}
BuildRequires: erlang-p1_utils >= %{p1_utils_ver}
BuildRequires: erlang-rebar3-pc
BuildRequires: erlang-stun >= %{stun_ver}
BuildRequires: gcc
BuildSystem:   rebar3
Obsoletes: erlang-p1_sip < 1.0.2
Provides: erlang-p1_sip = %{version}-%{release}
Requires: erlang-fast_tls >= %{fast_tls_ver}
Requires: erlang-p1_utils >= %{p1_utils_ver}
Requires: erlang-stun >= %{stun_ver}

%description
%{summary}.

%install -a
install -d $RPM_BUILD_ROOT%{_erllibdir}/esip-%{version}/include
install -d $RPM_BUILD_ROOT%{_erllibdir}/esip-%{version}/priv/lib

install -pm644 include/* $RPM_BUILD_ROOT%{_erllibdir}/esip-%{version}/include/
install -pm755 priv/lib/*.so $RPM_BUILD_ROOT%{_erllibdir}/esip-%{version}/priv/lib/

%files
%license LICENSE.txt
%doc CHANGELOG.md README.md
%{erlang_appdir}

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 1.0.61-1
- Rebuild for Erlang/OTP 29

* Wed Sep 30 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.0.61-1
- esip ver. 1.0.61

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Wed Mar 25 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.0.60-1
- esip ver. 1.0.60

* Thu Mar 19 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.0.54-5
- Rebuild with fixed rebar3

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 15 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.0.54-1
- esip ver. 1.0.54

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.37-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.37
- Update to 1.0.37 (#1807285).
- https://github.com/processone/esip/blob/1.0.37/CHANGELOG.md

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.31-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 17 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.31-1
- Update to 1.0.31 (#1789165).
- https://github.com/processone/esip/blob/1.0.31/CHANGELOG.md

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.30-2
- Drop the ExcludeArch on esip (#1772975).

* Thu Nov 14 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.30-1
- Update to 1.0.30 (#1742453).
- https://github.com/processone/esip/blob/1.0.30/CHANGELOG.md
- Add an exclusion on s390x (#1770256).

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.29-1
- Update to 1.0.29 (#1713297).
- https://github.com/processone/esip/blob/1.0.29/CHANGELOG.md

* Tue Apr 16 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.28-1
- Update to 1.0.28 (#1683113).
- https://github.com/processone/esip/blob/1.0.28/CHANGELOG.md

* Thu Feb 21 2019 Peter Lemenkov <lemenkov@gmail.com> - 1.0.27-3
- Rebuild for Erlang 21

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.27-1
- Update to 1.0.27.
- https://github.com/processone/esip/blob/1.0.27/CHANGELOG.md

