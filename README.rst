pathaliases
===========

|Build Status|

A python package for handling path aliases.

Path aliases can be loaded directly from YAML files:

.. code:: yaml

    dir/:
      subdir/:
        alias: SUBDIR
        some/other/dir/:
          alias: SUBDIR_2

    file.txt: { alias: [FILE, ALTERNATE_ALIAS] }

    dir2/:
      extra_keys: are ignored
      alias: 2ndDir

    some/very/long/path/:
      into/a/deep/file/hierarchy/:
        can/be/addressed/with: { alias: A_PATH_INDEPENDANT_ALIAS }

Resolving this with
``pathaliases.resolve_yaml_to_path_strings("aliases.yml")`` returns a
dictionary:

.. code:: python

    {
        "SUBDIR": "dir/subdir/",
        "SUBDIR_2": "dir/subdir/some/other/dir/"
        "FILE": "file.txt",
        "ALTERNATE_ALIAS": "file.txt",
        "2ndDir": "dir2/",
        "A_PATH_INDEPENDENT_ALIAS": "some/very/long/path/into/a/deep/file/hierarchy/can/be/addressed/with"
    }

Which can be used to make codebases independent from paths:

.. code:: python

    # Before
    subdir = "dir/subdir/"
    subdir_2 = os.path.join(subdir, subdir_2)

    # After: *where* the dirs are is configurable
    aliases = pathaliases.resolve_yaml_to_path_strings("aliases.yml")
    subdir = aliases["SUBDIR"]
    subdir_2 = aliases["SUBDIR_2"]

`pathaliases` is designed to be:

-  **Simple** - It just concatenates all the keys that lead up to an alias.
-  **Readable** - Developers and admins should be able to edit paths easily.
-  **Standard** - It uses standard file formats and conventions, making it
   easy to port to other languages.

Installation
============

Clone the repo:

::

    $ git clone https://github.com/adamkewley/pathaliases.git
    $ python setup.py install

Usage
=====

Resolve aliases directly from a YAML file:

.. code:: python

    import pathaliases

    aliases = pathaliases.resolve_yaml_to_path_strings("aliases.yml")

    print(aliases["SUBDIR"])  # echoes: "dir/subdir/"

Resolve aliases from a dict:

.. code:: python

    import pathaliases

    aliases_dict = {
        "dir/": {
            "subdir/": {"alias": "SUBDIR"}
        }
    }

    aliases = pathaliases.resolve_path_strings(aliases_dict)
    print(aliases["SUBDIR"])  # echoes: "dir/subdir/"

Substituting Variables
======================

Alias files can also contain variables, templated with ``${VARNAME}``:

.. code:: yaml

    foo/:
      ${var}/:
        alias: ${key}

``pathaliases`` allows you to pass in an environment when evaluating
paths:

.. code:: python

    env = {
      "var": "bar",
      "key": "some_alias"
    }

    aliases =  pathaliases.resolve_yaml_to_path_strings("aliases.yml", env=env)

    aliases == {
      "some_alias": "foo/bar/",
    }

.. |Build Status| image:: https://travis-ci.org/adamkewley/pathaliases.svg?branch=master
   :target: https://travis-ci.org/adamkewley/pathaliases
