import unittest
from os_simulator.algorithms import cpu_schedule, bankers_algorithm, page_replacement

class TestOSAlgorithms(unittest.TestCase):
    def test_fcfs_metrics(self):
        r = cpu_schedule([{"pid":"P1","arrival":0,"burst":5},{"pid":"P2","arrival":1,"burst":3}], "FCFS")
        self.assertEqual(r["average_waiting"], 2.0)
        self.assertEqual(r["average_turnaround"], 6.0)

    def test_round_robin_finishes_all(self):
        r = cpu_schedule([{"pid":"P1","arrival":0,"burst":5},{"pid":"P2","arrival":1,"burst":3}], "Round Robin", 2)
        self.assertEqual({x["pid"] for x in r["metrics"]}, {"P1", "P2"})
        self.assertEqual({x["completion"] > 0 for x in r["metrics"]}, {True})

    def test_banker_safe_example(self):
        a = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
        m = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
        r = bankers_algorithm(a, m, [3,3,2])
        self.assertTrue(r["safe"])
        self.assertEqual(len(r["sequence"]), 5)

    def test_page_fault_counts(self):
        r = page_replacement([1,2,3,1,4], 3, "FIFO")
        self.assertEqual(r["hits"], 1)
        self.assertEqual(r["faults"], 4)

if __name__ == "__main__":
    unittest.main()
