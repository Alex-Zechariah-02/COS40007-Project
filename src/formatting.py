import pandas as pd


def fmt_num(value, decimals=2):
    try:
        if pd.isna(value):
            return "N/A"
        return f"{float(value):,.{decimals}f}"
    except Exception:
        return str(value)


def fmt_pp(value, decimals=2):
    try:
        if pd.isna(value):
            return "N/A"
        return f"{float(value):,.{decimals}f} pp"
    except Exception:
        return str(value)


def fmt_pct(value, decimals=1):
    try:
        if pd.isna(value):
            return "N/A"
        return f"{float(value):,.{decimals}f}%"
    except Exception:
        return str(value)


def fmt_r2(value):
    return fmt_num(value, 3)


def humanize_name(name: str) -> str:
    return str(name).replace("_", " ").replace("-", " ").title()


def format_stage(stage: str) -> str:
    mapping = {"primary": "Primary", "secondary_lower": "Secondary Lower", "secondary_upper": "Secondary Upper"}
    return mapping.get(str(stage), humanize_name(stage))


def format_sex(sex: str) -> str:
    mapping = {"male": "Male", "female": "Female", "both": "Both"}
    return mapping.get(str(sex), humanize_name(sex))
