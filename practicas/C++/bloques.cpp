#include <iostream>
int foo = 1;

void bloque_d() {
  // Bloque D
  std::cout << "Bloque D: foo=" << foo << std::endl;
}

int main() {
  // Bloque A
  std::cout << "Bloque A: foo=" << foo << std::endl;
  int foo = 2;

  {
    // Bloque B
    int foo = 3;  // Variable local a este bloque.
    std::cout << "Bloque B: foo=" << foo << std::endl;
  }

  {
    // Bloque C
    std::cout << "Bloque C: foo=" << foo << std::endl;
  }

  bloque_d();  // Llamada a la función bloque_d

  std::cout << "Bloque A: foo=" << foo << std::endl;
  return 0;
}