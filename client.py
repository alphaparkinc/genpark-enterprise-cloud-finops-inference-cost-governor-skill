"""
Enterprise Cloud FinOps & Multi-Model Inference Cost Governor (Zero External Dependencies)
Routes agent tasks across model tiers to minimize cloud inference expenditure under strict budgets.
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional

MODEL_PRICING_PER_1M_TOKENS = {
    "FLASH_LITE": {"input_usd": 0.075, "output_usd": 0.30, "latency_ms": 180},
    "FLASH_STANDARD": {"input_usd": 0.30, "output_usd": 1.20, "latency_ms": 420},
    "PRO_DEEP_REASONING": {"input_usd": 2.50, "output_usd": 10.00, "latency_ms": 1850}
}

class EnterpriseCloudFinOpsInferenceCostGovernor:
    def __init__(self):
        self.tenant_ledger: Dict[str, Dict[str, Any]] = {}

    def route_and_govern_inference(
        self,
        tenant_id: str,
        task_complexity: str = "STANDARD_WORKFLOW",
        estimated_input_tokens: int = 2000,
        estimated_output_tokens: int = 800,
        daily_budget_usd: float = 50.0
    ) -> Dict[str, Any]:
        """
        Determines optimal model tier based on complexity and remaining tenant budget.
        Automatically downgrades tier if tenant exceeds 85% soft budget cap.
        """
        if tenant_id not in self.tenant_ledger:
            self.tenant_ledger[tenant_id] = {
                "tenant_id": tenant_id,
                "accumulated_spend_usd": 0.0,
                "total_requests": 0,
                "downgraded_requests": 0
            }

        ledger = self.tenant_ledger[tenant_id]
        budget_utilization = ledger["accumulated_spend_usd"] / max(0.01, daily_budget_usd)

        # Ideal tier mapping
        comp = task_complexity.upper()
        if comp == "SIMPLE_LOOKUP":
            ideal_tier = "FLASH_LITE"
        elif comp == "DEEP_ARCHITECTURAL_REASONING":
            ideal_tier = "PRO_DEEP_REASONING"
        else:
            ideal_tier = "FLASH_STANDARD"

        # FinOps circuit breaker / automatic tier cascading
        selected_tier = ideal_tier
        policy_action = "IDEAL_TIER_APPROVED"

        if budget_utilization >= 1.0:
            selected_tier = "FLASH_LITE"
            policy_action = "HARD_CAP_ENFORCED_EMERGENCY_LITE_ONLY"
            ledger["downgraded_requests"] += 1
        elif budget_utilization >= 0.85 and ideal_tier == "PRO_DEEP_REASONING":
            selected_tier = "FLASH_STANDARD"
            policy_action = "SOFT_CAP_85PCT_AUTO_DOWNGRADED_TO_FLASH"
            ledger["downgraded_requests"] += 1

        pricing = MODEL_PRICING_PER_1M_TOKENS[selected_tier]
        call_cost = ((estimated_input_tokens / 1_000_000.0) * pricing["input_usd"]) + (
            (estimated_output_tokens / 1_000_000.0) * pricing["output_usd"]
        )

        # Calculate baseline Pro cost to measure FinOps savings
        pro_pricing = MODEL_PRICING_PER_1M_TOKENS["PRO_DEEP_REASONING"]
        unoptimized_pro_cost = ((estimated_input_tokens / 1_000_000.0) * pro_pricing["input_usd"]) + (
            (estimated_output_tokens / 1_000_000.0) * pro_pricing["output_usd"]
        )
        cost_saved_usd = max(0.0, unoptimized_pro_cost - call_cost)

        ledger["accumulated_spend_usd"] = round(ledger["accumulated_spend_usd"] + call_cost, 6)
        ledger["total_requests"] += 1

        return {
            "tenant_id": tenant_id,
            "task_complexity": comp,
            "ideal_model_tier": ideal_tier,
            "routed_model_tier": selected_tier,
            "finops_policy_action": policy_action,
            "estimated_call_cost_usd": round(call_cost, 6),
            "cost_saved_vs_pro_usd": round(cost_saved_usd, 6),
            "expected_latency_ms": pricing["latency_ms"],
            "tenant_accumulated_spend_usd": ledger["accumulated_spend_usd"],
            "budget_utilization_pct": round((ledger["accumulated_spend_usd"] / max(0.01, daily_budget_usd)) * 100.0, 2)
        }

    def get_tenant_finops_report(self, tenant_id: str) -> Dict[str, Any]:
        return self.tenant_ledger.get(tenant_id, {"error": "Tenant not found"})
