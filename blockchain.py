import hashlib
import json
from time import time
from urllib.parse import urlparse

import requests

from interface import BMDBlockchainInterface


class Blockchain(BMDBlockchainInterface):
    def __init__(self):
        self.bmd_current_transactions = []
        self.bmd_chain = []
        self.bmd_nodes = set()

        self.bmd_new_block(proof=20040203, previous_hash="Bondarevskyi")

    def bmd_register_node(self, address: str) -> None:
        parsed = urlparse(address)
        self.bmd_nodes.add(parsed.netloc)

    def bmd_valid_chain(self, chain: list) -> bool:
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block["previous_hash"] != self.bmd_hash(last_block):
                return False

            if not self.bmd_valid_proof(last_block["proof"], block["proof"]):
                return False

            last_block = block
            current_index += 1

        return True

    def bmd_resolve_conflicts(self) -> bool:
        neighbours = self.bmd_nodes
        new_chain = None
        max_length = len(self.bmd_chain)

        for node in neighbours:
            try:
                response = requests.get(f"http://{node}/chain", timeout=5)
                if response.status_code == 200:
                    length = response.json()["length"]
                    chain = response.json()["chain"]

                    # Беремо ланцюг лише якщо він довший і валідний
                    if length > max_length and self.bmd_valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except requests.exceptions.ConnectionError:
                continue

        if new_chain:
            self.bmd_chain = new_chain
            return True

        return False

    def bmd_proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while not self.bmd_valid_proof(last_proof, proof, bmd_target="03"):
            proof += 1
        return proof

    @staticmethod
    def bmd_valid_proof(
        last_proof: int, proof: int, bmd_target: str = "03"
    ) -> bool:
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.endswith(bmd_target)

    @staticmethod
    def bmd_merkle_root(transactions: list) -> str:
        if not transactions:
            return "0" * 64

        def bmd_hash_tx(tx: dict) -> str:
            tx_string = json.dumps(tx, sort_keys=True).encode()
            return hashlib.sha256(tx_string).hexdigest()

        layer = [bmd_hash_tx(tx) for tx in transactions]

        while len(layer) > 1:
            next_layer = []
            if len(layer) % 2 == 1:
                layer.append(
                    layer[-1]
                )  # дублюємо останній при непарній кількості
            for i in range(0, len(layer), 2):
                combined = (layer[i] + layer[i + 1]).encode()
                next_layer.append(hashlib.sha256(combined).hexdigest())
            layer = next_layer

        return layer[0]

    def bmd_new_block(
        self, proof: int, previous_hash: str | None = None
    ) -> dict:
        merkle_root = self.bmd_merkle_root(self.bmd_current_transactions)

        block = {
            "index": len(self.bmd_chain) + 1,
            "timestamp": time(),
            "transactions": self.bmd_current_transactions,
            "merkle_root": merkle_root,
            "proof": proof,
            "previous_hash": previous_hash
            or self.bmd_hash(self.bmd_chain[-1]),
        }

        self.bmd_current_transactions = []
        self.bmd_chain.append(block)
        return block

    def bmd_new_transaction(
        self, sender: str, recipient: str, amount: int
    ) -> int:
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
