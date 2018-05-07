%define major 2
%define libname %mklibname fm-qt %major
%define devname %mklibname -d fm-qt

Name:           pcmanfm-qt
Version:        0.12.0
Release:        2%{?dist}
Source0:        http://downloads.lxqt.org/lxqt/%{version}/%{name}-%{version}.tar.xz
Source1:	settings.conf
Summary:        File manager for the LXQt desktop
URL:            http://lxqt.org/
License:        GPLv2+
Group:          Graphical desktop/Other
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  pkgconfig(libfm) >= 1.2.0
BuildRequires:  pkgconfig(libmenu-cache)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(lxqt)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5Help)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  cmake(fm-qt)
Requires:       lxqt-l10n

# recommended for kwin and kdesu for "run as root" functionality (mga#15088)
# changed to Recommends to allow parallel installation with plasma 5
Recommends: kde-cli-tools

%description
File manager for the LXQt desktop.

%prep
%setup -q %{name}-%{version}

# change desktop file name and comment to distinguish it from pcmanfm
sed -i 's/File Manager/QT File Manager/' pcmanfm/pcmanfm-qt.desktop.in

# change gksu to lxqt-sudo as with gksu no icons are shown when running as root
sed -i 's|gksu %s|%{_bindir}/lxqt-sudo -s %s|g' pcmanfm/preferences.ui

%build
%cmake_qt5 -DBUILD_DOCUMENTATION=ON -DPULL_TRANSLATIONS=NO
%make_build

%install
%make_install -C build

desktop-file-install --add-category="System;FileTools" \
 --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop

# Add a custom panel configuration as default
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/xdg/pcmanfm-qt/lxqt/settings.conf

%files
%doc %{_defaultdocdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_sysconfdir}/xdg/autostart/lxqt-desktop.desktop
%{_sysconfdir}/xdg/pcmanfm-qt/lxqt/settings.conf
%{_mandir}/man1/pcmanfm-qt.1.*
