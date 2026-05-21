from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.rsa_scheme import evaluate_key_sizes

RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def create_benchmark_dataframe(key_sizes=(512, 768, 1024), message="RSA test") -> pd.DataFrame:
    """Genera un DataFrame con tiempos medidos para cada tamaño de clave."""
    results = evaluate_key_sizes(key_sizes, message=message)
    df = pd.DataFrame.from_dict(results, orient="index")
    df.index.name = "tamaño_clave"
    df = df.reset_index()
    return df


def save_csv(df: pd.DataFrame, filename: str = "rsa_benchmark.csv") -> Path:
    """Guarda el DataFrame como CSV en la carpeta de resultados."""
    csv_path = RESULTS_DIR / filename
    df.to_csv(csv_path, index=False, float_format="%.6f")
    return csv_path


def plot_bar_chart(df: pd.DataFrame, filename: str = "rsa_barras.png") -> Path:
    """Dibuja y guarda una gráfica de barras comparando los tiempos RSA."""
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.25
    x = range(len(df))

    ax.bar([pos - bar_width for pos in x], df["keygen"], width=bar_width, label="Generación", color="#2a7f62")
    ax.bar(x, df["encrypt"], width=bar_width, label="Cifrado", color="#4069a1")
    ax.bar([pos + bar_width for pos in x], df["decrypt"], width=bar_width, label="Descifrado", color="#c04d30")

    ax.set_xticks(x)
    ax.set_xticklabels(df["tamaño_clave"].astype(str))
    ax.set_title("Comparación de tiempos RSA por tamaño de clave", fontsize=14, weight="bold")
    ax.set_xlabel("Tamaño de clave (bits)", fontsize=12)
    ax.set_ylabel("Tiempo (segundos)", fontsize=12)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()

    output_path = RESULTS_DIR / filename
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_line_chart(df: pd.DataFrame, filename: str = "rsa_lineas.png") -> Path:
    """Dibuja y guarda una gráfica de líneas de evolución de los tiempos RSA."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["tamaño_clave"], df["keygen"], marker="o", label="Generación", color="#2a7f62")
    ax.plot(df["tamaño_clave"], df["encrypt"], marker="o", label="Cifrado", color="#4069a1")
    ax.plot(df["tamaño_clave"], df["decrypt"], marker="o", label="Descifrado", color="#c04d30")

    ax.set_title("Evolución de los tiempos RSA según tamaño de clave", fontsize=14, weight="bold")
    ax.set_xlabel("Tamaño de clave (bits)", fontsize=12)
    ax.set_ylabel("Tiempo (segundos)", fontsize=12)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()

    output_path = RESULTS_DIR / filename
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def main() -> None:
    """Ejecuta la generación de CSV y las gráficas a partir de los datos de benchmark."""
    key_sizes = (512, 768, 1024)
    df = create_benchmark_dataframe(key_sizes=key_sizes, message="RSA test")
    csv_path = save_csv(df)
    bar_path = plot_bar_chart(df)
    line_path = plot_line_chart(df)

    print("CSV guardado en:", csv_path)
    print("Gráfica de barras guardada en:", bar_path)
    print("Gráfica de líneas guardada en:", line_path)


if __name__ == "__main__":
    main()
