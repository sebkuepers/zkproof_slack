# ZKProof Slack with CrewAI

## Introduction

This proof-of-concept (PoC) demonstrates a privacy-preserving delegation flow using Zero-Knowledge (ZK) proofs integrated with CrewAI to post to Slack. The scenario is that a user (identified by a DID) delegates certain actions—like posting messages to Slack—to an agent without revealing sensitive keys. Instead, the agent proves their authorization through a ZK proof generated and verified via ZoKrates.

To orchestrate the final step, we use CrewAI as a platform for building and running AI agents and their associated tools. We have developed a custom CrewAI tool that posts to Slack, but only after successfully verifying a ZK proof. This ensures that only a properly authorized agent, who can produce a valid proof, can trigger Slack postings.

We provide two Python scripts—one that simulates the creation of a simplified delegation credential (including a secret and its corresponding public value), and another that generates a zero-knowledge proof to confirm knowledge of the secret without revealing it. While these steps are shown as manual Python scripts for clarity, in a fully autonomous setup they would be carried out by AI agents themselves. The final stage involves a custom CrewAI tool that verifies the generated proof before allowing Slack posting actions, ensuring that only properly authorized parties can execute the delegated task.

## Installation Guide

1. You need to have crewai installed.

```bash
pip install crewai
```

2. You need to have the ZoKrates Docker image installed, which is being used to generate the ZK proofs and verify them.

```bash
docker pull zokrates/zokrates
```

3. You need to clone the repository and install the dependencies with CrewAI.

```bash
git clone https://github.com/crewai-ai/zkproof-slack.git
cd zkproof-slack
crewai install
```

4. You need to create a `.env` file in the root directory with the following environment variables:

```bash
SLACK_BOT_TOKEN=your_slack_bot_token
OPENAI_API_KEY=your_openai_api_key
```

5. you need to create a slack app and add it to the channel you want to post to.

	1.	Create a Slack App:
	•	Go to https://api.slack.com/apps and click “Create New App”.
	•	Choose “From scratch” and give it a name and select a workspace where you have permission to install apps.
	2.	Configure Bot User and Scopes:
	•	In the app configuration, go to “Basic Information” → “Add features and functionality” and enable a Bot User if not already created.
	•	Navigate to “OAuth & Permissions” and add the required scopes under “Bot Token Scopes”. At minimum, add chat:write to let the bot post messages. If you need to read channel history or other features, add those scopes as well.
	3.	Install the App to Your Workspace:
	•	In “OAuth & Permissions”, click “Install App to Workspace” and authorize the requested permissions.
	•	Once installed, Slack will provide you with a “Bot User OAuth Token”. This is your SLACK_BOT_TOKEN.
	4.	Invite the Bot to Your Channel:
	•	In Slack, go to the channel where you want to post messages and invite the bot by typing: `/invite @<your_slack_app>`

## How to run

1. In a first step you need to simulate the creation of a simplified delegation credential (including a secret and its corresponding public value) and the generation of a ZK proof.

```bash
python3 src/zkproof_slack/zkproof/create_credentials.py
```

This will create the files `secret_credential.txt` and `public_value.txt` in the `files` directory together with the credentials.json file, which contains the credential.

2. In a second step you need to generate a ZK proof to confirm knowledge of the secret without revealing it.

```bash
python3 src/zkproof_slack/zkproof/create_proof.py
```

This will create the files `proof.json` and `witness` in the `files` directory together with the verification.key and proving.key files, which contain the proof and witness.

3. In a third step you need to run the CrewAI agent to post to Slack.

```bash
crewai run
``` 

This will start the CrewAI agent and post to Slack. Take a look at the input in main.py to see how the agent is configured. For this to work you need to have added your Slack App to the channel before running the script.

## Closing Remarks

This proof-of-concept highlights how zero-knowledge proofs can enhance privacy and trust in delegated actions—like posting messages to Slack—without exposing sensitive credentials. By integrating DIDs, delegation credentials, and cryptographic proofs, we can enforce strong authorization policies while protecting user anonymity and data.

While this PoC uses a simplified setup—storing credentials in JSON, referencing a hardcoded public value, and relying on a single ZoKrates circuit—its principles can be extended to more complex and production-ready scenarios. Future iterations might incorporate real Verifiable Credentials, DID-based identity management, advanced revocation mechanisms, and broader interoperability with decentralized infrastructures.

With CrewAI’s tool-based architecture, it’s straightforward to integrate ZK proof verification into agent workflows, ensuring that only properly authorized agents execute sensitive tasks. As the ecosystem of DIDs, ZK tooling, and decentralized services matures, such patterns will become increasingly practical and powerful.

Thank you for exploring this PoC. We hope it provides insight into the potential of zero-knowledge proofs and decentralized identity solutions for secure, privacy-preserving automated workflows.

