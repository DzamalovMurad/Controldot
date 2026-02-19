from __future__ import annotations

# region agent log (logger)
import json
import os
import sys
import time
from pathlib import Path


def _dbg(*, runId: str, hypothesisId: str, location: str, message: str, data: dict) -> None:
    try:
        log_path = Path(r"c:\Users\Gigabyte\Desktop\Warship\.cursor\debug.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "id": f"log_{int(time.time() * 1000)}_{hypothesisId}",
            "timestamp": int(time.time() * 1000),
            "runId": runId,
            "hypothesisId": hypothesisId,
            "location": location,
            "message": message,
            "data": data,
        }
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _pycache_state() -> dict:
    return {
        "cwd": os.getcwd(),
        "dont_write_bytecode": getattr(sys, "dont_write_bytecode", None),
        "env_PYTHONDONTWRITEBYTECODE": os.environ.get("PYTHONDONTWRITEBYTECODE"),
        "env_PYTHONPYCACHEPREFIX": os.environ.get("PYTHONPYCACHEPREFIX"),
        "exists_battleship___pycache__": Path("battleship/__pycache__").exists(),
        "exists_battleship_game___pycache__": Path("battleship/game/__pycache__").exists(),
    }


# endregion agent log (logger)


if __name__ == "__main__":
    # region agent log (H2)
    _dbg(
        runId="pre-fix",
        hypothesisId="H2",
        location="main.py:startup",
        message="Before importing project modules",
        data=_pycache_state(),
    )
    # endregion agent log (H2)

    from battleship.main import main  # import after first log

    # region agent log (H1)
    _dbg(
        runId="pre-fix",
        hypothesisId="H1",
        location="main.py:after_import",
        message="After importing battleship.main",
        data=_pycache_state(),
    )
    # endregion agent log (H1)

    main()

