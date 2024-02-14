"""A package for testing the abiity of packageversion to manage package versions."""

from packageversion import getattr_with_version

__getattr__ = getattr_with_version("packageversion", __file__, __name__)