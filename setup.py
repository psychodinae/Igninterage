from setuptools import setup

setup(name='igninterage',
      version='1.0',
      description='Modulo para interagir no forum IGNboards',
      url='https://github.com/psychodinae',
      author='Psychodinae',
      author_email='https://github.com/psychodinae',
      license='MIT',
      packages=['igninterage'],
      install_requires=['requests', 'lxml'],
      python_requires='>=3.6'
      )
