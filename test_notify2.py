"""Tests for notify2.py.

We can't actually check that notifications are displayed, so this is mostly
just smoke tests to check errors aren't raised.

Running this may display several notifications.
"""

import unittest
import notify2

class ModuleTests(unittest.TestCase):
    """Test module level functions.
    """
    def test_init_uninit(self):
        notify2.init("notify2 test suite")
        
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

if __name__ == "__main__":
    unittest.main()
