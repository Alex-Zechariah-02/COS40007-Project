from __future__ import annotations
from pathlib import Path
from typing import Optional, Iterable
import json
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data(show_spinner=False)
def load_json(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def file_exists(path: str | Path) -> bool:
    return Path(path).exists()

def load_first_existing(paths: Iterable[str | Path]) -> tuple[pd.DataFrame, Optional[Path]]:
    for p in paths:
        p = Path(p)
        if p.exists():
            return load_csv(str(p)), p
    return pd.DataFrame(), None

def safe_head(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    return df.head(n)

def list_pngs(directory: str | Path):
    directory = Path(directory)
    if not directory.exists():
        return []
    return sorted(directory.glob("*.png"))

def get_column(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    lookup = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        key = cand.lower().strip()
        if key in lookup:
            return lookup[key]
    return None
