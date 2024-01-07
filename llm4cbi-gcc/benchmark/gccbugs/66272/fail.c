struct S
{
  int f0;
  int f1;
} a[2], c;

int b;




int
main ()
{
  struct S d = { 0, 1 };

  for (b = 0; b < 2; b++)
    {
      a[b] = d;
      c = d = a[0];
    }

  if (c.f1 != 1) // ###@@@### KEEP THIS LINE
  { // ###@@@### KEEP THIS LINE
    __builtin_abort (); // ###@@@### KEEP THIS LINE
  } // ###@@@### KEEP THIS LINE

  return 0;
}