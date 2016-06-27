from setuptools import setup, find_packages
import sys, os

version = '0.6'

setup(name='dopaminekit',
      version=version,
      description="A library to use DopamineLabs machine learning API",
      long_description="""\
This packages provides a framework for interacting with the Dopamine API from a Cocoa based iOS application. After you have received your API key and configured the actions and reinforcements relevant to your app on the developer dashboard, you may use this framework to place 'tracking', and 'reinforcement' calls from inside your app that will communicate directly with the Dopamine API.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='machinelearning analytics dopamine reinforcement behavior',
      author='Akash Desai',
      author_email='kash@usedopamine.com',
      url='https://github.com/DopamineLabs/DopamineKit-Python-Client',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
