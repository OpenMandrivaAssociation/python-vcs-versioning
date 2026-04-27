%define module vcs-versioning
%define oname vcs_versioning

# Bootstrap mode is needed to break circular dependency with setuptools-scm:
# - vcs-versioning tests require setuptools-scm
# - setuptools-scm >= 10 requires vcs-versioning
# - pytest itself also requires setuptools-scm
# When bootstrapping, we cannot run tests at all.
%bcond bootstrap 0
%bcond tests %{without bootstrap}

Name:		python-vcs-versioning
Summary:	The blessed package to manage your versions by vcs metadata
Version:	1.1.1
Release:	1
License:	MIT
Group:		Development/Python
URL:		https://pypi.org/project/vcs-versioning/
Source0:	https://files.pythonhosted.org/packages/source/v/%{module}/%{oname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildSystem:	python
BuildArch:	noarch
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(packaging)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-xdist)
BuildRequires:	python%{pyver}dist(pytest-console-scripts)
# some tests need setuptools-scm for file finder entry points
# the package is missing from the test dependency group:
# https://github.com/pypa/setuptools-scm/issues/1353
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:  git-core
BuildRequires:	mercurial
%endif

%description
The blessed package to manage your versions by vcs metadata.

%prep -a
# We dont need to be running upstream coverage tests,
# or want the extra test dependencies.
sed -i -e '/pytest-cov/d' pyproject.toml

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:%{python_sitelib}:%{python_sitearch}:$PATH"
# skip tests that require elevated permissions
pytest --ignore testing_vcs/test_file_finders.py --ignore testing_vcs/test_git.py
%endif

%files
%{_bindir}/%{module}
%{py_sitedir}/%{oname}
%{py_sitedir}/%{oname}-%{version}.dist-info
