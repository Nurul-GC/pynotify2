"""This is a pure-python replacement for notify-python, using python-dbus
to communicate with the notifications server directly.

See the notifications spec at:

http://developer.gnome.org/notification-spec/
"""

import dbus

# Constants
EXPIRES_DEFAULT = -1
EXPIRES_NEVER = 0

URGENCY_LOW = 0
URGENCY_NORMAL = 1
URGENCY_CRITICAL = 2
urgency_levels = [URGENCY_LOW, URGENCY_NORMAL, URGENCY_CRITICAL]

# Initialise the module (following pynotify's API) -----------------------------

initted = False
appname = ""

class UninittedError(RuntimeError):
    pass

class UninittedDbusObj(object):
    def __getattr__(self, name):
        raise UninittedError("You must call notify2.init() before using the "
                             "notification features.")
        
dbus_obj = UninittedDbusObj()

def init(app_name, mainloop=None):
    """Initialise the Dbus connection.
    
    mainloop is an optional DBus compatible mainloop, an instance of
    dbus.mainloop.glib.DBusGMainLoop or dbus.mainloop.qt.DBusQtMainLoop.
    Alternatively, instantiate either of these with ``set_as_default=True``
    before calling this function, then there is no need to pass them.
    """
    global appname, initted, dbus_obj
    
    bus = dbus.SessionBus(mainloop=mainloop)

    dbus_obj = bus.get_object('org.freedesktop.Notifications',
                              '/org/freedesktop/Notifications')
    appname = app_name
    initted = True
    return True

def is_initted():
    """Has init() been called? Only exists for compatibility with pynotify.
    """
    return initted

def get_app_name():
    """Return appname. Only exists for compatibility with pynotify.
    """
    return appname

def uninit():
    """Undo what init() does."""
    global initted, dbus_obj
    initted = False
    dbus_obj = UninittedDbusObj()

# Retrieve basic server information --------------------------------------------

def get_server_caps():
    """Get a list of server capabilities.
    """
    return [str(x) for x in dbus_obj.GetCapabilities()]

def get_server_info():
    """Get basic information about the server.
    """
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
        self.timeout = -1    # -1 = server default settings
    
    def show(self):
        """Ask the server to show the notification.
        """
        self.id = dbus_obj.Notify(appname,       # app_name       (spec names)
                                  self.id,       # replaces_id
                                  self.icon,     # app_icon
                                  self.summary,  # summary
                                  self.message,  # body
                                  [],            # actions
                                  self.hints,    # hints
                                  self.timeout,  # expire_timeout
                                  dbus_interface='org.freedesktop.Notifications')
    
    def update(self, summary, message="", icon=None):
        """Replace the summary and body of the notification, and optionally its
        icon. You should call show() again after this to display the updated
        notification.
        """
        self.summary = summary
        self.message = message
        if icon is not None:
            self.icon = icon
    
    def close(self):
        """Ask the server to close this notification.
        """
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
    
    def set_category(self, category):
        """Set the 'category' hint for this notification.
        """
        self.hints['category'] = category
    
    def set_timeout(self, timeout):
        """Set the display duration in milliseconds, or one of the special
        values EXPIRES_DEFAULT or EXPIRES_NEVER.
        
        Only exists for compatibility with pynotify; you can simply set::
        
          n.timeout = 5000
        """
        if not isinstance(timeout, int):
            raise TypeError("timeout value was not int", timeout)
        self.timeout = timeout
    
    def get_timeout(self):
        """Return the timeout value for this notification.
        
        Only exists for compatibility with pynotify; you can inspect the
        timeout attribute directly.
        """
        return self.timeout
                           
