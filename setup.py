from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

from domonic import __version__ as version

setup(
  name='domonic',
  version=version,
  author="@byteface",
  author_email="byteface@gmail.com",
  license="MIT",
  url='https://github.com/byteface/domonic',
  download_url='https://github.com/byteface/domonic/archive/' + version + ' .tar.gz',
  description='Generate html with python 3. DOM API, Javascript API and more...',
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords=['html', 'generate', 'templating', 'dom', 'vdom', 'terminal', 'json', 'web', 'template', 'javascript', 'DOM', 'GUI', 'render', 'website', 'apps', 'html5', 'framework', 'SVG', 'x3d', 'events', 'geom'],
  python_requires='>=3.6',
  classifiers=[
      "Programming Language :: Python :: 3",
      "Programming Language :: JavaScript",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Intended Audience :: Developers",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: MIT License",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Topic :: Internet",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Multimedia :: Graphics :: Presentation",
      "Topic :: Software Development",
      "Topic :: Software Development :: Code Generators",
      "Topic :: Terminals",
      "Topic :: Utilities",
      'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Text Processing :: Markup :: HTML',
  ],
  install_requires=[
      'requests==2.26.0', 'python-dateutil==2.8.2', 'urllib3==1.26.7', "elementpath==2.4.0"
  ],
  packages=find_packages(),
  include_package_data=True,
  entry_points={
      'console_scripts': [
          'domonic = domonic.__main__:run',
      ],
  },
)
