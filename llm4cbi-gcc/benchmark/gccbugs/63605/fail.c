
int printf (const char *, ...); // ###@@@### KEEP THIS LINE

int a;
int b[8] = { 2, 0, 0, 0, 0, 0, 0, 0 };
int c[8];




int
main ()
{
  int d;
  for (; a < 8; a++)
    {
      d = b[a] >> 1;
      c[a] = d != 0;
    }
  printf ("%d\n", c[0]); // ###@@@### KEEP THIS LINE
  return 0; // ###@@@### KEEP THIS LINE
}