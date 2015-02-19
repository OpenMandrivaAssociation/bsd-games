Summary: Collection of text-based games
Name: bsd-games
Version: 2.17
Release: 25
License: BSD
Group: Games/Other
URL: ftp://metalab.unc.edu/pub/Linux/games/
Source0: ftp://metalab.unc.edu/pub/Linux/games/bsd-games-%{version}.tar.gz
Source1: config.params
# A collection of patches from Debian.
Patch0: bsd-games-2.17-debian.patch
# Patches from Fedora Core 1
Patch1: bsd-games-2.17-ospeed.patch
Patch2: bsd-games-2.17-getline.patch
Patch3: bsd-games-2.17-utmpstruct.patch
# Additional new patches
Patch4: bsd-games-2.17-setresgid.patch
Patch5: bsd-games-2.17-tetrisgid.patch
Patch6: bsd-games-2.17-hackgid.patch
Patch7: bsd-games-2.17-phantasiagid.patch
# Add patches for man page renames
Patch8: bsd-games-2.17-monop-rename.patch
Patch9: bsd-games-2.17-banner-rename.patch
Patch10: bsd-games-2.17-stdio-c++.patch
Patch11: bsd-games-2.17-nolibtermcap.patch
Patch12: bsd-games-2.17-tetris-rename.patch
Patch13: bsd-games-2.17-gcc4.3.patch
Patch14: bsd-games-2.17-format-security.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires: ncurses-devel words flex bison

%description
Bsd-games includes adventure, arithmetic, atc, backgammon, battlestar,
bcd, caesar, canfield, cfscores, cribbage, go-fish, gomoku,
hunt, mille, mpoly, morse, number, phantasia, pig, pom, ppt, primes,
quiz, rain, random, robots, rot13, sail, snake, snscore, teachgammon,
bsd-fbg, trek, worm, worms and wump.

%prep
%setup -q
install -p -m 755 %{SOURCE1} .
%patch0 -p1 -b .debian
%patch1 -p1 -b .ospeed
%patch2 -p1 -b .getline
%patch3 -p1 -b .utmpstruct
%patch4 -p1 -b .setresgid
%patch5 -p1 -b .tetrisgid
%patch6 -p1 -b .hackgid
%patch7 -p1 -b .phantasiagid
%patch8 -p1 -b .monop.rename
%patch9 -p0 -b .banner.rename
%patch10 -p0 -b .cplusplus
%patch11 -p0 -b .nolibtermcap
%patch12 -p0 -b .tetris.rename
%patch13 -p1
%patch14 -p1 -b .format-security

%build
# We include a templatized configuration settings file to set
# reasonable defaults, and to tell the configure script not to
# run in interactive mode.
sed -i.bak -e "s#@DESTDIR@#$RPM_BUILD_ROOT#" \
    -e "s#@bindir@#%{_bindir}#" \
    -e "s#@docdir@#%{_docdir}#" \
    -e "s#@sbindir@#%{_sbindir}#" \
    -e "s#@datadir@#%{_datadir}#" \
    -e "s#@libdir@#%{_libdir}#" \
    -e "s#@mandir@#%{_mandir}#" \
    -e "s#@var@#%{_var}#" \
    -e "s#@RPM_OPT_FLAGS@#$RPM_OPT_FLAGS#" \
    config.params 

# Don't use %%configure.  This configure script wasn't generated by
# autoconf and doesn't obey things like --prefix.
export LDFLAGS="$LDFLAGS -lfl"
./configure
%make RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"

# Rename one doc file to avoid naming collisions
cp hunt/README README.hunt

%install
make RPM_BUILD_ROOT="$RPM_BUILD_ROOT" install

# Change the binary name for monop to prevent a conflict with the mono-devel
# package
mv $RPM_BUILD_ROOT/%{_bindir}/monop $RPM_BUILD_ROOT/%{_bindir}/mpoly
mv $RPM_BUILD_ROOT/%{_mandir}/man6/monop.6.gz $RPM_BUILD_ROOT/%{_mandir}/man6/mpoly.6.gz

# Change the binary name for banner to prevent a conflict with a Fedora
# package with the same name
mv $RPM_BUILD_ROOT/%{_bindir}/banner $RPM_BUILD_ROOT/%{_bindir}/vert-banner
mv $RPM_BUILD_ROOT/%{_mandir}/man6/banner.6.gz $RPM_BUILD_ROOT/%{_mandir}/man6/vert-banner.6.gz

