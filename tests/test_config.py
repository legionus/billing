import unittest2 as unittest
import unithelper

from bc import config
from bc import mongodb


class Test(unithelper.TestCase):
	def test_inline_config(self):
		"""Check reading configuration from string"""

		confstr = """
		{
			"database": {
				"name": "testing",
				"server": "127.0.0.1",
				"shards": ["127.0.0.10", "127.0.0.11", "127.0.0.12", "127.0.0.13", "127.0.0.14"]
			}
		}
		"""

		def setx():
			conf = config.read(inline = confstr, force=True)
		self.assertTrue(setx)


	def test_inline_wrong(self):
		"""Check wrong syntax in inline configuration"""

		confstr = """
		{
			"database": {
				"name": "testing
			}
		}
		"""

		def setx():
			conf = config.read(inline = confstr, force=True)
		self.assertRaises(ValueError,setx)


	def test_file_config(self):
		"""Check reading config file"""

		def setx():
			conf = config.read('./test_config1.conf', force=True)
		self.assertTrue(setx)


	def test_file_wrong(self):
		"""Check reading config file with wrong syntax"""

		def setx():
			conf = config.read('./test_config2.conf', force=True)
		self.assertRaises(ValueError,setx)
