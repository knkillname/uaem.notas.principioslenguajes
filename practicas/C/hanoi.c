#include <stdio.h>

/*
    Mover n_discos discos de la torre "A" a la
    torre "C" usando "B" como intermedia.
*/
void hanoi(int A, int B, int C, int n_discos) {
  if (n_discos <= 0) {
    return;  // Caso base.
  }
  hanoi(A, C, B, n_discos - 1);
  printf("Mover de %d a %d.\n", A, C);
  hanoi(B, A, C, n_discos - 1);
}

int main(void) {
  int n_discos;
  printf("n = ");
  scanf("%d", &n_discos);
  hanoi(1, 2, 3, n_discos);
}
