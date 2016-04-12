from setuptools import setup

setup(name='md2keynote',
      version='0.1',
      py_modules=[
          'md2keynote/applescripting',
          'md2keynote/md2keynote',
          'md2keynote/md2key'
      ],
      packages=['md2keynote'],
      package_data={
          'md2keynote':['md2keynote/helpers/keynote.applescript']
      },
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'md2key=md2keynote.md2key:main',
              ]
        }
)