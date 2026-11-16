%global srcname fast_tls
%global p1_utils_ver 1.0.29

Name: erlang-%{srcname}
Version: 1.1.26
Release: 2%{?dist}
License: Apache-2.0
Summary: TLS / SSL native driver for Erlang / Elixir
URL: https://github.com/processone/%{srcname}/
VCS: git:%{url}.git
Source0: %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
# Set the default cipher list to PROFILE=SYSTEM.
# https://fedoraproject.org/wiki/Packaging:CryptoPolicies
Patch: erlang-fast_tls-0001-Use-the-system-ciphers-by-default.patch
Provides:  erlang-p1_tls = %{version}-%{release}
Obsoletes: erlang-p1_tls < 1.0.1
BuildRequires: gcc
BuildRequires: erlang-p1_utils >= %{p1_utils_ver}
BuildRequires: erlang-rebar3
BuildRequires: erlang-rebar3-pc
BuildRequires: openssl-devel
Requires: erlang-p1_utils >= %{p1_utils_ver}

%description
TLS / SSL native driver for Erlang / Elixir. This is used by ejabberd.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}
install -p -D -m 755 priv/lib/* --target-directory=%{buildroot}%{erlang_appdir}/priv/lib/

%check
%{erlang3_test}

%files
%license LICENSE.txt
%doc CHANGELOG.md
%doc README.md
%{erlang_appdir}

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 1.1.26-2
- Rebuild for Erlang/OTP 29

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Wed Mar 25 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.1.26-1
- fast_tls ver. 1.1.26

* Wed Mar 18 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.1.25-2
- Rbuild with fixed rebar3

* Fri Feb 06 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.1.25-1
- fast_tls ver. 1.1.25

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 29 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.1.22-1
- fast_tls ver. 1.1.22

* Fri Jul 19 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.1.21-1
- fast_tls ver. 1.1.21

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.1.20-1
- fast_tls ver. 1.1.20

* Fri Apr 19 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.1.15-8
- Rebuild with a fixed Erlang macros

* Wed Apr 17 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.1.15-7
- Switch to SPDX macro

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Peter Lemenkov <lemenkov@gmail.com> - 1.1.15-1
- Update to 1.1.15

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.1.8-4
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.1.8-1
- Update to 1.1.8 (#1807288).
- https://github.com/processone/fast_tls/blob/1.1.8/CHANGELOG.md

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 14 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.1.3-1
- Update to 1.1.13 (#1789166).
- https://github.com/processone/fast_tls/blob/1.1.3/CHANGELOG.md

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.1.2-2
- Bring fast_tls back to s390x (#1772967).

* Thu Nov 14 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 (#1742457).
- https://github.com/processone/fast_tls/blob/1.1.2/CHANGELOG.md
- Add an exclusion on s390x (#1770256).

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (#1713299).
- https://github.com/processone/fast_tls/blob/1.1.1/CHANGELOG.md

* Tue Apr 16 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (#1683114).
- https://github.com/processone/fast_tls/blob/1.1.0/CHANGELOG.md

* Thu Feb 21 2019 Peter Lemenkov <lemenkov@gmail.com> - 1.0.26-3
- Rebuild for Erlang 21

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

