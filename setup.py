from setuptools import setup

setup(name='igninterage',
      version='1.2.0',
      description='Modulo para interagir no forum IGNboards',
      url='https://github.com/psychodinae',
      author='Psychodinae',
      author_email='https://github.com/psychodinae',
      license='MIT',
      packages=['igninterage'],
      install_requires=['requests', 'lxml', 'secretstorage', 'cryptography', "pywin32;platform_system=='Windows'"],
      python_requires='>=3.6'
      )
