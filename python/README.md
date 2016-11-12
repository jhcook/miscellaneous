File Checksum Daemon
=========

This is a Python daemon that works quite nicely. It was developed as a proof of
concept as software that could watch a file system and report any events.

Linux's inotify is used; however, it is possible to add Mac OSX fsevents
support. There is no plan to add this support any time soon.

ec2.py
=========

This was written years ago to create and instantiate instances in AWS EC2

matter
=========

The was written to integrate a Tweet stream with a mailing list. In this instance
it was used for Twitter and a Google Group for Stanford's AI course circa 2011.
