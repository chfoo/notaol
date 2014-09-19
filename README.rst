======
Notaol
======

Notaol is a work-in-progress client implementation of AOL's communication protocol P3 and display convention FDO.


Quick Start
===========

Notaol is written for Python 3.4 or greater.

1. ``pip3 install crcmod``
2. ``python3 -m notaol.rpc``
3. Connect to localhost on port 5000 using telnet.
4. Type ``{"command": "connect", "username": "someguy", "password": "password1"}`` on telnet.
5. See some logging on the Python process.
6. Type CTRL+], Enter, CTRL+D to quit telnet.

More to come!


Details
=======

For more info, please see 

* `ArchiveTeam's AOL wiki page <http://archiveteam.org/index.php?title=AOL>`_
* WAOL.doc
* `Penggy source code <https://github.com/chfoo/penggy-mirror/tree/master/pengfork>`_

Got more info? Please add to the ArchiveTeam wiki and let us know!

Contribution and feedback is greatly appreciated.
