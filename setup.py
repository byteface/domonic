from setuptools import setup

with open("README.md", "r") as f:
        long_description = f.read()

setup(
  name = 'domonic',
  version = '0.0.6',
  author="@byteface",
  author_email="byteface@gmail.com",
  license="MIT",
  url = 'https://github.com/byteface/domonic',
  download_url = 'https://github.com/byteface/pypals/archive/0.0.6.tar.gz',
  description = 'generate html with python 3',
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords = ['html','generate'],
  classifiers=[
      "Programming Language :: Python :: 3"
  ],
  install_requires=[
          'requests','python-dateutil','urllib3'
  ],
  packages = ['domonic'],
  include_package_data = True,
)
