%global realname hyper
%global git_commit 4b1abc4284fc784f6def4f4928f715b0d33136f9
%global git_date 20161011


Name:		erlang-%{realname}
Version:	0
Release:	0.32.20161011git4b1abc4%{?dist}
Summary:	An implementation of the HyperLogLog algorithm in Erlang
License:	MIT
URL:		https://github.com/GameAnalytics/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{git_commit}/%{realname}-%{version}.tar.gz
# Fedora-specific
Patch1:		erlang-hyper-0001-remove-need-for-bisect-lib-hyper_bisect-as-it.patch
# Sent upstream - https://github.com/GameAnalytics/hyper/pull/23
Patch2:		erlang-hyper-0002-Module-random-is-deprecated.patch
# Sent upstream - https://github.com/GameAnalytics/hyper/pull/21
Patch3:		erlang-hyper-0003-Remove-unused-functions.patch
# Sent upstream - https://github.com/GameAnalytics/hyper/pull/22
Patch4:		erlang-hyper-0004-Exclude-eunit-from-production-builds.patch
Patch5:		erlang-hyper-0005-Remove-test-failing-in-Erlang-20.patch
Patch6:		erlang-hyper-0006-Fix-for-Rebar3-layout.patch
# Builds with OTP 29
Patch7:		erlang-hyper-0007-Compare-the-contents-of-hyper_array-round-trips.patch
BuildRequires:	erlang-basho_stats
BuildRequires:	erlang-proper
BuildRequires:	erlang-rebar3
BuildRequires:	erlang-stdlib2
BuildRequires:	gcc


%description
An implementation of the HyperLogLog algorithm in Erlang. Using HyperLogLog you
can estimate the cardinality of very large data sets using constant memory. The
relative error is 1.04 * sqrt(2^P). When creating a new HyperLogLog filter, you
provide the precision P, allowing you to trade memory for accuracy. The union
of two filters is lossless.


%prep
%autosetup -p1 -n %{realname}-%{git_commit}


%build
%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
gcc c_src/hyper_carray.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/hyper_carray.o
gcc c_src/hyper_carray.o $LDFLAGS -shared -L%{_libdir}/erlang/usr/lib -lei -o priv/hyper_carray.so


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license LICENSE
%doc README.md
%{erlang_appdir}/


%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 0-0.32.20161011git4b1abc4
- Compare the contents of hyper_array round trips in the tests, as OTP 29
  changed the internal layout of array

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.32.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.31.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.30.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.29.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 08 2024 Peter Lemenkov <lemenkov@gmail.com> - 0-0.28.20161011git4b1abc4
- Spec-file cleanup

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.27.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Peter Lemenkov <lemenkov@gmail.com> - 0-0.26.20161011git4b1abc4
- Switch to Rebar3

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.21.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.20.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.19.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Peter Lemenkov <lemenkov@gmail.com> - 0-0.18.20161011git4b1abc4
- Rebuild for Erlang 25

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.17.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.16.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.15.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.14.20161011git4b1abc4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.13.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar  5 2020 Peter Lemenkov <lemenkov@gmail.com> - 0-0.12.20161011git4b1abc4
- Remove ExcludeArch for s390 - we've got a workaround fr rhbz #1770256

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.11.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Peter Lemenkov <lemenkov@gmail.com> - 0-0.10.20161011git4b1abc4
- Rebuild for Erlang 22

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.9.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 27 2019 Peter Lemenkov <lemenkov@gmail.com> - 0-0.8.20161011git4b1abc4
- Rebuild with noarch deps

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.7.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 02 2018 Peter Lemenkov <lemenkov@gmail.com> - 0-0.6.20161011git4b1abc4
- Rebuild with noarch deps

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.5.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 21 2018 Peter Lemenkov <lemenkov@gmail.com> - 0-0.4.20161011git4b1abc4
- Rebuild for Erlang 20 (with proper builddeps)

* Fri Feb 23 2018 Peter Lemenkov <lemenkov@gmail.com> - 0-0.3.20161011git4b1abc4
- Rebuild for Erlang 20

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.2.20161011git4b1abc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 22 2017 Peter Lemenkov <lemenkov@gmail.com> - 0-0.1.20161011git4b1abc4
- Initial build

