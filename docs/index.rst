notify2 API documentation
=========================

notify2 is - or was - a package to display desktop notifications on Linux.
Those are the little bubbles which tell a user about e.g. new emails.

notify2 is *deprecated*. Here are some alternatives:

- `desktop_notify <https://pypi.org/project/desktop-notify/>`_ is a newer module doing essentially the same thing.
- If you're writing a GTK application, you may want to use GNotification
  (`intro <https://developer.gnome.org/GNotification/>`__, `Python API <https://lazka.github.io/pgi-docs/#Gio-2.0/classes/Notification.html>`__).
- For simple cases, you can run ``notify-send`` as a subprocess.
  The `py-notifier <https://pypi.org/project/py-notifier/>`__ package provides a simple Python API around this, and can also display notifications on Windows.

notify2 is a replacement for pynotify which can be used from different GUI toolkits
and from programs without a GUI. The API is largely the same as that of pynotify,
but some less important parts are left out.

Notifications are sent to a notification daemon over `D-Bus <http://www.freedesktop.org/wiki/Software/dbus/>`_,
according to the `Desktop notifications spec <http://people.gnome.org/~mccann/docs/notification-spec/notification-spec-latest.html>`_,
and the server is responsible for displaying them to the user. So your application
has limited control over when and how a notification appears.

.. toctree::
   :maxdepth: 1
   
   license

.. module:: notify2

.. autofunction:: init

.. autofunction:: get_server_caps

.. autofunction:: get_server_info

Creating and showing notifications
----------------------------------

.. autoclass:: Notification

   .. automethod:: show
   
   .. automethod:: update
   
   .. automethod:: close

Extra parameters
----------------

.. class:: Notification

   .. automethod:: set_urgency
   
   .. automethod:: set_timeout
   
   .. automethod:: set_category
   
   .. automethod:: set_location
   
   .. automethod:: set_icon_from_pixbuf
   
   .. automethod:: set_hint
   
   .. automethod:: set_hint_byte
   
Callbacks
---------

To receive callbacks, you must have set a D-Bus event loop when you called
:func:`init`.

.. class:: Notification

   .. automethod:: connect
   
   .. automethod:: add_action
   

Constants
---------

.. data:: URGENCY_LOW
          URGENCY_NORMAL
          URGENCY_CRITICAL

   Urgency levels to pass to :meth:`Notification.set_urgency`.

.. data:: EXPIRES_DEFAULT
          EXPIRES_NEVER

   Special expiration times to pass to :meth:`Notification.set_timeout`.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

