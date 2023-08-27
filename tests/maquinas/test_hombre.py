import itertools
import unittest

from materiales.maquinas.hombre import (
    ComputadoraDetenida,
    ComputadoraHombrePequenno,
    Estado,
)


class TestCHP(unittest.TestCase):
    """Pruebas unitarias para la clase ComputadoraHombrePequenno."""

    def test_detener(self):
        """Verificar que la computadora se detiene correctamente."""
        computadora = ComputadoraHombrePequenno()
        computadora.detener()
        self.assertEqual(computadora.estado, Estado.DETENIDA)

    def test_reiniciar(self):
        """Verificar que la computadora se reinicia correctamente."""
        computadora = ComputadoraHombrePequenno()
        computadora.reiniciar()
        self.assertEqual(computadora.estado, Estado.ACTIVADA)
        self.assertEqual(list(computadora.memoria), [0] * 100)
        self.assertEqual(computadora.acumulador, 0)
        self.assertEqual(list(computadora.entrada), [])
        self.assertEqual(list(computadora.salida), [])

    def test_cargar_programa(self):
        """Verificar que la computadora carga correctamente."""
        computadora = ComputadoraHombrePequenno()
        computadora.cargar_programa([1, 2, 3])
        self.assertEqual(list(computadora.memoria), [1, 2, 3] + [0] * 97)
        computadora.memoria = [999] * 100
        computadora.cargar_programa([1, 2, 3])
        self.assertEqual(list(computadora.memoria), [1, 2, 3] + [0] * 97)

    def test_cargar_entrada(self):
        """Verificar que la computadora carga la entrada correctamente."""
        computadora = ComputadoraHombrePequenno()
        computadora.cargar_entrada([1, 2, 3])
        self.assertEqual(list(computadora.entrada), [1, 2, 3])
        computadora.entrada = [999] * 100
        computadora.cargar_entrada([1, 2, 3])
        self.assertEqual(list(computadora.entrada), [1, 2, 3])

    def test_op_hlt(self):
        """Verificar que la computadora se detiene correctamente."""
        computadora = ComputadoraHombrePequenno()
        with self.assertRaises(ComputadoraDetenida):
            computadora.transicion(ignorar_detener=False)
        self.assertEqual(computadora.estado, Estado.DETENIDA)

    def test_op_add(self):
        """Verificar que la computadora suma correctamente."""
        sumandos = [0, -1, 1, 2, -2, 3, -3, 97, -97]
        pruebas = itertools.product(sumandos, repeat=2)
        for acum, oper in pruebas:
            with self.subTest(f"{acum} + {oper}"):
                computadora = ComputadoraHombrePequenno()
                computadora.acumulador = acum
                computadora.memoria[0] = 101
                computadora.memoria[1] = oper
                computadora.transicion()
                self.assertEqual(computadora.acumulador, acum + oper)

        with self.subTest("Overflow positivo"):
            computadora = ComputadoraHombrePequenno()
            computadora.acumulador = 999
            computadora.memoria[0:2] = [101, 1]
            with self.assertRaises(OverflowError):
                computadora.transicion()

        with self.subTest("Overflow negativo"):
            computadora = ComputadoraHombrePequenno()
            computadora.acumulador = -999
            computadora.memoria[0:2] = [101, -1]
            with self.assertRaises(OverflowError):
                computadora.transicion()

    def test_op_sub(self):
        """Verificar que la computadora resta correctamente."""
        minuendos = [0, -1, 1, 2, -2, 3, -3, 97, -97]
        pruebas = itertools.product(minuendos, repeat=2)
        for acum, oper in pruebas:
            with self.subTest(f"{acum} - {oper}"):
                computadora = ComputadoraHombrePequenno()
                computadora.acumulador = acum
                computadora.memoria[0] = 201
                computadora.memoria[1] = oper
                computadora.transicion()
                self.assertEqual(computadora.acumulador, acum - oper)

        with self.subTest("Overflow positivo"):
            computadora = ComputadoraHombrePequenno()
            computadora.acumulador = 999
            computadora.memoria[0:2] = [201, -1]
            with self.assertRaises(OverflowError):
                computadora.transicion()

        with self.subTest("Overflow negativo"):
            computadora = ComputadoraHombrePequenno()
            computadora.acumulador = -999
            computadora.memoria[0:2] = [201, 1]
            with self.assertRaises(OverflowError):
                computadora.transicion()

    def test_op_sta(self):
        """Verificar que la computadora almacena correctamente."""
        valores = [0, -1, 1, -999, 999]
        for posicion in range(1, 100):
            for valor in valores:
                with self.subTest(f"{posicion} <- {valor}"):
                    computadora = ComputadoraHombrePequenno()
                    computadora.acumulador = valor
                    computadora.memoria[0] = 300 + posicion
                    computadora.transicion()
                    self.assertEqual(computadora.memoria[posicion], valor)

    def test_op_lda(self):
        """Verificar que la computadora carga correctamente."""
        valores = [0, -1, 1, -999, 999]
        for posicion in range(1, 100):
            for valor in valores:
                with self.subTest(f"{posicion} -> {valor}"):
                    computadora = ComputadoraHombrePequenno()
                    computadora.memoria[posicion] = valor
                    computadora.memoria[0] = 500 + posicion
                    computadora.transicion()
                    self.assertEqual(computadora.acumulador, valor)

    def test_op_bra(self):
        """Verificar que la computadora salta correctamente."""
        for posicion in range(1, 100):
            with self.subTest(f"{posicion}"):
                computadora = ComputadoraHombrePequenno()
                computadora.memoria[0] = 600 + posicion
                computadora.transicion()
                self.assertEqual(computadora.contador, posicion)

    def test_op_brz(self):
        """Verificar que la computadora salta correctamente."""
        acumuladores = [0, -1, 1]
        for posicion in range(1, 100):
            for acum in acumuladores:
                with self.subTest(f"{posicion} si {acum} == 0"):
                    computadora = ComputadoraHombrePequenno()
                    computadora.acumulador = acum
                    computadora.memoria[0] = 700 + posicion
                    computadora.transicion()
                    esperada = posicion if acum == 0 else 1
                    self.assertEqual(computadora.contador, esperada)

    def test_op_brp(self):
        """Verificar que la computadora salta correctamente."""
        acumuladores = [0, -1, 1]
        for posicion in range(1, 100):
            for acum in acumuladores:
                with self.subTest(f"{posicion} si {acum} >= 0"):
                    computadora = ComputadoraHombrePequenno()
                    computadora.acumulador = acum
                    computadora.memoria[0] = 800 + posicion
                    computadora.transicion()
                    esperada = posicion if acum > 0 else 1
                    self.assertEqual(computadora.contador, esperada)

    def test_op_in(self):
        """Verificar que la computadora lee correctamente."""
        valores = [0, -1, 1, -999, 999]
        for valor in valores:
            with self.subTest(f"{valor}"):
                computadora = ComputadoraHombrePequenno()
                computadora.cargar_entrada([valor])
                computadora.memoria[0] = 901
                computadora.transicion()
                self.assertEqual(computadora.acumulador, valor)

    def test_op_out(self):
        """Verificar que la computadora escribe correctamente."""
        valores = [0, -1, 1, -999, 999]
        for valor in valores:
            with self.subTest(f"{valor}"):
                computadora = ComputadoraHombrePequenno()
                computadora.acumulador = valor
                computadora.memoria[0] = 902
                computadora.transicion()
                self.assertEqual(list(computadora.salida), [valor])
