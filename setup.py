import os
from setuptools import setup, find_packages


version = '1.1.2'


tests_require = [
    'ftw.testbrowser',
    'plone.testing',
    'unittest2',
    ]


setup(name='ftw.maintenanceserver',
      version=version,
      description='Maintenance HTTP server, serving a static directory.',

      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw recipe maintenance',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.maintenanceserver',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'argparse',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points = {
        'console_scripts': [
            'maintenance = ftw.maintenanceserver.server:command']
        },
      )
