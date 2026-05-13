"""
conftest.py - Configuración global para todos los tests
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# =====================================================
# 1. CREAR ENGINE DE TESTS INMEDIATAMENTE
# =====================================================

TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# =====================================================
# 2. PARCHEAR db.session ANTES DE IMPORTAR LA APP
# =====================================================

# Parchear el módulo db.session para que use nuestro test engine
with patch('db.session.engine', test_engine):
    with patch('db.session.SessionLocal', TestingSessionLocal):
        # Ahora importar la app
        from api.main import app
        from db.base import Base
        from db.models.zona import Zona
        from db.models.medicion import Medicion


# =====================================================
# 3. CREAR TABLAS EN TEST ENGINE
# =====================================================

Base.metadata.create_all(bind=test_engine)


# =====================================================
# 4. FIXTURES DE PYTEST
# =====================================================

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """
    Limpia la BD después de cada test.
    """
    yield
    
    # Después del test, limpiar datos
    db = TestingSessionLocal()
    try:
        db.query(Medicion).delete()
        db.query(Zona).delete()
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


