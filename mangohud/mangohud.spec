%global appname MangoHud
%global forgeurl https://github.com/flightlessmango/MangoHud

%global imgui_ver 1.91.6
%global vulkan_headers_ver 1.4.346
%global vulkan_utility_libraries_ver 1.4.346
%global implot_ver 0.16
%global implot_wrap_ver 2

%global tarball_version %%(echo %{version} | tr '~' '-')

# TODO: try to fix amdgpu tests
%bcond_with tests

Name:           mangohud
Version:        0.8.4
%forgemeta
Release:        1%{?dist}
Summary:        Vulkan and OpenGL overlay for monitoring FPS, temperatures, CPU/GPU load

License:        MIT
URL:            %{forgeurl}
Source0:        %{url}/archive/v%{tarball_version}/%{name}-%{tarball_version}.tar.gz
# imgui; its meson build files are in subprojects/packagefiles
Source1:        https://github.com/ocornut/imgui/archive/v%{imgui_ver}/imgui-%{imgui_ver}.tar.gz
# Vulkan-Headers and Vulkan-Utility-Libraries; their meson build files are in
# subprojects/packagefiles
Source3:        https://github.com/KhronosGroup/Vulkan-Headers/archive/v%{vulkan_headers_ver}/Vulkan-Headers-%{vulkan_headers_ver}.tar.gz
Source4:        https://github.com/KhronosGroup/Vulkan-Utility-Libraries/archive/v%{vulkan_utility_libraries_ver}/Vulkan-Utility-Libraries-%{vulkan_utility_libraries_ver}.tar.gz
# implot
Source5:        https://github.com/epezent/implot/archive/v%{implot_ver}/implot-%{implot_ver}.tar.gz
Source6:        https://wrapdb.mesonbuild.com/v%{implot_wrap_ver}/implot_%{implot_ver}-1/get_patch#/implot-%{implot_ver}-wrap.zip
Source20:       README.Fedora.md

BuildRequires:  vulkan-headers
BuildRequires:  appstream
BuildRequires:  dbus-devel
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  libappstream-glib
BuildRequires:  libstdc++-static
BuildRequires:  meson >= 0.60
BuildRequires:  python3-mako
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(glfw3)
BuildRequires:  pkgconfig(glslang)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(spdlog)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xkbcommon)

%if %{with tests}
BuildRequires:  libcmocka-devel
%endif

Requires:       hicolor-icon-theme
Requires:       vulkan-loader%{?_isa}

Recommends:     (mangohud(x86-32) if glibc(x86-32))

Suggests:       %{name}-mangoplot
Suggests:       goverlay

Provides:       bundled(imgui) = %{imgui_ver}
Provides:       bundled(implot) = %{implot_ver}
Provides:       bundled(vulkan-headers) = %{vulkan_headers_ver}
Provides:       bundled(vulkan-utility-libraries) = %{vulkan_utility_libraries_ver}

%global _description %{expand:
A Vulkan and OpenGL overlay for monitoring FPS, temperatures, CPU/GPU load and
more.}

%description %{_description}


%package        mangoplot
Summary:        Local visualization "mangoplot" for %{name}
BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}
Requires:       python3-matplotlib
Requires:       python3-numpy

%description    mangoplot
Local visualization "mangoplot" for %{name}.


%prep
%autosetup -n %{appname}-%{tarball_version} -p1
%setup -qn %{appname}-%{tarball_version} -D -T -a1
%setup -qn %{appname}-%{tarball_version} -D -T -a3
%setup -qn %{appname}-%{tarball_version} -D -T -a4
%setup -qn %{appname}-%{tarball_version} -D -T -a5
%setup -qn %{appname}-%{tarball_version} -D -T -a6

# Meson only overlays a wrap's patch_directory when it unpacks the source
# itself, so copy the build files into the unpacked sources
mv imgui-%{imgui_ver} subprojects/
cp -p subprojects/packagefiles/imgui-%{imgui_ver}/* subprojects/imgui-%{imgui_ver}/
mv Vulkan-Headers-%{vulkan_headers_ver} subprojects/
cp -p subprojects/packagefiles/vulkan-headers/* \
    subprojects/Vulkan-Headers-%{vulkan_headers_ver}/
mv Vulkan-Utility-Libraries-%{vulkan_utility_libraries_ver} subprojects/
cp -p subprojects/packagefiles/vulkan-utility-libraries/* \
    subprojects/Vulkan-Utility-Libraries-%{vulkan_utility_libraries_ver}/
mv implot-%{implot_ver} subprojects/

%if %{with tests}
# Use system cmocka instead of subproject
# https://gitlab.archlinux.org/archlinux/packaging/packages/mangohud/-/blob/0.6.9.1-10/PKGBUILD?ref_type=tags#L32
sed -i "s/  cmocka = subproject('cmocka')//g" meson.build
sed -i "s/cmocka_dep = cmocka.get_variable('cmocka_dep')/cmocka_dep = dependency('cmocka')/g" meson.build
%endif


%build
%meson \
    -Dmangoapp=true \
    -Dmangohudctl=true \
    -Dinclude_doc=true \
    -Duse_system_spdlog=enabled \
    -Dwith_wayland=enabled \
    -Dwith_xnvctrl=disabled \
    %if %{with tests}
    -Dtests=enabled \
    %else
    -Dtests=disabled \
    %endif
    %{nil}
%meson_build


%install
%meson_install

# ERROR: ambiguous python shebang
sed -i "s@#!/usr/bin/env python@#!/usr/bin/python3@" \
    %{buildroot}%{_bindir}/mangoplot

# Install Fedora docs
install -D -p -m 0644 %{SOURCE20} %{buildroot}%{_docdir}/%{name}/README.Fedora.md


%check
# https://github.com/flightlessmango/MangoHud/issues/812
# ? tag-invalid           : stock icon is not valid [io.github.flightlessmango.mangohud]
%dnl appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
%if %{with tests}
%meson_test
%endif


%files
%license LICENSE
%doc README.md presets.conf.example README.Fedora.md
%{_bindir}/mangoapp
%{_bindir}/mangohud
%{_bindir}/mangohudctl
%{_datadir}/icons/hicolor/scalable/*/*.svg
%{_datadir}/vulkan/implicit_layer.d/*Mango*.json
%{_docdir}/%{name}/%{appname}.conf.example
%{_libdir}/%{name}/
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/mangoapp.1*
%{_metainfodir}/*.metainfo.xml

%files mangoplot
%{_bindir}/mangoplot


%changelog
* Wed Nov 18 2026 Trung Lê <8@tle.id.au> - 0.8.4-1
- Based on Fedora's mangohud 0.8.3~rc1-4, updated to 0.8.4
- Bundle Vulkan-Headers 1.4.346 and Vulkan-Utility-Libraries 1.4.346, as
  upstream now does, with the meson files from subprojects/packagefiles
  instead of the wrapdb patches
- Drop the removal of libimgui.a, which upstream no longer installs
