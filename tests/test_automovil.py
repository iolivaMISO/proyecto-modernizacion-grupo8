import unittest

from src.auto_perfecto.auto_perfecto import auto_perfecto
from src.modelo.automovil import Automovil
from faker import Faker
from src.modelo.declarative_base import Session, engine, Base


class AutomovilTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = auto_perfecto()
        '''Abre la sesión'''
        self.session = Session()

        '''Crea una isntancia de Faker'''
        self.data_factory = Faker()
        Faker.seed(1000)

        renault = Automovil(marca=self.data_factory.company(), placa=self.data_factory.license_plate(), modelo=self.data_factory.random_int(1886, 2022), kilometraje=self.data_factory.random_int(0, 10000), color=self.data_factory.color_name(),
                            cilindraje=self.data_factory.random_int(0, 1000),
                            combustible="gasolina")
        mini = Automovil(marca=self.data_factory.company(), placa=self.data_factory.license_plate(), modelo=self.data_factory.random_int(1886, 2022), kilometraje=self.data_factory.random_int(0, 10000), color=self.data_factory.color_name(), cilindraje=self.data_factory.random_int(0, 1000),
                         combustible="gasolina")

        self.session.add(renault)

        self.session.add(mini)

        self.session.commit()

        self.session.close()

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Consulta todos los autos'''
        busqueda = self.session.query(Automovil).all()

        '''Borra todos los autos'''
        # for auto in busqueda:
        #    self.session.delete(auto)

        self.session.commit()
        self.session.close()

    def test_listar_automoviles_01(self):
        autos = self.logica.dar_autos()
        self.assertIsNotNone(autos)

    def test_crear_automovil_01(self):
        self.logica.crear_auto(self.data_factory.company(), "JXL530", self.data_factory.random_int(1886, 2022),
                               self.data_factory.random_int(0, 10000), self.data_factory.color_name(), self.data_factory.random_int(0, 1000), "gasolina")
        automovil = self.session.query(Automovil).filter(
            Automovil.placa == 'JXL530').first()
        self.assertEqual(automovil.placa, "JXL530")

    def test_no_deberia_crear_automovil_02(self):
        self.logica.crear_auto(None, "JXL120", None, None, None, None, None)
        automovil = self.session.query(Automovil).filter(
            Automovil.placa == 'JXL120').first()
        self.assertIsNone(automovil)

    def test_no_deberia_crear_automovil_03(self):
        self.logica.crear_auto("500", "JXL74983", "A2020*/!#",
                               self.data_factory.random_int(0, 10000), self.data_factory.color_name(), self.data_factory.random_int(0, 1000), "gasolina")
        automovil = self.session.query(Automovil).filter(
            Automovil.placa == 'JXL74983').first()
        self.assertIsNone(automovil)

    def test_no_deberia_crear_automovil_04(self):
        self.logica.crear_auto(self.data_factory.company(), "JX", self.data_factory.random_int(1886, 2022),
                               "-1", self.data_factory.color_name(), self.data_factory.random_int(0, 1000), "gasolina")
        automovil = self.session.query(Automovil).filter(
            Automovil.placa == 'JX').first()
        self.assertIsNone(automovil)

    def test_no_deberia_crear_automovil_05(self):
        self.logica.crear_auto(self.data_factory.company(), "JXL749834232134213", self.data_factory.random_int(1886, 2022),
                               self.data_factory.random_int(0, 1000), self.data_factory.color_name(), "RFS2000", "gasolina")
        automovil = self.session.query(Automovil).filter(
            Automovil.placa == 'JXL749834232134213').first()
        self.assertIsNone(automovil)

    def test_no_deberia_crear_automovil_06(self):
        self.logica.crear_auto("", "", "1971", "-2",
                               self.data_factory.color_name(), self.data_factory.random_int(0, 1000), "gasolina")
        automovil = self.session.query(Automovil).filter(
            Automovil.modelo == '1971').first()
        self.assertIsNone(automovil)

    def test_no_deberia_crear_automovil_07(self):
        self.logica.crear_auto("KIA", self.data_factory.license_plate(), self.data_factory.random_int(1886, 2022),
                               self.data_factory.random_int(0, 10000), self.data_factory.color_name(), "-23", "gasolina")
        automovil = self.session.query(Automovil).filter(
            Automovil.marca == 'KIA').first()
        self.assertIsNone(automovil)

    def test_vender_auto_17(self):
        chevrolet = Automovil(marca=self.data_factory.company(), placa="JXL67845769", modelo= self.data_factory.random_int(1886, 2022), kilometraje=self.data_factory.random_int(0, 10000), color=self.data_factory.color_name(),
                              cilindraje=self.data_factory.random_int(0, 1000), combustible="gasolina", vendido=True)
        self.session.add(chevrolet)
        self.session.commit()
        cantidadDeAutos = len(self.logica.dar_autos())
        self.logica.vender_auto(cantidadDeAutos - 1, 4000, 83.200)
        automovil = self.session.query(Automovil).filter(
            Automovil.placa == 'JXL67845769').first()
        self.assertEqual(automovil.vendido, True)
        self.assertEqual(automovil.valorVenta, 83.200)
        self.assertEqual(automovil.kilometrajeVenta, 4000)

    def test_validar_vender_auto_ok_18(self):
        validacion = self.logica.validar_vender_auto(2, 999999999.0, 999999999)
        validacion2 = self.logica.validar_vender_auto(2, 83.200, 4000)
        self.assertTrue(validacion)
        self.assertTrue(validacion2)

    def test_validar_vender_auto_fail_19(self):
        validacion = self.logica.validar_vender_auto(2, 83.200, -4000)
        validacion2 = self.logica.validar_vender_auto(2, -83.200, 4000)
        validacion3 = self.logica.validar_vender_auto(
            2, 8343141341324124.200, 4000)
        validacion4 = self.logica.validar_vender_auto(
            2, 24.200, 413413241324123)
        self.assertFalse(validacion)
        self.assertFalse(validacion2)
        self.assertFalse(validacion3)
        self.assertFalse(validacion4)
