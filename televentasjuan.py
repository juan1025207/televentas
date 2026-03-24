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
    
# clase correo
class Correo:
    def enviar_catalogo(self, cliente, inventario):
        log.info("Catalogo enviado %s", cliente.email)  # envío de catálogo
    
    def avisar_gerente(self, queja):
        log.info("Queja %s enviada ala gerente", queja.id)  # notifica queja

# clase gestor ordenes 
class GestorOrdenes:
    def __init__(self, inventario):
        self.inventario = inventario  # referencia al inventario
        self.ordenes = {}  # guarda órdenes por id

    def crear_orden(self, cliente, items, tipo_pago):
        for item in items:
            prod = self.inventario.buscar(item.producto.codigo)  # verifica producto
            if not prod or prod.stock < item.cantidad:
                print("No hay stock suficiente para crear la orden")
                return None
        orden = OrdenCompra(cliente, items, tipo_pago)  # crea orden
        orden.confirmar()  # confirma orden
        self.ordenes[orden.id] = orden  # guarda orden
        return orden

    def cancelar_orden(self, orden_id):
        orden = self.ordenes.get(orden_id)  # busca orden
        if orden:
            orden.cancelar()  # cancela orden

    def ordenes_confirmadas(self):
        resultado = []
        for orden in self.ordenes.values():
            if orden.estado == EstadoOrden.CONFIRMADA:
                resultado.append(orden)  # agrega confirmadas
        return resultado

    def armar_orden(self, orden_id):
        orden = self.ordenes.get(orden_id)  # busca orden
        if not orden:
            print("Orden no encontrada")
            return False
        for item in orden.items:
            self.inventario.descontar_stock(item.producto.codigo, item.cantidad)  # descuenta stock
        orden.armar()  # marca como armada
        return True

class GestorQuejas:
    def __init__(self, correo):
        self.correo = correo  # servicio de correo
        self.quejas = []  # lista de quejas

    def registrar(self, cliente, descripcion):
        queja = Queja(cliente, descripcion)  # crea queja
        self.quejas.append(queja)  # guarda queja
        self.correo.avisar_gerente(queja)  # notifica al gerente
        return queja  # devuelve la queja

class Transporte:
    def __init__(self, nombre):
        self.nombre = nombre

    def entregar(self, orden):
        log.info("Entrega a cargo de %s | orden %s", self.nombre, orden.id)
        orden.despachar()
class Agente:
    def __init__(self, gestor, transportes):
        self.gestor = gestor
        self.transportes = transportes

    def ver_ordenes(self):
        ordenes = self.gestor.ordenes_confirmadas()
        print(f"\nOrdenes pendientes de armado: {len(ordenes)}")
        return ordenes

    def procesar_orden(self, orden_id, indice_transporte=0):
        ok = self.gestor.armar_orden(orden_id)
        if not ok:
            return False
        orden = self.gestor.ordenes[orden_id]
        transporte = self.transportes[indice_transporte]
        transporte.entregar(orden)
        return True

class Transporte:
    def __init__(self, nombre):
        self.nombre = nombre  #nombre de la empresa

    def entregar(self, orden):
        log.info("Entrega a cargo de %s | orden %s", self.nombre, orden.id)  # registra envío
        orden.despachar()  #marca como despachada


class Agente:
    def __init__(self, gestor, transportes):
        self.gestor = gestor   # gestor de órdenes
        self.transportes = transportes  #lista de transportes

    def ver_ordenes(self):
        ordenes = self.gestor.ordenes_confirmadas()  #obtiene órdenes confirmadas
        print(f"\nOrdenes pendientes de armado: {len(ordenes)}")
        return ordenes

    def procesar_orden(self, orden_id, indice_transporte=0):
        ok = self.gestor.armar_orden(orden_id)  #intenta armar orden
        if not ok:
            return False
        orden = self.gestor.ordenes[orden_id]  #btiene la orden
        transporte = self.transportes[indice_transporte]  #selecciona transporte
        transporte.entregar(orden)  #envía la orden
        return True

#METODO MAIN
def main():
    print("=== Sistema TeleVentas ===\n")

    inventario = Inventario()  #  inventario
    inventario.agregar(Producto("P001", "Televisor 55 pulgadas", 1500, 10))  #agregar producto
    inventario.agregar(Producto("P002", "Auriculares Bluetooth", 80, 50))
    inventario.agregar(Producto("P003", "Control Remoto", 25, 100))

    inventario.mostrar_catalogo()  #Mostrar catálogo

    correo = Correo()  #ervicio de correo
    gestor_ordenes = GestorOrdenes(inventario)  #gestor de órdenes
    gestor_quejas = GestorQuejas(correo)  #gestor de quejas
    transportes = [
        Transporte("TransRapido S.A."),
        Transporte("LogiExpress")
    ]
    agente = Agente(gestor_ordenes, transportes)  #agente de depósito

    print("\n--- Ana realiza una compra ---")
    ana = Cliente("Ana Garcia", "ana@email.com")  #crear cliente
    ana.suscribirse()  #suscribirse al catálogo
    correo.enviar_catalogo(ana, inventario)  #enviar catálogo

    producto1 = inventario.buscar("P001")  #buscar producto
    item1 = ItemOrden(producto1, 2)  #crear ítem
    orden1 = gestor_ordenes.crear_orden(ana, [item1], TipoPago.TARJETA)  #crear orden

    if orden1:
        print(f"Orden creada: {orden1.id}")
        print(f"Total a pagar: ${orden1.calcular_total()}")
        print(f"Estado: {orden1.estado.value}")

    print("\n--- Ana presenta una queja ---")
    gestor_quejas.registrar(ana, "El paquete llego tarde")  #registrar queja

    print("\n--- Agente procesa la orden ---")
    ordenes = agente.ver_ordenes()  #ver órdenes
    if ordenes:
        agente.procesar_orden(ordenes[0].id, indice_transporte=0)  #procesar orden
        print(f"Estado final: {ordenes[0].estado.value}")

    print("\n--- Luis cancela su orden ---")
    luis = Cliente("Luis Perez", "luis@email.com")  #crear cliente
    producto2 = inventario.buscar("P002")  #buscar producto
    item2 = ItemOrden(producto2, 1)  #crear ítem
    orden2 = gestor_ordenes.crear_orden(luis, [item2], TipoPago.TARJETA)  #crear orden

    if orden2:
        print(f"Orden creada: {orden2.id}")
        orden2.cancelar()  #cancelar orden
        print(f"Estado: {orden2.estado.value}")

    print("\n=== Fin del programa ===")


if __name__ == "__main__":
    main()  #se jecuta programa