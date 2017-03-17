#
# rpmbuild -ba sysmo-operator.spec
#

Name:		sysmo-operator
Version:	0
Release:	1%{?dist}
Summary:	Sysmo Core client UI
Group:		Application/Productivity
License:	GPLv3+
URL:		http://www.sysmo.io/
Source:         %{name}-%{version}.tar.gz


# centos/redhad 6
%{?el6:BuildRequires: gcc-c++,qt-devel,desktop-file-utils,cmake}
%{?el6:Requires: qt,java}
%{?el6:Requires(post): desktop-file-utils}
%{?el6:Requires(postun): desktop-file-utils}

# centos/redhad 7
%{?el7:BuildRequires: gcc-c++,qt-devel,desktop-file-utils,cmake}
%{?el7:Requires: qt,java}
%{?el7:Requires(post): desktop-file-utils}
%{?el7:Requires(postun): desktop-file-utils}

# fedora 23
%{?fc23:BuildRequires: gcc-c++,qt-devel,desktop-file-utils,cmake}
%{?fc23:Requires: qt,java}
%{?fc23:Requires(post): desktop-file-utils}
%{?fc23:Requires(postun): desktop-file-utils}
%{?fc23:%global qmake /usr/bin/qmake-qt4}

# fedora 24
%{?fc24:BuildRequires: gcc-c++,qt-devel,desktop-file-utils,cmake}
%{?fc24:Requires: qt,java}
%{?fc24:Requires(post): desktop-file-utils}
%{?fc24:Requires(postun): desktop-file-utils}
%{?fc24:%global qmake /usr/bin/qmake-qt4}

# fedora 25
%{?fc25:BuildRequires: gcc-c++,qt-devel,desktop-file-utils,cmake}
%{?fc25:Requires: qt,java}
%{?fc25:Requires(post): desktop-file-utils}
%{?fc25:Requires(postun): desktop-file-utils}
%{?fc25:%global qmake /usr/bin/qmake-qt4}


%description
Sysmo-Operator is the main UI for interacting with Sysmo-Core server.

%prep
%setup

%build
./bootstrap
make

# install
%install
mkdir -p "%{buildroot}%{_bindir}"
mkdir -p "%{buildroot}%{_datadir}/applications"
install -m 751 _build/sysmo-operator %{buildroot}%{_bindir}/
desktop-file-install \
	--vendor="" \
	--dir=%{buildroot}%{_datadir}/applications/ \
	support/packages/obs/common/sysmo-operator.desktop

mkdir -p %{buildroot}%{_datadir}
cp -R support/packages/obs/rpm/icons %{buildroot}%{_datadir}
find %{buildroot}%{_datadir} -name "*.png" -exec chmod 644 {} \;

%post
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/HighContrast &> /dev/null || :
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/HighContrast &> /dev/null || :
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%files
%{_bindir}/sysmo-operator
%{_datadir}/applications/sysmo-operator.desktop
%{_datadir}/icons/*



%changelog
* Tue Nov  3 2015 Sebastien Serre <ssbx@sysmo.io> 1.1.1-1
- Initial rpm build
