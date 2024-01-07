int a = 1;
int b;
int d;
short e;






int
main ()
{
  for (; b; b++)
  {
    ;
  }
  short f = a;
  int g = 15;
  e = f ? f : 1 << g;
  int h = e;
  d = h == 83647 ? 0 : h;
  if (d != 1) // ###@@@### KEEP THIS LINE
  { // ###@@@### KEEP THIS LINE
    __builtin_abort (); // ###@@@### KEEP THIS LINE
  } // ###@@@### KEEP THIS LINE
  return 0;
}