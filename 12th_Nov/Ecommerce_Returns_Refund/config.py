
import os

from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from agent_framework.foundry import FoundryChatClient


load_dotenv()


def create_foundry_client():

    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model = os.getenv("FOUNDRY_MODEL")

    if not endpoint or not model:
        raise ValueError(
            "Missing Foundry configuration. "
            "Check FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL."
        )

    credential = AzureCliCredential()

    client = FoundryChatClient(
        project_endpoint=endpoint,
        model=model,
        credential=credential
    )

    return client
