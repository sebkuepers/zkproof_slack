import os
import sys
import subprocess

# -------------------------------------------------------------------
# This script automates the ZoKrates proof generation steps.
#
# It:
# 1. Reads secret_credential and public_value from files (created by create_credential.py).
# 2. Runs ZoKrates commands via Docker:
#    - compile the circuit (poseidon_hash_check.zok)
#    - setup (trusted setup)
#    - compute-witness with the given secret_credential and public_value
#    - generate-proof to produce proof.json and related keys
#
# After this script:
# - proof.json, verification.key, proving.key, and witness will be in the files directory.
# - These artifacts can be used later to verify the proof and integrate with the Slack posting logic.
#
# Note: We assume the ZoKrates version being used doesn't provide 'simulate' or 'run' to show outputs.
# For the PoC, we trust this workflow is enough to demonstrate ZK proof generation.
# -------------------------------------------------------------------

base_dir = os.path.dirname(__file__)
files_dir = os.path.abspath(os.path.join(base_dir, "../../../files"))

secret_file = os.path.join(files_dir, "secret_credential.txt")
public_file = os.path.join(files_dir, "public_value.txt")
zok_file = os.path.join(files_dir, "poseidon_hash_check.zok")

if not (os.path.exists(secret_file) and os.path.exists(public_file) and os.path.exists(zok_file)):
    print("Missing required files. Ensure secret_credential.txt, public_value.txt, and poseidon_hash_check.zok exist.")
    sys.exit(1)

with open(secret_file, "r") as f:
    secret_credential = f.read().strip()

with open(public_file, "r") as f:
    public_value = f.read().strip()

# Docker image for ZoKrates
docker_image = "zokrates/zokrates"

# We'll mount the files directory and work from there.
docker_base = [
    "docker", "run", "--rm",
    "--platform=linux/amd64",
    "-v", f"{files_dir}:/home/zokrates/code",
    "-w", "/home/zokrates/code",
    docker_image,
    "zokrates"
]

# 1. Compile the circuit
compile_cmd = docker_base + ["compile", "-i", "poseidon_hash_check.zok", "-o", "poseidon_hash_check.out"]
print("Compiling circuit...")
subprocess.run(compile_cmd, check=True)

# 2. Setup (trusted setup phase)
setup_cmd = docker_base + ["setup", "-i", "poseidon_hash_check.out"]
print("Performing setup...")
subprocess.run(setup_cmd, check=True)

# 3. Compute witness
# Provide secret_credential and public_value as arguments
witness_cmd = docker_base + ["compute-witness", "-i", "poseidon_hash_check.out", "-a", secret_credential, public_value]
print("Computing witness...")
subprocess.run(witness_cmd, check=True)

# 4. Generate proof
proof_cmd = docker_base + ["generate-proof", "-i", "poseidon_hash_check.out"]
print("Generating proof...")
subprocess.run(proof_cmd, check=True)

print("Proof generation completed!")
print("Check the files directory for proof.json, witness, proving.key, and verification.key.")
print("Next steps: use these artifacts to verify the proof and integrate with Slack posting.")