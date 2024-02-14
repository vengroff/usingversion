import unittest
import testme


class PackageVersionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """Set up before each test."""
        self.expected_version = '0.1.0+'

    def test_testme_version(self):
        """Test the .version attribute."""
        self.assertEqual(self.expected_version, testme.version)  # add assertion here

    def test_testme_underscore_version(self):
        """Test the ._version attribute."""
        self.assertEqual(self.expected_version, testme._version)  # add assertion here

    def test_testme_other_attribute(self):
        """Test an attribute that is there naturally to be sure passing through finds it."""
        testme_dict = testme.__dict__

        self.assertIsInstance(testme_dict, dict)

    def test_testme_missing_attribute(self):
        """Test a missing attribute."""
        with self.assertRaises(AttributeError):
            testme.version_x


if __name__ == '__main__':
    unittest.main()
