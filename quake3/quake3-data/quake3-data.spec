# Quake III Arena game data from your own copy of the game, installed where
# the ioquake3 package looks for it (/usr/share/quake3). The data is not
# redistributable, so this package is built locally, not in COPR: copy the
# pak files next to this spec and build
#
#   rpmbuild -bb --define "_sourcedir $PWD" quake3-data.spec
#
# The baseq3 paks are pak0.pk3 from the retail game and pak1-8.pk3 from the
# 1.32 point release (digital editions ship all nine). With Team Arena, build
# with "--with missionpack" and its missionpack/pak0.pk3 and pak1-3.pk3 from
# the point release next to the spec as well, renamed missionpack-pak0.pk3
# to missionpack-pak3.pk3 (rpmbuild looks sources up by file name only).
%bcond missionpack 0

Name:           quake3-data
Version:        1.32
Release:        1%{?dist}
Summary:        Quake III Arena game data
License:        LicenseRef-Proprietary
URL:            https://ioquake3.org/
Source0:        pak0.pk3
Source1:        pak1.pk3
Source2:        pak2.pk3
Source3:        pak3.pk3
Source4:        pak4.pk3
Source5:        pak5.pk3
Source6:        pak6.pk3
Source7:        pak7.pk3
Source8:        pak8.pk3
%if %{with missionpack}
Source10:       missionpack-pak0.pk3
Source11:       missionpack-pak1.pk3
Source12:       missionpack-pak2.pk3
Source13:       missionpack-pak3.pk3
%endif

BuildArch:      noarch
# Owns /usr/share/quake3 and looks for the data there
Requires:       ioquake3

%description
The game data of Quake III Arena 1.32 (baseq3), packaged from a locally
owned copy of the game for the ioquake3 engine. This package is not
redistributable.

%if %{with missionpack}
%package -n quake3-data-missionpack
Summary:        Quake III: Team Arena game data
Requires:       %{name} = %{version}-%{release}

%description -n quake3-data-missionpack
The game data of Quake III: Team Arena 1.32 (missionpack), packaged from a
locally owned copy of the game for the ioquake3 engine. This package is not
redistributable.
%endif

%prep
# Say which pak files are missing rather than fail in %%install
missing=
for f in pak{0..8}.pk3 %{?with_missionpack:missionpack-pak{0..3}.pk3}; do
    [ -f %{_sourcedir}/$f ] || missing="$missing $f"
done
if [ -n "$missing" ]; then
    echo "error: copy these next to the spec:$missing" >&2
    exit 1
fi

%install
install -Dpm 0644 -t %{buildroot}%{_datadir}/quake3/baseq3 \
    %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} \
    %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8}
%if %{with missionpack}
for i in 0 1 2 3; do
    install -Dpm 0644 %{_sourcedir}/missionpack-pak$i.pk3 \
        %{buildroot}%{_datadir}/quake3/missionpack/pak$i.pk3
done
%endif

%files
%{_datadir}/quake3/baseq3/pak[0-8].pk3

%if %{with missionpack}
%files -n quake3-data-missionpack
%dir %{_datadir}/quake3/missionpack
%{_datadir}/quake3/missionpack/pak[0-3].pk3
%endif

%changelog
* Thu Nov 05 2026 Trung Le <8@tle.id.au> - 1.32-1
- Package the baseq3 and, optionally, missionpack data of a local copy
