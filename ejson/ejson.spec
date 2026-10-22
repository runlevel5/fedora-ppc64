%bcond check 1

Name:           ejson
Version:        1.0.6
Release:        2%{?dist}
Summary:        Manage encrypted secrets using public key encryption

# ejson:           MIT
# vendored crates: see the license summary printed in %%build
SourceLicense:  MIT
License:        %{shrink:
    MIT AND
    BSD-3-Clause AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    (MIT OR Apache-2.0 OR BSD-1-Clause) AND
    (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND
    (Unlicense OR MIT)
}
URL:            https://github.com/runlevel5/ejson-rs
# Upstream's release CI attaches this tarball, with the crates pinned by
# Cargo.lock vendored into vendor/, to the GitHub Release.
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}-vendored.tar.xz

BuildRequires:  cargo-rpm-macros >= 26

%description
ejson is a Rust implementation of Shopify/ejson: a drop-in replacement for
the original Go tool that manages secrets in source control using
public-key cryptography. Legacy v1 keys use NaCl Box (Curve25519 +
XSalsa20 + Poly1305); hybrid post-quantum v2 keys combine X25519 with
ML-KEM-768 and encrypt values with XChaCha20-Poly1305. Public keys are
embedded in the secrets file; private keys are stored separately on the
filesystem. Supports JSON, YAML and TOML secret files.

%prep
%autosetup -n %{name}-%{version}
# Replace upstream's cargo vendor config with the one %%cargo_prep writes.
rm .cargo/config.toml
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
%cargo_install
# The crate also has a library target, so %%cargo_install installs its
# sources for a -devel package; this package ships only the binary.
rm -r %{buildroot}%{_datadir}/cargo/registry
install -Dpm 0644 -t %{buildroot}%{_mandir}/man1 man/*.1
install -Dpm 0644 -t %{buildroot}%{_mandir}/man5 man/*.5

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE.txt LICENSE.dependencies cargo-vendor.txt
%doc README.md
%{_bindir}/ejson
%{_mandir}/man1/ejson*.1*
%{_mandir}/man5/ejson.5*

%changelog
* Thu Oct 22 2026 Trung Le <8@tle.id.au> - 1.0.6-2
- Build with Fedora's Rust flags and debuginfo (%%cargo_prep -v vendor)
- Ship the vendored crates' licenses and a vendor manifest
- Install the man pages

* Thu Jul 09 2026 Trung Lê <8@tle.id.au> - 1.0.6-1
- Update to 1.0.6.

* Wed Jul 08 2026 Trung Lê <8@tle.id.au> - 1.0.5-1
- Update to 1.0.5.

* Wed Jul 08 2026 Trung Lê <8@tle.id.au> - 1.0.3-1
- Initial package.
