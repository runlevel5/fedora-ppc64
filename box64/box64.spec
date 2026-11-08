# Tests are disabled as they require x86_64 libraries to run
%bcond tests 0

%global forgeurl https://github.com/ptitSeb/box64
%global commit 37f5e4b7b0002a247c04866a44d0321e92cfef3c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapdate 20261107

%global common_description %{expand:
Box64 lets you run x86_64 Linux programs (such as games) on non-x86_64 Linux
systems, like ARM (host system needs to be 64-bit little-endian).}

Name:           box64
# Snapshot of upstream main ahead of the 0.4.5 release; it carries the
# PPC64LE dynarec, which no release of box64 has yet
Version:        0.4.5~%{snapdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        Linux userspace x86_64 emulator with a twist, targeted at ARM64

License:        MIT
URL:            https://box86.org
Source:         %{forgeurl}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# ppc64le: the PPC64LE dynamic recompiler (JIT) work from the ppc64le-jit
# branch of https://github.com/runlevel5/box64-ppc64 (585bd6d2f), as a diff
# against upstream %%{commit}, without docs and tests
Patch:          box64-ppc64le-jit.patch

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-podlators
BuildRequires:  python3
BuildRequires:  systemd-rpm-macros

# This build is for ppc64le only; the PPC64LE dynarec needs POWER9 or newer
ExclusiveArch:  ppc64le

Requires:       %{name}-data = %{version}-%{release}
Recommends:     %{name}-binfmts = %{version}-%{release}

%description    %{common_description}

This build includes the PPC64LE dynamic recompiler and needs a POWER9 or
newer CPU.

%package        data
Summary:        Common files for %{name}
BuildArch:      noarch

%description    data %{common_description}

This package provides common data files for box64.

%package        binfmts
Summary:        binfmt_misc handler configurations for box64

%description    binfmts %{common_description}

This package provides binfmt_misc handler configurations to use box64 to
execute x86_64 binaries.

%package        configurator
Summary:        Graphical editor for box64 configuration files
BuildArch:      noarch

Requires:       %{name}-data = %{version}-%{release}
Requires:       gtk3
Requires:       python3-gobject

%description    configurator %{common_description}

This package provides box64-configurator, a GTK tool to edit the per-program
settings in box64rc files.

%prep
%autosetup -n %{name}-%{commit} -p1

# Remove prebuilt libraries
rm -r x64lib

# Fix encoding
sed -i 's/\r$//' docs/*.md

# Fix install paths
sed -i 's:/etc/binfmt.d:%{_binfmtdir}:g' CMakeLists.txt

%build
# With -fexceptions, glibc's pthread_cleanup_push runs box32's thread-cancel
# handler from inside the unwinder, where re-entering the emulator deadlocks
# (tests32/test14, conditionalThreads_32bits, never finishes)
%global optflags %{optflags} -fno-exceptions
%cmake -DNOGIT=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBOX32=ON -DBOX32_BINFMT=ON \
  -DNO_LIB_INSTALL=ON -DPPC64LE=ON
%cmake_build

# Build manpage
pod2man --stderr docs/%{name}.pod > docs/%{name}.1

%install
%cmake_install

# Install manpage
install -Dpm0644 -t %{buildroot}%{_mandir}/man1 docs/%{name}.1

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-configurator.desktop
%if %{with tests}
%ctest
%endif

%files
%{_bindir}/%{name}

%files data
%license LICENSE
%doc README.md
%doc %lang(cn) README_CN.md
%doc %lang(uk) README_UK.md
%doc docs/*.md docs/img
%{_mandir}/man1/box64.1*
%config(noreplace) %{_sysconfdir}/box64.box64rc

%files binfmts
%{_binfmtdir}/box32.conf
%{_binfmtdir}/box64.conf

%files configurator
%{_bindir}/%{name}-configurator
%{_datadir}/applications/%{name}-configurator.desktop

%changelog
* Sun Nov 08 2026 Trung Le <8@tle.id.au> - 0.4.5~20261107git37f5e4b-1
- Based on Fedora's box64 0.3.6 spec, updated to an upstream main snapshot
  (37f5e4b7b) ahead of 0.4.5, the first with the PPC64LE dynarec
- Add the PPC64LE dynarec (JIT) work from runlevel5/box64-ppc64 ppc64le-jit
  (585bd6d2f)
- Build only on ppc64le
- Add python3 to the build requirements, which upstream's CMake now needs
- Package the new box64-configurator in a subpackage
- Build with -fno-exceptions: with Fedora's -fexceptions, cancelling a 32-bit
  guest thread deadlocks
