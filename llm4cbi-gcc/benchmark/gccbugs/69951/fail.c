int a = 1, c = 1;
extern int b __attribute__((alias("a")));
extern int d __attribute__((alias("c")));







int main(int argc) {
  int *p, *q;
  if (argc)
    p = &c, q = &d;
  else
    p = &b, q = &d;
  *p = 1;
  *q = 2;
  if (*p == 1) // ###@@@### KEEP THIS LINE
    __builtin_abort(); // ###@@@### KEEP THIS LINE
  return 0;
}

