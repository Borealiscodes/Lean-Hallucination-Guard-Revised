# ==========================================================================
# MODULE: geometry.py (Lean-Hallucination-Guard-Revised Engine)
# PROJECT: Borealiscodes / Lean-Hallucination-Guard-Revised
# PURPOSE: FFI Marshalling Orchestrator. Coordinates continuous state vectors
#          across the CAUSA metric core and the compiled Coq .so enclave.
# ==========================================================================

import ctypes
import os
import numpy as np
from causa import directional_ownership, DirectionalConfig

# --------------------------------------------------------------------------
# C-ABI INTERFACE LINKING (Coq Enclave Object Binaries)
# --------------------------------------------------------------------------
SO_PATH = os.path.abspath("./libchguard_enclave.so")

class CoqEnclaveBridge:
    def __init__(self):
        if not os.path.exists(SO_PATH):
            raise FileNotFoundError(
                f"🚨 [CRITICAL FFI ERROR]: Compiled artifact {SO_PATH} missing. "
                "Run 'make' to generate libchguard_enclave.so first."
            )
        self.lib = ctypes.CDLL(SO_PATH)
        
        # Configure register-aligned C-ABI input type structures
        self.lib.chguard_enclave_init.argtypes = []
        self.lib.chguard_enclave_init.restype = None
        
        self.lib.c_pack_list.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t]
        self.lib.c_pack_list.restype = ctypes.c_int64
        
        self.lib.c_audit_ledger_epoch.argtypes = [ctypes.c_int64, ctypes.c_int64]
        self.lib.c_audit_ledger_epoch.restype = ctypes.c_int32
        
        # Fire the embedded OCaml runtime state initialization sequence
        self.lib.chguard_enclave_init()

    def verify_ternary_ledger_bounds(self, trits: list[int], max_drift: int) -> bool:
        """
        Pipes raw telemetry lists down to Coq list-induction bijections
        and verifies the Z3 modular parity safety rings.
        """
        c_array = (ctypes.c_int64 * len(trits))(*trits)
        packed_scalar = self.lib.c_pack_list(c_array, len(trits))
        
        # Evaluate allostatic collapse boundaries over the compiled ledger
        status = self.lib.c_audit_ledger_epoch(packed_scalar, max_drift)
        return status == 0x00  # Returns True if compliance is met cleanly

# --------------------------------------------------------------------------
# HIGH-DIMENSIONAL SUPERVISOR CLASS
# --------------------------------------------------------------------------
class ManifoldGeometrySupervisor:
    def __init__(self, drift_ceiling_num: int = 1000):
        self.bridge = CoqEnclaveBridge()
        self.causa_config = DirectionalConfig(floor=0.25, surprise_floor=0.38)
        self.drift_max = drift_ceiling_num

    def evaluate_trajectory_step(
        self,
        state_before: list[float],
        state_predicted: list[float],
        state_after: list[float],
        telemetry_trits: list[int]
    ) -> bool:
        """
        Executes a dual-layer causal and geometric verification check:
        1. Employs CAUSA directional ownership to expose Semantic Mimicry.
        2. Leverages Coq inductive proofs to verify bit-exact structural alignment.
        """
        # Step 1: Execute CAUSA Causal Agency evaluation
        causal_result = directional_ownership(
            state_before=state_before,
            state_predicted=state_predicted,
            state_after=state_after,
            config=self.causa_config
        )
        
        # If the causal tracking link falls below chance or is undefined, drop immediately
        if not causal_result.defined or causal_result.score < 0.40:
            return False

        # Step 2: Validate the telemetry bitstream through our Coq FFI layer
        return self.bridge.verify_ternary_ledger_bounds(telemetry_trits, self.drift_max)
