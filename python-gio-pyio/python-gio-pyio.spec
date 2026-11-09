Name:           python-gio-pyio
Version:        0.0.6
Release:        1%{?dist}
Summary:        Python-like file objects for Gio streams

# The tests, which are not installed, are under PSF-2.0.
License:        GPL-3.0-only
URL:            https://github.com/cmkohnen/gio_pyio
# The PyPI sdist leaves out the tests' data files
Source:         %{url}/archive/%{version}/gio_pyio-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
# The tests use Gio, and glib-compile-resources
BuildRequires:  python3-gobject
BuildRequires:  /usr/bin/glib-compile-resources

%global _description %{expand:
gio-pyio wraps Gio streams and files as Python file objects, for GTK apps
that handle files as GFile and use Python libraries that expect file
objects. It is used by Graphs.}

%description %_description

%package -n     python3-gio-pyio
Summary:        %{summary}

%description -n python3-gio-pyio %_description

%prep
%autosetup -n gio-pyio-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l gio_pyio

%check
%pyproject_check_import
%{py3_test_envvars} %{python3} -m unittest discover -v -s tests

%files -n python3-gio-pyio -f %{pyproject_files}
%doc README.md

%changelog
* Tue Nov 10 2026 Trung Lê <trung.le@ruby-journal.com> - 0.0.6-1
- Initial package
