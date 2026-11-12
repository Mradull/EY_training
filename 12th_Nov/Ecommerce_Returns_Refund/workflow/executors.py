
from dataclasses import dataclass
from typing import Never

from agent_framework import (
    Executor,
    WorkflowContext,
    handler,
    response_handler,
)

from policy import (
    evaluate_eligibility,
    evaluate_risk,
    evaluate_automatic_approval,
)

from agents.eligibility_agent import run_eligibility_agent
from agents.risk_agent import run_risk_agent
from agents.customer_response_agent import (
    run_customer_response_agent,
)


# =====================================================
# MANAGER APPROVAL REQUEST
# =====================================================

@dataclass
class ManagerApprovalRequest:
    request_id: str
    details: dict
    eligibility: dict
    eligibility_explanation: str
    risk: dict


# =====================================================
# 1. ELIGIBILITY EXECUTOR
# =====================================================

class EligibilityExecutor(Executor):

    def __init__(self, agent):
        super().__init__(id="eligibility_executor")
        self.agent = agent

    @handler
    async def process(
        self,
        request: dict,
        ctx: WorkflowContext[dict, dict],
    ) -> None:

        print(f"\n[Eligibility] Processing {request['request_id']}")

        policy_result = evaluate_eligibility(request)

        explanation = await run_eligibility_agent(
            self.agent,
            request,
            policy_result,
        )

        state = {
            "request": request,
            "eligibility": policy_result,
            "eligibility_explanation": explanation,
        }

        await ctx.send_message(state)


# =====================================================
# 2. RISK EXECUTOR
# =====================================================

class RiskExecutor(Executor):

    def __init__(self, agent):
        super().__init__(id="risk_executor")
        self.agent = agent

    @handler
    async def process(
        self,
        state: dict,
        ctx: WorkflowContext[dict, dict],
    ) -> None:

        request = state["request"]

        print(f"[Risk] Assessing {request['request_id']}")

        risk_result = evaluate_risk(request)

        risk_result = await run_risk_agent(
            self.agent,
            request,
            risk_result,
        )

        state["risk"] = risk_result

        await ctx.send_message(state)


# =====================================================
# 3. APPROVAL GATEWAY
# =====================================================

class ApprovalGatewayExecutor(Executor):

    def __init__(self):
        super().__init__(id="approval_gateway")

    @handler
    async def process(
        self,
        state: dict,
        ctx: WorkflowContext[dict, dict],
    ) -> None:

        eligibility = state["eligibility"]
        risk = state["risk"]

        automatic = evaluate_automatic_approval(
            eligibility,
            risk,
        )

        if automatic:

            state["approval_route"] = "AUTOMATIC"
            state["final_decision"] = "AUTO_APPROVED"

            print(
                f"[Approval] {state['request']['request_id']} "
                "automatically approved."
            )

            await ctx.send_message(state)

        else:

            print(
                f"[Approval] Manager review required for "
                f"{state['request']['request_id']}."
            )

            approval_request = ManagerApprovalRequest(
                request_id=state["request"]["request_id"],
                details=state["request"],
                eligibility=eligibility,
                eligibility_explanation=state["eligibility_explanation"],
                risk=risk,
            )

            await ctx.request_info(
                request_data=approval_request,
                response_type=str,
                request_id=f"manager_{approval_request.request_id}",
            )

    @response_handler
    async def handle_manager_response(
        self,
        original_request: ManagerApprovalRequest,
        response: str,
        ctx: WorkflowContext[dict, dict],
    ) -> None:

        decision = response.strip().lower()

        # The main program validates this before resuming.
        if decision not in ("approve", "reject"):
            raise ValueError("Manager response must be approve or reject.")

        state = {
            "request": original_request.details,
            "eligibility": original_request.eligibility,
            "eligibility_explanation": original_request.eligibility_explanation,
            "risk": original_request.risk,
            "approval_route": "MANAGER_REVIEW",
        }

        if decision == "approve":
            state["final_decision"] = "MANAGER_APPROVED"
        else:
            state["final_decision"] = "MANAGER_REJECTED"

        print(
            f"[Approval] Manager decision for "
            f"{original_request.request_id}: {decision.upper()}"
        )

        await ctx.send_message(state)


# =====================================================
# 4. CUSTOMER RESPONSE EXECUTOR
# =====================================================

class CustomerResponseExecutor(Executor):

    def __init__(self, agent):
        super().__init__(id="customer_response_executor")
        self.agent = agent

    @handler
    async def process(
        self,
        state: dict,
        ctx: WorkflowContext[Never, dict],
    ) -> None:

        print(
            f"[Customer Response] Drafting message for "
            f"{state['request']['request_id']}"
        )

        customer_message = await run_customer_response_agent(
            self.agent,
            state["request"],
            state["final_decision"],
            state["eligibility"],
            state["risk"],
        )

        result = {
            "request_id": state["request"]["request_id"],
            "order_id": state["request"]["order_id"],
            "product": state["request"]["product"],
            "amount_inr": state["request"]["amount_inr"],
            "eligibility_findings": state["eligibility"],
            "eligibility_explanation": state["eligibility_explanation"]
                if "eligibility_explanation" in state
                else None,
            "risk_assessment": state["risk"],
            "approval_route": state["approval_route"],
            "final_decision": state["final_decision"],
            "customer_message": customer_message,
        }

        await ctx.yield_output(result)
