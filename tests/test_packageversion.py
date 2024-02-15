import unittest

import testme


class PackageVersionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """Set up before each test."""
        # Note that this will have to be updated manually
        # as we update versions in pyproject.toml.
        self.expected_version = "0.1.1"

    def asserExpectedVersion(self, version: str):
        self.assertTrue(
            (version == self.expected_version)
            or (version == f"{self.expected_version}+"),
            msg=f"Expected version {self.expected_version} or {self.expected_version}+ but got {version}.",
        )

    def test_testme_version(self):
        """Test the .version attribute."""
        self.asserExpectedVersion(testme.version)  # add assertion here

    def test_testme_underscore_version(self):
        """Test the ._version attribute."""
        self.asserExpectedVersion(testme._version)  # add assertion here

    def test_testme_other_attribute(self):
        """Test an attribute that is there naturally to be sure passing through finds it."""
        testme_dict = testme.__dict__

        self.assertIsInstance(testme_dict, dict)

    def test_testme_missing_attribute(self):
        """Test a missing attribute."""
        with self.assertRaises(AttributeError):
            testme.version_x


if __name__ == "__main__":
    unittest.main()
