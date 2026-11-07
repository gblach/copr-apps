# COPR packages

Spec files for [imge](https://github.com/gblach/imge), [kondor](https://github.com/gblach/kondor)
and [PreTTY](https://github.com/gblach/PreTTY), built on Fedora COPR.

```sh
sudo dnf copr enable gblachx/apps
```

COPR builds each package with the `make_srpm` method: `.copr/Makefile` runs
`.copr/make-srpm.sh`, which downloads the release tarball, vendors all crates from
`Cargo.lock` into `<name>-<version>-vendor.tar.xz` and builds the source RPM. The binary RPM is
then built offline from that.

## COPR setup

```sh
copr-cli create apps \
    --chroot fedora-45-x86_64 --chroot fedora-45-aarch64 \
    --chroot fedora-rawhide-x86_64 --chroot fedora-rawhide-aarch64

for pkg in imge kondor pretty; do
    copr-cli add-package-scm apps --name "$pkg" --clone-url https://github.com/gblach/copr-apps \
        --method make_srpm --spec "$pkg.spec"
done

copr-cli build-package apps --name imge
```

## New upstream release

1. Bump `Version`, reset `Release` to 1 and add a `%changelog` entry.
2. For pretty, update `gpui_component_version` and `gpui_pre_wgpu_version` to the versions in
   upstream `Cargo.lock`.
3. Build, then compare the `License` tag with the license summary printed in the build log
   (`%cargo_license_summary`) and update it if dependencies changed.

## Local test build

```sh
mkdir -p out
./.copr/make-srpm.sh imge.spec out/
mock -r fedora-rawhide-x86_64 out/imge-*.src.rpm
```
