==========================
NGNIX configuration recipe
==========================

The gocept.nginx recipe allows to configure an nginx server in buildout::

    [ngnix]
    recipe = zc.recipe.cmmi
    url = http://sysoev.ru/nginx/nginx-0.5.30.tar.gz
    md5sum = 804cf3d6583fe820de42c5e7c50d7a1a

    [frontend]
    recipe = gocept.nginx
    hostname = localhost
    port = 8080
    configuration =
        worker_processes 1;
        events {
            worker_connections 1024;
        }
        http {
          ...



Changes
=======

0.9.5 (unreleased)
------------------

- Migrate repository to Bitbucket.

- Updated test to pass with current versions of zc.buildout.

0.9.4 (2008-10-01)
------------------

- Added a way to prevent setting the user in nginx.conf when using a deployment
  recipe.
- Fixed names of config, log, run and lock files when using a deployment
  recipe.

0.9.3 (2008-09-19)
------------------

- Added support for zc.recipe.deployment / gocept.recipe.deploymentsandbox,
  including logrotate.

0.9.2 (2008-06-18)
------------------

- Override accidental -dev release.

0.9.1 (2008-06-18)
------------------

- Fix configtest command in the generated ctl script.

0.9 (2008-01-14)
----------------

- Allowing configuration of config file location.

- Writing config file in own part by default.
