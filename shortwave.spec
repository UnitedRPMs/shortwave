%global debug_package %{nil}

%global commit0 e73ec4a24717e30a6745c1ef0150a57db710da3b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:       shortwave
Version:    1.0.1
Release:    7%{?gver}%{?dist}
Summary:    Find and listen to internet radio stations

Group:      Applications/Internet
License:    GPLv3
URL:        https://gitlab.gnome.org/World/Shortwave
Source0:    https://gitlab.gnome.org/World/Shortwave/-/archive/%{commit0}/Shortwave-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  meson
BuildRequires:  ninja-build
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

# New
BuildRequires:	git
BuildRequires:	libhandy-devel
# We need Rust 1.39
#BuildRequires:	rust 
#BuildRequires:	cargo
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
%autosetup -n Shortwave-%{commit0} -p1 

# We need Rust 1.39
mkdir -p rustdir
curl -O https://static.rust-lang.org/dist/rust-nightly-x86_64-unknown-linux-gnu.tar.gz
tar xmzvf rust-nightly-x86_64-unknown-linux-gnu.tar.gz -C $PWD
chmod a+x rust-nightly-x86_64-unknown-linux-gnu/install.sh
rust-nightly-x86_64-unknown-linux-gnu/install.sh --prefix=rustdir --disable-ldconfig --verbose

%build

export PATH=$PATH:$PWD/rustdir/bin:/usr/bin
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

* Mon Mar 16 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.0.1-7.gite73ec4a
- Final release
