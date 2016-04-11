from distutils.core import setup

setup(name='md2keynote',
      version='0.1',
      py_modules=[
          'applescripting', 
          'md2keynote'
      ],
      data_files=[
          ('', ['keynote.applescript'])
      ],
      scripts=[
          'md2keynote'
      ]
)