# quake3

- `ioquake3/`: the engine, built in COPR.
- `quake3-data/`: a spec for the game data of your own copy of Quake III
  Arena, built locally only (the data is not redistributable, so the
  directory has no `.copr` link). Copy the pak files next to the spec and
  build:

      cd quake3/quake3-data
      rpmbuild -bb --define "_sourcedir $PWD" quake3-data.spec

  The package installs the data to `/usr/share/quake3`, where `ioquake3`
  looks for it. See the spec for the pak files needed and for Team Arena.
