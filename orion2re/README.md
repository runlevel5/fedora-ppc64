# orion2re

- `orion2re/`: the engine, built in COPR, with the system libraries (it
  needs `imgui` from this repository) instead of upstream's submodules.
- `orion2re-data/`: a spec for the game data of your own copy of Master of
  Orion II, built locally only (the data is not redistributable, so the
  directory has no `.copr` link). Copy GOG's offline installer, or a
  tarball of an installed copy, next to the spec and build:

      cd orion2re/orion2re-data
      cp /path/to/the/installer.exe setup_master_of_orion_2.exe
      # or: tar -C /path/to/the/game -czf master_of_orion_2.tar.gz .
      rpmbuild -bb --define "_sourcedir $PWD" orion2re-data.spec

  The installer needs `innoextract`. For the launcher's icon, also copy a
  square PNG (such as 256x256 box art) as `orion2re.png`. The package
  installs the LBX archives and `ORIONCD.INI` to `/usr/share/orion2re/game`,
  the `orion2re/game` directory under `$XDG_DATA_DIRS` where `orion2re`
  looks for them, and the icon to the hicolor theme.
