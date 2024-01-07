int printf (const char *, ...);  // ###@@@### KEEP THIS LINE

int a, b, c = 1, d = 1, e;







int
fn1 (int p1)
{
  char g, h;
  int i, j;

  for (;;)
    {
      if (c)
	h = d;
      g = h < p1 ? h : 0; 
      i = (char) ((g - 120) ^ 1);
      j = i > 97;
      if (a - j) // ###@@@### KEEP THIS LINE
	    printf ("%d\n", 0); // ###@@@### KEEP THIS LINE
      if (!b) // ###@@@### KEEP THIS LINE
	return e; // ###@@@### KEEP THIS LINE
    }
}

int
main ()
{
  fn1 (2);
  return 0;
}
