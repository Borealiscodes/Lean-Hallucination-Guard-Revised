# ==========================================================================
# MODULE: test_lhguard_core.py (Enclave Stress-Test Harness)
# PROJECT: Borealiscodes / Lean-Hallucination-Guard-Revised
# PURPOSE: Formally verify the Python-to-Coq/Julia FFI boundaries.
#          Simulates adversarial metric drift and semantic mimicry to 
#          falsify or validate the 0x0F stasis shutdown sequence.
# ==========================================================================

import os
import subprocess
import pytest
import numpy as np
from lhguard.geometry import ManifoldGeometrySupervisor
from lhguard.interceptor import InterceptorGatekeeper

# --------------------------------------------------------------------------
# FIXTURES & SYSTEM PRECONDITION VERIFICATION
# --------------------------------------------------------------------------
@pytest.fixture(scope="module")
def verify_enclave_binary():
    """ Ensures the Coq compiled shared object exists before running harness """
    so_path = "./libchguard_enclave.so"
    if not os.path.exists(so_path):
        pytest.skip(
            "⚠️ [TEST BYPASS]: libchguard_enclave.so not found. "
            "Please run 'make coq_compile' and build the .so library first."
        )
    return so_path

# --------------------------------------------------------------------------
# CORE ENFORCEMENT TRIAD VALIDATION TESTS
# --------------------------------------------------------------------------

def test_nominal_stable_trajectory(verify_enclave_binary):
    """
    Validates that a geometrically stable, causally aligned step trajectory
    passes through both CAUSA and the Coq inductive codec without triggering blocks.
    """
    supervisor = ManifoldGeometrySupervisor(drift_ceiling_num=1000)
    
    # Nominal, highly congruent state transitions (Prediction matches Outcome)
    state_before = [0.10, 0.20, 0.50]
    state_predicted = [0.40, 0.20, 0.60]
    state_after = [0.39, 0.21, 0.59]
    
    # Compliant 15-trit metadata telemetry bitstream satisfying Z3 parity ring
    # Sum(t_i + 1) = 15, which is 0 mod 3
    valid_parity_trits = [0] * 15 
    
    passed = supervisor.evaluate_trajectory_step(
        state_before=state_before,
        state_predicted=state_predicted,
        state_after=state_after,
        telemetry_trits=valid_parity_trits
    )
    
    assert passed is True, "❌ [FAILURE]: Nominal stable trajectory rejected by supervisor."


def test_semantic_mimicry_causa_rejection(verify_enclave_binary):
    """
    Validates that if an LLM generates a proof state that looks structurally correct
    but its internal states are completely decoupled (Illusion of Agency),
    CAUSA flags the semantic mimicry and blocks the trajectory step.
    """
    supervisor = ManifoldGeometrySupervisor(drift_ceiling_num=1000)
    
    # Decoupled state transition: The actual outcome moves opposite to predicted intention
    state_before = [0.10, 0.20, 0.50]
    state_predicted = [0.90, 0.80, 0.95]
    state_after = [0.05, 0.10, 0.40] # Catastrophic reverse drift
    
    valid_parity_trits = [0] * 15
    
    passed = supervisor.evaluate_trajectory_step(
        state_before=state_before,
        state_predicted=state_predicted,
        state_after=state_after,
        telemetry_trits=valid_parity_trits
    )
    
    assert passed is False, "❌ [FAILURE]: Supervisor failed to intercept severe Semantic Mimicry."


def test_interceptor_guillotine_isolation():
    """
    Validates that when accumulated drift energy breaches the Coq-proved 
    unconditional_epochal_guillotine threshold, the interceptor forcefully 
    halts execution with exit code 15 (0x0F), bypassing Python exceptions.
    """
    # Because a successful interceptor hit terminates the active process instantly via os._exit,
    # we must execute this test inside an isolated subprocess shell to capture the system return code.
    test_code = """
import sys
from lhguard.interceptor import InterceptorGatekeeper

gatekeeper = InterceptorGatekeeper(target_worker_id=3, max_ceiling=500)
# Inject a catastrophic drift integer breaching the 500 ceiling
gatekeeper.enforce_allostatic_limit(
    accumulated_drift=842, 
    failure_signature="Simulated Singular Value Condition Collapse"
)
print("ALIVE") # Should never be reached
sys.exit(0)
"""
    
    process = subprocess.run(
        ["python3", "-c", test_code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Assert that the sub-process return code is exactly our 0x0F stasis opcode (15)
    assert process.returncode == 15, (
        f"❌ [FAILURE]: Interceptor failed to drop the epochal guillotine safely. "
        f"Exit code observed: {process.returncode}, expected: 15."
    )
    
    # Verify that the standard process execution paths were cleanly bypassed
    assert "ALIVE" not in process.stdout
    assert "🚨 [ALLOSTATIC COLLAPSE TRIGGERED]" in process.stderr
    assert "0x0F" in process.stderr

