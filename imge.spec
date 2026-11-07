Name:           imge
Version:        1.1.0
Release:        1%{?dist}
Summary:        TUI for copying disk images to and from drives

SourceLicense:  MPL-2.0
# Licenses of all crates built into the binary; %%cargo_license_summary prints them in the log.
License:        %{shrink:
    (0BSD OR Apache-2.0 OR MIT) AND
    (Apache-2.0 OR Apache-2.0 WITH LLVM-exception OR MIT) AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 OR MIT OR Zlib) AND
    BSD-3-Clause AND
    bzip2-1.0.6 AND
    MIT AND
    (MIT OR Unlicense) AND
    MPL-2.0 AND
    Zlib
}
URL:            https://github.com/gblach/imge
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# Created by .copr/make-srpm.sh.
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo-rpm-macros >= 26
# liblzma-sys and zstd-sys compile bundled C libraries.
BuildRequires:  gcc

%description
TUI tool for copying disk images to and from drives with on-the-fly
compression and decompression - a less error-prone (and simpler) alternative
to dd.

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
%{_bindir}/imge

%changelog
* Sat Nov 07 2026 Grzegorz Blach <grzegorz@blach.dev> - 1.1.0-1
- Initial package
