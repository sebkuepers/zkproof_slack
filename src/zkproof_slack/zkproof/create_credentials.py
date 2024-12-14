import json
import os

# -------------------------------------------------------------------
# This script simulates the process of creating a delegation credential.
#
# In a future scenario, the user (represented by a DID) would:
# 1. Dynamically compute a 'public_value' (e.g. a poseidon hash of a secret)
#    that will serve as a cryptographic commitment to certain permissions.
# 2. Sign and issue a credential stating that a given Writer Agent DID is allowed
#    to instruct a Slack Agent DID to post on Slack, referencing this 'public_value'.
#
# For this proof-of-concept (PoC), we skip the complexity of computing 'public_value'
# dynamically with ZoKrates. Instead, we:
# - Hardcode a 'secret_credential' and a corresponding 'public_value' (a placeholder).
# - Store these in files and a JSON credential store.
#
# Later steps in the PoC will:
# - Use this 'public_value' during zero-knowledge proof generation and verification.
# - Prove that the holder of 'secret_credential' is authorized to request Slack posting.
#
# By hardcoding these values, we focus on demonstrating the overall system
# (DID-based delegation, ZK proofs, and Slack posting) without getting stuck on
# dynamic hash extraction issues.
#
# Files created:
# - secret_credential.txt: The chosen secret credential (private).
# - public_value.txt: The chosen public value (placeholder hash).
# - credentials.json: A record mapping 'public_value' to delegated permissions.
#
# After running this script:
# - The credential issuance step is simulated.
# - Other parts of the PoC can rely on these stored values.
# -------------------------------------------------------------------

# Determine the path to the 'files' directory relative to this script.
base_dir = os.path.dirname(__file__)
files_dir = os.path.abspath(os.path.join(base_dir, "../../../files"))

# Example DIDs for demonstration (in a real scenario, these come from a DID registry)
USER_DID = "did:user:123"
WRITER_AGENT_DID = "did:agent:writer456"
SLACK_AGENT_DID = "did:agent:slack789"

# Hardcoded values for the proof-of-concept:
# The secret_credential might represent a private key or secret the Writer Agent holds.
# The public_value would normally be a poseidon hash computed via ZoKrates or another tool.
# Here, we manually compute the poseidon hash of the secret_credential to keep things simple.
secret_credential = 12345
public_value = 4267533774488295900887461483015112262021273608761099826938271132511348470966  # Manually computed poseidon hash of secret_credential

# Path to the JSON credentials file
credentials_file = os.path.join(files_dir, "credentials.json")

# Ensure credentials.json exists
if not os.path.exists(credentials_file):
    with open(credentials_file, "w") as f:
        json.dump({}, f)

# Load existing credentials
with open(credentials_file, "r") as f:
    creds = json.load(f)

# Assign a pseudonymous token identifier that the Slack Agent will later use
# to determine which Slack token to use. This avoids revealing user identity directly.
token_identifier = "tokenA"

# Store a record in credentials.json that ties the public_value to a Slack posting permission.
# In reality, this would be a verifiable credential signed by the USER_DID, stating:
# "WriterAgent can instruct SlackAgent to post on Slack, evidenced by public_value."
creds[str(public_value)] = {
    "action": "slack_post",
    "token_identifier": token_identifier,
    "issuer_did": USER_DID,
    "subject_did": WRITER_AGENT_DID,
    "target_did": SLACK_AGENT_DID
}

# Write updated credentials back to credentials.json
with open(credentials_file, "w") as f:
    json.dump(creds, f, indent=2)

# Write out the secret_credential and public_value to files for other parts of the PoC to access.
with open(os.path.join(files_dir, "secret_credential.txt"), "w") as f:
    f.write(str(secret_credential))

with open(os.path.join(files_dir, "public_value.txt"), "w") as f:
    f.write(str(public_value))

# Print a summary of what we've done
print("Credential created with hardcoded values:")
print(f"secret_credential: {secret_credential}")
print(f"public_value: {public_value}")
print("action: slack_post, token_identifier:", token_identifier)
print("Issuer:", USER_DID, "Subject:", WRITER_AGENT_DID, "Target:", SLACK_AGENT_DID)
print("Stored in credentials.json")
print("This simulates the user's issuance of a delegation credential without dynamic hashing.")