"""记录每次新打开页面的访问，并把地区写入 data/visitors.json。

访问记录和地区库都不进入 git。页面上只显示次数和人数。
人数按浏览器区分：同一台电脑或手机反复打开，人数不变，次数增加。
电脑和手机即使用同一个网络，也各算一个人。
"""

from __future__ import annotations

import ipaddress
import json
import re
import threading
from datetime import datetime
from pathlib import Path

import streamlit as st

_LOCK = threading.Lock()
_SEARCH_LOCK = threading.Lock()
_ROOT = Path(__file__).resolve().parents[1]
_STORE = _ROOT / "data" / "visitors.json"
_REGION_DB = _ROOT / "data" / "ip2region_v4.xdb"
_VISITOR_ID = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
_FORWARDED_HEADERS = (
    "X-Forwarded-For",
    "X-Real-Ip",
    "CF-Connecting-IP",
    "True-Client-IP",
    "X-Client-Ip",
    "X-Original-Forwarded-For",
)
_searcher = None
_searcher_ready = False

# 浏览器里记住一个编号，并把该网络出口所在的地区送回来。
# 服务器看到的连接经常是本机转发，单靠连接地址分不开电脑和手机，也查不到地区。
_VISITOR_JS = """
export default function(component) {
    const { setStateValue } = component;
    const idKey = "missionary_visitor";
    const placeKey = "missionary_place";
    let id = localStorage.getItem(idKey);
    if (!id) {
        id = (crypto.randomUUID && crypto.randomUUID()) || String(Date.now());
        localStorage.setItem(idKey, id);
    }
    setStateValue("visitor_id", id);

    const cached = localStorage.getItem(placeKey);
    if (cached) {
        setStateValue("client_place", cached);
        return;
    }
    fetch("https://myip.ipip.net/json")
        .then((response) => response.json())
        .then((payload) => {
            const parts = payload && payload.data && payload.data.location;
            if (!Array.isArray(parts)) {
                return;
            }
            const place = parts.slice(0, 3).filter((part, index, all) => {
                return part && part !== all[index - 1];
            }).join(" ");
            if (!place) {
                return;
            }
            localStorage.setItem(placeKey, place);
            setStateValue("client_place", place);
        })
        .catch(() => {});
}
"""

_visitor_probe = st.components.v2.component("visitor_probe", js=_VISITOR_JS)


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _header_values(name: str) -> list[str]:
    try:
        headers = st.context.headers
        if hasattr(headers, "get_all"):
            return [str(value) for value in headers.get_all(name)]
        return [str(headers[name])]
    except (KeyError, TypeError, AttributeError):
        return []


def _parse_ip(text: str) -> str | None:
    token = text.strip().strip('"').removeprefix("for=").strip().strip('"')
    if token.startswith("[") and "]" in token:
        token = token[1 : token.index("]")]
    elif token.count(":") == 1 and "." in token:
        token = token.split(":", 1)[0]
    if token.lower().startswith("::ffff:"):
        token = token.split(":")[-1]
    try:
        return str(ipaddress.ip_address(token))
    except ValueError:
        return None


def _kind(ip: str) -> str:
    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return "invalid"
    if address.is_loopback:
        return "loopback"
    if address.is_global:
        return "public"
    return "private"


def _client_ip() -> tuple[str, str]:
    """优先用代理转发来的公网地址，其次用连接上的局域网地址。"""
    found: list[tuple[str, str]] = []
    for name in _FORWARDED_HEADERS:
        for value in _header_values(name):
            for part in value.split(","):
                ip = _parse_ip(part)
                if ip:
                    found.append((ip, name.lower()))
    for value in _header_values("Forwarded"):
        for part in value.split(";"):
            ip = _parse_ip(part)
            if ip:
                found.append((ip, "forwarded"))

    visible = getattr(st.context, "ip_address", None)
    if visible:
        ip = _parse_ip(str(visible))
        if ip:
            found.append((ip, "connection"))

    for kind in ("public", "private"):
        for ip, via in found:
            if _kind(ip) == kind:
                return ip, via
    return "127.0.0.1", "localhost"


def _device() -> str:
    agent = " ".join(_header_values("User-Agent")).lower()
    if any(word in agent for word in ("iphone", "ipad", "android", "mobile")):
        return "手机"
    if agent:
        return "电脑"
    return "未知设备"


