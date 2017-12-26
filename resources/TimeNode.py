from typing import List
from datetime import datetime
import unittest


class TimeNode(object):
    def __init__(self,
                 start_time: datetime=None,
                 end_time: datetime=None,
                 children=None):
        if children is None:
            self.start_time = start_time
            self.end_time = end_time
            self.children = []
        else:
            self.start_time = min([node.start_time for node in children])
            self.end_time = max([node.end_time for node in children])
            self.children = children
            self.children.sort()
        self.links = []

    def __lt__(self, other):
        self_tuple = (self.start_time, self.end_time)
        other_tuple = (other.start_time, other.end_time)
        return self_tuple < other_tuple

    def strong_verify_children(self):
        for i, node in enumerate(self.children):
            if i > 0 and node.start_time != self.children[i-1].end_time:
                return False
        return True

    def weak_verify_children(self):
        for i, node in enumerate(self.children):
            if i > 0 and node.start_time < self.children[i - 1].end_time:
                return False
        return True

    def add_link(self, link):
        if link not in self.links:
            self.links.append(link)
            return True
        return False


class TestTimeNode(unittest.TestCase):

    def test_create_node_by_interval(self):
        before = datetime.now()
        after = datetime.now()
        root_node = TimeNode(start_time=before, end_time=after)
        self.assertEqual(before, root_node.start_time)
        self.assertEqual(after, root_node.end_time)

    def test_create_node_from_subchildren(self):
        time1 = datetime.now()
        time2 = datetime.now()
        time3 = datetime.now()
        left_child = TimeNode(start_time=time1, end_time=time2)
        right_child = TimeNode(start_time=time2, end_time=time3)
        root_node = TimeNode(children=[right_child, left_child])
        self.assertEqual(root_node.children[0], left_child)
        self.assertEqual(root_node.children[1], right_child)

    def test_strong_verify_pass(self):
        time1 = datetime.now()
        time2 = datetime.now()
        time3 = datetime.now()
        left_child = TimeNode(start_time=time1, end_time=time2)
        right_child = TimeNode(start_time=time2, end_time=time3)
        root_node = TimeNode(children=[right_child, left_child])
        self.assertTrue(root_node.strong_verify_children())

    def test_strong_verify_fail(self):
        time1 = datetime.now()
        time2 = datetime.now()
        time3 = datetime.now()
        time4 = datetime.now()
        left_child = TimeNode(start_time=time1, end_time=time2)
        right_child = TimeNode(start_time=time3, end_time=time4)
        root_node = TimeNode(children=[right_child, left_child])
        self.assertFalse(root_node.strong_verify_children())

    def test_weak_verify_pass(self):
        time1 = datetime.now()
        time2 = datetime.now()
        time3 = datetime.now()
        time4 = datetime.now()
        left_child = TimeNode(start_time=time1, end_time=time2)
        right_child = TimeNode(start_time=time3, end_time=time4)
        root_node = TimeNode(children=[right_child, left_child])
        self.assertTrue(root_node.weak_verify_children())

if __name__ == '__main__':
    unittest.main()
