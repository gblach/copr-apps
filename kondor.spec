Name:           kondor
Version:        0.1.0
Release:        1%{?dist}
Summary:        Cleans build artifacts from software projects

SourceLicense:  GPL-3.0-or-later
# Licenses of all crates built into the binary; %%cargo_license_summary prints them in the log.
License:        %{shrink:
    (Apache-2.0 OR Apache-2.0 WITH LLVM-exception OR MIT) AND
    (Apache-2.0 OR MIT) AND
    BSD-3-Clause AND
    GPL-3.0-or-later AND
    MIT AND
    (MIT OR Unlicense)
}
URL:            https://github.com/gblach/kondor
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# Created by .copr/make-srpm.sh.
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo-rpm-macros >= 26

%description
Cleans build artifacts from software projects, including nested projects.

%prep
%autosetup -p1 -a1
%cargo_prep -v cargo-vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest

%install
%cargo_install

%check
%cargo_test

%files
%license LICENSE LICENSE.dependencies cargo-vendor.txt
%doc README.md
%{_bindir}/kondor

%changelog
* Sat Nov 07 2026 Grzegorz Blach <grzegorz@blach.dev> - 0.1.0-1
- Initial package
