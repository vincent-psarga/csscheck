from setuptools import setup, find_packages
import sys, os

version = open(os.path.join("version.txt")).read().strip()

setup(name='csscheck',
      version=version,
      description="Simple command line tool to help CSS developers",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("csscheck",
                                         "HISTORY.txt")).read(),

      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Vincent Pretre (Zest software)',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'cssutils'
      ],
      
      entry_points={
          'console_scripts': [
              'css_check = csscheck.main:main'
              ]}
      )
