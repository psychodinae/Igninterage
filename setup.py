from setuptools import setup

setup(name='igninterage',
      version='0.1',
      description='Modulo para interagir no forum IGNboards',
      url='https://github.com/psychodinae',
      author='Psychodinae',
      author_email='https://github.com/psychodinae',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=['requests', 'selenium'],
      python_requires='>=3.6'
     )
