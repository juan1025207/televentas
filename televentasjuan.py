"""
TeleVentas - Sistema de Compras a Distancia
estudiante: Juan Moreno
"""
 
# Importamos las herramientas de phyton que necesitamos
import logging
import uuid
from datetime import datetime
from enum import Enum
 
 #configuramos el logueo con el siguiente codigo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("televentas.log"),
    ],
)
log = logging.getLogger("TeleVentas")
 