

int a = 128;
int b;






int
fn1 (char p1, int p2)
{
  return p1 < 0 || p1 > 1 >> p2 ? 0 : p1 << 1;
}

int
fn2 ()
{
  char c = a;
  b = fn1 (c, 1);
  if ((128 | c) < 0 ? 1 : 0)
  {
    return 1;
  }
  return 0;
}

int
main ()
{
  if (fn2 () != 1) // ###@@@### KEEP THIS LINE
  { // ###@@@### KEEP THIS LINE
    __builtin_abort (); // ###@@@### KEEP THIS LINE
  } // ###@@@### KEEP THIS LINE

  return 0;
}