# Change the binary name for tetris to prevent a conflict with the mono-devel
# package
mv $RPM_BUILD_ROOT/%{_bindir}/tetris-bsd $RPM_BUILD_ROOT/%{_bindir}/bsd-fbg
mv $RPM_BUILD_ROOT/%{_mandir}/man6/tetris-bsd.6.gz $RPM_BUILD_ROOT/%{_mandir}/man6/bsd-fbg.6.gz

# Change the binary name for rain to prevent a conflict with mesa-demos package
mv $RPM_BUILD_ROOT/%{_bindir}/rain $RPM_BUILD_ROOT/%{_bindir}/bsd-rain
mv $RPM_BUILD_ROOT/%{_mandir}/man6/rain.6.gz $RPM_BUILD_ROOT/%{_mandir}/man6/bsd-rain.6.gz

# Change the binary name for hunt to prevent a conflict with hunt package
mv $RPM_BUILD_ROOT/%{_bindir}/hunt $RPM_BUILD_ROOT/%{_bindir}/bsd-hunt
mv $RPM_BUILD_ROOT/%{_mandir}/man6/hunt.6.gz $RPM_BUILD_ROOT/%{_mandir}/man6/bsd-hunt.6.gz

# Remove this doc file.  We're copying it to a different location for Fedora.
rm -f $RPM_BUILD_ROOT/%{_docdir}/trek.me

%pre
%_pre_groupadd gamehack
%_pre_groupadd gamesail
%_pre_groupadd gamephant

%postun
%_postun_groupdel gamehack
%_postun_groupdel gamesail
%_postun_groupdel gamephant

%files
%defattr(-,root,root)
%{_bindir}/adventure
%{_bindir}/arithmetic
%attr(2755,root,games) %{_bindir}/atc
%{_bindir}/backgammon
%{_bindir}/teachgammon
%attr(2755,root,games) %{_bindir}/battlestar
%{_bindir}/boggle
%{_bindir}/bcd
%{_bindir}/caesar
%{_bindir}/dab
%{_bindir}/rot13
%attr(2755,root,games) %{_bindir}/canfield
%{_bindir}/cfscores
%attr(2755,root,games) %{_bindir}/cribbage
%{_bindir}/go-fish
%{_bindir}/gomoku
%attr(2755,root,gamehack) %{_bindir}/hack
%{_bindir}/hangman
%{_bindir}/bsd-hunt
%{_bindir}/mille
%{_bindir}/mpoly
%{_bindir}/morse
%{_bindir}/number
%attr(2755,root,gamephant) %{_bindir}/phantasia
%{_bindir}/pig
%{_bindir}/pom
%{_bindir}/ppt
%{_bindir}/primes
%{_bindir}/quiz
%{_bindir}/bsd-rain
%{_bindir}/random
%attr(2755,root,games) %{_bindir}/robots
%attr(2755,root,gamesail) %{_bindir}/sail
%attr(2755,root,games) %{_bindir}/snake
%{_bindir}/snscore
%attr(2755,root,games) %{_bindir}/bsd-fbg
%{_bindir}/trek
%{_bindir}/vert-banner
%{_bindir}/worm
%{_bindir}/worms
%{_bindir}/wtf
%{_bindir}/wump
%{_datadir}/%{name}
%{_datadir}/misc/acronyms
%{_datadir}/misc/acronyms.comp
%{_mandir}/man6/*
%{_sbindir}/huntd
%config %attr(664,root,games) %{_var}/games/atc_score
%config %attr(664,root,games) %{_var}/games/battlestar.log
%config %attr(664,root,games) %{_var}/games/cfscores
%config %attr(664,root,games) %{_var}/games/criblog
%dir %attr(0775,root,gamehack) %{_var}/games/hack
%config %attr(664,root,gamehack) %{_var}/games/hack/*
%dir %attr(775,root,gamephant) %{_var}/games/phantasia
%config %attr(664,root,gamephant) %{_var}/games/phantasia/*
%dir %attr(775,root,gamesail) %{_var}/games/sail
%config %attr(644,root,games) %{_var}/games/robots_roll
%config %attr(664,root,gamesail) %{_var}/games/saillog
%config %attr(664,root,games) %{_var}/games/snake.log
%config %attr(664,root,games) %{_var}/games/snakerawscores
%config %attr(664,root,games) %{_var}/games/bsd-fbg.scores
%doc AUTHORS COPYING ChangeLog ChangeLog.0 THANKS YEAR2000 README.hunt trek/USD.doc/trek.me


