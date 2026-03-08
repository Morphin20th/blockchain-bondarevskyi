import hashlib
import json
from time import time

from interface import BMDBlockchainInterface


class Blockchain(BMDBlockchainInterface):
    def __init__(self):
        self.bmd_current_transactions = []
        self.bmd_chain = []

        self.bmd_new_block(proof=20040203, previous_hash="MAIN")

    def bmd_proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while not self.bmd_valid_proof(last_proof, proof, bmd_target="03"):
            proof += 1
        return proof

    @staticmethod
    def bmd_valid_proof(last_proof: int, proof: int, bmd_target: str = "03") -> bool:
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.endswith(bmd_target)


    def bmd_new_block(self, proof: int, previous_hash: str | None = None) -> dict:
        block = {
            "index": len(self.bmd_chain) + 1,
            "timestamp": time(),
            "transactions": self.bmd_current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.bmd_hash(self.bmd_chain[-1]),
        }

        self.bmd_current_transactions = []
        self.bmd_chain.append(block)
        return block

    def bmd_new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        self.bmd_current_transactions.append(
            {
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
            }
        )
        return self.bmd_last_block["index"] + 1

    @staticmethod
    def bmd_hash(block: dict) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def bmd_last_block(self) -> dict:
        return self.bmd_chain[-1]
