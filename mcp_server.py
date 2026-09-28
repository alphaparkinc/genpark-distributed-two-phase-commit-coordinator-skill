import sys, json
from client import TwoPhaseCommitCoordinator

coord = TwoPhaseCommitCoordinator()

def handle_jsonrpc(line):
    global coord
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-distributed-two-phase-commit-coordinator-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "initiate_transaction", "description": "Initiate 2PC transaction.", "inputSchema": {"type": "object", "properties": {"tx_id": {"type": "string"}, "action": {"type": "string"}}, "required": ["tx_id", "action"]}},
                {"name": "record_vote", "description": "Record participant vote.", "inputSchema": {"type": "object", "properties": {"tx_id": {"type": "string"}, "participant": {"type": "string"}, "vote": {"type": "boolean"}}, "required": ["tx_id", "participant", "vote"]}},
                {"name": "benchmark_2pc_transaction", "description": "Run 2PC benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "initiate_transaction":
                res = coord.initiate_transaction(args.get("tx_id"), args.get("action"))
            elif tool == "record_vote":
                res = coord.record_vote(args.get("tx_id"), args.get("participant"), args.get("vote"))
            elif tool == "benchmark_2pc_transaction":
                res = coord.benchmark_2pc_transaction()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
