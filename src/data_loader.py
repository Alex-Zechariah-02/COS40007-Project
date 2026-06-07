from __future__ import annotations

from pathlib import Path
import json
import pandas as pd
import streamlit as st
from .config import CHECKS_DIR, TABLES_DIR, ARTIFACTS_DIR, RAW_DATA_DIR, SVR_FIGURES_DIR, SVR_MODELS_DIR, DATA_DIR


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_csv_cached(path_str: str) -> pd.DataFrame:
    path = Path(path_str)
    if not path.exists():
        return pd.DataFrame()
    try:
        return _read_csv(path)
    except Exception as exc:
        return pd.DataFrame({"load_error": [str(exc)], "path": [str(path)]})


@st.cache_data(show_spinner=False)
def load_json_cached(path_str: str) -> dict:
    path = Path(path_str)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"load_error": str(exc), "path": str(path)}


def table_path(name: str) -> Path:
    p = TABLES_DIR / name
    if p.exists():
        return p
    return CHECKS_DIR / name


def artifact_path(name: str) -> Path:
    return ARTIFACTS_DIR / name


def figure_path(filename: str) -> Path:
    return SVR_FIGURES_DIR / filename


def raw_path(filename: str) -> Path:
    return RAW_DATA_DIR / filename


def model_path(filename: str) -> Path:
    return SVR_MODELS_DIR / filename


def load_table(name: str) -> pd.DataFrame:
    return load_csv_cached(str(table_path(name)))


def load_check(name: str) -> pd.DataFrame:
    return load_csv_cached(str(CHECKS_DIR / name))


def load_raw(name: str) -> pd.DataFrame:
    return load_csv_cached(str(raw_path(name)))


def load_artifact_json(name: str) -> dict:
    return load_json_cached(str(artifact_path(name)))


def file_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def list_files(directory: Path, suffix: str | None = None) -> list[Path]:
    if not directory.exists():
        return []
    files = [p for p in directory.iterdir() if p.is_file()]
    if suffix:
        files = [p for p in files if p.suffix.lower() == suffix.lower()]
    return sorted(files, key=lambda p: p.name.lower())


def folder_inventory() -> pd.DataFrame:
    rows = []
    for label, directory in [("checks", CHECKS_DIR), ("tables", TABLES_DIR), ("artifacts", ARTIFACTS_DIR), ("raw", RAW_DATA_DIR), ("figures_svr", SVR_FIGURES_DIR), ("models_svr", SVR_MODELS_DIR)]:
        files = list_files(directory)
        rows.append({
            "folder": label,
            "path": str(directory.relative_to(DATA_DIR.parent)),
            "file_count": len(files),
            "total_size_kb": round(sum(f.stat().st_size for f in files) / 1024, 2),
            "exists": directory.exists(),
        })
    return pd.DataFrame(rows)
