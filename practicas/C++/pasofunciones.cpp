// Este código ejemplifica cómo pasar una función
// como argumento a otra función.

#include <iostream>
using namespace std;

// Calcular el tiempo que toma la ejecución de la función func
// que no recibe parámetros
double tiempo(void (*func)()) {
  clock_t t1, t2;
  t1 = clock();
  func();
  t2 = clock();
  return (double)(t2 - t1) / CLOCKS_PER_SEC;
}

// Función de ejemplo, el n-ésimo número de Fibonacci
int fib(int n) {
  if (n < 2)
    return n;
  else
    return fib(n - 1) + fib(n - 2);
}

void llamador_fib() {
  int n = 40;
  cout << "fib(" << n << ") = " << fib(n) << endl;
}

int main() {
  int n = 40;
  double total = tiempo(llamador_fib);
  cout << "Tiempo de ejecución de fib(" << n << "): " << total << endl;
}
