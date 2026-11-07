%global gpui_component_version 0.9.0
%global gpui_pre_wgpu_version 0.3.11
%global crates_url https://static.crates.io/crates
# Full debug info makes the final LTO link of ~800 crates run out of memory.
%global rustflags_debuginfo 1

Name:           pretty
Version:        0.1.0
Release:        1%{?dist}
Summary:        Pretty terminal emulator

SourceLicense:  GPL-3.0-or-later
# Licenses of all crates built into the binary; %%cargo_license_summary prints them in the log.
License:        %{shrink:
    0BSD AND
    (0BSD OR Apache-2.0 OR MIT) AND
    Apache-2.0 AND
    (Apache-2.0 OR Apache-2.0 WITH LLVM-exception OR MIT) AND
    (Apache-2.0 OR BSD-2-Clause OR MIT) AND
    (Apache-2.0 OR BSD-3-Clause) AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 OR CC0-1.0 OR MIT-0) AND
    (Apache-2.0 OR GPL-2.0-only) AND
    (Apache-2.0 OR ISC OR MIT) AND
    (Apache-2.0 OR LGPL-2.1-or-later OR MIT) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 OR MIT OR Zlib) AND
    BSD-2-Clause AND
    BSD-3-Clause AND
    CC0-1.0 AND
    GPL-3.0-or-later AND
    ISC AND
    MIT AND
    (MIT OR Unlicense) AND
    MPL-2.0 AND
    Unicode-3.0 AND
    Zlib
}
URL:            https://github.com/gblach/PreTTY
Source0:        %{url}/archive/v%{version}/PreTTY-%{version}.tar.gz
# Created by .copr/make-srpm.sh.
Source1:        %{name}-%{version}-vendor.tar.xz
# Cargo.toml points [patch.crates-io] at vendor/<crate>. Upstream fills those folders with
# `cargo setup`, which downloads the crate and applies patches/<crate>.diff; %%prep does the
# same offline.
Source2:        %{crates_url}/gpui-component/gpui-component-%{gpui_component_version}.crate
Source3:        %{crates_url}/gpui-pre-wgpu/gpui-pre-wgpu-%{gpui_pre_wgpu_version}.crate

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)

# Loaded with dlopen at runtime, so RPM does not detect them.
Requires:       libwayland-client
Requires:       vulkan-loader

%description
A pretty terminal emulator for Linux, clean, GPU-rendered and easy on the
eyes, that always shows where your shell is: over SSH, as root or inside a
container.

%prep
%autosetup -n PreTTY-%{version} -p1 -a1
mkdir -p vendor/gpui-component vendor/gpui-pre-wgpu
tar xzf %{SOURCE2} -C vendor/gpui-component --strip-components=1
tar xzf %{SOURCE3} -C vendor/gpui-pre-wgpu --strip-components=1
patch -d vendor/gpui-component -p1 < patches/gpui-component.diff
patch -d vendor/gpui-pre-wgpu -p1 < patches/gpui-pre-wgpu.diff
%cargo_prep -v cargo-vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest

%install
%cargo_install
install -Dpm 0644 assets/pretty.desktop %{buildroot}%{_datadir}/applications/pretty.desktop
install -Dpm 0644 assets/pretty.png \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/pretty.png
install -Dpm 0644 assets/pretty.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/pretty.svg

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/pretty.desktop
%cargo_test

%files
%license LICENSE LICENSE.dependencies cargo-vendor.txt
%doc README.md
%{_bindir}/pretty
%{_datadir}/applications/pretty.desktop
%{_datadir}/icons/hicolor/512x512/apps/pretty.png
%{_datadir}/icons/hicolor/scalable/apps/pretty.svg

%changelog
* Sat Nov 07 2026 Grzegorz Blach <grzegorz@blach.dev> - 0.1.0-1
- Initial package
