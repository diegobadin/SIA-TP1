import time

class Metrics:
    def __init__(self):
        self.expanded_nodes_qty = 0
        self.frontier_nodes_qty = 0
        self.duration = 0
        self.result = None
        self.cost = 0
        self.solution = []

    def start_timer(self):
        self._start_time = time.time()

    def stop_timer(self):
        self.duration = time.time() - self._start_time

    def to_dict(self):
        return {
            "result": self.result,
            "cost": self.cost,
            "expanded_nodes_qty": self.expanded_nodes_qty,
            "frontier_nodes_qty": self.frontier_nodes_qty,
            "solution": self.solution,
            "duration": self.duration
        }
