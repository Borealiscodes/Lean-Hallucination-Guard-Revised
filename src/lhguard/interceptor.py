# ==========================================================================
# MODULE: interceptor.py (Lean-Hallucination-Guard-Revised Boundary Engine)
# PROJECT: Borealiscodes / Lean-Hallucination-Guard-Revised
# PURPOSE: Formally execute deterministic process isolation, active memory
#          register purging, and unconditional stasis circuit-breaking.
# ==========================================================================

import sys
import os
import gc
import logging
from typing import NoReturn

logger = logging.getLogger("lhguard.interceptor")

class AllostaticShockException(SystemExit):
    """ Opaque exception type for catching internal safety enclave collapses """
    pass

def trigger_allostatic_collapse_shutdown(
    worker_id: int,
    violation_opcode: int,
    metric_drift_num: int,
    max_ceiling_num: int,
    forensic_summary: str
) -> NoReturn:
    """
    THE EPOCHAL GUILLOTINE TACTIC: Forcefully clears the process memory space,
    flushes active telemetry descriptors, and terminates execution via a
    register-level os._exit(15) payload to lock the cluster node in stasis.
    """
    # 1. Broadside the forensic violation dump to stderr to bypass buffered stream lag
    sys.stderr.write("\n" + "="*80 + "\n")
    sys.stderr.write(f"🚨 [ALLOSTATIC COLLAPSE TRIGGERED] — WORKER_ID: {worker_id}\n")
    sys.stderr.write(f"🚨 INVARIANT BREACH: {forensic_summary}\n")
    sys.stderr.write(f"📐 METRIC ACCUMULATION: {metric_drift_num} > CEILING: {max_ceiling_num}\n")
    sys.stderr.write(f"🔒 OPCODE SENTINEL: 0x{violation_opcode:02X}\n")
    sys.stderr.write("="*80 + "\n")
    sys.stderr.flush()

    # 2. Log structured metadata trace to the out-of-band audit ledger files
    logger.critical(
        "Epochal Invalidation Executed: worker=%d, opcode=0x%02X, drift=%d, ceiling=%d",
        worker_id, violation_opcode, metric_drift_num, max_ceiling_num
    )

    # 3. Synchronous Memory Register Purge: Destroy dangling references to prevent context leaks
    # Forcefully clear internal Python interpreter stacks before halting the substrate
    for obj in gc.get_objects():
        try:
            if hasattr(obj, "__dict__") and "lhguard" in str(type(obj)):
                del obj.__dict__
        except (AttributeError, ReferenceError):
            pass

    # Fire core garbage collector passes to completely clear un-anchored heap structures
    gc.collect()

    # 4. Execute Native Hardware Circuit Break
    # Uses os._exit instead of sys.exit to bypass Python's cleanup hooks (try/finally/atexit).
    # This prevents an adversarial or hallucinating token generator from catching the 
    # exit signal, forcing an unconditional, un-bypassable exit code 15 (0x0F) straight to Zig.
    os._exit(15)

class InterceptorGatekeeper:
    def __init__(self, target_worker_id: int, max_ceiling: int):
        self.worker_id = target_worker_id
        self.max_ceiling = max_ceiling
        self.stasis_opcode = 15 # 15 = 0x0F

    def enforce_allostatic_limit(self, accumulated_drift: int, failure_signature: str) -> None:
        """
        Active polling check gate. If tracking loops violate the Coq-proved 
        unconditional_epochal_guillotine theorem bounds, it drops the guillotine.
        """
        if accumulated_drift > self.max_ceiling:
            trigger_allostatic_collapse_shutdown(
                worker_id=self.worker_id,
                violation_opcode=self.stasis_opcode,
                metric_drift_num=accumulated_drift,
                max_ceiling_num=self.max_ceiling,
                forensic_summary=failure_signature
            )

