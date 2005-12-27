%define nhgamedir /usr/games/nethack-3.4.3
%define nhdatadir /var/games/nethack

Name:           nethack
Version:        3.4.3
Release:        6%{?dist}
Summary:        A rogue-like single player dungeon exploration game

Group:          Amusements/Games
License:        NetHack General Public License
URL:            http://nethack.org
Source0:        http://dl.sf.net/%{name}/%{name}-343-src.tgz
Source1:        %{name}.desktop
Patch0:         %{name}-%{version}-makefile.patch
Patch1:         %{name}-%{version}-config.patch
Patch2:         %{name}-%{version}-x11.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel
BuildRequires:  bison, flex, desktop-file-utils
BuildRequires:  bdftopcf, mkfontdir, libX11-devel, libXaw-devel, libXext-devel
BuildRequires:  libXmu-devel, libXpm-devel, libXt-devel


%description
NetHack is a single player dungeon exploration game that runs on a
wide variety of computer systems, with a variety of graphical and text
interfaces all using the same game engine.

Unlike many other Dungeons & Dragons-inspired games, the emphasis in
NetHack is on discovering the detail of the dungeon and not simply
killing everything in sight - in fact, killing everything in sight is
a good way to die quickly.

Each game presents a different landscape - the random number generator
provides an essentially unlimited number of variations of the dungeon
and its denizens to be discovered by the player in one of a number of
characters: you can pick your race, your role, and your gender.


%prep
%setup -q
%patch0 -b .makefile
%patch1 -b .config
%patch2 -b .x11
(source sys/unix/setup.sh)

# Set our paths
%{__sed} -i -e "s:^\(HACKDIR=\).*:\1%{nhgamedir}:" sys/unix/nethack.sh
%{__sed} -i -e "s:FEDORA_CONFDIR:%{nhgamedir}:" sys/unix/nethack.sh
%{__sed} -i -e "s:FEDORA_STATEDIR:%{nhdatadir}:" include/unixconf.h
%{__sed} -i -e "s:FEDORA_HACKDIR:%{nhgamedir}:" include/config.h
%{__sed} -i -e "s:/usr/games/lib/nethackdir:%{nhgamedir}:" \
        doc/nethack.6 doc/nethack.txt doc/recover.6 doc/recover.txt

# Point the linker in the right direction
%{__sed} -i -e "s:-L/usr/X11R6/lib:-L/usr/X11R6/%{_lib}:" \
        src/Makefile util/Makefile


%build
make all


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall \
        GAMEDIR=$RPM_BUILD_ROOT%{nhgamedir} \
        VARDIR=$RPM_BUILD_ROOT%{nhdatadir} \
        SHELLDIR=$RPM_BUILD_ROOT%{_bindir} \
        CHOWN=/bin/true \
        CHGRP=/bin/true

rm -rf $RPM_BUILD_ROOT%{nhgamedir}/save
mv $RPM_BUILD_ROOT%{nhgamedir}/recover $RPM_BUILD_ROOT%{_bindir}/nethack-recover

install -d -m 0755 $RPM_BUILD_ROOT%{_mandir}/man6
make -C doc MANDIR=$RPM_BUILD_ROOT%{_mandir}/man6 manpages

install -D -p -m 0644 win/X11/nh_icon.xpm \
        $RPM_BUILD_ROOT%{_datadir}/pixmaps/nethack.xpm

desktop-file-install \
        --vendor fedora \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications \
        --add-category X-Fedora \
        --add-category Application \
        --add-category Game \
        %{SOURCE1}

# Install the fonts for the X11 interface
cd win/X11
bdftopcf -o nh10.pcf nh10.bdf
bdftopcf -o ibm.pcf ibm.bdf
install -D -p -m 644 ibm.pcf $RPM_BUILD_ROOT%{nhgamedir}/fonts/ibm.pcf
install -D -p -m 644 nh10.pcf $RPM_BUILD_ROOT%{nhgamedir}/fonts/nh10.pcf

%{__sed} -i -e 's:^!\(NetHack.tile_file.*\):\1:' \
        $RPM_BUILD_ROOT%{nhgamedir}/NetHack.ad

%post
mkfontdir $RPM_BUILD_ROOT%{nhgamedir}/fonts


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*.txt README dat/license dat/history
%doc dat/opthelp dat/wizhelp
%{_mandir}/man6/*
%{_datadir}/pixmaps/nethack.xpm
%{_datadir}/applications/fedora-nethack.desktop
%{nhgamedir}/nhdat
%{_bindir}/nethack
%{_bindir}/nethack-recover
%{nhgamedir}/NetHack.ad
%{nhgamedir}/pet_mark.xbm
%{nhgamedir}/rip.xpm
%{nhgamedir}/x11tiles
%{nhgamedir}/fonts/
%defattr(0664,root,games)
%config(noreplace) %{nhdatadir}/record
%config(noreplace) %{nhdatadir}/perm
%config(noreplace) %{nhdatadir}/logfile
%attr(0775,root,games) %dir %{nhdatadir}
%attr(0775,root,games) %dir %{nhdatadir}/save
%attr(2755,root,games) %{nhgamedir}/nethack


%changelog
* Tue Dec 27 2005 Luke Macken <lmacken@redhat.com> 3.4.3-6
- Rebuild

* Wed Nov 23 2005 Luke Macken <lmacken@redhat.com> 3.4.3-5
- Keep the license in the game directory (Bug #173385)
- Don't obsolete falconseye anymore (Bug #173385)

* Fri Nov 11 2005 Luke Macken <lmacken@redhat.com> 3.4.3-4
- Utilize modular xorg

* Thu Sep 08 2005 Luke Macken <lmacken@redhat.com> 3.4.3-3
- Point linker in the right direction using %%{_lib} to fix x86_64 build issues

* Tue Sep 06 2005 Luke Macken <lmacken@redhat.com> 3.4.3-2
- Enable x11 support

* Sun Jul 10 2005 Luke Macken <lmacken@redhat.com> 3.4.3-1
- Initial package for Fedora Extras
