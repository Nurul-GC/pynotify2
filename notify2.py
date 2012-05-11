"""This is a pure-python replacement for notify-python, using python-dbus
to communicate with the notifications server directly.

To use it, first call ``notify2.init()``, then create and show notifications::

    n = notify2.Notification("Summary",
                             "Some body text",
                             "notification-message-im"   # Icon name
                            )
    n.show()

To see more of what's possible, refer to docstrings of methods and objects.

Based on the notifications spec at:
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
_have_mainloop = False

class UninittedError(RuntimeError):
    pass

class UninittedDbusObj(object):
    def __getattr__(self, name):
        raise UninittedError("You must call notify2.init() before using the "
                             "notification features.")
        
dbus_obj = UninittedDbusObj()

def init(app_name, mainloop=None):
    """Initialise the Dbus connection.
    
    To get callbacks from notifications, DBus must be integrated with a mainloop.
    There are three ways to achieve this:
    
    - Set a default mainloop (dbus.set_default_main_loop) before calling init()
    - Pass the mainloop parameter as a string 'glib' or 'qt' to integrate with
      those mainloops.
    - Pass the mainloop parameter a DBus compatible mainloop instance, such as
      dbus.mainloop.glib.DBusGMainLoop().
    
    If you only want to display notifications, without receiving information
    back from them, you can safely omit mainloop.
    """
    global appname, initted, dbus_obj, _have_mainloop
    
    if mainloop == 'glib':
        from dbus.mainloop.glib import DBusGMainLoop
        mainloop = DBusGMainLoop()
    elif mainloop == 'qt':
        from dbus.mainloop.qt import DBusQtMainLoop
        mainloop = DBusQtMainLoop()
    
    bus = dbus.SessionBus(mainloop=mainloop)

    dbus_obj = bus.get_object('org.freedesktop.Notifications',
                              '/org/freedesktop/Notifications')
    appname = app_name
    initted = True
    
    if mainloop or dbus.get_default_main_loop():
        _have_mainloop = True
        dbus_obj.connect_to_signal('ActionInvoked', _action_callback,
                               dbus_interface='org.freedesktop.Notifications')
        dbus_obj.connect_to_signal('NotificationClosed', _closed_callback,
                               dbus_interface='org.freedesktop.Notifications')
        
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
    global initted, dbus_obj, _have_mainloop
    initted = False
    _have_mainloop = False
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

# Action callbacks -------------------------------------------------------------

notifications_registry = {}

def _action_callback(nid, action):
    nid, action = int(nid), str(action)
    n = notifications_registry[nid]
    n._action_callback(action)

def _closed_callback(nid, reason):
    nid, reason = int(nid), int(reason)
    n = notifications_registry[nid]
    n._closed_callback(n)
    del notifications_registry[nid]

def no_op(*args):
    """No-op function for callbacks.
    """
    pass

# Controlling notifications ----------------------------------------------------

class Notification(object):
    id = 0
    timeout = -1    # -1 = server default settings
    _closed_callback = no_op
    
    def __init__(self, summary, message='', icon=''):
        self.summary = summary
        self.message = message
        self.icon = icon
        self.hints = {}
        self.actions = {}
    
    def show(self):
        """Ask the server to show the notification.
        """
        nid = dbus_obj.Notify(appname,       # app_name       (spec names)
                              self.id,       # replaces_id
                              self.icon,     # app_icon
                              self.summary,  # summary
                              self.message,  # body
                              self._make_actions_array(),  # actions
                              self.hints,    # hints
                              self.timeout,  # expire_timeout
                              dbus_interface='org.freedesktop.Notifications')
        
        self.id = int(nid)
        
        if _have_mainloop:
            notifications_registry[self.id] = self
        return True
    
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
    
    def add_action(self, action, label, callback, user_data=None):
        """Add an action to the notification (if the server supports it).
        
        action : str
          A brief key.
        label : str
          The text displayed on the action button
        callback : callable
          A function taking at 2-3 parameters: the Notification object, the
          action key and (if specified) the user_data.
        user_data :
          An extra argument to pass to the callback.
        """
        self.actions[action] = (label, callback, user_data)
    
    def _make_actions_array(self):
        """Make the actions array to send over DBus.
        """
        arr = []
        for action, (label, callback, user_data) in self.actions.items():
            arr.append(action)
            arr.append(label)
        return arr
    
    def _action_callback(self, action):
        """Called when the user selects an action on the notification, to
        dispatch it to the relevant user-specified callback.
        """
        try:
            label, callback, user_data = self.actions[action]
        except KeyError:
            return
        
        if user_data is None:
            callback(self, action)
        else:
            callback(self, action, user_data)
    
    def connect(self, event, callback):
        """Set the callback for the notification closing; the only valid value
        for event is 'closed'. The API is compatible with pynotify.
        """
        if event != 'closed':
            raise ValueError("'closed' is the only valid value for event", event)
        self._closed_callback = callback
