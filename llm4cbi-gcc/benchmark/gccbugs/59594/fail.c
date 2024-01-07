int printf (const char *, ...); // ###@@@### KEEP THIS LINE

int a;
static int b[7];





int
main ()
{
  for (a = 5; a >= 0; a--)
    {
      b[a + 1] = b[a];
      b[a] = 1;
    }
  printf ("%d\n", b[1]); // ###@@@### KEEP THIS LINE
  return 0;
}
