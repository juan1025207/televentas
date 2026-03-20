"""
TeleVentas - Sistema de Compras a Distancia
estudiante: Juan Camilo Moreno 
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
  
  #ahora creamos las clases y sus metodos siguiendo el diagrama UML

class EstadoOrden ( Enum ): #LISTA DE ESTADOS DE ORDEN  FIJOS
   PENDIENTE = "PENDIENTE"
   CONFIRMADA = "CONFIRMADA"
   ARMADA  = "ARMADA"
   DESPACHADA = "DESPACHADA"
   CANCELADA = "CANCELADA"

class TipoPago(Enum): 
   TARJETA = "TARJETA_CREDITO"

class Producto : #creamos el objeto "producto" 
   def __init__(self, codigo, nombre, precio, stock):
      #guardamos los datosd
      self.codigo = codigo
      self.nombre = nombre
      self.precio = precio
      self.stock = stock
    #valores que queremos mostrar
   def mostrar (self):
      print(f"  [{self.codigo}] {self.nombre} - ${self.precio} (stock: {self.stock})")
 
   

 
  