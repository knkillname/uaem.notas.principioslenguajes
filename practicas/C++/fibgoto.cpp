#include <iostream>

int main() {
  int n_max, i = 1, j = 0;
  std::cout << "n = ";
  std::cin >> n_max;

loop:
  if (j <= n_max) goto iterate;
  goto exit;

iterate:
  std::cout << j << " ";
  j += i;
  i = j - i;
  goto loop;

exit:
  std::cout << std::endl;
  return 0;
}