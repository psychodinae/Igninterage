from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='igninterage',
      version='1.2.0',
      description='Modulo para interagir no forum IGNboards+',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/psychodinae/Igninterage',
      author='Psychodinae',
      author_email='noteprof213@gmail.com',
      packages=['igninterage'],
      install_requires=['requests', 'lxml', 'secretstorage', 'cryptography', "pywin32;platform_system=='Windows'"],
      classifiers=[
          "Programming Language :: Python :: 3.6",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: POSIX :: Linux",
          "License :: OSI Approved :: MIT License"
      ],
      python_requires='>=3.6'
      )
