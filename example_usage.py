from client import TwoPhaseCommitCoordinator

def run_example():
    print("=== GenPark 2PC Transaction Coordinator Example ===")
    coord = TwoPhaseCommitCoordinator(["db1", "db2"])
    coord.initiate_transaction("tx-demo-01", "BATCH_PAYMENT")
    coord.record_vote("tx-demo-01", "db1", True)
    final = coord.record_vote("tx-demo-01", "db2", True)
    print("Final Consensus Status:", final["status"])

if __name__ == "__main__":
    run_example()
