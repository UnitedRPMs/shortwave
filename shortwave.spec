%global debug_package %{nil}

%global commit0 bf3585fd0dd690f1963ca6c4b6deb2bb6a3f4786
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:       shortwave
Version:    7.2
Release:    7%{?gver}%{?dist}
Summary:    Find and listen to internet radio stations

Group:      Applications/Internet
License:    GPLv3
URL:        https://gitlab.gnome.org/World/Shortwave
Source0:    https://gitlab.gnome.org/World/Shortwave/-/archive/%{commit0}/Shortwave-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Patch:      drop_desktop_build.patch

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
BuildRequires:  intltool desktop-file-utils
BuildRequires:  libappstream-glib-builder
BuildRequires:	libappstream-glib-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(sqlite3)
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
mkdir build
pushd build
meson .. --prefix /usr
%ninja_build

%install
pushd build
%ninja_install
popd

install -Dm644 data/de.haeckerfelix.Shortwave.desktop.in %{buildroot}/%{_datadir}/applications/de.haeckerfelix.Shortwave.desktop
install -Dm644 data/de.haeckerfelix.Shortwave.appdata.xml.in %{buildroot}/%{_datadir}/appdata/de.haeckerfelix.Shortwave.appdata.xml

desktop-file-install --add-category=AudioVideo %{buildroot}/%{_datadir}/applications/de.haeckerfelix.Shortwave.desktop


# Not yet finished
#find_lang shortwave

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

%files
%license COPYING.md
%{_bindir}/%{name}
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/applications/de.haeckerfelix.Shortwave.desktop
%{_datadir}/icons/hicolor/*/apps/de.haeckerfelix.*
%{_datadir}/appdata/*.appdata.xml
#{_datadir}/locale/*/LC_MESSAGES/{name}.*
%{_datadir}/dbus-1/services/*.service
#{_datadir}/gnome-shell/search-providers/*.ini

%changelog

* Fri Sep 13 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.2-7.gitbf3585f
- Updated to current commit

* Sun Nov 04 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.2-1.git4ccfdb0
- Updated to 7.2-2.git4ccfdb0

* Sun Jan 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.1-1.gitb3bb06b
- Updated to 7.1-1.gitb3bb06b

* Sun Dec 17 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.0-1.git55b6e26
- Updated to 7.0-1.git55b6e26

* Sun Sep 10 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.0.2-1.git73a3cc9
- Updated to 6.0.2-1.git73a3cc9

* Sun Sep 10 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.0-1.git3e8502a
- Updated to 6.0-1.git3e8502a 

* Sat Aug 12 2017 Pavlo Rudyi <paulcarroty at riseup.net> -  5.9-1
- Update to the latest snapshot
- New UI and search engine

* Mon Jan 02 2017 Pavlo Rudyi <paulcarroty at riseup.net> -  5.0.0-4
- Update to the latest snapshot

* Mon Nov 07 2016 Pavlo Rudyi <paulcarroty at riseup.net> -  5.0.0-2
- Update to 5.0.0b2

* Tue Sep 27 2016 Pavlo Rudyi <paulcarroty at riseup.net> -  5.0.0-1
- Update to the latest 5.0.0 beta 1

* Tue Sep 06 2016 Pavlo Rudyi <paulcarroty at riseup.net> -  4.0.1-3
- Update to the latest git snapshot

* Fri Aug 05 2016 Pavlo Rudyi <paulcarroty at riseup> -  4.0.1-2
- Update to the latest git snapshot
