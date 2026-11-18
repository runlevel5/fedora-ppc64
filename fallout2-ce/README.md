# fallout2-ce

- `fallout2-ce/`: the engine, built in COPR.
- `fallout2-ce-data/`: a spec for the game data of your own copy of
  Fallout 2, built locally only (the data is not redistributable, so the
  directory has no `.copr` link). Copy GOG's offline installer, or a
  tarball of an installed copy, next to the spec and build:

      cd fallout2-ce/fallout2-ce-data
      cp /path/to/the/installer.exe setup_fallout2.exe
      # or: tar -C /path/to/the/game -czf fallout2.tar.gz .
      rpmbuild -bb --define "_sourcedir $PWD" fallout2-ce-data.spec

  The installer needs `innoextract`. The package installs the DAT
  archives, the `data` and `sound` directories and the game's
  configuration to `/usr/share/fallout2-ce`, which the `fallout2-ce`
  launcher mirrors into each user's game directory.
