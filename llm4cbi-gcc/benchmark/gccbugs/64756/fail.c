

int a;
int *tmp;
int **c = &tmp;
volatile int d;
static int *volatile *e = &tmp;
unsigned int f; 


static void
fn1 (int *p)
{
  int g;
  for (; f < 1; f++)
  {
    for (g = 1; g >= 0; g--)
    {
	    d || d;
	    *c = p;

	    if (tmp != &a) // ###@@@### KEEP THIS LINE
	    { // ###@@@### KEEP THIS LINE
        __builtin_abort ();  // ###@@@### KEEP THIS LINE
      } // ###@@@### KEEP THIS LINE

	    *e = 0;
    }
  }
}

int
main ()
{
  fn1 (&a);
  return 0;
}