"""Tests for notify2.py.

We can't actually check that notifications are displayed, so this is mostly
just smoke tests to check errors aren't raised.

Running this may display several notifications.
"""

import unittest
import notify2
from gi.repository import GdkPixbuf

class ModuleTests(unittest.TestCase):
    """Test module level functions.
    """
    def setUp(self):
        notify2.init("notify2 test suite")
    
    def test_init_uninit(self):
        assert notify2.is_initted()
        self.assertEqual(notify2.get_app_name(), "notify2 test suite")
        
        notify2.uninit()
        assert not notify2.is_initted()
    
    def test_get_server_info(self):
        r = notify2.get_server_info()
        assert isinstance(r, dict), type(r)
    
    def test_get_server_caps(self):
        r = notify2.get_server_caps()
        assert isinstance(r, list), type(r)

class NotificationTests(unittest.TestCase):
    """Test notifications.
    """
    def setUp(self):
        notify2.init("notify2 test suite")
    
    def test_basic(self):
        n = notify2.Notification("Title", "Body text")
        n.show()
        n.close()
    
    def test_icon(self):
        n = notify2.Notification("MLK", "I have a dream", "notification-message-im")
        n.show()
        n.close()
    
    def test_icon_only(self):
        if 'x-canonical-private-icon-only' in notify2.get_server_caps():
            n = notify2.Notification ("", # for a11y-reasons put something meaningfull here
                                      "", # for a11y-reasons put something meaningfull here
                                      "notification-device-eject")
            n.set_hint_string ("x-canonical-private-icon-only", "true");
            n.show ()
    
    def test_urgency(self):
        nl = notify2.Notification("Low", "Who cares?")
        nl.set_urgency(notify2.URGENCY_LOW)
        nl.show()
        nl.close()
        
        nn = notify2.Notification("Normal", "Some information")
        nn.set_urgency(notify2.URGENCY_NORMAL)
        nn.show()
        nn.close()
        
        nu = notify2.Notification("Urgent", "Vital information!")
        nu.set_urgency(notify2.URGENCY_CRITICAL)
        nu.show()
        nu.close()
    
    def test_update(self):
        n = notify2.Notification("First message", "Some text", "notification-message-im")
        n.show()
        
        # The icon should stay the same with this
        n.update("Second message", "Some more text")
        n.show()
        
        # But this should replace the icon
        n.update("Third message", "Yet more text, new icon.", "notification-message-email")
        n.show()
        n.close()
    
    def test_category(self):
        n = notify2.Notification("Plain")
        n.set_category('im.received')
        n.show()
        n.close()
    
    def test_timeout(self):
        n = notify2.Notification("Plain")
        self.assertEqual(n.get_timeout(), notify2.EXPIRES_DEFAULT)
        n.set_timeout(notify2.EXPIRES_NEVER)
        self.assertEqual(n.get_timeout(), notify2.EXPIRES_NEVER)
        n.set_timeout(5000)
        self.assertEqual(n.get_timeout(), 5000)
        n.show()
        n.close()
    
    def test_data(self):
        n = notify2.Notification("Plain")
        n.data['a'] = 1
        n.set_data('b', 2)  # pynotify API
        n.show()
        self.assertEqual(n.get_data('a'), 1)   # pynotify API
        self.assertEqual(n.data['b'], 2)
        n.close()
    
    def test_icon_from_pixbuf(self):
        pb = GdkPixbuf.Pixbuf.new_from_file("examples/applet-critical.png")
        n = notify2.Notification("Icon", "Testing icon from pixbuf")
        n.set_icon_from_pixbuf(pb)
        n.show()
        n.close()
    
    def test_set_location(self):
        n = notify2.Notification("Location", "Test setting location")
        n.set_location(320, 240)
        n.show()
        n.close()

if __name__ == "__main__":
    unittest.main()