def _tidy_place(place: str) -> str:
    names: list[str] = []
    for part in place.replace("|", " ").split():
        if part and part != "0" and (not names or names[-1] != part):
            names.append(part)
    return " ".join(names)


def _format_region(raw: str) -> str:
    parts = [part.strip() for part in raw.split("|")]
    while len(parts) < 3:
        parts.append("")
    names = [part for part in parts[:3] if part and part != "0"]
    return " ".join(names)


def _load_searcher():
    global _searcher, _searcher_ready
    if _searcher_ready:
        return _searcher
    _searcher_ready = True
    if not _REGION_DB.exists():
        return None
    try:
        import ip2region.searcher as xdb
        import ip2region.util as util

        content = util.load_content_from_file(str(_REGION_DB))
        _searcher = xdb.new_with_buffer(util.IPv4, content)
    except (OSError, ValueError, ImportError):
        _searcher = None
    return _searcher


def _server_place(ip: str) -> str:
    kind = _kind(ip)
    if kind == "loopback":
        return "本机"
    if kind != "public":
        return "局域网"
    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return "未查到"
    if address.version != 4:
        return "IPv6，当前地区库只收录 IPv4"
    try:
        with _SEARCH_LOCK:
            searcher = _load_searcher()
            raw = "" if searcher is None else searcher.search(ip)
    except (ValueError, OSError):
        return "未查到"
    if searcher is None:
        return "地区库不在本机"
    return _format_region(raw) or "未查到"


def _empty() -> dict:
    return {"visits": 0, "places": {}, "visitors": {}}


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
    if not isinstance(data.get("places"), dict):
        data["places"] = {}
    return data


def _people(data: dict) -> int:
    return sum(1 for key in data["visitors"] if _VISITOR_ID.fullmatch(str(key)))


def _summarize(visitors: dict) -> dict[str, int]:
    places: dict[str, int] = {}
    for key, entry in visitors.items():
        if not _VISITOR_ID.fullmatch(str(key)) or not isinstance(entry, dict):
            continue
        place = entry.get("place")
        if not isinstance(place, str) or not place:
            continue
        places[place] = places.get(place, 0) + int(entry.get("count", 0))
    return places


def _save(data: dict) -> None:
    data["places"] = _summarize(data["visitors"])
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    temporary = _STORE.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(_STORE)


def _remember(visitor_id: str | None, client_place: str | None) -> tuple[int, int]:
    """同一个浏览器会话只加一次次数。地区晚到时补写，不再加次数。"""
    if not visitor_id or not _VISITOR_ID.fullmatch(visitor_id):
        data = _load()
        return int(data["visits"]), _people(data)

    fresh = not st.session_state.get("visit_recorded")
    ip, via = _client_ip()
    place = _tidy_place(client_place) if client_place else _server_place(ip)
    seen = _now()
    with _LOCK:
        data = _load()
        visitors = data["visitors"]
        entry = visitors.get(visitor_id)
        changed = False
        if not isinstance(entry, dict):
            entry = {
                "count": 0,
                "first_seen": seen,
                "last_seen": seen,
                "device": _device(),
                "ip": ip,
                "via": via,
                "place": place,
            }
            changed = True
        counted = int(entry.get("count", 0))
        if fresh or counted == 0:
            if fresh:
                data["visits"] = int(data["visits"]) + 1
            entry["count"] = counted + 1
            entry["last_seen"] = seen
            entry["ip"] = ip
            entry["via"] = via
            entry["device"] = _device()
            changed = True
        if place and entry.get("place") != place:
            # 浏览器查到的地区比「本机 / 局域网」更能说明人在哪里。
            weak = {"本机", "局域网", "未查到", "地区库不在本机"}
            if client_place or entry.get("place") in weak or not entry.get("place"):
                entry["place"] = place
                changed = True
        entry.setdefault("first_seen", seen)
        visitors[visitor_id] = entry
        if changed:
            _save(data)

    if fresh:
        st.session_state.visit_recorded = True
    return int(data["visits"]), _people(data)


def _state_text(result: object, name: str) -> str | None:
    try:
        value = result[name]  # type: ignore[index]
    except (KeyError, TypeError, AttributeError):
        return None
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def show_counter() -> None:
    result = _visitor_probe(key="missionary_visitor_probe", height=0)
    visits, people = _remember(
        _state_text(result, "visitor_id"),
        _state_text(result, "client_place"),
    )
    st.caption(f"访问 {visits} 次 · {people} 人到过")
