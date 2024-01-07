
int a;
int b;
int c[1];
int d;
int e;
int f;





void
fn1 ()
{
  for (; d < 1; d++)
    {
      if (b) 
	{
	  a = e++ && f; 
	  b = f; 
	}
      c[b] = 0;
    }
}

int
main ()
{
  fn1 ();

  if (e != 0)  // ###@@@### KEEP THIS LINE
  { // ###@@@### KEEP THIS LINE
    __builtin_abort ();  // ###@@@### KEEP THIS LINE
  } // ###@@@### KEEP THIS LINE

  return 0;
}