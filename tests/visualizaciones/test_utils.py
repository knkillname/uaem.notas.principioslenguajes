"""Pruebas para materiales.visualizaciones.utils."""

import unittest
from unittest.mock import MagicMock

from materiales.visualizaciones.utils import dibujar_svg


class TestDibujarSvg(unittest.TestCase):
    """Cobertura de dibujar_svg utility."""

    def test_dibujar_svg_success(self) -> None:
        """dibujar_svg retorna SVG string cuando draw() retorna bytes."""
        mock_arbol = MagicMock()
        mock_arbol.draw.return_value = b"<svg>test</svg>"
        resultado = dibujar_svg(mock_arbol)
        self.assertEqual(resultado, "<svg>test</svg>")
        mock_arbol.draw.assert_called_once_with(format="svg", prog="dot")

    def test_dibujar_svg_none_raises_error(self) -> None:
        """dibujar_svg lanza RuntimeError si draw() retorna None."""
        mock_arbol = MagicMock()
        mock_arbol.draw.return_value = None
        with self.assertRaises(RuntimeError):
            dibujar_svg(mock_arbol)

    def test_dibujar_svg_decoding(self) -> None:
        """dibujar_svg decodifica bytes UTF-8 correctamente."""
        mock_arbol = MagicMock()
        svg_bytes = "<svg>éàü</svg>".encode("utf-8")
        mock_arbol.draw.return_value = svg_bytes
        resultado = dibujar_svg(mock_arbol)
        self.assertIn("éàü", resultado)

    def test_dibujar_svg_large_svg(self) -> None:
        """dibujar_svg maneja SVG grandes."""
        mock_arbol = MagicMock()
        # Create a large SVG content
        large_svg = "<svg>" + "A" * 10000 + "</svg>"
        mock_arbol.draw.return_value = large_svg.encode("utf-8")
        resultado = dibujar_svg(mock_arbol)
        self.assertEqual(len(resultado), len(large_svg))

    def test_dibujar_svg_special_chars(self) -> None:
        """dibujar_svg maneja caracteres especiales XML."""
        mock_arbol = MagicMock()
        svg_bytes = "<svg><text>&lt;tag&gt;</text></svg>".encode("utf-8")
        mock_arbol.draw.return_value = svg_bytes
        resultado = dibujar_svg(mock_arbol)
        self.assertIn("&lt;", resultado)
        self.assertIn("&gt;", resultado)

    def test_dibujar_svg_error_message(self) -> None:
        """RuntimeError tiene mensaje apropiado."""
        mock_arbol = MagicMock()
        mock_arbol.draw.return_value = None
        try:
            dibujar_svg(mock_arbol)
            self.fail("Should have raised RuntimeError")
        except RuntimeError as e:
            self.assertIn("SVG", str(e))


if __name__ == "__main__":
    unittest.main()
