"""
Climate Data Pipeline Auditor
=================================================
Passively observes the data flow, takes snapshots at each stage,
and generates detailed lineage reports without modifying any
existing script or pipeline.

Stages documented:
  1. Raw data (from AEMET API or a pre-fetched file)
  2. Normalized data (as read from the existing normalized JSON)
  3. Transformed data (by calling Helen's transform_data)

Two lineage comparisons are produced:
  - raw -> normalized
  - normalized -> transformed
"""

import sys
import os

# Add the project root to the path to be able to import the team modules
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

# Existing project modules (public APIs only, no modifications)
from etl.extract import extract_data
from etl.transform import transform_data
from etl.lineage import LineageLogger
from services.weather_api_service import WeatherAPIService

from dotenv import load_dotenv
load_dotenv()  # Carga las variables de entorno desde .env

class DataPipelineAuditor:
    """
    Silent observer that tracks the journey of climate data.
    """

    def __init__(
        self,
        snapshots_dir: str = "logs/snapshots",
        lineage_dir: str = "logs/lineage",
    ):
        """
        Args:
            snapshots_dir: Base directory where intermediate snapshots
                           (raw, normalized, transformed) will be stored.
            lineage_dir: Directory where lineage reports will be written.
        """
        self.snapshots_dir = Path(snapshots_dir)
        self.lineage_dir = Path(lineage_dir)

        # Ensure base directories exist (subdirs will be created per run)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.lineage_dir.mkdir(parents=True, exist_ok=True)

        # Lineage logger (reuses your existing class)
        self.lineage_logger = LineageLogger(
            source_name="vortex_pipeline",  # default, will be overridden per stage
            output_dir=str(self.lineage_dir),
        )

        # Weather service (lazy initialisation, only if needed)
        self._weather_service: Optional[WeatherAPIService] = None

        # Internal logger for the auditor
        self.logger = logging.getLogger("DataPipelineAuditor")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            # File handler (appends to app.log)
            fh = logging.FileHandler("logs/app.log")
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        self.logger.info("DataPipelineAuditor inicializado.")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _ensure_directories(self) -> None:
        """Create stage subdirectories inside snapshots_dir (raw skipped by design)."""
        for stage in ("normalized", "transformed"):   # sin "raw"
            (self.snapshots_dir / stage).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _df_from_dicts(data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert a list of dictionaries into a pandas DataFrame.

        Args:
            data: List of records.

        Returns:
            DataFrame containing the data.
        """
        return pd.DataFrame(data)

    def _save_raw_summary(
        self,
        raw_data: List[Dict[str, Any]],
        timestamp: datetime,
    ) -> Path:
        """
        Save a lightweight summary of the raw data instead of the full snapshot.

        Args:
            raw_data: List of raw observation dicts.
            timestamp: UTC timestamp for the filename.

        Returns:
            Path to the summary file.
        """
        # Convert to DataFrame for easy statistics
        df = self._df_from_dicts(raw_data)

        summary = {
            "total_records": len(df),
            "columns": df.columns.tolist(),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "null_counts": df.isnull().sum().to_dict(),
        }

        safe_ts = timestamp.strftime("%Y-%m-%dT%H-%M-%SZ")
        filename = f"raw_summary_{safe_ts}.json"
        file_path = self.lineage_dir / filename  # save alongside lineage reports
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str, ensure_ascii=False)

        self.logger.info("Resumen de datos crudos guardado en %s", file_path)
        return file_path
    
    def _save_snapshot(
        self,
        data: Any,
        stage: str,
        timestamp: datetime,
    ) -> Path:
        """
        Persist a snapshot of data at a particular pipeline stage.

        Args:
            data: Either a list of dicts (raw/normalized) or a DataFrame (transformed).
            stage: One of 'raw', 'normalized', 'transformed'.
            timestamp: UTC timestamp used to build the filename.

        Returns:
            Path to the saved file.
        """
        stage_dir = self.snapshots_dir / stage
        stage_dir.mkdir(parents=True, exist_ok=True)

        safe_ts = timestamp.strftime("%Y-%m-%dT%H-%M-%SZ")
        filename = f"{safe_ts}.json"
        file_path = stage_dir / filename

        if isinstance(data, pd.DataFrame):
            records = data.to_dict(orient="records")
        else:
            records = data

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, default=str, ensure_ascii=False)

        self.logger.info(
            "Snapshot guardado: %s/%s → %d registros",
            stage,
            filename,
            len(records),
        )
        return file_path

    def _load_normalized(self, normalized_file: str) -> List[Dict[str, Any]]:
        """
        Load the existing normalized data from the given JSON file.

        Args:
            normalized_file: Relative path (from etl/) to the normalized JSON,
                             e.g. "../data/registros_climaticos_normalizados.json".

        Returns:
            List of normalized records as dicts.
        """
        self.logger.info("Cargando datos normalizados desde %s", normalized_file)
        data = extract_data(normalized_file)
        if data is None:
            raise ValueError(
                f"No se pudieron cargar los datos normalizados desde {normalized_file}"
            )
        self.logger.info("Normalizados cargados: %d registros.", len(data))
        return data
    
    def _transform(self, normalized_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Apply Helen's transform_data to the normalized data.

        This method does NOT alter any file that the real pipeline uses.
        It only obtains the DataFrame for documentation purposes.

        Args:
            normalized_data: List of normalized records.

        Returns:
            Transformed DataFrame.
        """
        self.logger.info("Aplicando transform_data de Helen a %d registros.", len(normalized_data))
        df_clean = transform_data(normalized_data)
        self.logger.info("Transformación completada. DataFrame resultante: %d filas, %d columnas.",
                          len(df_clean), len(df_clean.columns))
        return df_clean
    
    def _fetch_raw(
        self,
        source: str = "file",
        file_path: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Obtain raw climate data either from a local file or from the AEMET API.

        Args:
            source: "file" to read a JSON file, or "api" to download from AEMET.
            file_path: Path to the raw JSON file (required when source="file").

        Returns:
            List of raw observation dictionaries.
        """
        if source == "api":
            self.logger.info("Descargando datos crudos desde la API de AEMET...")
            if self._weather_service is None:
                self._weather_service = WeatherAPIService()
            raw_data = self._weather_service._obtener_datos_crudos()
            self.logger.info("Datos crudos descargados: %d observaciones.", len(raw_data))
            return raw_data

        if source == "file":
            if file_path is None:
                raise ValueError("file_path es obligatorio cuando source='file'")
            self.logger.info("Leyendo datos crudos desde archivo: %s", file_path)
            data = extract_data(file_path)
            if data is None:
                raise ValueError(f"No se pudieron leer los datos crudos desde {file_path}")
            self.logger.info("Datos crudos leídos: %d registros.", len(data))
            return data

        raise ValueError(f"Origen no soportado: {source}. Usa 'file' o 'api'.")
    
    def _generate_lineage_report(
        self,
        df_original: pd.DataFrame,
        df_cleaned: pd.DataFrame,
        stage_name: str,
        timestamp: datetime,
    ) -> Path:
        """
        Generate both a counts log (via LineageLogger) and a detailed
        discrepancy report for the given stage.

        Args:
            df_original: DataFrame before the transformation.
            df_cleaned: DataFrame after the transformation.
            stage_name: Identifier like 'raw_to_normalized' or
                        'normalized_to_transformed'.

        Returns:
            Path to the detailed report file.
        """
        # 1. Conteos básicos con LineageLogger
        self.lineage_logger.source_name = stage_name
        self.lineage_logger.generate_log(df_original, df_cleaned)

        # 2. Informe detallado
        report = {
            "stage": stage_name,
            "total_original": len(df_original),
            "total_cleaned": len(df_cleaned),
            "discarded_rows": len(df_original) - len(df_cleaned),
            "columns_original": df_original.columns.tolist(),
            "columns_cleaned": df_cleaned.columns.tolist(),
            "columns_added": sorted(
                set(df_cleaned.columns) - set(df_original.columns)
            ),
            "columns_removed": sorted(
                set(df_original.columns) - set(df_cleaned.columns)
            ),
            "nulls_original": df_original.isnull().sum().to_dict(),
            "nulls_cleaned": df_cleaned.isnull().sum().to_dict(),
        }

        # Cambios de tipo en columnas comunes
        common_cols = set(df_original.columns) & set(df_cleaned.columns)
        type_changes = {}
        for col in sorted(common_cols):
            if df_original[col].dtype != df_cleaned[col].dtype:
                type_changes[col] = {
                    "original": str(df_original[col].dtype),
                    "cleaned": str(df_cleaned[col].dtype),
                }
        report["type_changes"] = type_changes

        safe_ts = timestamp.strftime("%Y-%m-%dT%H-%M-%SZ")
        details_filename = f"{stage_name}_{safe_ts}_details.json"
        details_path = self.lineage_dir / details_filename
        with open(details_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        self.logger.info(
            "Informe detallado de linaje generado: %s", details_path
        )
        return details_path
    
    # ------------------------------------------------------------------
    # Public orchestrator
    # ------------------------------------------------------------------

    def run(
        self,
        normalized_file: str,
        raw_source: str = "file",
        raw_file: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute the full audit pipeline:
        raw -> normalized -> transformed.

        Snapshots are saved at each stage and lineage reports are
        generated for raw→normalized and normalized→transformed.

        Args:
            normalized_file: Path to the existing normalized JSON
                             (e.g. "../data/registros_climaticos_normalizados.json").
            raw_source: "file" (default) or "api".
            raw_file: Path to the raw JSON file (required if source="file").

        Returns:
            A dictionary with counts and paths of all generated artifacts.
        """
        timestamp = datetime.now(timezone.utc)
        self._ensure_directories()

        self.logger.info("=== INICIO DE AUDITORÍA ===")

        # ── 1. Raw ──────────────────────────────────────────
        raw_data = self._fetch_raw(source=raw_source, file_path=raw_file)
        raw_df = self._df_from_dicts(raw_data)
        # Instead of a full snapshot, store a lightweight summary
        raw_summary_path = self._save_raw_summary(raw_data, timestamp)

        # ── 2. Normalized ───────────────────────────────────
        norm_data = self._load_normalized(normalized_file)
        norm_df = self._df_from_dicts(norm_data)
        norm_snap = self._save_snapshot(norm_data, "normalized", timestamp)

        # ── 3. Transformed ──────────────────────────────────
        trans_df = self._transform(norm_data)
        trans_snap = self._save_snapshot(trans_df, "transformed", timestamp)

        # ── 4. Lineage reports ──────────────────────────────
        lineage_rn = self._generate_lineage_report(raw_df, norm_df, "raw_to_normalized", timestamp)
        lineage_nt = self._generate_lineage_report(norm_df, trans_df, "normalized_to_transformed", timestamp)

        # ── 5. Summary ──────────────────────────────────────
        summary = {
            "timestamp": timestamp.isoformat(),
            "raw_count": len(raw_df),
            "normalized_count": len(norm_df),
            "transformed_count": len(trans_df),
            "snapshots": {
                "raw_summary": str(raw_summary_path),
                "normalized": str(norm_snap),
                "transformed": str(trans_snap),
            },
            "lineages": {
                "raw_to_normalized": str(lineage_rn),
                "normalized_to_transformed": str(lineage_nt),
            },
        }

        self.logger.info("=== AUDITORÍA COMPLETADA ===")
        self.logger.info("Resumen: %s", summary)

        return summary
    
# ------------------------------------------------------------------
# Auditor Entry Point
# Runs a full audit using the AEMET API as the
# raw data source. The results (snapshots and lineage reports) are stored in logs/snapshots/ and logs/lineage/.
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 55)
    print("Pipeline Auditor – Modo API AEMET")
    print("=" * 55)
    auditor = DataPipelineAuditor()
    resumen = auditor.run(
        normalized_file="../data/registros_climaticos_normalizados.json",
        raw_source="api",
    )
    print("\nResumen de la auditoría:")
    for k, v in resumen.items():
        print(f"  {k}: {v}")