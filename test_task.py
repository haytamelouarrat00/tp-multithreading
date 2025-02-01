import unittest
import numpy

from task import Task


class TestTask(unittest.TestCase):
    def test_equal(self):
        task = Task()
        task.work()
        numpy.testing.assert_allclose(task.a @ task.x, task.b)


if __name__ == "__main__":
    unittest.main()
