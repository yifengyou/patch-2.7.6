%global gnulib_ver 20180203

Summary: Utility for modifying/upgrading files
Name: patch
Version: 2.7.6
Release: 11%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/patch/patch.html
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/patch/patch-%{version}.tar.xz
Patch1: patch-2.7.6-CVE-2018-6951.patch
Patch2: patch-CVE-2018-1000156.patch
Patch3: patch-2.7.6-gcc8.patch
Patch4: patch-2.7.6-CVE-2018-6952.patch
Patch5: patch-2.7.6-CVE-2018-20969.patch
Patch6: patch-2.7.6-CVE-2019-13636-symlinks.patch
Patch7: patch-2.7.x-abort_when_cleaning_up_fails.patch
Patch100: patch-selinux.patch
BuildRequires: libselinux-devel
BuildRequires: libattr-devel
BuildRequires: ed
BuildRequires: automake autoconf

Provides: bundled(gnulib) = %{gnulib_ver}

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

Patch should be installed because it is a common way of upgrading
applications.

%prep
%setup -q

# CVE-2018-6951, NULL pointer dereference causes a crash
%patch1 -p1 -b .CVE-2018-6951

# CVE-2018-1000156, Malicious patch files cause ed to execute arbitrary commands
%patch2 -p1 -b .CVE-2018-1000156

# Fix to build with gcc8
%patch3 -p1 -b .gcc8

# CVE-2018-6952, Double free of memory
%patch4 -p1 -b .CVE-2018-6952

# CVE-2018-20969, do_ed_script in pch.c does not block strings beginning with a ! character
%patch5 -p1 -b .CVE-2018-20969

# CVE-2019-13636, Don't follow symlinks unless --follow-symlinks is given
%patch6 -p1 -b .CVE-2019-13636

# bz#1665928, Abort when cleaning up fails
%patch7 -p1 -b .abort_when_cleaning_up_fails

# SELinux support.
%patch100 -p1 -b .selinux

%build
CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"
%ifarch sparcv9
CFLAGS=`echo $CFLAGS|sed -e 's|-fstack-protector||g'`
%endif
%configure --disable-silent-rules
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%files
%defattr(-,root,root,-)
%license COPYING
%doc NEWS README
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Tue Nov 19 2019 Than Ngo <than@redhat.com> - 2.7.6-11
- Related: #1733565, apply the patch correctly

* Tue Nov 19 2019 Than Ngo <than@redhat.com> - 2.7.6-10
- CVE-2019-13636 , Don't follow symlinks unless --follow-symlinks is given
- Resolves: #1665928, patch has a huge error output and segfaults when the file to be patched does not exist

* Mon Sep 02 2019 Than Ngo <than@redhat.com> - 2.7.6-9
- CVE-2018-20969, invoke ed directly instead of using the shell

* Tue Nov 27 2018 Than Ngo <than@redhat.com> - 2.7.6-8
- Added virtual provides for bundled gnulib library

* Wed Sep 12 2018 Than Ngo <than@redhat.com> - 2.7.6-7
- Resolves: #1554752, CVE-2018-6952 Double free of memory

* Mon Jun 18 2018 Than Ngo <than@redhat.com> - 2.7.6-6
- avoid warnings from GCC8

* Mon Apr 09 2018 Than Ngo <than@redhat.com> - 2.7.6-5
- fixed CVE-2018-1000156

* Tue Mar 13 2018 Than Ngo <than@redhat.com> - 2.7.6-4
- apply the patch for CVE-2018-6951

* Mon Feb 12 2018 Tim Waugh <twaugh@redhat.com> - 2.7.6-3
- 2.7.6 (CVE-2016-10713, CVE-2018-6951, CVE-2018-6952).

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.7.5-4
- Add missing %%license macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar  9 2015 Tim Waugh <twaugh@redhat.com> - 2.7.5-1
- Fixed memory leak in selinux patch.
- 2.7.5, including an even better fix for CVE-2015-1196 that still
  allows relative symlinks to be created/used.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.7.4-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Feb  1 2015 Tim Waugh <twaugh@redhat.com> - 2.7.4-1
- 2.7.4, including a better fix for CVE-2015-1196 that still allows
  symlinks referencing ".." to be created.

