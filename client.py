from typing import List, Dict, Any, Optional

class TwoPhaseCommitCoordinator:
    def __init__(self, participants: Optional[List[str]] = None):
        self.participants = participants or ["shard_east", "shard_west", "shard_eu"]
        self.transactions: Dict[str, Dict[str, Any]] = {}

    def initiate_transaction(self, tx_id: str, action: str) -> Dict[str, Any]:
        self.transactions[tx_id] = {
            "tx_id": tx_id,
            "action": action,
            "phase": "PREPARE",
            "votes": {},
            "status": "IN_PROGRESS"
        }
        return self.transactions[tx_id]

    def record_vote(self, tx_id: str, participant: str, vote: bool) -> Dict[str, Any]:
        tx = self.transactions.get(tx_id)
        if not tx:
            return {"error": "Tx not found"}
        tx["votes"][participant] = vote
        if len(tx["votes"]) == len(self.participants):
            all_yes = all(tx["votes"].values())
            tx["phase"] = "COMMIT" if all_yes else "ABORT"
            tx["status"] = "COMMITTED" if all_yes else "ABORTED"
        return tx

    def benchmark_2pc_transaction(self) -> Dict[str, Any]:
        tx_id = "tx-benchmark-99"
        self.initiate_transaction(tx_id, "ESCROW_RELEASE")
        self.record_vote(tx_id, "shard_east", True)
        self.record_vote(tx_id, "shard_west", True)
        return self.record_vote(tx_id, "shard_eu", True)
