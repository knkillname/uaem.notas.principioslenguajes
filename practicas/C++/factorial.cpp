#include <iostream>

int factorial(int n) {
  int resultado = 1;
  for (int i = 1; i <= n; i++) {
    resultado *= i;
  }
  return resultado;
}

int main() {
  int entrada = 0;
  std::cout << "Introduce un numero: ";
  std::cin >> entrada;
  int resultado = factorial(entrada);
  std::cout << "El factorial de " << entrada << " es " << resultado
            << std::endl;
}