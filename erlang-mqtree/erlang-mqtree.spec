%global srcname mqtree
%global p1_utils_ver 1.0.29

Name:       erlang-%{srcname}
Version:    1.0.20
Release:    2%{?dist}
License:    Apache-2.0
Summary:    Index tree for MQTT topic filters
URL:        https://github.com/processone/%{srcname}
VCS:        git:%{url}.git
Source0:    %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
Patch:      erlang-mqtree-0001-Remove-bundled-uthash.patch
BuildRequires: erlang-p1_utils >= %{p1_utils_ver}
BuildRequires: erlang-rebar3
BuildRequires: erlang-rebar3-pc
BuildRequires: gcc
BuildRequires: openssl-devel
BuildRequires: uthash-devel
Requires: erlang-p1_utils >= %{p1_utils_ver}

%description
An Erlang NIF implementation of N-ary tree to keep MQTT topic filters for
efficient matching.

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
%license LICENSE
%doc README.md
%{erlang_appdir}

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 1.0.20-2
- Rebuild for Erlang/OTP 29

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Wed Mar 25 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.0.20-1
- mqtree ver. 1.0.20

* Wed Mar 18 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.0.19-2
- Rebuild with fixed rebar3

* Fri Feb 06 2026 Peter Lemenkov <lemenkov@gmail.com> - 1.0.19-1
- mqtree ver. 1.0.19

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 29 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.0.17-1
- mqtree ver. 1.0.17

* Wed Jun 12 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.0.16-1
- mqtree ver. 1.0.16

* Fri Apr 19 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.0.10-12
- More macros

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.10-1
- Update to 1.0.10 (#1807345).
- https://github.com/processone/mqtree/blob/1.0.10/CHANGELOG.md

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 17 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6 (#1788885).
- https://github.com/processone/mqtree/blob/1.0.6/CHANGELOG.md

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.5-2
- Bring mqtree back to s390x (#1772970).

* Thu Nov 14 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5 (#1742469)
- https://github.com/processone/mqtree/compare/1.0.3...1.0.5
- Add an exclusion on s390x (#1770256).

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 (#1713422).
- https://github.com/processone/mqtree/compare/1.0.2...1.0.3

* Sun Apr 14 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.2-2
- Correct license to ASL 2.0 and BSD because c_src/uthash.h is unspecified BSD.

* Sat Apr 13 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.2-1
- Initial release.

