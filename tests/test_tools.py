import unittest
from unittest import TestCase

from uds.tools import cli


class TestCLI(TestCase):

    def setUp(self):
        pass

    def test_help(self):
        try:
            cli.execute(['--help'])
            # cli.main(['-h'])
        except SystemExit as e:
            print '=='
            print 'SystemExit=%s' % e
            print '=='

    def test_version(self):
        try:
            cli.execute(['--version'])
            # cli.main(['-v'])
        except SystemExit as e:
            print '=='
            print 'SystemExit=%s' % e
            print '=='

    def test_newproject(self):
        cli.execute(['new-project', 'my-project1'])

    def test_newsensor(self):
        cli.execute(['new-sensor', 'MySensor1'])

    def test_run(self):
        cli.execute(['run', 'MySensor1'])
        assert False


if __name__ == '__main__':
    unittest.main()