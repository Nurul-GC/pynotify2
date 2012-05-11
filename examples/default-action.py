#!/usr/bin/env python

from gi.repository import Gtk
import notify2
import sys

def default_cb(n, action):
    assert action == "default"
    print("You clicked the default action")
    n.close()

def closed_cb(n):
    print("Notification closed")
    Gtk.main_quit()

if __name__ == '__main__':
    if not notify2.init("Default Action Test", mainloop='glib'):
        sys.exit(1)

    n = notify2.Notification("Matt is online")
    n.set_category("presence.online")
    n.add_action("default", "Default Action", default_cb)
    n.connect('closed', closed_cb)

    if not n.show():
        print("Failed to send notification")
        sys.exit(1)

    Gtk.main()
