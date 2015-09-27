from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '2.5.4'

long_description = (
    read('README.rst')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.rst')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('src', 'archetypes', 'referencebrowserwidget', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n\n' +
    'Download\n'
    '********\n'
    )

setup(name='archetypes.referencebrowserwidget',
      version=version,
      description="A referencebrowser implementation for Archetypes",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='Relation Widget',
      author='Tom Gross',
      author_email='itconsense@gmail.com',
      url='http://pypi.python.org/pypi/archetypes.referencebrowserwidget',
      license='ZPL 2.1',
      namespace_packages=['archetypes'],
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
#          'DateTime',
#          'Products.Archetypes',
          'zope.interface',
          'zope.component',
          'zope.formlib',
#          'Products.CMFCore',
#          'ZODB3',
#          'Zope2',
#          'Acquisition',
          'plone.app.form',
          'plone.app.jquerytools>=1.1b1',
#          'plone.uuid'
# Older versions of jquerytools don't work. See #10939
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
