usingversion
============

`usingversion` is a package designed to help
other packages help their users keep tract of 
what version they are using.

It was built with packages that are maintained with
[poetry](https://github.com/python-poetry/poetry) in
mind but it works in a more limited way with other
approaches.

What is the Problem?
--------------------

As developers, we would like to have a single source or truth for
the version number of packages we maintain. In projects that use
[poetry](https://github.com/python-poetry/poetry), 
this is a `pyproject.toml` file, which typically begins 
something like

```
[tool.poetry]
name = "mypackage"
version = "1.2.3"
...
```

Once I have put a version number there, I would like the
code

```python
import mypackage

myppackage.version
```

to return the version number from `pyproject.toml`.

The issue is that project versions go through different
lifecycle phases. A package that has been built and published
on [pypi](https://www.pypi.org) has the version number that
started in `pyproject.toml` when it was built encoded elsewhere.
But a newer version that I am actively developing, testing, or debugging
before release only has the `pyproject.toml` version.

`usingversion` knows about this, and knows how to find the version
in either of those places in different scenarios. It makes 
`mypackage.version` always work no matter how I am using or developing
or testing.

### What about the `+`

As an added measure, to reduce confusion between development and 
production environments, when the version number comes straight
from `pyproject.toml` in a development environment, a `+` is 
appended. This indicates that the source could have been modified
in the development environment. So instead of `"1.2.3"`, the
version will be reported as `"1.2.3+"`.

For Package Maintainers
-----------------------

To use `usingversion` in your package, first take
a dependency on `usingversion`. In Poetry, you would
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
You might not even know or care that the developer
of a package you depend on chose to use `usingversion`.
If a package `somepackage` that you depend on uses
`usingversion` then you can check the version with

```python
import somepackage

print(f"The version of somepackage is {somepackage.version}.")
```

Unless the maintainters of `somepackage` have chosen
otherwise, `somepackage._version` is the same as 
`somepackage.version` so you can use whichever you
prefer.
