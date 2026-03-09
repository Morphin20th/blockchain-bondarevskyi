import hashlib

from blockchain import Blockchain

if __name__ == "__main__":
    bmd_blockchain = Blockchain()

    print("=" * 60)
    print("БЛОКЧЕЙН — Bondarevskyi")
    print("PoW критерій: хеш закінчується на '03'")
    print("=" * 60)

    # --- Блок генезису ---
    genesis = bmd_blockchain.bmd_last_block
    print("\n[ГЕНЕЗИС-БЛОК]")
    print(f"Індекс: {genesis['index']}")
    print(f"Proof: {genesis['proof']}")
    print(f"Previous hash: {genesis['previous_hash']}")
    print(f"Hash блоку: {Blockchain.bmd_hash(genesis)}")

    print("\n[ТРАНЗАКЦІЇ]")
    idx1 = bmd_blockchain.bmd_new_transaction(
        sender="Bondarevskyi", recipient="Recipient_A", amount=50
    )
    print(f"Транзакція 1 буде в блоці #{idx1}")

    idx2 = bmd_blockchain.bmd_new_transaction(
        sender="Recipient_A", recipient="Recipient_B", amount=25
    )
    print(f"Транзакція 2 буде в блоці #{idx2}")

    print("\n[МАЙНІНГ БЛОКУ #2]")
    last_proof = bmd_blockchain.bmd_last_block["proof"]
    print(f"Попередній proof: {last_proof}")
    print("Шукаємо новий proof (хеш має закінчуватись на '03')...")

    new_proof = bmd_blockchain.bmd_proof_of_work(last_proof)
    print(f"Знайдено proof: {new_proof}")

    # Перевірка знайденого proof
    check_hash = hashlib.sha256(
        f"{last_proof}{new_proof}".encode()
    ).hexdigest()
    print(f"Хеш(pp'): {check_hash}")
    print(f"Закінчується на '03': {check_hash.endswith('03')}")

    block2 = bmd_blockchain.bmd_new_block(proof=new_proof)
    print("\n[БЛОК #2 СТВОРЕНО]")
    print(f"Індекс: {block2['index']}")
    print(f"Proof: {block2['proof']}")
    print(f"Транзакцій: {len(block2['transactions'])}")
    print(f"Previous hash: {block2['previous_hash']}")
    print(f"Hash блоку: {Blockchain.bmd_hash(block2)}")

    # --- Майнінг блоку 3 (порожній) ---
    print("\n[МАЙНІНГ БЛОКУ #3]")
    last_proof = bmd_blockchain.bmd_last_block["proof"]
    new_proof = bmd_blockchain.bmd_proof_of_work(last_proof)
    block3 = bmd_blockchain.bmd_new_block(proof=new_proof)
    check_hash = hashlib.sha256(
        f"{last_proof}{new_proof}".encode()
    ).hexdigest()
    print(f"Знайдено proof: {new_proof}")
    print(f"Хеш(pp'): {check_hash}")
    print(f"Закінчується на '03': {check_hash.endswith('03')}")
    print(f"Hash блоку: {Blockchain.bmd_hash(block3)}")

    # --- Стан ланцюга ---
    print("\n[СТАН ЛАНЦЮГА]")
    print(f"Кількість блоків: {len(bmd_blockchain.bmd_chain)}")
    for b in bmd_blockchain.bmd_chain:
        print(
            f"Блок #{b['index']} | proof={b['proof']} | "
            f"tx={len(b['transactions'])} | prev={b['previous_hash'][:20]}..."
        )

    print("\n" + "=" * 60)
    print("Протокол виконаної роботи підтверджено")
    print("=" * 60)
