int printf (const char *, ...); // ###@@@### KEEP THIS LINE

int a[6];
int b;
int c = 1;
int d;
short e;




void
fn1 (int p)
{
  b = a[p];
}

int
main ()
{
  a[0] = 1;
  if (c)
  {
    e--;
  }
  d = e;
  long long f = e;
  fn1 ((f >> 56) & 1);
  printf ("%d\n", b); // ###@@@### KEEP THIS LINE
  return 0; // ###@@@### KEEP THIS LINE
}