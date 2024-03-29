from setuptools import setup, find_packages

name = "gocept.nginx"
setup(
    name=name,
    version="0.9.5dev",
    author='gocept gmbh & co. kg',
    author_email='mail@gocept.com',
    url='https://bitbucket.org/gocept/gocept.nginx',
    description="zc.buildout recipe for configuring an nginx server",
    long_description=file('README.txt').read(),
    license="ZPL 2.1",
    keywords="zope3 buildout nginx",
    classifiers=["Framework :: Buildout"],

    zip_safe=False,
    packages=find_packages('.'),
    include_package_data=True,
    namespace_packages=['gocept'],
    install_requires=[
        'setuptools',
        'zc.buildout',
    ],
    extras_require={'test': ['zope.testing']},
    entry_points={
        'zc.buildout': [
            'default = %s.recipe:Recipe' % name,
        ]
    },
)
