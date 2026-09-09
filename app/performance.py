import time


class PerformanceTimer:

    def __init__(self):

        self.start_time = time.perf_counter()
        self.checkpoints = {}

    def checkpoint(self, name):

        current_time = time.perf_counter()

        elapsed = round(
            current_time - self.start_time,
            3
        )

        self.checkpoints[name] = elapsed

        return elapsed

    def get_total_time(self):

        return round(
            time.perf_counter() - self.start_time,
            3
        )

    def get_checkpoints(self):

        return self.checkpoints.copy()