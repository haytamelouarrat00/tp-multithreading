import unittest

from task import Task


class TestTask(unittest.TestCase):
    def test_equal(self):
        task_1 = Task()
        txt_task = task_1.to_json()
        task_2 = Task.from_json(txt_task)
        self.assertEqual(task_1, task_2)
