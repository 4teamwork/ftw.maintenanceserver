=======================
 ftw.maintenanceserver
=======================

Provides a simple server serving a static directory, which can be configured
as haproxy backup server, kicking in when all normal servers are offline.


How it works
------------

It is simple HTTP server, serving a static directory.
All requests which match no file in the static directory are responded with
the ``index.html`` which is expected to be placed in the static directory.

This is useful when a user is visiting the page at any URL while the maintenance
server is activated. The user then stays at the same URL and can refresh until
the system is back online and he is at the same place as he was before.


Installation
------------

The server can be installed using zc.buildout, which generates a pre configured
``bin/maintenance`` script::

    [buildout]
    parts += maintenance

    [maintenance]
    recipe = zc.recipe.egg
    eggs = ftw.maintenanceserver
    arguments = '${buildout:directory}/static', 8088


HAProxy configuration
---------------------

When using HAProxy the server can be simply configured as ``backup`` server,
which will only be used when all "normal" servers are offline::

    backend plone
    server plone1 127.0.0.1:8080 cookie p1 check downinter 15s maxconn 5 rise 1 slowstart 60s
    server plone2 127.0.0.1:8081 cookie p2 check downinter 15s maxconn 5 rise 1 slowstart 60s
    server maintenance 127.0.0.1:8088 check backup



Links
=====

- Github: https://github.com/4teamwork/ftw.maintenanceserver
- Issues: https://github.com/4teamwork/ftw.maintenanceserver/issues
- Pypi: http://pypi.python.org/pypi/ftw.maintenanceserver
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.maintenanceserver


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.maintenanceserver`` is licensed under GNU General Public License, version 2.
