"""zc.buildout recipe for an Apache HTTP server root and apachectl script.
"""

import os
import os.path
import stat

import pkg_resources


read_resource = lambda filename: pkg_resources.resource_string(__name__,
                                                               filename)


class Recipe(object):
    """zc.buildout recipe configuring an nginx server and startup script.

    Configuration options:
        nginx

        configuration
    """

    def __init__(self, buildout, name, options):
        self.name = name
        self.options = options

        deployment = self.deployment = options.get('deployment')
        if deployment:
            self.deployment = buildout[deployment].get('name', deployment)
            options['etc-directory'] = buildout[deployment]['etc-directory']
            options['rc-directory'] = buildout[deployment]['rc-directory']
            options['run-directory'] = buildout[deployment]['run-directory']
            options['user'] = buildout[deployment]['user']
        else:
            options['etc-directory'] = options["run-directory"] = os.path.join(
                buildout["buildout"]["parts-directory"], name)
            options['rc-directory'] = buildout['buildout']['bin-directory']

        options.setdefault('nginx', 'nginx')
        options.setdefault('nginx_location', os.path.join(
            buildout["buildout"]["parts-directory"], options['nginx']))

    def install(self):
        if self.deployment:
            prefix = self.deployment + '-'
        else:
            prefix = ""
            if not os.path.exists(self.options['run-directory']):
                os.mkdir(self.options['run-directory'])
                self.options.created(self.options['run-directory'])

        config_path = os.path.join(
            self.options['etc-directory'],
            prefix+self.name+'.conf')
        ctl_path = os.path.join(self.options["rc-directory"],
                                prefix+self.name)
        pid_path = os.path.join(
            self.options['run-directory'], prefix+self.name+'.pid')


        # Write the configuration file
        config_file = file(config_path, 'w')
        config_file.write('pid %s;\n' % pid_path)
        if self.deployment:
            config_file.write('user %s;\n' % self.options['user'])
        config_file.write(self.options['configuration'])
        config_file.close()
        self.options.created(config_path)

        # files
        open(ctl_path, "w").write(read_resource("nginxctl.in") % dict(
            nginx_location=self.options['nginx_location'],
            pid_file=pid_path,
            config_file=config_path))

        os.chmod(ctl_path, (os.stat(ctl_path).st_mode |
                            stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        self.options.created(ctl_path)
        return self.options.created()

    def update(self):
        pass
