'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from src.modelo import mantenimiento
from src.modelo.auto import Auto
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.declarative_base import session, engine, Base
class auto_perfecto():

    def __init__(self):
        #Este constructor contiene los datos falsos para probar la interfaz
        self.autos = []
        self.mantenimientos = []
        self.acciones = []
        self.gastos = []
        Base.metadata.create_all(engine)
        

    def dar_autos(self):
        autos = [elem.__dict__ for elem in session.query(Auto).all()]
        return autos

    def dar_auto(self, id_auto):
        return self.autos[id_auto].copy()
    
    def crear_auto(self, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        return False

    def editar_auto(self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        self.autos[id]['Marca'] = marca
        self.autos[id]['Placa'] = placa
        self.autos[id]['Modelo'] = modelo
        self.autos[id]['Kilometraje'] = float(kilometraje)
        self.autos[id]['Color'] = color
        self.autos[id]['Cilindraje'] = cilindraje
        self.autos[id]['TipoCombustible'] = tipo_combustible

    def vender_auto(self, id, kilometraje_venta, valor_venta):
        self.autos[id]['ValorVenta'] = valor_venta
        self.autos[id]['KilometrajeVenta'] = kilometraje_venta
        self.autos[id]['Vendido'] = True

    def eliminar_auto(self, id):
        del self.autos[id]
        
    def validar_crear_editar_auto(self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        validacion = False
        try:
            float(kilometraje)
            validacion = True
        except ValueError:
            return False
        return validacion
        
    def validar_vender_auto(self, id, kilometraje_venta, valor_venta):
        validacion = False
        try:
            float(kilometraje_venta)
            float(valor_venta)
            validacion = True
        except ValueError:
            validacion = False

        return validacion
        

    def dar_mantenimientos(self):
        return self.mantenimientos.copy()

    def aniadir_mantenimiento(self, nombre, descripcion):
        if (len(descripcion) > 30 or len(nombre) > 20):
            return False
        busqueda = session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).all()
        if len(busqueda) == 0:
             mantenimiento = Mantenimiento(nombre=nombre, descripcion = descripcion)
             session.add(mantenimiento)
             session.commit()
             return True
        else:
            return False
    
    def editar_mantenimiento(self, id, nombre, descripcion):
        self.mantenimientos[id]['Nombre'] = nombre
        self.mantenimientos[id]['Descripcion'] = descripcion
    
    def eliminar_mantenimiento(self, id):
        del self.mantenimientos[id]

    def validar_crear_editar_mantenimiento(self, nombre, descripcion):
        validacion = False
        if nombre!=None and descripcion!=None:
            validacion = True
        return validacion
        
    def dar_acciones_auto(self, id_auto):
        marca_auto = self.autos[id_auto]['Marca']
        return list(filter(lambda x: x['Auto']==marca_auto, self.acciones))

    def dar_accion(self, id_auto, id_accion):
        return self.dar_acciones_auto(id_auto)[id_accion].copy()

    def crear_accion(self, mantenimiento, id_auto, valor, kilometraje, fecha):
        n_accion = {}
        n_accion['Mantenimiento'] = mantenimiento
        n_accion['Auto'] = self.autos[id_auto]['Marca']
        n_accion['Valor'] = valor
        n_accion['Kilometraje'] = kilometraje
        n_accion['Fecha'] = fecha
        self.acciones.append(n_accion)

    def editar_accion(self, id_accion, mantenimiento, id_auto, valor, kilometraje, fecha):
        self.acciones[id_accion]['Mantenimiento'] = mantenimiento
        self.acciones[id_accion]['Auto'] = self.autos[id_auto]['Marca']
        self.acciones[id_accion]['Valor'] = valor
        self.acciones[id_accion]['Kilometraje'] = kilometraje
        self.acciones[id_accion]['Fecha'] = fecha

    def eliminar_accion(self, id_auto, id_accion):
        marca_auto =self.autos[id_auto]['Marca']
        i = 0
        id = 0
        while i < len(self.acciones):
            if self.acciones[i]['Auto'] == marca_auto:
                if id == id_accion:
                    self.acciones.pop(i)
                    return True
                else:
                    id+=1
            i+=1
        
        return False
                

        del self.accion[id_accion]
        
    def validar_crear_editar_accion(self, id_accion, mantenimiento, id_auto, valor, kilometraje, fecha):
        validacion = False
        try:
            float(kilometraje)
            float(valor)
            validacion = True
        except ValueError:
            validacion = False

        return validacion

    def dar_reporte_ganancias(self, id_auto):
        n_auto = self.autos[id_auto]['Marca']
        
        for gasto in self.gastos:
            if gasto['Marca'] == n_auto:
                return gasto['Gastos'], gasto['ValorKilometro']

        return [('Total',0)], 0