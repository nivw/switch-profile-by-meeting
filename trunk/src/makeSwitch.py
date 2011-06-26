#!/usr/bin/python
# -*- coding: utf-8 -*-
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
import pypackager
import os

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass

    p=pypackager.PyPackager("switch-profile-by-meeting")
    p.version='0.0.1'
    p.buildversion='1'
    p.display_name='profile-appointments'
    p.description="widget to switch profile to silent when a meeting is in progress , and switch back to general afterward"
    p.author="Niv Waizer"
    p.maintainer="Niv Waizer"
    p.email="nivwiz@gmail.com"
    p.depends = "python-dbus,python-mafw,python-gobject,python-hildon,python-hildondesktop"
    p.section="user/development"
    p.arch="all"
    p.urgency="extra"
    p.bugtracker='http://unknown'
    p.distribution="fremantle"
    p.repository="extras-devel"
    p.icon='switchProf.png'
    p["/etc/init.d"] = ["switch_backend",]
    p["/usr/lib/hildon-desktop"] = ["switchProfByMeeting.py",]
    p["/usr/lib/switchProfByMeeting"] = ["debug.py", "switch_backend.py",]
    p["/usr/share/icons/hicolor/32x32/hildon"] = ["switchProfile.png",]
    p["/etc/sudoers.d"] = ["switchProfByMeeting.sudoers",]
    p["/usr/share/applications/hildon-status-menu"] = ["switchProfByMeeting.desktop",]
    
    p.postinstall = """#!/bin/sh
update-sudoers || true

gtk-update-icon-cache /usr/share/icons/hicolor/

#chmod 755".join(p['/usr/...']
for file in /etc/init.d/switch_backend /usr/lib/switchProfByMeeting/switch_backend.py ; do
chmod 755 $file
done
for file in /usr/share/applications/hildon-status-menu/switchProfByMeeting.desktop /usr/lib/hildon-desktop/switchProfByMeeting.py ; do
chmod 644 $file
chown root:root $file
done
#Force applet reloading to get the icon
  echo "Reloading switchByProfile"
  TMPFILE=`mktemp /tmp/temp.XXXXXX`
  mv /usr/share/applications/hildon-status-menu/switchProfByMeeting.desktop $TMPFILE
  sleep 2
  mv $TMPFILE /usr/share/applications/hildon-status-menu/switchProfByMeeting.desktop
  rm -f $TMPFILE

# Automatically added by dh_pysupport
#if which update-python-modules >/dev/null 2>&1; then
#        update-python-modules  openvpn-applet.private
#fi
exit 0
"""

    p.changelog="""First Release
"""

print p.generate(build_binary=True,build_src=True)
