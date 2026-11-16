%global realname lfe

Name:		erlang-%{realname}
Version:	2.2.2
Release:	1%{?dist}
Summary:	Lisp Flavoured Erlang
License:	Apache-2.0
URL:		https://github.com/lfe/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch:		erlang-lfe-0001-Restore-functions-removed-in-pre-R17-Erlang.patch
Patch:		erlang-lfe-0002-We-don-t-have-proper-yet.patch
BuildRequires:	emacs
BuildRequires:	erlang-proper
BuildRequires:	erlang-rebar3
BuildRequires:	gcc
Obsoletes:	emacs-erlang-lfe
Obsoletes:	emacs-erlang-lfe-el
Requires:	emacs-filesystem

%description
Lisp Flavoured Erlang, is a lisp syntax front-end to the Erlang
compiler. Code produced with it is compatible with "normal" Erlang
code. An LFE evaluator and shell is also included.

%prep
%autosetup -p 1 -n %{realname}-%{version}

%build
%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
gcc c_src/lfeexec.c $CFLAGS -fPIC -c -o c_src/lfeexec.o
gcc c_src/lfeexec.o $LDFLAGS -o bin/lfeexec

emacs -L emacs/ -batch -f batch-byte-compile emacs/inferior-lfe.el emacs/lfe-mode.el emacs/lfe-indent.el

%install
%{erlang3_install}

install -m 0755 -d %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/bin
install -p -m 0755 -D bin/*  %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/bin/
install -m 0755 -d %{buildroot}/%{_bindir}
ln -s %{_libdir}/erlang/lib/%{realname}-%{version}/bin/{lfe,lfe-test,lfec,lfedoc,lfeexec,lfescript} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_emacs_sitelispdir}
mkdir -p %{buildroot}%{_emacs_sitestartdir}
install -p -m 0644 emacs/inferior-lfe.el %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/inferior-lfe.elc %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-mode.el %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-mode.elc %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-indent.el %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-indent.elc %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-start.el %{buildroot}%{_emacs_sitestartdir}

%check
%{erlang3_test}

%files
%license LICENSE
%doc README.md doc/ examples/
%{_bindir}/lfe
%{_bindir}/lfe-test
%{_bindir}/lfec
%{_bindir}/lfedoc
%{_bindir}/lfeexec
%{_bindir}/lfescript
%{erlang_appdir}/
%{_emacs_sitelispdir}/inferior-lfe.el
%{_emacs_sitelispdir}/inferior-lfe.elc
%{_emacs_sitelispdir}/lfe-indent.el
%{_emacs_sitelispdir}/lfe-indent.elc
%{_emacs_sitelispdir}/lfe-mode.el
%{_emacs_sitelispdir}/lfe-mode.elc
%{_emacs_sitestartdir}/lfe-start.el

%changelog
* Mon Nov 16 2026 Trung Lê <8@tle.id.au> - 2.2.2-1
- Rebuild for Erlang/OTP 29

* Fri Aug 07 2026 Peter Lemenkov <lemenkov@gmail.com> - 2.2.2-1
- LFE ver. 2.2.0

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Sat Mar 21 2026 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-4
- Simplify gitignore

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Mar 18 2025 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-1
- LFE ver. 2.2.0

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 15 2024 Peter Lemenkov <lemenkov@gmail.com> - 2.1.5-1
- LFE ver. 2.1.5

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Peter Lemenkov <lemenkov@gmail.com> - 2.1.4-47
- Switch to Rebar3

* Fri May 31 2024 Peter Lemenkov <lemenkov@gmail.com> - 2.1.4-46
- Fix patch

* Fri May 31 2024 Peter Lemenkov <lemenkov@gmail.com> - 2.1.4-45
- LFE ver. 2.1.4

* Fri Apr 19 2024 Peter Lemenkov <lemenkov@gmail.com>
- More macros

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan  4 2023 Peter Lemenkov <lemenkov@gmail.com> - 2.1.1-1
- LFE ver. 2.1.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Peter Lemenkov <lemenkov@gmail.com> - 2.0.1-1
- LFE ver. 2.0.1

* Tue Jul 27 2021 Peter Lemenkov <lemenkov@gmail.com> - 2.0.1-0.1
- Bootstrap ver. 2.0.1

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Peter Lemenkov <lemenkov@gmail.com> - 1.3-1
- Ver. 1.3

* Tue Jun 20 2017 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0
- Bootstrap ver. 1.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 23 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1
- Ver. 1.2.1
- Disable tests for now

* Wed Nov 23 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-0
- Bootstrap ver. 1.2.1

* Thu Oct 20 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.2.0-1
- Ver. 1.2.0

* Wed Jun  8 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-2
- No longer providing separate emacs-subpackages

* Sat Apr 16 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-1
- Ver. 1.0.2

* Mon Apr  4 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.0.1-2
- Ver. 1.0.1

* Mon Apr  4 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.0.1-1
- Ver. 1.0.1 (bootstrap)

* Wed Mar 30 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.10.1-3
- Rebuild with Erlang 18.3

* Wed Mar 30 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.10.1-2.1
- Bootstrap (build w/o rebar) against Erlang 18.3

* Tue Mar  1 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.10.1-2
- Install CLI tools as well

* Tue Mar  1 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.10.1-1
- Ver. 0.10.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.9.0-2
- Disable debuginfo

* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.9.0-1
- Ver. 0.9.0
- Drop support for EL5

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.6.2-1
- Ver. 0.6.2 (Backwards API/ABI compatible)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-5
- Make building of emacs sub-packages conditional (and disable on EL-5)

* Sun Nov 14 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-4
- Remove duplicated emacs files from docs

* Sun Oct 31 2010 Tim Niemueller <tim@niemueller.de> - 0.6.1-3
- Added Emacs sub-package
- Fix inconsitent macro usage

* Fri Oct 15 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-2
- Provide (x)emacs subpackages

* Fri Oct  1 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-1
- Initial build

