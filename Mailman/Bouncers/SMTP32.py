# Copyright (C) 1998,1999,2000,2001 by the Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

"""Something which claims
X-Mailer: <SMTP32 vXXXXXX>

What the heck is this thing?  Here's a recent host:

% telnet 207.51.255.218 smtp
Trying 207.51.255.218...
Connected to 207.51.255.218.
Escape character is '^]'.
220 X1 NT-ESMTP Server 208.24.118.205 (IMail 6.00 45595-15)

"""

import re
from mimelib.MsgReader import MsgReader

ecre = re.compile('original message follows', re.IGNORECASE)
acre = re.compile(r'''
    (                                             # several different prefixes
    user\ mailbox[^:]*:                           # have been spotted in the
    |delivery\ failed[^:]*:                       # wild...
    |undeliverable\ to
    )
    \s*                                           # space separator
    (?P<addr>.*)                                  # and finally, the address
    ''', re.IGNORECASE | re.VERBOSE)



def process(msg):
    mailer = msg['x-mailer']
    if not mailer.startswith('<SMTP32 v'):
        return
    mi = MsgReader(msg)
    addrs = {}
    while 1:
        line = mi.readline()
        if not line:
            break
        if ecre.search(line):
            break
        mo = acre.search(line)
        if mo:
            addrs[mo.group('addr')] = 1
    return addrs.keys()
