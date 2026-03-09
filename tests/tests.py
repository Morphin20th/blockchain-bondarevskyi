import unittest
from blockchain import Blockchain


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.bc = Blockchain()

    def test_new_block_creation(self):
        initial_length = len(self.bc.bmd_chain)

        self.bc.bmd_new_block(proof=777, previous_hash="test_hash")

        self.assertEqual(len(self.bc.bmd_chain), initial_length + 1)
        self.assertEqual(self.bc.bmd_chain[-1]["proof"], 777)
        self.assertEqual(self.bc.bmd_chain[-1]["previous_hash"], "test_hash")


if __name__ == "__main__":
    unittest.main()
