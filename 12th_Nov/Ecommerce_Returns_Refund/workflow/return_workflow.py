
from agent_framework import WorkflowBuilder

from workflow.executors import (
    EligibilityExecutor,
    RiskExecutor,
    ApprovalGatewayExecutor,
    CustomerResponseExecutor,
)


def build_return_workflow(agents):

    # Create workflow executors
    eligibility = EligibilityExecutor(
        agents["eligibility"]
    )

    risk = RiskExecutor(
        agents["risk"]
    )

    approval = ApprovalGatewayExecutor()

    customer_response = CustomerResponseExecutor(
        agents["customer_response"]
    )

    # Connect executors into a graph
    workflow = (
        WorkflowBuilder(start_executor=eligibility)
        .add_edge(eligibility, risk)
        .add_edge(risk, approval)
        .add_edge(approval, customer_response)
        .build()
    )

    return workflow
