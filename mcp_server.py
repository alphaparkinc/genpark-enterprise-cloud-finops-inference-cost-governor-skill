"""MCP Server for Enterprise Cloud FinOps Inference Cost Governor."""
import sys
import json
import time
from client import EnterpriseCloudFinOpsInferenceCostGovernor

governor = EnterpriseCloudFinOpsInferenceCostGovernor()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "govern_cloud_inference_finops":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "route_and_govern_inference")
    tenant = args.get("tenant_id", "dept_finance_01")

    if action == "route_and_govern_inference":
        return governor.route_and_govern_inference(
            tenant_id=tenant,
            task_complexity=args.get("task_complexity", "STANDARD_WORKFLOW"),
            estimated_input_tokens=int(args.get("estimated_input_tokens", 5000)),
            estimated_output_tokens=int(args.get("estimated_output_tokens", 1500)),
            daily_budget_usd=float(args.get("daily_budget_usd", 10.0))
        )
    elif action == "get_tenant_finops_report":
        return governor.get_tenant_finops_report(tenant)
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        res1 = governor.route_and_govern_inference("tenant_a", "SIMPLE_LOOKUP", 10000, 2000, daily_budget_usd=1.0)
        assert res1["routed_model_tier"] == "FLASH_LITE"
        assert res1["cost_saved_vs_pro_usd"] > 0

        # Simulate high spend to trigger soft cap downgrade
        governor.tenant_ledger["tenant_a"]["accumulated_spend_usd"] = 0.90
        res2 = governor.route_and_govern_inference("tenant_a", "DEEP_ARCHITECTURAL_REASONING", 10000, 2000, daily_budget_usd=1.0)
        assert res2["routed_model_tier"] == "FLASH_STANDARD"
        assert "SOFT_CAP" in res2["finops_policy_action"]
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "EnterpriseCloudFinOpsInferenceCostGovernor", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "govern_cloud_inference_finops",
                            "description": "Route agent queries to cost-optimal LLM tiers, calculate token inference cost, and enforce tenant FinOps budget limits.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["route_and_govern_inference", "get_tenant_finops_report"]},
                                    "tenant_id": {"type": "string"},
                                    "task_complexity": {"type": "string"},
                                    "estimated_input_tokens": {"type": "integer"},
                                    "estimated_output_tokens": {"type": "integer"},
                                    "daily_budget_usd": {"type": "number"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
