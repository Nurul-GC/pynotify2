"""This is a pure-python replacement for notify-python, using python-dbus
to communicate with the notifications server directly.

See the notifications spec at:

http://developer.gnome.org/notification-spec/
"""

import dbus

bus = dbus.SessionBus()

dbus_obj = bus.get_object('org.freedesktop.Notifications',
                          '/org/freedesktop/Notifications')

# Constants
EXPIRES_DEFAULT = -1
EXPIRES_NEVER = 0

# Initialise the module (following pynotify's API) -----------------------------

_initted = False
appname = ""

def init(app_name):
    """Set appname. Only exists for compatibility with pynotify.
    """
    appname = app_name
    _initted = True
    return True

def is_initted():
    """Has init() been called? Only exists for compatibility with pynotify.
    """
    return _initted

def get_app_name():
    """Return appname. Only exists for compatibility with pynotify.
    """
    return appname

def uninit():
    """Only exists for compatibility with pynotify."""
    _initted = False

# Retrieve basic server information --------------------------------------------

def get_server_caps():
    """Get a list of server capabilities.
    """
    return [str(x) for x in dbus_obj.GetCapabilities()]

def get_server_info():
    res = dbus_obj.GetServerInformation()
    return {'name': str(res[0]),
             'vendor': str(res[1]),
             'version': str(res[2]),
             'spec-version': str(res[3]),
            }

# Controlling notifications ----------------------------------------------------

class Notification(object):
    id = None
    
    def __init__(self, summary, message='', icon=''):
        self.summary = summary
        self.message = message
        self.icon = icon
    
    def show(self):
        self.id = dbus_obj.Notify(appname,       # app_name       (spec names)
                                  0,             # replaces_id
                                  self.icon,     # app_icon
                                  self.summary,  # summary
                                  self.message,  # body
                                  [],            # actions
                                  {},            # hints
                                  -1,            # expire_timeout
                                  dbus_interface='org.freedesktop.Notifications')
    
    def close(self):
        if self.id is not None:
            dbus_obj.CloseNotification(self.id,
                                dbus_interface='org.freedesktop.Notifications')
                           
