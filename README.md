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
git clone https://github.com/sebkuepers/zkproof_slack
cd zkproof_slack
crewai install
```

4. You need to create a `.env` file in the root directory with the following environment variables:

```python
SLACK_BOT_TOKEN=your_slack_bot_token
OPENAI_API_KEY=your_openai_api_key
```

5. you need to create a slack app and add it to the channel you want to post to.

- Create a Slack App:
	- Go to https://api.slack.com/apps and click “Create New App”.
	- Choose “From scratch” and give it a name and select a workspace where you have permission to install apps.
- Configure Bot User and Scopes:
	- In the app configuration, go to “Basic Information” → “Add features and functionality” and enable a Bot User if not already created.
	- Navigate to “OAuth & Permissions” and add the required scopes under “Bot Token Scopes”. At minimum, add chat:write to let the bot post messages. If you need to read channel history or other features, add those scopes as well.
- Install the App to Your Workspace:
	- In “OAuth & Permissions”, click “Install App to Workspace” and authorize the requested permissions.
	- Once installed, Slack will provide you with a “Bot User OAuth Token”. This is your SLACK_BOT_TOKEN.
-Invite the Bot to Your Channel:
	- In Slack, go to the channel where you want to post messages and invite the bot by typing: `/invite @<your_slack_app>`

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

This proof-of-concept lays out a foundational pattern for privacy-preserving delegation, combining zero-knowledge proofs with a Slack integration. Despite successfully demonstrating the concept, it remains a simplified model with several notable limitations:

### Credential Representation:
The current “credential” is just a JSON entry mapping a public_value to actions. In a production environment, these credentials would be formal Verifiable Credentials (VCs), signed by a trusted issuer’s DID key. Such credentials, stored off-chain, would provide authenticity, integrity, and interoperability, enabling verifiers to cryptographically confirm who issued them.

### DID Integration and Verification:
DIDs in this PoC are simple strings without actual resolution. A real system would leverage decentralized identity frameworks and DID resolvers to verify issuer DIDs and associated public keys. This DID infrastructure would generally run off-chain, while references to DID documents or VC registries might be anchored on-chain for tamper-resistant transparency.

### ZK Proof Generation and Verification:
We currently rely on manual scripting and Dockerized ZoKrates commands. A production system could:
- Automate these steps as services, allowing agents to autonomously produce and verify proofs.
- Potentially store verification keys or credential commitments on-chain, so that anyone can verify proofs without centralized trust.
- Keep secret credentials and heavy computation off-chain, thus preserving privacy and reducing costs. The proofs themselves, however, can be verified against on-chain references (like Merkle roots or cryptographic commitments) that ensure credentials haven’t been revoked or modified.

### Revocation and Lifecycle Management:
No revocation logic exists in this PoC. In a real-world scenario:
- On-chain data structures (e.g., Merkle trees, accumulators) could store commitments to valid credentials.
- Revocation updates would be published on-chain, ensuring a global, tamper-proof state of which credentials remain valid.
- Agents would produce ZK proofs referencing these on-chain commitments, while all sensitive logic (like handling the user’s secret) stays off-chain.

### Scalability and Interoperability:
While our PoC is minimal, a full production architecture would consider:
- On-chain anchoring of verification keys or credential state for global verifiability.
- Off-chain services or microservices automating proof generation and verification requests.
- Standardized credential formats and DID methods enabling interoperability with other decentralized identity and authorization systems.

### On-Chain vs. Off-Chain Summary:
- On-Chain:
	- Anchoring verification keys or Merkle roots of valid credentials.
	- Storing cryptographic commitments or references for revocation and credential state, ensuring tamper resistance.
- Off-Chain:
	- Holding secret credentials privately.
	- Running heavy computations for generating and verifying proofs.
	- Managing the full DID resolution process and retrieving Verifiable Credentials.
	- Interacting with Slack and other external services.

### In Summary:
This PoC provides a glimpse of how zero-knowledge proofs, decentralized identity, and service integrations (like Slack) can come together to create a privacy-preserving, trust-minimized delegation system. Moving to a production-ready architecture would involve integrating robust DID frameworks, verifiable credential standards, revocation mechanisms, and carefully dividing on-chain and off-chain responsibilities to achieve both integrity and efficiency. Such a system would scale to more complex use cases, ensuring that only properly authorized entities carry out delegated tasks without sacrificing user privacy or security.

