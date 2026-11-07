#!/usr/bin/env bash
# Builds a source RPM from a spec file. COPR builds the binary RPM without network access, so
# this also creates the vendor tarball holding every crate from Cargo.lock.
set -euo pipefail

spec=$(realpath "$1")
outdir=$(realpath "$2")
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

read -r name version < <(rpmspec -q --srpm --qf '%{name} %{version}\n' "$spec")
spectool -g -C "$outdir" "$spec"

mkdir "$work/src"
source0=$(spectool -l -s 0 "$spec" | awk '{print $2}')
tar xzf "$outdir/$(basename "$source0")" -C "$work/src" --strip-components=1

# A .crate source backs a [patch.crates-io] path dependency in vendor/<crate>. Cargo only needs
# it to exist to resolve Cargo.lock; the spec applies upstream's patches in %prep.
for url in $(spectool -l "$spec" | awk '$2 ~ /\.crate$/ {print $2}'); do
    file=$(basename "$url")
    crate=$(sed -E 's/-[0-9][^-]*\.crate$//' <<< "$file")
    mkdir -p "$work/src/vendor/$crate"
    tar xzf "$outdir/$file" -C "$work/src/vendor/$crate" --strip-components=1
done

(cd "$work/src" && cargo vendor --locked cargo-vendor > /dev/null)
tar cJf "$outdir/$name-$version-vendor.tar.xz" -C "$work/src" cargo-vendor

rpmbuild -bs --define "_sourcedir $outdir" --define "_srcrpmdir $outdir" "$spec"
