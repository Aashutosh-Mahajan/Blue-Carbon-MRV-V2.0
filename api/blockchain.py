import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from django.conf import settings
from django.db import transaction as db_transaction

# Import models lazily to avoid app registry issues at import time
def _import_models():
    from .models import ChainBlock, ChainTransaction
    return ChainBlock, ChainTransaction


@dataclass
class Tx:
    sender: str
    recipient: str
    amount: float
    project_id: int | None
    kind: str  # ISSUE or TRANSFER
    meta: Dict[str, Any] | None = None


class SimpleBlockchain:
    """Ultra-light in-app blockchain for demo purposes.

    Blocks are appended atomically in memory + optional future persistence.
    No POW for speed; hash links only.
    """

    def __init__(self):
        self.chain: List[dict] = []
        self.pending: List[Tx] = []
        # Load persisted chain from DB if present, otherwise create genesis
        try:
            ChainBlock, ChainTransaction = _import_models()
            blocks = list(ChainBlock.objects.all().order_by("index"))
            if blocks:
                for b in blocks:
                    item = b.raw or {
                        "index": b.index,
                        "timestamp": b.timestamp,
                        "transactions": [],
                        "previous_hash": b.previous_hash,
                        "nonce": b.nonce,
                        "hash": b.hash,
                    }
                    # load txs
                    txs = []
                    for tx in b.txs.all():
                        txs.append({
                            "sender": tx.sender,
                            "recipient": tx.recipient,
                            "amount": tx.amount,
                            "project_id": tx.project_id,
                            "kind": tx.kind,
                            "meta": tx.meta,
                        })
                    item["transactions"] = txs
                    self.chain.append(item)
            else:
                self.new_block(previous_hash="GENESIS", nonce=0)
        except Exception:
            # If DB isn't ready (migrations not applied) fallback to in-memory genesis
            self.new_block(previous_hash="GENESIS", nonce=0)

    # ----------------- Core -----------------
    def new_block(self, nonce: int, previous_hash: str | None = None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "transactions": [asdict(t) for t in self.pending],
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
            "nonce": nonce,
        }
        block["hash"] = self.hash(block)
        # persist block and transactions
        try:
            ChainBlock, ChainTransaction = _import_models()
            with db_transaction.atomic():
                b = ChainBlock.objects.create(
                    index=block["index"],
                    timestamp=block["timestamp"],
                    previous_hash=block.get("previous_hash"),
                    nonce=block["nonce"],
                    hash=block["hash"],
                    raw=block,
                )
                for tx in block["transactions"]:
                    ChainTransaction.objects.create(
                        block=b,
                        sender=tx.get("sender"),
                        recipient=tx.get("recipient"),
                        amount=tx.get("amount"),
                        project_id=tx.get("project_id"),
                        kind=tx.get("kind"),
                        meta=tx.get("meta"),
                    )
        except Exception:
            b = None

        self.pending = []
        self.chain.append(block)
        return block

    def new_transaction(self, tx: Tx):
        self.pending.append(tx)
        # Auto mine if more than ~5 tx for responsiveness
        if len(self.pending) >= 5:
            self.new_block(nonce=0)
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block: dict) -> str:
        content = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(content).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    # ----------------- Convenience -----------------
    def issue_credits(self, recipient_addr: str, amount: float, project_id: int):
        self.new_transaction(Tx(sender="SYSTEM", recipient=recipient_addr, amount=float(amount), project_id=project_id, kind="ISSUE"))
        # mine immediately for deterministic demo ordering
        self.new_block(nonce=0)

    def transfer_credits(self, sender_addr: str, recipient_addr: str, amount: float, project_id: int):
        self.new_transaction(Tx(sender=sender_addr, recipient=recipient_addr, amount=float(amount), project_id=project_id, kind="TRANSFER"))
        self.new_block(nonce=0)


blockchain = SimpleBlockchain()

def get_chain():
    # Return the persisted chain list for compatibility with views
    return blockchain.chain
