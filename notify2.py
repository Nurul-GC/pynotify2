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

URGENCY_LOW = 0
URGENCY_NORMAL = 1
URGENCY_CRITICAL = 2
urgency_levels = [URGENCY_LOW, URGENCY_NORMAL, URGENCY_CRITICAL]

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
    id = 0
    
    def __init__(self, summary, message='', icon=''):
        self.summary = summary
        self.message = message
        self.icon = icon
        self.hints = {}
    
    def show(self):
        """Show the notification.
        """
        self.id = dbus_obj.Notify(appname,       # app_name       (spec names)
                                  self.id,       # replaces_id
                                  self.icon,     # app_icon
                                  self.summary,  # summary
                                  self.message,  # body
                                  [],            # actions
                                  self.hints,    # hints
                                  -1,            # expire_timeout
                                  dbus_interface='org.freedesktop.Notifications')
    
    def update(self, summary, message="", icon=None):
        self.summary = summary
        self.message = message
        if icon is not None:
            self.icon = icon
    
    def close(self):
        if self.id != 0:
            dbus_obj.CloseNotification(self.id,
                                dbus_interface='org.freedesktop.Notifications')
    
    def set_hint(self, key, value):
        """n.set_hint(key, value) <--> n.hints[key] = value
        
        Only exists for compatibility with pynotify.
        """
        self.hints[key] = value
    
    set_hint_string = set_hint_int32 = set_hint_double = set_hint
    
    def set_hint_byte(self, key, value):
        """Set a hint with a dbus byte value. The input value can be an
        integer or a bytes string of length 1.
        """
        self.hints[key] = dbus.Byte(value)
    
    def set_urgency(self, level):
        """Set the urgency level to one of URGENCY_LOW, URGENCY_NORMAL or
        URGENCY_CRITICAL.
        """
        if level not in urgency_levels:
            raise ValueError("Unknown urgency level specified", level)
        self.set_hint_byte("urgency", level)
                           
