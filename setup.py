#!/usr/bin/env python
from setuptools import setup, Command, Extension
import os


long_description = r"""

Stemming algorithms

PyStemmer provides access to efficient algorithms for calculating a
"stemmed" form of a word.  This is a form with most of the common
morphological endings removed; hopefully representing a common
linguistic base form.  This is most useful in building search engines
and information retrieval software; for example, a search with stemming
enabled should be able to find a document containing "cycling" given the
query "cycles".

PyStemmer provides algorithms for several (mainly European) languages,
by wrapping the libstemmer library from the Snowball project in a Python
module.

It also provides access to the classic Porter stemming algorithm for
English: although this has been superseded by an improved algorithm, the
original algorithm may be of interest to information retrieval
researchers wishing to reproduce results of earlier experiments.

""".strip()

version_str = '3.0.0'
# libstemmer_c versions have 3 components but pystemmer versions may have more
# (so we can address a pystemmer-specific issue without having to wait for the
# next libstemmer_c release) so take the first 3 components from version_str.
libstemmer_c_version = '.'.join(version_str.split('.')[0:3])

class LibrarySourceCode:

    # Directories in libstemmer which contain libstemmer sources (ie, not
    # examples, etc).
    LIBRARY_CORE_DIRS = ('src_c', 'runtime', 'libstemmer', 'include')
    DEFAULT_URI = 'https://snowballstem.org/dist/libstemmer_c-%s.tar.gz' % \
        libstemmer_c_version
    DEFAULT_CHECKSUM = \
        'd4eca4485f6d3cb4387626a5f508b9b3489d24737525c23ba58026159497a8bc'

    def __init__(self, directory='libstemmer_c-%s' % libstemmer_c_version):
        """ Constructor.

        :param str directory: Path to directory where source code should
            reside.
        :return void:
        """
        self._directory = directory

    @property
    def manifest_file_path(self):
        """ Produce a path to the manifest within the source code.

        :return str:
        """
        return os.path.join(self._directory, 'mkinc_utf8.mak')

    @property
    def include_directories(self):
        """ Return all paths to include during the compilation of extension.

        :return list(str):
        """
        return [os.path.join(self._directory, 'include')]

    def iter_manifest_lines(self):
        """ Open the manifest file from disk and yield its contents, line by
        line.

        :yield str:
        """
        with open(self.manifest_file_path) as file:
            for line in file:
                yield line

    def source_code_paths(self):
        """ Find paths to source code files.

        :return set(str):
        """
        paths = set()

        for line in self.iter_manifest_lines():
            line = line.strip().replace(' \\', '')
            directory = os.path.split(line)[0]
            if line.endswith('.c') and directory in self.LIBRARY_CORE_DIRS:
                paths.add(os.path.join(self._directory, line))

        return paths

    def is_present_on_disk(self):
        """ Is the source code present on disk?

        :return bool:
        """
        return os.path.exists(self._directory)

    def download(self, url=None, checksum=None):
        """ Download and extract the source code from the web.

        :param str url: Url to the zipped source code.
        :param str checksum: Sha256 hash of the archive.
        :return void:
        """
        from tarballfetcher import download_and_extract_tarball
        download_and_extract_tarball(
            url or self.DEFAULT_URI,
            expected_sha256=checksum or self.DEFAULT_CHECKSUM)


LIBRARY_SOURCE_CODE = LibrarySourceCode()

SYSTEM_LIBSTEMMER = os.environ.get('PYSTEMMER_SYSTEM_LIBSTEMMER', False)
if SYSTEM_LIBSTEMMER:
    C_EXTENSION = Extension(
        'Stemmer',
        ['src/Stemmer.pyx'],
        libraries=['stemmer'],
    )
else:
    if not LIBRARY_SOURCE_CODE.is_present_on_disk():
        LIBRARY_SOURCE_CODE.download()
    C_EXTENSION = Extension(
        'Stemmer',
        ['src/Stemmer.pyx'] + list(LIBRARY_SOURCE_CODE.source_code_paths()),
        include_dirs=LIBRARY_SOURCE_CODE.include_directories
    )


class BootstrapCommand(Command):
    description = 'Download libstemmer_c dependency'
    user_options = [
        ('libstemmer-url=', None, 'path to libstemmer c library'),
        ('libstemmer-sha256=', None, 'Expected SHA256 for the tarball'),
    ]

    def initialize_options(self):
        self.libstemmer_url = LIBRARY_SOURCE_CODE.DEFAULT_URI
        self.libstemmer_sha256 = LIBRARY_SOURCE_CODE.DEFAULT_CHECKSUM

    def finalize_options(self):
        pass

    def run(self):
        LIBRARY_SOURCE_CODE.download(
            self.libstemmer_url, self.libstemmer_sha256)


setup(name='PyStemmer',
      version=version_str,
      author='Richard Boulton',
      author_email='richard@tartarus.org',
      maintainer='Richard Boulton',
      maintainer_email='richard@tartarus.org',
      url='https://github.com/snowballstem/pystemmer/',
      description='Snowball stemming algorithms, for information retrieval',
      long_description=long_description,
      platforms=["any"],
      license="MIT, BSD",
      keywords=[
          "python",
          "information retrieval",
          "language processing",
          "morphological analysis",
          "stemming algorithms",
          "stemmers"
      ],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "License :: OSI Approved :: BSD License",
          "Natural Language :: Arabic",
          "Natural Language :: Basque",
          "Natural Language :: Catalan",
          "Natural Language :: Danish",
          "Natural Language :: Dutch",
          "Natural Language :: English",
          "Natural Language :: Esperanto",
          "Natural Language :: Finnish",
          "Natural Language :: French",
          "Natural Language :: German",
          "Natural Language :: Greek",
          "Natural Language :: Hindi",
          "Natural Language :: Hungarian",
          "Natural Language :: Indonesian",
          "Natural Language :: Irish",
          "Natural Language :: Italian",
          "Natural Language :: Lithuanian",
          "Natural Language :: Nepali",
          "Natural Language :: Norwegian",
          "Natural Language :: Portuguese",
          "Natural Language :: Romanian",
          "Natural Language :: Russian",
          "Natural Language :: Serbian",
          "Natural Language :: Spanish",
          "Natural Language :: Swedish",
          "Natural Language :: Tamil",
          "Natural Language :: Turkish",
          "Operating System :: OS Independent",
          "Programming Language :: C",
          "Programming Language :: Other",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3.13",
          "Topic :: Database",
          "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
          "Topic :: Text Processing :: Indexing",
          "Topic :: Text Processing :: Linguistic",
      ],
      setup_requires=['Cython>=0.28.5', 'setuptools>=18.0'],
      ext_modules=[
          C_EXTENSION
      ],
      cmdclass={'bootstrap': BootstrapCommand}
      )
