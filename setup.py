from distutils.core import setup

setup(name='md2keynote',
      version='0.1',
      py_modules=[
          'md2keynote/applescripting',
          'md2keynote/md2keynote'
      ],
      package_data={
          'md2keynote':['md2keynote/keynote.applescript']
      },
      include_package_data=True,
      scripts=[
          'md2key'
      ]
)