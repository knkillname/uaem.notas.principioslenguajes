"""Pruebas para materiales.visualizaciones.hexadecimal."""

import unittest
from io import StringIO
from unittest.mock import patch

from materiales.visualizaciones.hexadecimal import VisorHexadecimal, _generar_traductor


class TestGenerarTraductor(unittest.TestCase):
    """Cobertura de _generar_traductor."""

    def test_generador_retorna_diccionario(self) -> None:
        """_generar_traductor retorna un diccionario."""
        traductor = _generar_traductor("·")
        self.assertIsInstance(traductor, dict)
        self.assertEqual(len(traductor), 256)

    def test_generador_no_imprimibles(self) -> None:
        """Bytes no imprimibles se mapean al carácter especial."""
        traductor = _generar_traductor("·")
        # Null byte (0) no es imprimible
        self.assertEqual(traductor[0], "·")

    def test_generador_imprimibles(self) -> None:
        """Bytes imprimibles se mapean a sí mismos."""
        traductor = _generar_traductor("·")
        # 'A' es ASCII 65
        self.assertEqual(traductor[65], "A")

    def test_generador_carac_no_imprimible_diferente(self) -> None:
        """_generar_traductor funciona con diferentes caracteres."""
        traductor = _generar_traductor("?")
        self.assertEqual(traductor[0], "?")
        self.assertEqual(traductor[65], "A")


