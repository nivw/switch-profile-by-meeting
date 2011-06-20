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
    p.depends = "python-dbus,python-mafw"
    p.section="user/development"
    p.arch="all"
    p.urgency="extra"
    p.bugtracker='http://unknown'
    p.distribution="fremantle"
    p.repository="extras-devel"
    p.icon='switchProf.png'
    p["/etc/init.d"] = ["switch_backend",]
    p["/usr/lib/hildon-desktop"] = ["switchProfByMeeting.py",]
    p["/usr/lib/switchProfByMeeting"] = ["debug.py", "switch_backend.py", "switch_frontend.py",]
    p["/usr/share/applications/hildon-status-menu"] = ["switchProfByMeeting.desktop",]
    p["/usr/share/icons/hicolor/32x32/hildon"] = ["switchProfile.png",]
    p["/etc/sudoers.d"] = ["switchProfByMeeting.sudoers",]

    p.postinstall = """#!/bin/sh
update-sudoers
#no need according to MohammadAG pkill status
#chmod 755".join(p['/usr/...']
for file in /etc/init.d/switch_backend /usr/lib/switchProfByMeeting/switch_frontend.py /usr/lib/switchProfByMeeting/switch_backend.py /usr/lib/hildon-desktop/switchProfByMeeting.py ; do
chmod 755 $file
done
exit 0
"""

    p.changelog="""First Release
"""

#print p.generate(build_binary=False,build_src=True)
print p.generate(build_binary=True,build_src=True)
