# scripts/update.py
# Мінімальний "живий" збирач. Далі підставиш реальні дані (API/ончейн).
import json, pathlib, random
from datetime import datetime, timezone

def fetch_stats():
    # TODO: заміни на реальні метрики: depth/fees/slippage/gas і т.д.
    return {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ybBTC": {
            "depth": round(100000 + random.random()*1000, 2),
            "fees_24h": round(200 + random.random()*5, 2)
        },
        "ybETH": {
            "depth": round(90000 + random.random()*1000, 2),
            "fees_24h": round(180 + random.random()*5, 2)
        }
    }

def write_snapshot(data):
    # Кожні 30 хв створюємо новий файл: це реальний снапшот (нова мітка часу).
    dt = datetime.now(timezone.utc)
    folder = pathlib.Path("data") / dt.strftime("%Y-%m-%d")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{dt.strftime('%H%M')}.json"

    # Якщо файл уже є і дані ті ж — не перезаписуємо, щоб не плодити шум
    old = json.loads(path.read_text()) if path.exists() else None
    if old != data:
        path.write_text(json.dumps(data, indent=2))
        return True
    return False

if __name__ == "__main__":
    write_snapshot(fetch_stats())
