from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generate_charts import main as generate_charts_main


def main() -> None:
    """Ejecuta el flujo completo de benchmark y generación de gráficas."""
    generate_charts_main()


if __name__ == "__main__":
    main()
