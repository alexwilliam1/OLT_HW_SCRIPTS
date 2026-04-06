---
name: _ placeholder as safety fuse in OLT scripts
description: The _ in slot=_ / pon=_ is intentional to prevent accidental script execution
type: feedback
---

The `_` placeholders in `onu_modify_desc.py`, `onu_remove.py`, `onu_srv_port_vl.py` are intentional safety guards to force the operator to fill in parameters before running. Do not "fix" these as errors.

**Why:** Prevents accidental execution with wrong slot/pon values, which could impact production OLT equipment.
**How to apply:** When editing OLT scripts, keep the `_` pattern intact. Do not suggest replacing with defaults.
