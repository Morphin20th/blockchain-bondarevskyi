from abc import ABC, abstractmethod


class BMDBlockchainInterface(ABC):
    @abstractmethod
    def bmd_new_block(self, proof: int, previous_hash: str | None = None) -> dict:
        """
        Creating a new block in the blockchain

        :param proof: Evidence of work done
        :param previous_hash: Hash of the previous block
        :return: New block in the blockchain
        """

    @abstractmethod
    def bmd_new_transaction(self, sender: str, recipient: str, amount: int) -> int:
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
        Find a number p' such that hash(pp') contains specific trailing criteria.

        :param last_proof: The proof of the previous block.
        :return: The found proof.
        """

    @staticmethod
    @abstractmethod
    def bmd_valid_proof(last_proof: int, proof: int, bmd_target: str) -> bool:
        """
        Validates the proof: Does hash(last_proof, proof) contain the target criteria?

        :param last_proof: Previous proof.
        :param proof: Current proof.
        :param bmd_target: Target string (e.g., birth month) to find at the end of the hash.
        :return: True if correct, False if not.
        """
