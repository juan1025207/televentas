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
   
    #valores que queremos mostrar.
   def mostrar (self):
      print(f"  [{self.codigo}] {self.nombre} - ${self.precio} (stock: {self.stock})")

class Cliente:
    def __init__(self, nombre, email):
        #guardamos los datos
        self.nombre = nombre
        self.email = email
        self.recibe_catalogo = False

    def suscribirse(self):
        self.recibe_catalogo = True
        log.info("Cliente %s se suscribio al catalogo", self.email)

class ItemOrden:
    def __init__(self, producto, cantidad):
        # Validamos que la cantidad sea válida
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        self.producto = producto
        self.cantidad = cantidad

    def subtotal(self):
        # Calcula el precio total de este ítem
        return self.producto.precio * self.cantidad
    
class OrdenCompra:
    def __init__(self, cliente, items, tipo_pago):
        #guardamos los datos
        self.id = str(uuid.uuid4())[:8] #para hacer el id y guardarlo
        self.cliente = cliente
        self.items = items
        self.tipo_pago = tipo_pago
        self.estado = EstadoOrden.PENDIENTE
        self.fecha = datetime.now()
        #registro del log
        log.info("Orden creada | id=%s | cliente=%s", self.id, cliente.email)

    def calcular_total(self): #se calcula el total de la orden sumando lo subtotales
        total = 0
        for item in self.items:
            total += item.subtotal()
        return total

    def confirmar(self): #se cambia el estado de la orden
        self.estado = EstadoOrden.CONFIRMADA
        log.info("Orden %s CONFIRMADA", self.id)

    def cancelar(self):#se cancela si la orden no ha sido despachada
        if self.estado == EstadoOrden.DESPACHADA:
            print("No se puede cancelar una orden ya despachada")
            return
        self.estado = EstadoOrden.CANCELADA
        log.info("Orden %s CANCELADA", self.id)

    def armar(self):# marca la orden como aramda
        self.estado = EstadoOrden.ARMADA
        log.info("Orden %s ARMADA", self.id)

    def despachar(self): #marca la orden para despachar 
        self.estado = EstadoOrden.DESPACHADA
        log.info("Orden %s DESPACHADA", self.id)


class Queja:
    def __init__(self, cliente, descripcion):
        self.id = str(uuid.uuid4())[:8]# se hace el id
        self.cliente = cliente
        self.descripcion = descripcion
        self.fecha = datetime.now()
        log.info("Queja registrada | id=%s | cliente=%s", self.id, cliente.email)

 
class Inventario:
    def __init__(self):
        self.productos = {}  #Productos por código
        log.info("Inventario iniciado")

    def agregar(self, producto):
        self.productos[producto.codigo] = producto  #Agregar producto

    def buscar(self, codigo): 
        producto = self.productos.get(codigo)
        if not producto:
            print(f"Producto {codigo} no encontrado")
        return producto

    def mostrar_catalogo(self):# Se muestra el producto
        print("\nCatalogo de productos:")
        for p in self.productos.values():
            p.mostrar()

    def descontar_stock(self, codigo, cantidad):
        producto = self.productos.get(codigo)
        if not producto:
            print(f"Producto {codigo} no existe")
            return False
        if producto.stock < cantidad:
            print(f"No hay suficiente stock de {producto.nombre}")
            return False
        producto.stock -= cantidad  # restar stock
        log.info("Stock actualizado | %s | nuevo stock: %d", codigo, producto.stock)
        return True