class TestVisorHexadecimal(unittest.TestCase):
    """Cobertura de VisorHexadecimal."""

    def setUp(self) -> None:
        self.visor = VisorHexadecimal()

    def test_inicializacion_defecto(self) -> None:
        """Inicialización con valores por defecto."""
        self.assertEqual(self.visor.n_renglon, 10)
        self.assertEqual(self.visor.car_no_imprimible, "·")

    def test_inicializacion_custom(self) -> None:
        """Inicialización con valores personalizados."""
        visor = VisorHexadecimal(n_renglon=16, car_no_imprimible="?")
        self.assertEqual(visor.n_renglon, 16)
        self.assertEqual(visor.car_no_imprimible, "?")

    def test_n_renglon_setter_valido(self) -> None:
        """n_renglon setter acepta valores positivos."""
        self.visor.n_renglon = 16
        self.assertEqual(self.visor.n_renglon, 16)

    def test_n_renglon_setter_invalido(self) -> None:
        """n_renglon setter rechaza valores no positivos."""
        with self.assertRaises(ValueError):
            self.visor.n_renglon = 0
        with self.assertRaises(ValueError):
            self.visor.n_renglon = -1

    def test_car_no_imprimible_setter_valido(self) -> None:
        """car_no_imprimible setter acepta un carácter."""
        self.visor.car_no_imprimible = "?"
        self.assertEqual(self.visor.car_no_imprimible, "?")

    def test_car_no_imprimible_setter_invalido(self) -> None:
        """car_no_imprimible setter rechaza múltiples caracteres."""
        with self.assertRaises(ValueError):
            self.visor.car_no_imprimible = "ab"

    def test_car_no_imprimible_setter_vacio(self) -> None:
        """car_no_imprimible setter rechaza cadena vacía."""
        with self.assertRaises(ValueError):
            self.visor.car_no_imprimible = ""

    def test_car_no_imprimible_setter_regenera_traductor(self) -> None:
        """Cambiar car_no_imprimible regenera el traductor."""
        self.visor.car_no_imprimible = "?"
        resultado = self.visor.representar_bytes(b"\x00")
        self.assertIn("?", resultado)

    def test_representar_bytes_vacio(self) -> None:
        """representar_bytes con contenido vacío retorna cadena vacía."""
        resultado = self.visor.representar_bytes(b"")
        self.assertEqual(resultado, "")

    def test_representar_bytes_simple(self) -> None:
        """representar_bytes retorna formato correcto."""
        resultado = self.visor.representar_bytes(b"ABC")
        # Debe contener hex y caracteres separados por │
        self.assertIn("│", resultado)
        self.assertIn("41", resultado)  # 'A' en hex
        self.assertIn("42", resultado)  # 'B' en hex
        self.assertIn("43", resultado)  # 'C' en hex

    def test_representar_bytes_no_imprimibles(self) -> None:
        """representar_bytes maneja bytes no imprimibles."""
        resultado = self.visor.representar_bytes(b"\x00\x01\x02")
        # Debe contener el carácter no imprimible
        self.assertIn("·", resultado)

    def test_representar_bytes_multi_renglon(self) -> None:
        """representar_bytes genera múltiples renglones."""
        # 25 bytes con n_renglon=10 = 3 renglones
        contenido = bytes(range(25))
        resultado = self.visor.representar_bytes(contenido)
        renglones = resultado.split("\n")
        self.assertEqual(len(renglones), 3)

    def test_representar_bytes_renglon_incompleto(self) -> None:
        """representar_bytes alinea renglones incompletos."""
        # 5 bytes con n_renglon=10 - debe tener espaciado para 10
        resultado = self.visor.representar_bytes(b"ABCDE")
        # Debe contener espacios de relleno
        linea = resultado.split("│")[0]
        self.assertIn("  ", linea)  # Espacios de alineación

    def test_mostrar_bytes(self) -> None:
        """mostrar_bytes imprime el contenido sin error."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.visor.mostrar_bytes(b"test")
            output = mock_stdout.getvalue()
            self.assertIn("74", output)  # 't' en hex

    def test_representar_bytes_todos_bytes_posibles(self) -> None:
        """representar_bytes maneja todos los bytes (0-255)."""
        contenido = bytes(range(256))
        resultado = self.visor.representar_bytes(contenido)
        # Debe generar múltiples renglones
        renglones = resultado.split("\n")
        # 256 bytes / 10 por renglón = 25.6, así que 26 renglones
        self.assertEqual(len(renglones), 26)

    def test_representar_bytes_caracteres_especiales(self) -> None:
        """representar_bytes maneja caracteres especiales imprimibles."""
        resultado = self.visor.representar_bytes(b"!@#$%^&*()")
        # Todos estos son imprimibles
        for char in "!@#$%^&*()":
            self.assertIn(char, resultado)

    def test_formatear_hex_alineacion(self) -> None:
        """_formatear_hex alinea correctamente renglones incompletos."""
        # Un renglon con 5 bytes cuando n_renglon es 10
        contenido = b"ABCDE"
        resultado = self.visor.representar_bytes(contenido)
        # El hex debe estar alineado
        linea = resultado.split("│")[0]
        # 5 bytes de hex + espacios de alineación
        # Debe contener "41 42 43 44 45" + relleno
        self.assertIn("41", linea)
        self.assertIn("45", linea)

    def test_formatear_str_espacios(self) -> None:
        """_formatear_str separa caracteres con espacios."""
        contenido = b"AB"
        resultado = self.visor.representar_bytes(contenido)
        # Los caracteres deben estar separados por espacios
        partes = resultado.split("│")
        self.assertEqual(len(partes), 2)
        chars_parte = partes[1].strip()
        # Debe tener A y B separados
        self.assertEqual(len(chars_parte.split(" ")), 2)

    def test_mostrar_bytes_no_produce_error(self) -> None:
        """mostrar_bytes no lanza excepciones con entrada normal."""
        # Simplemente no debe lanzar excepción
        try:
            self.visor.mostrar_bytes(b"test content")
        except Exception as e:
            self.fail(f"mostrar_bytes lanzó {type(e).__name__}: {e}")

    def test_inicializacion_custom_valores(self) -> None:
        """Inicialización con múltiples valores personalizados."""
        visor = VisorHexadecimal(n_renglon=8, car_no_imprimible="?")
        self.assertEqual(visor.n_renglon, 8)
        self.assertEqual(visor.car_no_imprimible, "?")
        # Test that custom char is used
        resultado = visor.representar_bytes(b"\x00")
        self.assertIn("?", resultado)
        self.assertNotIn("·", resultado)


if __name__ == "__main__":
    unittest.main()
