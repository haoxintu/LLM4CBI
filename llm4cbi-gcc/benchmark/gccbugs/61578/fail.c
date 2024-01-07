
int printf (const char *, ...); // ###@@@### KEEP THIS LINE

volatile int a;
volatile int b;
int c;
int d;
int e;
int f;




static int
fn1 ()
{
  if (b)
    {
      d++;
      e = c || f;
    }
  return 0;
}

int
main ()
{
  for (; a < 1; a++)
    {
      fn1 ();
      continue;
    }
  printf ("%d\n", d); // ###@@@### KEEP THIS LINE
  return 0; // ###@@@### KEEP THIS LINE
}