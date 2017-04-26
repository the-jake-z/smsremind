import unittest
import os
os.environ['CONFIG_CLASS'] = 'config.TestingConfig'
from main import commands, Lists

"""
commands = {
    'create': create_list,
    'delete': delete_list,
    'add': add_item,
    'rm': remove_item,
    'sub': add_sub,
    'unsub': remove_sub,
    'stop': stop,
    'help': help
}
"""


class SMSRemindTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_list(self):
        message = commands['create']('708-287-0004', 'create groceries')
        self.assertEqual(Lists.objects.count(), 1)
        self.assertEqual(message, "list \"groceries\" created")

    def test_delete_list(self):
        create_message = commands['create']('708-287-0004', 'create groceries')
        second_create = commands['create']('708-867-5309', 'create groceries')
        delete_message = commands['delete']('708-287-0004', 'delete groceries')
        self.assertEqual(Lists.objects.count(), 1)
        self.assertEqual(delete_message, 'list \"groceries\" deleted')

    def test_add_item(self):
        pass

    def test_remove_item(self):
        pass

    def test_add_subscription(self):
        pass

    def test_remove_subscription(self):
        pass

    def test_stop(self):
        pass

    def test_help(self):
        pass

    def tearDown(self):
        Lists.drop_collection()

if __name__ == "__main__":
    unittest.main()
