#include <iostream>

#include "geometria.hpp"

int main() {
  double lado = 0.0;
  std::cout << "Introduce el lado: " << std::endl;
  std::cin >> lado;
  double resultado = area_cuadrado(lado);
  std::cout << "El área del cuadrado es " << resultado << std::endl;
  return 0;
}