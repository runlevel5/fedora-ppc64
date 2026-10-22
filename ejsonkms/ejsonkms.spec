%bcond check 1

Name:           ejsonkms
Version:        1.0.6
Release:        1%{?dist}
Summary:        Manage encrypted secrets using EJSON and AWS KMS

# ejsonkms:        MIT
# vendored crates: see the license summary printed in %%build
SourceLicense:  MIT
License:        %{shrink:
    MIT AND
    Apache-2.0 AND
    BSD-3-Clause AND
    ISC AND
    Unicode-3.0 AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 OR ISC) AND
    (Apache-2.0 OR ISC OR MIT) AND
    (Apache-2.0 OR ISC OR MIT-0) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    (CC0-1.0 OR MIT-0 OR Apache-2.0) AND
    (Unlicense OR MIT)
}
URL:            https://github.com/runlevel5/ejsonkms-rs
Source0:        %{url}/archive/v%{version}/%{name}-rs-%{version}.tar.gz
# The crates pinned by upstream's Cargo.lock; sources.sh creates it when the
# SRPM is built.
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo-rpm-macros >= 26
# aws-lc-sys (the rustls crypto provider) builds AWS-LC from C sources
BuildRequires:  cmake
BuildRequires:  gcc

# vendor/aws-lc-sys/aws-lc
Provides:       bundled(aws-lc)

%description
ejsonkms combines ejson with AWS KMS: the ejson private key is stored in the
secrets file itself, encrypted with a KMS key, so decrypting the file needs
only access to that KMS key instead of a private key file on disk.

%prep
%autosetup -n %{name}-rs-%{version} -a1
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

%if %{with check}
%check
# The integration test talks to a mock KMS it starts on localhost.
%cargo_test
%endif

%files
%license LICENSE.txt LICENSE.dependencies cargo-vendor.txt
%doc README.md
%{_bindir}/ejsonkms

%changelog
* Thu Oct 22 2026 Trung Le <8@tle.id.au> - 1.0.6-1
- Initial package
