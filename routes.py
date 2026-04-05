from uuid import uuid4

from fastapi import APIRouter, HTTPException

from blockchain import Blockchain
from schemas import BMDTransactionRequest, BMDNodesRequest

bmd_node_identifier = str(uuid4()).replace("-", "")

bmd_blockchain = Blockchain()
router = APIRouter()


@router.post(
    "/transactions/new",
    status_code=201,
    description="Create a new transaction",
)
def bmd_new_transaction(tx: BMDTransactionRequest) -> dict:
    index = bmd_blockchain.bmd_new_transaction(
        sender=tx.sender,
        recipient=tx.recipient,
        amount=tx.amount,
    )
    return {"message": f"Transaction will be added to Block {index}"}


@router.get(
    "/mine", description="Performs PoW, hash transactions to Merkle Tree"
)
def bmd_mine() -> dict:
    last_block = bmd_blockchain.bmd_last_block
    last_proof = last_block["proof"]
    # 1. Знаходимо новий proof
    proof = bmd_blockchain.bmd_proof_of_work(last_proof)
    # 2. Нагорода майнеру (відправник "0" = нова монета)
    bmd_blockchain.bmd_new_transaction(
        sender="0",
        recipient=bmd_node_identifier,
        amount=2,
    )
    # 3. Хешуємо транзакції в меркель-дерево
    merkle_root = bmd_blockchain.bmd_merkle_root(
        bmd_blockchain.bmd_current_transactions
    )
    # 4. Створюємо новий блок
    previous_hash = Blockchain.bmd_hash(last_block)
    block = bmd_blockchain.bmd_new_block(proof, previous_hash)

    return {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "merkle_root": merkle_root,
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }


@router.get("/chain", description="Get all blockchain")
def bmd_full_chain() -> dict:
    return {
        "chain": bmd_blockchain.bmd_chain,
        "length": len(bmd_blockchain.bmd_chain),
    }


@router.post("/nodes/register", status_code=201)
def bmd_register_nodes(request: BMDNodesRequest) -> dict:
    if not request.nodes:
        raise HTTPException(
            status_code=400, detail="Please supply a valid list of nodes"
        )

    for node in request.nodes:
        bmd_blockchain.bmd_register_node(node)

    return {
        "message": "New nodes have been added",
        "total_nodes": list(bmd_blockchain.bmd_nodes),
    }


@router.get("/nodes/resolve")
def bmd_consensus() -> dict:
    replaced = bmd_blockchain.bmd_resolve_conflicts()

    if replaced:
        return {
            "message": "Our chain was replaced",
            "new_chain": bmd_blockchain.bmd_chain,
        }
    return {
        "message": "Our chain is authoritative",
        "chain": bmd_blockchain.bmd_chain,
    }
