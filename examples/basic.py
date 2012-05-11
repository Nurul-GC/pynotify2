#!/usr/bin/env python
"""This illustrates the basic functionality of notify2 - creating and displaying
a notification message.
"""

import notify2

# This must be called before using notify2
notify2.init("Demo application")

# A number of stock 
n = notify2.Notification("Summary", "Body text goes here",
            "notification-message-im") # A stock icon name. For more icon
                                       # options, see icon.py in this folder.
n.show()
