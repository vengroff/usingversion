"""A package for testing the abiity of usingversion to manage package versions."""

from usingversion import getattr_with_version

__getattr__ = getattr_with_version("usingversion", __file__, __name__)
