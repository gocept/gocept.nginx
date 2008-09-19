==========================
NGNIX configuration recipe
==========================

The gocept.nginx recipe allows to configure an nginx in buildout:

>>> write("buildout.cfg", """
... [buildout]
... parts = frontend
...
... [frontend]
... recipe = gocept.nginx
... configuration = 
...     error_log = ${frontend:error_log}
...     worker_processes 1;
...     events {
...         worker_connections 1024;
...     }
...     http {
...         access_log ${frontend:access_log};
...         ...
...     }
... """)

>>> print system(buildout),
Installing frontend.

There is a script called ``frontend`` which is used to control nginx:

>>> cat('bin', 'frontend')
#!/bin/sh
ARGV="$@"
NGINX='.../_TEST_/sample-buildout/parts/nginx/sbin/nginx'
PIDFILE='.../_TEST_/sample-buildout/parts/frontend/frontend.pid'
CONFIGURATION='.../_TEST_/sample-buildout/parts/frontend/frontend.conf'
<BLANKLINE>
ERROR=0
if [ "x$ARGV" = "x" ] ; then 
    ARGV="-h"
fi
<BLANKLINE>
case $ARGV in
start)
    echo "Starting nginx "
    $NGINX -c $CONFIGURATION
    error=$?
    ;;
stop)
    echo "Stopping nginx "
    kill `cat $PIDFILE`
    error=$?
    ;;
reload)
    echo "Reloading nginx "
    kill -HUP `cat $PIDFILE`
    error=$?
    ;;
configtest)
    echo "Testing nginx configuration "
    $NGINX -c $CONFIGURATION -t
    ERROR=$?
    ;;
esac
<BLANKLINE>
exit $ERROR

In the parts directory the configuration file is created. Note that the PID
file location is prepended automatically:

>>> ls('parts')
d  frontend
>>> ls('parts', 'frontend')
-  frontend.conf
>>> cat('parts', 'frontend', 'frontend.conf')
pid .../_TEST_/sample-buildout/parts/frontend/frontend.pid;
<BLANKLINE>
worker_processes 1;
events {
worker_connections 1024;
}
http {}




Deployment support
++++++++++++++++++

The recipe is zc.deployment compatible. The created files will be put in the
deployment specifig locations:


>>> mkdir('etc')
>>> mkdir('init.d')
>>> mkdir('logrotate')

>>> write("buildout.cfg", """
... [buildout]
... parts = frontend
...
... [deploy]
... user = testuser
... name = testdeploy
... etc-directory = etc
... rc-directory = init.d
... log-directory = logs
... run-directory = run
... logrotate-directory = logrotate
...
... [frontend]
... recipe = gocept.nginx
... deployment = deploy
... configuration = 
...     worker_processes 1;
...     events {
...         worker_connections 1024;
...     }
...     http {}
... """)

>>> print system(buildout),
Uninstalling frontend.
Installing frontend.


The ctl-script is in init.d now:

>>> cat('init.d', 'testdeploy-frontend')
#!/bin/sh
ARGV="$@"
NGINX='.../_TEST_/sample-buildout/parts/nginx/sbin/nginx'
PIDFILE='run/testdeploy-frontend.pid'
CONFIGURATION='etc/testdeploy-frontend.conf'
...

The config file also includes the user now:

>>> cat('etc', 'testdeploy-frontend.conf')
pid run/testdeploy-frontend.pid;
user testuser;
<BLANKLINE>
worker_processes 1;
events {
worker_connections 1024;
}
http {}
