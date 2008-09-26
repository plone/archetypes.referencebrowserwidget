from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='archetypes.referencebrowserwidget',
      version=version,
      description="An alternate atreferencebrowser implementation",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Relation Widget',
      author='Tom Gross',
      author_email='itconsense@gmail.com',
      url='http://pypi.python.org/archetypes.referencebrowserwidget',
      license='ZPL 2.1',
      namespace_packages=['archetypes'],
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
