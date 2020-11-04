Pynotify2 is - or was - a package to display desktop notifications on Linux. Those are the little bubbles which tell a user about e.g. new emails.

Pynotify2 is *deprecated*. Here are some alternatives:

- [desktop_notify](https://pypi.org/project/desktop-notify/#description) is a newer module doing essentially the same thing.
- If you're writing a GTK application, you may want to use GNotification ([intro](https://developer.gnome.org/GNotification/), [Python API](https://lazka.github.io/pgi-docs/#Gio-2.0/classes/Notification.html))
- For simple cases, you can run `notify-send` as a subprocess. The [py-notifier](https://pypi.org/project/py-notifier/) package provides a simple Python API around this, and can also display notifications on Windows.