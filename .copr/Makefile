# COPR "make_srpm" method runs `make -f .copr/Makefile srpm outdir=... spec=...` as root
# from the root of this repository, with network access.
srpm:
	dnf -y install cargo curl rpm-build rpmdevtools tar xz
	./.copr/make-srpm.sh "$(spec)" "$(outdir)"
