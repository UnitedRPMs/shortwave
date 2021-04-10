%global debug_package %{nil}
%define _legacy_common_support 1

%global commit0 f67468a56364db7729cbe1b8b696b45dc1e10f3e
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:       shortwave
Version:    1.1.1
Release:    8%{?gver}%{?dist}
Summary:    Find and listen to internet radio stations

Group:      Applications/Internet
License:    GPLv3
URL:        https://gitlab.gnome.org/World/Shortwave
Source0:    https://gitlab.gnome.org/World/Shortwave/-/archive/%{commit0}/Shortwave-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Patch0:     https://gitlab.gnome.org/World/Shortwave/-/commit/164b18de79ebc765818ccd9b718f1527c92ba19e.patch
Patch1:     handy.patch

BuildRequires:  meson
BuildRequires:	cmake
BuildRequires:  ninja-build
# libhandy will replaced with adwaita in 2.0.0
# BuildRequires:  gtk4-devel
# BuildRequires:  libadwaita-qt5-devel adwaita-qt5 libadwaita-qt5
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.14
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires:  intltool desktop-file-utils
BuildRequires:  libappstream-glib-builder
BuildRequires:	libappstream-glib-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:	gettext
BuildRequires:	gcc-c++

# New
BuildRequires:	git
BuildRequires:	libhandy-devel
# We need Rust 1.39
BuildRequires:	rust 
BuildRequires:	cargo
BuildRequires:	libdazzle-devel
BuildRequires:	desktop-file-utils
BuildRequires:	openssl-devel
BuildRequires:	gcc

Requires:       dconf
Requires:       gstreamer1-plugins-base-tools
Requires:       gstreamer1-plugins-base
Requires:       libappstream-glib
Requires:       sqlite-libs
Requires:       gstreamer1-plugins-bad-nonfree
Requires:       gstreamer1-libav
Obsoletes:	gradio 

%description
A GTK3 app for finding and listening to internet radio stations.

%prep 
%setup -n Shortwave-%{commit0} 
%if 0%{?fedora} >= 34
%patch0 -p1 
%else
%patch1 -p1 
%endif

# We need Rust 1.39
# mkdir -p rustdir
#curl -O https://static.rust-lang.org/dist/rust-nightly-x86_64-unknown-linux-gnu.tar.gz
#tar xmzvf rust-nightly-x86_64-unknown-linux-gnu.tar.gz -C $PWD
#chmod a+x rust-nightly-x86_64-unknown-linux-gnu/install.sh
#rust-nightly-x86_64-unknown-linux-gnu/install.sh --prefix=rustdir --disable-ldconfig --verbose

%build

#export PATH=$PATH:$PWD/rustdir/bin:/usr/bin
CFLAGS+=' -fcommon'
%meson
%meson_build

%install
%meson_install

%find_lang shortwave

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/de.haeckerfelix.Shortwave.desktop

%post
%{_bindir}/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ]
then
    %{_bindir}/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
%{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%license COPYING.md
%{_bindir}/%{name}
%{_datadir}/shortwave/
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/applications/de.haeckerfelix.Shortwave.desktop
%{_datadir}/icons/hicolor/*/apps/de.haeckerfelix.*
%{_datadir}/metainfo/*.xml
%{_datadir}/dbus-1/services/*.service


%changelog

* Thu Apr 08 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.1-8.gitf67468a
- Rebuilt

* Mon Jun 08 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.1-7.gitf67468a
- Updated to 1.1.1

* Tue Jun 02 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.0-7.git04d8961
- Updated to 1.1.0

* Fri Mar 27 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.0.1-8.gite73ec4a
- Rebuilt

* Mon Mar 16 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.0.1-7.gite73ec4a
- Final release
