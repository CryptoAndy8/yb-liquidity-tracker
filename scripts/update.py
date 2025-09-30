import json
import pathlib
import random
import sys
from datetime import datetime, timezone


def fetch_stats():
    """
    Заглушка з «живими» значеннями (рандом усередині допустимого діапазону).
    Пізніше сюди підключиш реальні джерела (API/RPC) замість random.
    """
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "ts": now_iso,
        "ybBTC": {
            "depth": round(100000 + random.random() * 1000, 2),
            "fees_24h": round(200 + random.random() * 5, 2),
        },
        "ybETH": {
            "depth": round(90000 + random.random() * 1000, 2),
            "fees_24h": round(180 + random.random() * 5, 2),
        },
    }


def write_snapshot(data: dict) -> pathlib.Path:
    """
    Створює новий файл-снапшот з точністю до секунд,
    щоб завжди був новий diff і реальний коміт.
    """
    dt = datetime.now(timezone.utc)
    folder = pathlib.Path("data") / dt.strftime("%Y-%m-%d")
    folder.mkdir(parents=True, exist_ok=True)

    # Ім'я файлу включає секунди → кожен запуск створює новий файл.
    path = folder / f"{dt.strftime('%H%M%S')}.json"
    path.write_text(json.dumps(data, indent=2))
    return path


if __name__ == "__main__":
    payload = fetch_stats()
    out_path = write_snapshot(payload)
    print(f"[update.py] wrote file: {out_path}")
    sys.exit(0)
