# worldofpadman

- `worldofpadman/`: the engine, built in COPR. Its source tarball is made by
  `sources.sh` from upstream's git, without the game's artwork, which is not
  free and so must not be in the SRPM.
- `worldofpadman-data/`: the game data of the official 1.7.0 release, built
  locally only (the data may be distributed for non-commercial purposes only,
  which rules it out of COPR, so the directory has no `.copr` link). Fetch the
  release zip next to the spec and build:

      cd worldofpadman/worldofpadman-data
      spectool -g worldofpadman-data.spec
      rpmbuild -bb --define "_sourcedir $PWD" worldofpadman-data.spec

  The package installs the data to `/usr/share/worldofpadman`, where
  `worldofpadman` looks for it, with the desktop entry and icon. The pk3
  files are the release's own, so pure 1.7.0 servers accept them; they
  include the game modules (`wop_vm_1.7.0.pk3`).
