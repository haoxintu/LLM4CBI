int printf(const char *, ...);
struct S2 {
  int f2;
  char f4;
  int f5;
  char f6;
} a;




int main() {
  struct S2 b[][1] = {3, 0, 3, 4, 3, 0, 3, 4, 3, 0, 3, 4, 3, 0, 3, 4, 3,
                      0, 3, 4, 3, 0, 3, 4, 3, 0, 3, 4, 3, 0, 3, 4, 3, 0,
                      3, 4, 3, 4, 7, 7, 3, 5, 0, 3, 4, 7, 7, 3, 5, 0, 3,
                      4, 3, 4, 7, 7, 3, 5, 0, 3, 4, 7, 7, 3, 5, 0, 3, 4};
  a = b[4][0];
  b[4][0].f4 &printf("%d\n", a.f6); // ###@@@### KEEP THIS LINE
  return 0; // ###@@@### KEEP THIS LINE
}
