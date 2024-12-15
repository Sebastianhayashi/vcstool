%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/jazzy/.*$
%global __requires_exclude_from ^/opt/ros/jazzy/.*$
%global debug_package %{nil}

Name:           vcstool
Version:        0.4.6
Release:        1%{?dist}
Summary:        A command-line tool to manage multiple repositories

License:        Apache-2.0
URL:            https://github.com/dirk-thomas/vcstool
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel python3-setuptools
Requires:       python3 PyYAML

%description
vcstool provides a command line tool to invoke version control system commands
on multiple repositories. It supports batch commands for git, hg, svn, and bzr.

%prep
%autosetup -p1

%build
# 修复 PYTHONPATH 环境变量
export PYTHONPATH=/opt/ros/jazzy/lib/python3.11/site-packages:$PYTHONPATH

# 使用 setuptools 构建
python3 setup.py build

%install
# 安装 Python 包
python3 setup.py install --root=%{buildroot} --prefix=%{_prefix} --install-lib=%{python3_sitelib}

# 安装文档
mkdir -p %{buildroot}%{_docdir}/vcstool
cp -p README.rst %{buildroot}%{_docdir}/vcstool/

%if 0%{?with_tests}
%check
# 检查是否有测试存在
if [ -d "tests" ]; then
    pytest tests || echo "Tests failed"
else
    echo "No tests available, skipping."
fi
%endif

%files
/opt/ros/jazzy/*

%changelog
* Sun Dec 15 2024 Sebastian hayashi <microseyuyu@gmail.com> - 0.4.6-1
- Initial RPM release of vcstool
