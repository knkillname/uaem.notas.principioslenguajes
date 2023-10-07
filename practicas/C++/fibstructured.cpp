#include <iostream>

int main() {
  int n_max;
  std::cout << "n = ";
  std::cin >> n_max;

  int i = 1, j = 0;
  while (j <= n_max) {
    std::cout << j << " ";
    j += i;
    i = j - i;
  }
  std::cout << std::endl;
  return 0;
}