* Fri Jan 23 2015 Tim Waugh <twaugh@redhat.com> - 2.7.3-1
- 2.7.3 (bug #1182157, CVE-2015-1196, bug #1184491, CVE-2014-9637).

* Tue Jan 20 2015 Tim Waugh <twaugh@redhat.com> - 2.7.1-12
- Apply upstream patch to fix line numbering integer overflow.

* Tue Jan 20 2015 Tim Waugh <twaugh@redhat.com> - 2.7.1-11
- Apply upstream patch to fix directory traversal via symlinks
  (bug #1182157, CVE-2015-1196).

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Tim Waugh <twaugh@redhat.com> 2.7.1-6
- Don't segfault when given bad arguments (bug #972330).

* Thu Apr 11 2013 Tim Waugh <twaugh@redhat.com> 2.7.1-5
- Don't document unsupported -m option; document -x option (bug #948972).

* Mon Mar 25 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.7.1-4
- Build with xattr support.
- Make build output more verbose.
- Fix bogus date in %%changelog.

* Mon Mar 11 2013 Tim Waugh <twaugh@redhat.com> 2.7.1-3
- Upstream patch to fix removal of empty directories (bug #919489).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Tim Waugh <twaugh@redhat.com> 2.7.1-1
- Fixed license (since 2.6 it has been GPLv3+).
- 2.7.1.

* Thu Oct 18 2012 Tim Waugh <twaugh@redhat.com> 2.7-1
- 2.7.  No longer need sigsegv, get-arg, CVE-2010-4651,
  backup-if-mismatch or coverity-leak patches.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-11
- Fixed NULL dereference in selinux patch.

* Mon May 16 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-10
- Applied Jiri Popelka's fixes from Coverity scan (bug #704554):
  - Avoid unchecked return from getfilecon() in patch-selinux.patch.
  - Fix memory leak.

* Wed Feb 16 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-9
- Let --posix cause --no-backup-if-mismatch (bug #678016).

* Thu Feb 10 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-8
- Incorporate upstream fix for CVE-2010-4651 patch so that a target
  name given on the command line is not validated (bug #667529).

* Tue Feb  8 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-7
- Applied upstream patch to fix CVE-2010-4651 so that malicious
  patches cannot create files above the current directory
  (bug #667529).

* Tue Jan  4 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-6
- Use smp_mflags correctly (bug #665770).

* Mon Aug 16 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-5
- Another fix for the selinux patch (bug #618215).

* Fri Aug  6 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-4
- Fixed interpretation of return value from getfilecon().
- Fixed argument type for --get (bug #553624).

* Fri Aug  6 2010 Dennis Gilmore <dennis@ausil.us>
- using -fstack-projector causes weirdness on 32 bit sparc so disabling for now

* Tue Jul 27 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-3
- Fixed argument type for --get (bug #553624).

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-2
- Added comments for all patches.
- Ship COPYING file.
- Removed sparc ifdefs in spec file.

* Mon Jan  4 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-1
- 2.6.1 (bug #551569).  No longer need best-name patch.

* Thu Dec 24 2009 Tim Waugh <twaugh@redhat.com> 2.6-2
- Applied upstream patch to prevent incorrect filename being chosen
  when adding a new file (bug #549122).

* Mon Nov 16 2009 Tim Waugh <twaugh@redhat.com> 2.6-1
- 2.6.  No longer need stderr, suffix, stripcr, parse, allow-spaces,
  ifdef, program_name, or posix-backup patches.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 29 2009 Tim Waugh <twaugh@redhat.com> 2.5.4-39
- Fixed operation when SELinux is disabled (bug #498102).  Patch from
  Jan Kratochvil.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Tim Waugh <twaugh@redhat.com> 2.5.4-37
- Don't set SELinux file context if it is already correct.

* Mon Nov 24 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-36
- Better summary.

* Mon Jun 30 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-35
- Don't fail if setfilecon() returns EPERM (bug #453365), although the
  setfilecon man page suggests that ENOTSUP will be returned in this
  case.

* Mon Jun 16 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-34
- Only write simple backups for each file once during a run
  (bug #234822).

* Thu Jun 12 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-33
- Fix selinux patch and apply it.  Build requires libselinux-devel.

* Fri Feb  8 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-32
- Applied patch from 2.5.9 to allow spaces in filenames (bug #431887).

* Mon Dec  3 2007 Tim Waugh <twaugh@redhat.com> 2.5.4-31
- Convert spec file to UTF-8 (bug #226233).
- Use _bindir macro in %%files (bug #226233).
- Parallel make (bug #226233).
- Better defattr declaration (bug #226233).

* Thu Oct  4 2007 Tim Waugh <twaugh@redhat.com>
- Beginnings of an SELinux patch (bug #165799); not applied yet.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 2.5.4-30
- Added dist tag.
- More specific license tag.
- Fixed summary.
- Better buildroot tag.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4-29.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4-29.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4-29.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Sep  8 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-29
- Remove SELinux patch for now (bug #167822).

* Wed Sep  7 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-27
- Applied patch from Ulrich Drepper to fix string overread (bug #167675).

* Tue Sep  6 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-26
- Preserve SELinux file contexts (bug #165799).

* Thu Aug 11 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-25
- Fixed CRLF detection (bug #154283).

* Wed May  4 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-24
- Reverted last change (bug #154283, bug #156762).

* Fri Apr 29 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-23
- Applied patch from Toshio Kuratomi to avoid problems with DOS-format
  newlines (bug #154283).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-22
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-21
- Rebuilt.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Oct 25 2003 Tim Waugh <twaugh@redhat.com> 2.5.4-18
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuilt in current collinst

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  9 2002 Tim Waugh <twaugh@redhat.com> 2.5.4-12
- Fix error reporting when given bad options (bug #62981).

* Tue Mar  5 2002 Tim Waugh <twaugh@redhat.com> 2.5.4-11
- s/Copyright:/License:/.
- Fix -D behaviour (bug #60688).

* Tue May 29 2001 Tim Waugh <twaugh@redhat.com> 2.5.4-10
- Merge Mandrake patch:
  - fix possible segfault

* Fri Dec  1 2000 Tim Waugh <twaugh@redhat.com>
- Rebuild because of fileutils bug.

* Thu Nov  2 2000 Tim Waugh <twaugh@redhat.com>
- use .orig as default suffix, as per man page and previous behaviour
  (bug #20202).
- use better patch for this, from maintainer.

* Wed Oct  4 2000 Tim Waugh <twaugh@redhat.com>
- actually use the RPM_OPT_FLAGS

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%makeinstall, %%{_tmppath} and %%{_mandir}

* Fri May 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added URL

* Wed Feb 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.5.4
- Fix up LFS support on Alpha (Bug #5732)

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Jun 06 1999 Alan Cox <alan@redhat.com>
- Fix the case where stderr isnt flushed for ask(). Now the 'no such file'
  appears before the skip patch question, not at the very end, Doh!

* Mon Mar 22 1999 Jeff Johnson <jbj@redhat.com>
- (ultra?) sparc was getting large file system support.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Tue Sep  1 1998 Jeff Johnson <jbj@redhat.com>
- bump release to preserve newer than back-ported 4.2.

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- Fix for problem #682 segfault.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- added buildroot

* Tue Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 2.5

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
