%global realname snappy


Name:		erlang-%{realname}
Version:	1.1.2
Release:	7%{?dist}
Summary:	An Erlang NIF wrapper for Google's snappy library
License:	Apache-2.0
URL:		https://github.com/skunkwerks/%{realname}-erlang-nif
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-snappy-0001-No-bundled-snappy.patch
Patch3:		erlang-snappy-0002-Added-a-check-for-empty-IOLists-during-decompression.patch
BuildRequires:	erlang-rebar3
BuildRequires:	gcc-c++
BuildRequires:	snappy-devel


%description
An Erlang NIF wrapper for Google's snappy compressor/decompressor.


%prep
%autosetup -p1 -n %{realname}-erlang-nif-%{version}
rm -rf c_src/snappy
rm -rf rebar.config rerar.config.script


%build
%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
mkdir -p priv/
g++ c_src/snappy_nif.cc	$CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/snappy_nif.o
g++ c_src/snappy_nif.o	$LDFLAGS -shared -L%{_libdir}/erlang/usr/lib -lei -L%{_libdir} -lsnappy -lm -o priv/snappy_nif.so

%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%doc README.md
%{erlang_appdir}/


%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 1.1.2-7
- Rebuild for Erlang/OTP 29

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-2
- Switch to Rebar3

* Tue Apr 23 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-1
- Update to ver. 1.1.2

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.28.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.27.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.26.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.25.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.24.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Peter Lemenkov <lemenkov@gmail.com> - 1.1.1-0.23.git348da43
- Rebuild for Erlang 25

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.22.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.21.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.20.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.19.git348da43
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.18.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.17.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Peter Lemenkov <lemenkov@gmail.com> - 1.1.1-0.16.git348da43
- Rebuild for Erlang 22

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.15.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 21 2019 Peter Lemenkov <lemenkov@gmail.com> - 1.1.1-0.14.git348da43
- Rebuild for Erlang 21

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.13.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.12.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 21 2018 Peter Lemenkov <lemenkov@gmail.com> - .1.1-0.11.git348da43
- Rebuild for Erlang 20 (with proper builddeps)

* Fri Feb 23 2018 Peter Lemenkov <lemenkov@gmail.com> - 1.1.1-0.10.git348da43
- Rebuild for Erlang 20

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.9.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.8.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.7.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.6.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 07 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.1-0.5.git348da43
- Rebuild for Erlang 19

* Fri Apr 15 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.1.1-0.4.git348da43
- Drop unneeded macro

* Wed Mar 30 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.1.1-0.3.git348da43
- Rebuild with Erlang 18.3

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-0.2.git348da43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.1.1-0.1.git348da43
- Ver. 1.1.1
- Rebuild with Erlang 18.2.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.12.git80db168
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.3-0.11.git80db168
- Rebuilt for GCC 5 C++11 ABI change

* Tue Nov 04 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.0.3-0.10.git80db168
- Rebuild with Erlang 17.3.3

* Thu Aug 28 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.0.3-0.9.git80db168
- Rebuild with Erlang 17.2.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.8.git80db168
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.0.3-0.7.git80db168
- Use new erlang macros to build with $RPM_OPT/LD_FLAGS etc, verbosely

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.6.git80db168
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.5.git80db168
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.0.3-0.4.git80db168
- Fixed FTBFS in Rawhide (F19)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.3.git80db168
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 07 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.0.3-0.2.git80db168
- Ensure consistent usage of macros (cosmetic)

* Mon Sep 24 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.0.3-0.1.git80db168
- initial build

