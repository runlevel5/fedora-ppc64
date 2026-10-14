# COPR "make_srpm" source method: COPR runs
#   make -f <checkout>/.copr/Makefile srpm outdir=<dir> spec=<path to spec>
# inside a mock chroot. Fetch the spec's remote sources, then build the SRPM.
# Each package directory links its own .copr to this one.

specdir := $(abspath $(dir $(spec)))

srpm:
	dnf -y install rpmdevtools rpm-build
	spectool --get-files --directory $(specdir) $(spec)
	rpmbuild -bs \
		--define "_sourcedir $(specdir)" \
		--define "_srcrpmdir $(outdir)" \
		$(spec)

.PHONY: srpm
