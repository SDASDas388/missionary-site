"""记录每次新打开页面的访问，并把地址写入 data/visitors.json。

这个文件不进入 git。页面上只显示次数和人数，不显示地址。
"""

from __future__ import annotations

import json
import threading
from datetime import datetime
from pathlib import Path

import streamlit as st

_LOCK = threading.Lock()
_STORE = Path(__file__).resolve().parents[1] / "data" / "visitors.json"


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _header(name: str) -> str | None:
    try:
        value = st.context.headers[name]
    except (KeyError, TypeError, AttributeError):
        return None
    text = str(value).strip()
    return text or None


def _client_ip() -> tuple[str, str]:
    """返回 (地址, 来源)。

    直接连上来时用连接上的地址。本机打开时 Streamlit 不提供 127.0.0.1，
    这时再看反向代理转发的地址；仍然没有，就记成本机。
    """
    ip = getattr(st.context, "ip_address", None)
    if ip:
        return str(ip), "connection"

    forwarded = _header("X-Forwarded-For")
    if forwarded:
        first = forwarded.split(",")[0].strip()
        if first:
            return first, "x-forwarded-for"

    real = _header("X-Real-Ip")
    if real:
        return real, "x-real-ip"

    return "127.0.0.1", "localhost"


def _empty() -> dict:
    return {"visits": 0, "visitors": {}}


def _load() -> dict:
    if not _STORE.exists():
        return _empty()
    try:
        data = json.loads(_STORE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _empty()
    if not isinstance(data, dict):
        return _empty()
    if not isinstance(data.get("visits"), int):
        data["visits"] = 0
    if not isinstance(data.get("visitors"), dict):
        data["visitors"] = {}
    return data


def _save(data: dict) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    temporary = _STORE.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(_STORE)


def record_visit() -> tuple[int, int]:
    """同一个浏览器会话只记一次。返回 (访问次数, 不同地址数)。"""
    if st.session_state.get("visit_recorded"):
        data = _load()
        return int(data["visits"]), len(data["visitors"])

    address, via = _client_ip()
    seen = _now()
    with _LOCK:
        data = _load()
        data["visits"] = int(data["visits"]) + 1
        visitors = data["visitors"]
        entry = visitors.get(address)
        if not isinstance(entry, dict):
            entry = {"count": 0, "first_seen": seen, "last_seen": seen, "via": via}
        entry["count"] = int(entry.get("count", 0)) + 1
        entry["last_seen"] = seen
        entry["via"] = via
        entry.setdefault("first_seen", seen)
        visitors[address] = entry
        _save(data)

    st.session_state.visit_recorded = True
    return int(data["visits"]), len(data["visitors"])


def show_counter() -> None:
    visits, people = record_visit()
    st.caption(f"访问 {visits} 次 · {people} 人到过")
