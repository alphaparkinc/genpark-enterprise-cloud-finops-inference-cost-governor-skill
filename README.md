# genpark-enterprise-cloud-finops-inference-cost-governor-skill

[![GenPark AI](https://img.shields.io/badge/GenPark_AI-www.genpark.ai-blue.svg)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark_Company_92955550-0077B5.svg)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Enterprise Cloud FinOps & Multi-Model LLM Inference Cost Governor. Monitors tenant token burn rates across Tencent Cloud and multi-model runtimes, routes queries across Flash-Lite, Flash, and Pro reasoning tiers based on task complexity and budget ceilings, and enforces automated cost circuit breakers.

---

## 🌐 Official GenPark AI Ecosystem Links

- **GenPark Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Official Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) ([https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550))

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
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

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License & Community

Licensed under the [MIT License](LICENSE). Copyright © 2026 [GenPark AI](https://www.genpark.ai).
Follow us on LinkedIn: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) | [https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550)
