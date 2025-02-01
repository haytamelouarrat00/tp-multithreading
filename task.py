import time

import numpy as np
import json


class Task:
    def __init__(self, identifier=0, size=None):
        self.identifier = identifier
        # choosee the size of the problem
        self.size = size or np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def __str__(self) -> str:
        return f"Task {self.identifier}"

    def get_identifier(self):
        return self.identifier

    def get_result(self):
        return self.x

    def get_time(self):
        return self.time

    def to_json(self) -> str:
        data = {
            "identifier": self.identifier,
            "size": self.size,
            "a": self.a.tolist(),  # Convert numpy array to list
            "b": self.b.tolist(),  # Convert numpy array to list
            "x": self.x.tolist(),  # Convert numpy array to list
            "time": self.time,
        }
        return json.dumps(data, indent=4)

    @staticmethod
    def from_json(text: str) -> "Task":
        # Parse the JSON text into a dictionary
        data = json.loads(text)
        # Create a new Task task using the parsed data
        task = Task(data["identifier"], data["size"])
        # Overwrite the randomly initialized attributes with the loaded values
        task.a = np.array(data["a"])
        task.b = np.array(data["b"])
        task.x = np.array(data["x"])
        task.time = data["time"]
        return task

    def __eq__(self, other: "Task") -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.identifier == other.identifier
            and self.size == other.size
            and np.array_equal(self.a, other.a)
            and np.array_equal(self.b, other.b)
            and np.array_equal(self.x, other.x)
            and self.time == other.time
        )
