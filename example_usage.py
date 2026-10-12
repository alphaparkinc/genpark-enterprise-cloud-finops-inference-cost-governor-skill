"""Example usage for EnterpriseCloudFinOpsInferenceCostGovernor."""
import sys
import json
from client import EnterpriseCloudFinOpsInferenceCostGovernor

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Tencent Cloud & WorkBuddy LLM Inference FinOps Governor Demo ===")
    governor = EnterpriseCloudFinOpsInferenceCostGovernor()

    # 1. Route a routine lookup task
    print("\n--- 1. Routing Routine Table Lookup (50k Input / 5k Output Tokens) ---")
    r1 = governor.route_and_govern_inference(
        tenant_id="marketing_dept",
        task_complexity="SIMPLE_LOOKUP",
        estimated_input_tokens=50000,
        estimated_output_tokens=5000,
        daily_budget_usd=0.50
    )
    print(f"Routed Tier: {r1['routed_model_tier']} | Call Cost: ${r1['estimated_call_cost_usd']:.4f} (Saved ${r1['cost_saved_vs_pro_usd']:.4f} vs Pro)")

    # 2. Simulate nearing budget limit and requesting Deep Reasoning
    print("\n--- 2. Triggering 85% Soft Cap Budget Protection ---")
    governor.tenant_ledger["marketing_dept"]["accumulated_spend_usd"] = 0.45
    r2 = governor.route_and_govern_inference(
        tenant_id="marketing_dept",
        task_complexity="DEEP_ARCHITECTURAL_REASONING",
        estimated_input_tokens=40000,
        estimated_output_tokens=8000,
        daily_budget_usd=0.50
    )
    print(f"Ideal Tier: {r2['ideal_model_tier']} -> Enforced Tier: {r2['routed_model_tier']}")
    print(f"FinOps Policy Action: {r2['finops_policy_action']} (Utilization: {r2['budget_utilization_pct']}%)")

if __name__ == "__main__":
    main()
