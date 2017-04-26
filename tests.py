import unittest
import os
os.environ['CONFIG_CLASS'] = 'config.TestingConfig'
from main import commands, Lists

"""
    SMSRemind
    commons ops:
    lists
    create [list]
    delete [list]
    add [list] [item]
    rm [list] [item index]
    ls [list]
    sub [list] [phone]
    lsub [list]
    unsub [list] [phone index]
    s
    h
    """

_from_number = '+17088675309'
_list_name = 'groceries'


def create_list(from_number, list_name):
    Lists(subs=[from_number], items=[], name=list_name).save()


def add_item_message(item, list_name):
    return 'add {list_name} {item}'.format(list_name=list_name, item=item)


def remove_item_message(item_index, list_name):
    return 'rm {list_name} {item_index}'.format(list_name=list_name, item_index=item_index)


class SMSRemindTests(unittest.TestCase):

    def setUp(self):
        Lists.drop_collection()

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
        create_list(_from_number, _list_name)
        response = commands['add'](_from_number, add_item_message('apples', _list_name))
        l = Lists.objects(subs=_from_number, name=_list_name).first()
        self.assertEqual(len(l.items), 1)

    def test_remove_item(self):
        create_list(_from_number, _list_name)
        commands['add'](_from_number, add_item_message('apples', _list_name))
        commands['add'](_from_number, add_item_message('oranges', _list_name))
        l = Lists.objects(subs=_from_number, name=_list_name).first()
        self.assertEqual(len(l.items), 2)
        commands['rm'](_from_number, remove_item_message(1, _list_name))
        l = Lists.objects(subs=_from_number, name=_list_name).first()
        self.assertEqual(len(l.items), 1)

    def test_add_subscription(self):
        create_list(_from_number, _list_name)
        commands['sub'](_from_number, 'sub {list_name} {phone}'.format(list_name=_list_name, phone='+15551234567'))
        l = Lists.objects(subs=_from_number, name=_list_name).first()
        self.assertEqual(len(l.subs), 2)

    def test_remove_subscription(self):
        create_list(_from_number, _list_name)
        commands['sub'](_from_number, 'sub {list_name} {phone}'.format(list_name=_list_name, phone='+15551234567'))
        l = Lists.objects(subs=_from_number, name=_list_name).first()
        self.assertEqual(len(l.subs), 2)
        commands['unsub'](_from_number, 'unsub {list_name} {phone}'.format(list_name=_list_name, phone=2))
        l = Lists.objects(subs=_from_number, name=_list_name).first()
        self.assertEqual(len(l.subs), 1)

    def test_stop(self):
        create_list(_from_number, _list_name)
        lists = Lists.objects(subs=_from_number, name=_list_name)
        self.assertEqual(len(lists), 1)
        commands['s'](_from_number, 's')
        lists = Lists.objects(subs=_from_number, name=_list_name)
        self.assertEqual(len(lists), 0)

    def test_help(self):
        pass

    def tearDown(self):
        Lists.drop_collection()

if __name__ == "__main__":
    unittest.main()
