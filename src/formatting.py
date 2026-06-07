from __future__ import annotations
import math
from typing import Any
from src.config import STAGE_LABELS, SEX_LABELS

def fmt_num(value: Any, digits: int = 3, suffix: str = "") -> str:
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return "N/A"
        return f"{float(value):,.{digits}f}{suffix}"
    except Exception:
        return str(value)

def fmt_pp(value: Any, digits: int = 2) -> str:
    return fmt_num(value, digits, " pp")

def fmt_pct(value: Any, digits: int = 1) -> str:
    return fmt_num(value, digits, "%")

def clean_label(value: Any) -> str:
    if value is None:
        return "N/A"
    s = str(value).replace("_", " ").strip()
    if s.lower() in STAGE_LABELS:
        return STAGE_LABELS[s.lower()]
    if s.lower() in SEX_LABELS:
        return SEX_LABELS[s.lower()]
    return s.title()

def status_text(ok: bool) -> str:
    return "Pass" if ok else "Missing"
