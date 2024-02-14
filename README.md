packageversion
==============

`packageversion` is a package designed to help
other packages help their users keep tract of 
what version they are using.

It was built with packages that are maintained with
[poetry](https://github.com/python-poetry/poetry) in
mind but it works in a more limited way with other
approaches.

For Package Maintainers
-----------------------

To use `packageversion` in your package, first take
a dependency on `packageversion`. In Poetry, you would
do this with 

```shell
poetry add usingversion
```

In other environments, you might add it to e.g. 
`requirements.txt.`

Now, just
add the following to the very end of your top-level `__init__.py`:

```python
from usingversion import getattr_with_version

__getattr__ = getattr_with_version("mypackage", __file__, __name__)
```

Be sure to substitute the actual name of your package for 
`"mypackage"`.

To test, try

```python
import mypackage

print(f"The version of mypackage is {mypackage.version}.")
```

For End Users
-------------

There's really nothing all that exciting to do.
If a package `somepackage` that you depend on uses
`packageversion` then you can check the version with

```python
import somepackage

print(f"The version of somepackage is {somepackage.version}.")
```

Unless the maintainters of `somepackage` have chosen
otherwise, `somepackage._version` is the same as 
`somepackage.version` so you can use whichever you
prefer.
