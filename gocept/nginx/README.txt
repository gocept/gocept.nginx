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
...     worker_processes 1;
...     events {
...         worker_connections 1024;
...     }
...     http {}
... """)

>>> print system(buildout),
Installing frontend.

There is a script called ``frontend`` which is used to control nginx:

>>> cat('bin', 'frontend')
#!/bin/sh
ARGV="$@"
NGINX='.../_TEST_/sample-buildout/parts/nginx/sbin/nginx'
PIDFILE='.../_TEST_/sample-buildout/parts/frontend/nginx.pid'
CONFIGURATION='.../_TEST_/sample-buildout/parts/frontend/nginx.conf'
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
-  nginx.conf
>>> cat('parts', 'frontend', 'nginx.conf')
pid .../_TEST_/sample-buildout/parts/frontend/nginx.pid;
<BLANKLINE>
worker_processes 1;
events {
worker_connections 1024;
}
http {}
