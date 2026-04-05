from abc import ABC, abstractmethod


class BMDBlockchainInterface(ABC):
    @abstractmethod
    def bmd_new_block(
        self, proof: int, previous_hash: str | None = None
    ) -> dict:
        """
        Creating a new block in the blockchain

        :param proof: Evidence of work done
        :param previous_hash: Hash of the previous block
        :return: New block in the blockchain
        """

    @abstractmethod
    def bmd_new_transaction(
        self, sender: str, recipient: str, amount: int
    ) -> int:
        """
        Creates a new transaction to go into the next mined block.

        :param sender: Address of the sender.
        :param recipient: Address of the recipient.
        :param amount: Amount of the transaction.
        :return: The index of the block that will hold this transaction.
        """

    @staticmethod
    @abstractmethod
    def bmd_hash(block: dict) -> str:
        """
        Creates a SHA-256 hash of a block.

        :param block: The block to be hashed.
        :return: The hex string representation of the hash.
        """

    @property
    @abstractmethod
    def bmd_last_block(self) -> dict:
        """
        Returns the last block in the chain.

        :return: Last block dictionary.
        """

    @abstractmethod
    def bmd_proof_of_work(self, last_proof: int) -> int:
        """
        Simple Proof of Work Algorithm.
        Find a number p' such that hash(pp') contains specific trailing
        criteria

        :param last_proof: The proof of the previous block.
        :return: The found proof.
        """

    @staticmethod
    @abstractmethod
    def bmd_valid_proof(last_proof: int, proof: int, bmd_target: str) -> bool:
        """
        Validates the proof: Does hash(last_proof, proof)
        contain the target criteria?

        :param last_proof: Previous proof.
        :param proof: Current proof.
        :param bmd_target: Target string (e.g., birth month)
                            to find at the end of the hash.
        :return: True if correct, False if not.
        """

    @staticmethod
    @abstractmethod
    def bmd_merkle_root(transactions: list) -> str:
        """
        Builds a Merkle tree from transactions and returns the root hash.

        Merkle tree — Binary Tree of hashes:
        - Leaves: SHA-256 of each transaction
        - Nodes: SHA-256 concatenation of two child hashes
        - Root: a single hash representing all transactions

        :param transactions: List of transaction dicts.
        :return: Merkle root as hex string, or '0'*64 if no transactions.
        """

    @abstractmethod
    def bmd_register_node(self, address: str) -> None:
        """
        Adds a new node to the set of known nodes in the network.

        :param address: URL of node'
        """

    @abstractmethod
    def bmd_valid_chain(self, chain: list) -> bool:
        """
        Checks the validity of the transmitted chain:
         - the correctness of the previous_hash of each block
         - the correctness of the proof of each block

         :param chain: list of the blocks
         :return: True if valid, else False
        """

    @abstractmethod
    def bmd_resolve_conflicts(self) -> bool:
        """
        Consensus algorithm: replaces the current chain with the longest
        valid chain among all known nodes in the network.

        :return: True if the chain has been replaced, False if not
        """
