#!/usr/bin/env python

from gi.repository import Gtk
from dbus.mainloop.glib import DBusGMainLoop
import notify2
import sys

def help_cb(n, action):
    assert action == "help"
    print("You clicked Help")
    n.close()

def ignore_cb(n, action):
    assert action == "ignore"
    print("You clicked Ignore")
    n.close()

def empty_cb(n, action):
    assert action == "empty"
    print("You clicked Empty Trash")
    n.close()

def closed_cb(n):
    print("Notification closed")
    Gtk.main_quit()

if __name__ == '__main__':
    if not notify2.init("Multi Action Test", mainloop=DBusGMainLoop()):
        sys.exit(1)

    n = notify2.Notification("Low disk space",
                              "You can free up some disk space by " +
                              "emptying the trash can.")
    n.set_urgency(notify2.URGENCY_CRITICAL)
    n.set_category("device")
    n.add_action("help", "Help", help_cb)
    n.add_action("ignore", "Ignore", ignore_cb)
    n.add_action("empty", "Empty Trash", empty_cb)
    n.connect('closed', closed_cb)

    if not n.show():
        print("Failed to send notification")
        sys.exit(1)

    Gtk.main()
