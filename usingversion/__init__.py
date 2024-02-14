"""
A package for managing package versions for other packages.

Versions are based on a two part check:

1. Can `importlib.metadata.version` find the version of the installed package?
   If so, that is the version that is used.
2. If  `importlib.metadata.version` can't find the version, often because it is
   a development version, look for a `pyproject.toml` file and try to find
   the version there.

Canonical usage of this package is to add the following to the end of the `__init__.py`
file of the package's top-level Python package::

    from usingversion import getattr_with_version

    __getattr__ = getattr_with_version("packagename", __file__, __name__)

"""

import importlib.metadata
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Optional

__package_versions = defaultdict(lambda: "unknown")
"""
A dictionary of package versions that have been found and cached.

This is managed by `__get_package_version` whose existence is hidden behind
:py:func:`~getattr_with_version`.
"""


def __get_package_version(package: str, file: str) -> str:
    """
    Find the version of this package.
    """
    global __package_versions

    if __package_versions[package] != "unknown":
        # We already set it at some point in the past,
        # so return that previous value without any
        # extra work.
        return __package_versions[package]

    try:
        # Try to get the version of the current package if
        # it is running from a distribution.
        package_version = importlib.metadata.version(package)

        __package_versions[package] = package_version
    except importlib.metadata.PackageNotFoundError:
        # Fall back on getting it from a local pyproject.toml.
        # This works in a development environment where the
        # package has not been installed from a distribution.
        import toml

        file_path = Path(file)

        for pyproject_toml_dir in [
            file_path.parent,
            file_path.parent.parent,
            file_path.parent.parent.parent,
        ]:
            pyproject_toml_file = pyproject_toml_dir / "pyproject.toml"

            if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
                package_version = toml.load(pyproject_toml_file)["tool"]["poetry"][
                    "version"
                ]
                # Indicate it might be locally modified or unreleased.
                package_version = package_version + "+"

                __package_versions[package] = package_version
                break

    return __package_versions[package]


def getattr_with_version(
    package: str,
    file: str,
    module_name: str,
    *,
    attribute_name: Optional[str] = None,
) -> Callable[[str], Any]:
    """
    Add a version attribute to a package based on the version installed.

    Canonical usage in the __init__.py file of the root-level module of
    a package named `packagename` is::

        from usingversion import getattr_with_version

        __getattr__ = getattr_with_version("packagename", __file__, __name__)

    Ideally, this should come at the very end of the `__init__.py` file.

    Parameters
    ----------
    package
        The name of the package whose version attribute we want to use.
    file
        Should always be `__file__`.
    module_name
        Should always be `__name__`.
    attribute_name
        An optional name for the version attribute. By default, both
        `version` and `_version` are set, but this can be used to override
        that if needed for some reason.
    Returns
    -------
        A function that is suitable for assingining to `package.__getattr__`.
    """

    def version_getter(name: str) -> Any:
        """
        Get package attributes.

        This function is returned by :py:func:`~getattr_with_version`.
        """
        is_version_attribute = (
            attribute_name is not None and name == attribute_name
        ) or (attribute_name is None and name in ["version", "_version"])
        if is_version_attribute:
            return __get_package_version(package, file)
        else:
            raise AttributeError(f"No attribute {name} in module {module_name}.")

    return version_getter
