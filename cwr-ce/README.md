# cwr-ce

- `cwr-ce/`: the engine, built in COPR, with the system libraries (it
  needs `imgui` from this repository) instead of upstream's vcpkg.
- `cwr-ce-data/`: a spec for the Remastered game data of your own copy of
  ARMA: Cold War Assault from GOG, built locally only (the data is not
  redistributable, so the directory has no `.copr` link). Copy GOG's offline
  installer next to the spec and build:

      cd cwr-ce/cwr-ce-data
      cp /path/to/the/installer.exe setup_arma_cold_war_assault.exe
      rpmbuild -bb --define "_sourcedir $PWD" cwr-ce-data.spec

  It needs `innoextract`. The package installs the data to
  `/usr/share/cwr-ce`, where the `cwr-ce` and `cwr-ce-server` launchers
  point the engine.
