import os
import subprocess
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackPostToolInput(BaseModel):
    """Input schema for SlackPostTool."""
    channel: str = Field(..., description="The Slack channel (e.g. #general) or channel ID to post to.")
    message: str = Field(..., description="The message text to post to Slack.")

class SlackPostTool(BaseTool):
    name: str = "slack_post_tool"
    description: str = (
        "Use this tool to post a message to a Slack channel. "
        "You must provide a channel and a message. "
        "Make sure the bot user is properly installed in the workspace and invited to the channel if needed."
        "Before posting, the tool will verify a proof (proof.json) with verification.key to ensure authorization."
    )
    args_schema: Type[BaseModel] = SlackPostToolInput

    def _verify_proof(self) -> bool:
        """
        Run 'zokrates verify' inside Docker to verify the proof before posting.
        Returns True if verification succeeds, False otherwise.
        """

        # Determine the path to the files directory
        base_dir = os.path.dirname(__file__)
        files_dir = os.path.abspath(os.path.join(base_dir, "../../../files"))

        proof_file = os.path.join(files_dir, "proof.json")
        verification_key = os.path.join(files_dir, "verification.key")

        if not (os.path.exists(proof_file) and os.path.exists(verification_key)):
            # If we don't have proof.json or verification.key, we cannot verify.
            print("Proof or verification key not found, cannot verify proof.")
            return False

        # Run 'zokrates verify' in Docker
        docker_image = "zokrates/zokrates"
        docker_cmd = [
            "docker", "run", "--rm",
            "--platform=linux/amd64",
            "-v", f"{files_dir}:/home/zokrates/code",
            "-w", "/home/zokrates/code",
            docker_image,
            "zokrates", "verify"
        ]

        print("Verifying proof...")
        result = subprocess.run(docker_cmd, capture_output=True, text=True)

        if result.returncode == 0 and "PASSED" in result.stdout:
            print("Proof verification succeeded.")
            return True
        else:
            print("Proof verification failed.")
            print("Output:", result.stdout, result.stderr)
            return False

    def _run(self, channel: str, message: str) -> str:
        # Verify the proof before posting
        if not self._verify_proof():
            return "Error: Proof verification failed. Cannot post to Slack."

        # Get the Slack Bot token from environment variables
        slack_token = os.environ.get("SLACK_BOT_TOKEN")
        if not slack_token:
            return "Error: SLACK_BOT_TOKEN not found in environment variables."

        client = WebClient(token=slack_token)

        try:
            response = client.chat_postMessage(channel=channel, text=message)
            if response["ok"]:
                return f"Message posted successfully to {channel}: {message}"
            else:
                return f"Failed to post message: {response['error']}"
        except SlackApiError as e:
            return f"Slack API Error: {e.response['error']}"