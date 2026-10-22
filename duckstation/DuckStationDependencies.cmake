# Replaces CMakeModules/DuckStationDependencies.cmake for the Fedora build.
#
# Upstream links against a prebuilt dependency pack (dep/prebuilt/<platform>),
# which does not exist for ppc64le. This module uses Fedora's libraries instead,
# plus the few that Fedora lacks or builds differently, which the spec builds
# into DS_BUNDLED_PREFIX first:
#   libbacktrace, cpuinfo, SPIRV-Cross C API, shaderc (stenzek fork),
#   discord-rpc and SoundTouchDLL, as shared libraries installed next to the
#   binary.
#
# It creates the same imported targets as upstream's module, so the rest of the
# build is unchanged.

if(NOT DS_BUNDLED_PREFIX)
  message(FATAL_ERROR "DS_BUNDLED_PREFIX must point to the bundled dependencies prefix.")
endif()

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)
find_package(PkgConfig REQUIRED)

# Headers of the bundled libraries (e.g. discord_rpc.h) for every target.
include_directories(SYSTEM "${DS_BUNDLED_PREFIX}/include")

# Creates an interface target ${target} from pkg-config module ${module}, unless a CMake
# package config already defined it. Libraries that DuckStation loads at runtime only
# need the headers, so linking is opt-in with LINK.
function(ds_pkg_target target module)
  if(TARGET ${target})
    return()
  endif()
  cmake_parse_arguments(ARG "LINK" "" "" ${ARGN})
  string(MAKE_C_IDENTIFIER "DSPC_${module}" prefix)
  pkg_check_modules(${prefix} REQUIRED IMPORTED_TARGET ${module})
  add_library(${target} INTERFACE IMPORTED GLOBAL)
  set_target_properties(${target} PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${${prefix}_INCLUDE_DIRS}")
  if(ARG_LINK)
    target_link_libraries(${target} INTERFACE PkgConfig::${prefix})
  endif()
endfunction()

# Creates an imported target ${target} for a library in the bundled prefix, with
# headers in include/ or the subdirectory given as the third argument.
function(ds_bundled_target target libname)
  find_library(DS_BUNDLED_${libname} NAMES ${libname} PATHS "${DS_BUNDLED_PREFIX}/lib" NO_DEFAULT_PATH REQUIRED)
  add_library(${target} UNKNOWN IMPORTED GLOBAL)
  set_target_properties(${target} PROPERTIES
    IMPORTED_LOCATION "${DS_BUNDLED_${libname}}"
    INTERFACE_INCLUDE_DIRECTORIES "${DS_BUNDLED_PREFIX}/include/${ARGV2}"
  )
endfunction()

# Package configs first: they may define targets with the names used below.
set(QT_NO_PRIVATE_MODULE_WARNING ON)
find_package(Qt6 6.11 REQUIRED COMPONENTS Core Gui GuiPrivate Widgets LinguistTools DBus)
find_package(SDL3 REQUIRED CONFIG COMPONENTS Headers)
find_package(zstd CONFIG QUIET)

# Linked libraries.
find_package(ZLIB REQUIRED)
find_package(CURL REQUIRED)
find_package(UDEV REQUIRED)
ds_pkg_target(zstd::libzstd_shared libzstd LINK)

# Bundled, linked libraries.
set(CMAKE_PREFIX_PATH "${DS_BUNDLED_PREFIX}")
find_package(Libbacktrace REQUIRED)
find_package(cpuinfo REQUIRED CONFIG NO_DEFAULT_PATH PATHS "${DS_BUNDLED_PREFIX}")
ds_bundled_target(SoundTouch::SoundTouchDLL soundtouch)

# Libraries loaded at runtime: only their headers are used at build time.
ds_pkg_target(libjpeg-turbo::jpeg libjpeg)
ds_pkg_target(PNG::png_shared libpng16)
ds_pkg_target(WebP::webp libwebp)
ds_pkg_target(WebP::sharpyuv libsharpyuv)
ds_pkg_target(WebP::webpdecoder libwebpdecoder)
ds_pkg_target(WebP::webpdemux libwebpdemux)
ds_pkg_target(WebP::libwebpmux libwebpmux)
ds_pkg_target(libzip::zip libzip)
ds_pkg_target(SQLite3::sqlite3-shared sqlite3)
ds_pkg_target(freetype freetype2)
ds_pkg_target(harfbuzz::harfbuzz harfbuzz)
ds_pkg_target(plutosvg::plutosvg plutosvg)
ds_bundled_target(Shaderc::shaderc_shared shaderc_shared)
ds_bundled_target(spirv-cross-c-shared spirv-cross-c-shared spirv_cross)
ds_bundled_target(DiscordRPC::discord-rpc discord-rpc)

if(ENABLE_X11)
  find_package(X11 REQUIRED)
  if(NOT X11_xcb_FOUND)
    message(FATAL_ERROR "XCB is required")
  endif()
endif()

if(ENABLE_WAYLAND)
  find_package(ECM REQUIRED NO_MODULE)
  list(APPEND CMAKE_MODULE_PATH "${ECM_MODULE_PATH}")
  find_package(Wayland REQUIRED Egl)
endif()

find_package(FFMPEG COMPONENTS avcodec avformat avutil swresample swscale REQUIRED)

# The binary and the bundled shared libraries are installed in the same directory,
# and system libraries are found through the default search path, so $ORIGIN is
# the only RPATH needed. These override the functions in DuckStationUtils.cmake:
# the top-level CMakeLists.txt sets CMAKE_INSTALL_RPATH from the first.
function(get_origin_relative_path OUTVAR DIR)
  set(${OUTVAR} "$ORIGIN" PARENT_SCOPE)
endfunction()

function(add_runtime_libraries TARGET)
endfunction()
