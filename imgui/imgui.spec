Name:           imgui
Version:        1.92.8
Release:        1%{?dist}
Summary:        Bloat-free graphical user interface library for C++

# imgui:                                       MIT
# imstb_rectpack.h, imstb_textedit.h, imstb_truetype.h (modified stb):
#                                              MIT OR Unlicense
License:        MIT AND (MIT OR Unlicense)
URL:            https://github.com/ocornut/imgui
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# Upstream ships no build system
Source1:        %{name}-CMakeLists.txt

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(sdl3)
BuildRequires:  pkgconfig(vulkan)

# Modified copies, used for the text editing widget, the font atlas packer
# and, with FreeType disabled at runtime, glyph rasterisation
Provides:       bundled(stb_rect_pack) = 1.01
Provides:       bundled(stb_textedit) = 1.14
Provides:       bundled(stb_truetype) = 1.26

BuildSystem:    cmake
BuildOption:    -DIMGUI_VERSION=%{version}

%description
Dear ImGui is a bloat-free graphical user interface library for C++. It
outputs optimized vertex buffers that you can render anytime in your
3D-pipeline-enabled application. It is fast, portable, renderer agnostic,
and self-contained (no external dependencies).

This build includes the FreeType font loader, imgui_stdlib and the SDL3
(platform, SDL_Renderer and SDL_GPU), OpenGL 2, OpenGL 3 and Vulkan
backends.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Included by imgui_impl_sdlgpu3.h and imgui_impl_vulkan.h
Requires:       pkgconfig(sdl3)
Requires:       pkgconfig(vulkan)

%description devel
The headers, CMake package (imgui::imgui) and pkg-config file for
developing applications that use Dear ImGui.

%prep -a
cp -p %{SOURCE1} CMakeLists.txt
# The library is built with the FreeType font loader, so applications must
# see the same configuration
sed -i 's|^//#define IMGUI_ENABLE_FREETYPE$|#define IMGUI_ENABLE_FREETYPE|' imconfig.h
grep -q '^#define IMGUI_ENABLE_FREETYPE$' imconfig.h

%check
# Build and run the headless example against the library just built
%{__cxx} %{optflags} -I. examples/example_null/main.cpp \
    -L%{__cmake_builddir} -limgui -o example_null
LD_LIBRARY_PATH=%{__cmake_builddir} ./example_null

%files
%license LICENSE.txt
%{_libdir}/libimgui.so.%{version}

%files devel
%doc docs/CHANGELOG.txt docs/FAQ.md docs/FONTS.md docs/README.md
%{_includedir}/imgui
%{_libdir}/libimgui.so
%{_libdir}/cmake/imgui
%{_libdir}/pkgconfig/imgui.pc

%changelog
* Tue Nov 17 2026 Trung Lê <8@tle.id.au> - 1.92.8-1
- Initial package of Dear ImGui 1.92.8, with the FreeType font loader and
  the SDL3, OpenGL and Vulkan backends
