import unittest
import numpy as np
from task import Task


class TestTask(unittest.TestCase):
    def test_solution_accuracy(self):
        task = Task(identifier=1, size=500)
        task.work()
        Ax = np.dot(task.a, task.x)
        np.testing.assert_allclose(Ax, task.b, atol=1e-5)

    def test_execution_time(self):
        task = Task(identifier=2, size=500)
        task.work()

        self.assertLess(task.time, 5.0, "Computation took too long!")


if __name__ == "__main__":
    unittest.main()
