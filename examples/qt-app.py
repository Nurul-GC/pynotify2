#!/usr/bin/env python
"""Callbacks from notify2 work with PyQt applications as well.
"""

from PyQt4.QtCore import QCoreApplication
import notify2
import sys

# Ubuntu's notify-osd doesn't officially support actions. However, it does have
# a dialog fallback which we can use for this demonstration. In real use, please
# respect the capabilities the notification server reports!
OVERRIDE_NO_ACTIONS = True

class MyApp(QCoreApplication):
    def __init__(self, argv):
        super(MyApp, self).__init__(argv)

        # This needs to be before any other use of notify2, but after the Qt
        # application has been instantiated.
        notify2.init("Multi Action Test", mainloop='qt')
        
        server_capabilities = notify2.get_server_caps()

        n = notify2.Notification("Low disk space",
                                "You can free up some disk space by " +
                                "emptying the trash can.")
        n.set_urgency(notify2.URGENCY_CRITICAL)
        n.set_category("device")
        if ('actions' in server_capabilities) or OVERRIDE_NO_ACTIONS:
            n.add_action("help", "Help", self.help_cb)
            n.add_action("ignore", "Ignore", self.ignore_cb)
            n.add_action("empty", "Empty Trash", self.empty_cb)
        n.connect('closed', self.closed_cb)

        n.show()
    
    def help_cb(self, n, action):
        assert action == "help"
        print("You clicked Help")
        n.close()

    def ignore_cb(self, n, action):
        assert action == "ignore"
        print("You clicked Ignore")
        n.close()

    def empty_cb(self, n, action):
        assert action == "empty"
        print("You clicked Empty Trash")
        n.close()

    def closed_cb(self, n):
        print("Notification closed")
        self.quit()

if __name__ == "__main__":
    MyApp(sys.argv).exec_()
