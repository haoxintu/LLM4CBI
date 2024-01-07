
int printf(const char *, ...);  // ###@@@### KEEP THIS LINE

static short a = 0;
short b = -1; 
static unsigned short c = 0;






int
main ()
{
  if (a <= b)  // ###@@@### KEEP THIS LINE
  { // ###@@@### KEEP THIS LINE
    printf ("%d\n", c); // ###@@@### KEEP THIS LINE
  } // ###@@@### KEEP THIS LINE
  return 0;
}