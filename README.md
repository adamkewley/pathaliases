# pathaliases

A python package for handling path aliases.

Path aliases can be loaded directly from YAML files:

```yaml
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
```

Resolving this with `pathaliases.resolve_yaml_to_path_strings("aliases.yml")`
returns a dictionary:

```python
{
    "SUBDIR": "dir/subdir/",
    "SUBDIR_2": "dir/subdir/some/other/dir/"
    "FILE": "file.txt",
    "ALTERNATE_ALIAS": "file.txt",
    "2ndDir": "dir2/",
    "A_PATH_INDEPENDENT_ALIAS": "some/very/long/path/into/a/deep/file/hierarchy/can/be/addressed/with"
}
```

Which can then be used to give code some path-independence:

```python
# Before
subdir = "dir/subdir/"
subdir_2 = os.path.join(subdir, subdir_2)

# After: *where* the dirs are is configurable
aliases = pathaliases.resolve_yaml_to_path_strings("aliases.yml")
subdir = aliases["SUBDIR"]
subdir_2 = aliases["SUBDIR_2"]
```

This approach is designed to be:

- **Extremely simple** - `pathaliases` is just concatenating all the keys
  that lead up to an alias.
- **Readable** - A developer/sysadmin should be able to read, understand,
  and edit pathaliases without much effort.
- **Easy to port** - The implementation uses standard file formats and
  conventions, making it easy to reimplement in other languages


# Installation

Clone the repo:

    $ git clone https://github.com/adamkewley/pathaliases.git
    $ python setup.py install


# Usage

Resolve aliases directly from a YAML file:

```python
import pathaliases

aliases = pathaliases.resolve_yaml_to_path_strings("aliases.yml")

print(aliases["SUBDIR"])  # echoes: "dir/subdir/"
```

Resolve aliases from a dict:

```python
import pathaliases

aliases_dict = {
    "dir/": {
        "subdir/": {"alias": "SUBDIR"}
    }
}

aliases = pathaliases.resolve_path_strings(aliases_dict)
print(aliases["SUBDIR"])  # echoes: "dir/subdir/"
```
