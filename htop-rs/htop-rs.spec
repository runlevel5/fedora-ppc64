%bcond check 1

Name:           htop-rs
Version:        0.2.0
Release:        1%{?dist}
Summary:        Interactive process viewer, a Rust port of htop

# htop-rs:         GPL-2.0-or-later
# vendored crates: see the license summary printed in %%build
SourceLicense:  GPL-2.0-or-later
License:        %{shrink:
    GPL-2.0-or-later AND
    MIT AND
    (0BSD OR MIT OR Apache-2.0) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    (BSD-2-Clause OR MIT OR Apache-2.0) AND
    (MIT OR Apache-2.0) AND
    ((MIT OR Apache-2.0) AND Unicode-3.0) AND
    (MIT OR Zlib OR Apache-2.0) AND
    (Zlib OR Apache-2.0 OR MIT)
}
URL:            https://github.com/runlevel5/htop-rs
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# The crates pinned by upstream's Cargo.lock; sources.sh creates it when the
# SRPM is built.
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo >= 1.99.1
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  gcc

%description
htop-rs is an interactive process viewer, a port of htop to Rust. It shows a
continuously updated list of processes with their CPU, memory and I/O usage
under a configurable header of meters, and lets you sort, filter and search
the list, change process priorities and send signals. It reads the same
configuration file as htop.

%prep
%autosetup -n %{name}-%{version} -p1 -a1
%cargo_prep -v vendor
# ncurses-pure is a git dependency: take it from the vendored crates as well
cat >> .cargo/config.toml << 'EOF2'

[source."git+https://github.com/runlevel5/ncurses-pure-rs"]
git = "https://github.com/runlevel5/ncurses-pure-rs"
replace-with = "vendored-sources"
EOF2

%build
%cargo_build
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest

%install
# Only the viewer: the crate also builds developer tools and a benchmark
install -Dpm 0755 target/rpm/htop-rs %{buildroot}%{_bindir}/htop-rs

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE.dependencies cargo-vendor.txt
%doc README.md IMPROVEMENTS.md
%{_bindir}/htop-rs

%changelog
* Wed Nov 04 2026 Trung Lê <trung.le@ruby-journal.com> - 0.2.0-1
- Initial package
