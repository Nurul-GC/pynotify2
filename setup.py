from distutils.core import setup

# To load the docstring, we need to be able to import dbus, but we don't
# actually use it.
try:
    import dbus
except ImportError:
    import sys
    sys.modules['dbus'] = object()

import notify2
long_description = notify2.__doc__

setup(name='notify2',
      version='0.3.1',
      description='Python interface to DBus notifications',
      long_description=long_description,
      author='Thomas Kluyver',
      author_email='takowl@gmail.com',
      url='https://bitbucket.org/takluyver/pynotify2',
      py_modules=['notify2'],
      classifiers = [
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
      )
