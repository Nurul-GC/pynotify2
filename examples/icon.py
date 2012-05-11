#!/usr/bin/env python
from __future__ import print_function

import notify2
from gi.repository import Gtk
import sys
import os

if __name__ == '__main__':
    if not notify2.init("Images Test"):
        sys.exit(1)

    # Stock icon
    n = notify2.Notification("Icon Test", "Testing stock icon",
                              "notification-message-email")

    if not n.show():
        print("Failed to send notification")
        sys.exit(1)

    # Image URI
    uri = "file://" + os.path.abspath(os.path.curdir) + "/applet-critical.png"
    print("Sending", uri)

    n = notify2.Notification("Alert!", "Testing URI icons", uri)
    if not n.show():
        print("Failed to send notification")
        sys.exit(1)

    # Raw image
    n = notify2.Notification("Raw image test",
                              "Testing sending raw pixbufs")
    helper = Gtk.Button()
    icon = helper.render_icon(Gtk.STOCK_DIALOG_QUESTION, Gtk.IconSize.DIALOG)
    n.set_icon_from_pixbuf(icon)

    if not n.show():
        print("Failed to send notification")
        sys.exit(1)
