# COPR "make_srpm" source method: COPR runs
#   make -f <checkout>/.copr/Makefile srpm outdir=<dir> spec=<path to spec>
# inside a mock chroot. Fetch the spec's remote sources, run the package's
# sources.sh if it has one (to generate local sources, given the spec), then
# build the SRPM.
# Each package directory links its own .copr to this one.

specdir := $(abspath $(dir $(spec)))

srpm:
	dnf -y install rpmdevtools rpm-build
	spectool --get-files --directory $(specdir) $(spec)
	if [ -x $(specdir)/sources.sh ]; then $(specdir)/sources.sh $(spec); fi
	rpmbuild -bs \
		--define "_sourcedir $(specdir)" \
		--define "_srcrpmdir $(outdir)" \
		$(spec)

.PHONY: srpm
