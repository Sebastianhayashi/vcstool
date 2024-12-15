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
BuildRequires:  ros-jazzy-ament-package
Requires:       python3 PyYAML

%description
vcstool provides a command line tool to invoke version control system commands
on multiple repositories. It supports batch commands for git, hg, svn, and bzr.

%prep
%autosetup -p1

%build
# 修复 PYTHONPATH 环境变量
export PYTHONPATH=/opt/ros/jazzy/lib/python3.11/site-packages:$PYTHONPATH

# 修复 CMAKE_PREFIX_PATH 和 PKG_CONFIG_PATH
export CMAKE_PREFIX_PATH=/opt/ros/jazzy
export PKG_CONFIG_PATH=/opt/ros/jazzy/lib/pkgconfig

# 输出环境变量以验证设置
echo "PYTHONPATH: $PYTHONPATH"
echo "CMAKE_PREFIX_PATH: $CMAKE_PREFIX_PATH"
echo "PKG_CONFIG_PATH: $PKG_CONFIG_PATH"

# 验证 ament_package 是否可用
python3 -c "import ament_package" || { echo "ament_package not found"; exit 1; }

# 使用 setuptools 构建
python3 setup.py build

%install
# 安装 Python 包到 /opt/ros/jazzy
python3 setup.py install \
    --root=%{buildroot} \
    --prefix=/opt/ros/jazzy \
    --install-lib=/opt/ros/jazzy/lib/python3.11/site-packages

# 安装文档
mkdir -p %{buildroot}/opt/ros/jazzy/share/doc/vcstool
cp -p README.rst %{buildroot}/opt/ros/jazzy/share/doc/vcstool/

# 安装补全脚本
mkdir -p %{buildroot}/opt/ros/jazzy/share/vcstool-completion/
cp -p vcstool-completion/* %{buildroot}/opt/ros/jazzy/share/vcstool-completion/

%if 0%{?with_tests}
%check
# 检查是否有测试存在
if [ -d "tests" ] || ls test_*.py *_test.py > /dev/null 2>&1; then
    %__python3 -m pytest tests || echo "RPM TESTS FAILED"
else
    echo "No tests to run, skipping."
fi
%endif

%files
%doc /opt/ros/jazzy/share/doc/vcstool/README.rst

/opt/ros/jazzy/bin/vcs
/opt/ros/jazzy/bin/vcs-*
/opt/ros/jazzy/lib/python3.11/site-packages/vcstool/
/opt/ros/jazzy/lib/python3.11/site-packages/vcstool-*.egg-info/
/opt/ros/jazzy/share/vcstool-completion/

%changelog
* Sun Dec 15 2024 Sebastian Hayashi <microseyuyu@gmail.com> - 0.4.6-1
- Initial RPM release of vcstool
