"""
Lineage Logger for the Vortex Climate Intelligence ETL.
Uses a class-based design to generate a JSON log after each pipeline run.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from services.logging_service import log_info

class LineageLogger:
    """Handles lineage tracking for ETL pipelines."""

    def __init__(self, source_name: str = "unknown_source", output_dir: str = "logs/lineage"):
        """
        Initialize the LineageLogger.

        Args:
            source_name: Identifier for the data source (e.g. 'aemet_json').
            output_dir: Directory where the JSON log will be saved.
        """
        self.source_name = source_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_log(
        self,
        df_original: pd.DataFrame,
        df_cleaned: pd.DataFrame,
    ) -> Path:
        """
        Generate a lineage log file comparing original and cleaned DataFrames.

        Args:
            df_original: Raw data before transformations.
            df_cleaned: Data after cleaning and validation.

        Returns:
            Path object pointing to the generated log file.
        """
        original_count = len(df_original)
        cleaned_count = len(df_cleaned)
        discarded_count = original_count - cleaned_count

        timestamp_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        safe_timestamp = timestamp_utc.replace(":", "-")  # avoid colons in filenames

        lineage_info = {
            "timestamp": timestamp_utc,
            "source": self.source_name,
            "total_original": original_count,
            "total_cleaned": cleaned_count,
            "total_discarded": discarded_count,
        }

        # Build filename: lineage_<source>_<timestamp>.json
        filename = f"lineage_{self.source_name}_{safe_timestamp}.json"
        file_path = self.output_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(lineage_info, f, indent=2)

        # Also write a one-line summary to the application log
        log_info(
            f"Linaje generado: {self.source_name} -> "
            f"original={original_count}, limpias={cleaned_count}, "
            f"descartadas={discarded_count}"
        )

        return file_path

if __name__ == "__main__":
    # Create mock data
    data_original = {
        "ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"],
        "temperatura": [15.2, 18.1, 16.7, 20.3, 14.8],
    }
    data_cleaned = {
        "ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla"],
        "temperatura": [15.2, 18.1, 16.7, 20.3],
    }

    df_orig = pd.DataFrame(data_original)
    df_clean = pd.DataFrame(data_cleaned)

    # Instantiate the logger
    logger = LineageLogger(source_name="aemet_test")  # usa el nuevo default logs/lineage

    # Generate log
    archivo_generado = logger.generate_log(df_orig, df_clean)

    print(f"Log generado exitosamente en: {archivo_generado}")
    print("Contenido del JSON:")
    print(archivo_generado.read_text(encoding="utf-8"))