short a = -1;
int b;
char c;







int
main ()
{
  c = a;
  b = a | c;
  if (b != -1)  // ###@@@### KEEP THIS LINE
  { // ###@@@### KEEP THIS LINE
    __builtin_abort ();  // ###@@@### KEEP THIS LINE
  } // ###@@@### KEEP THIS LINE
  return 0;
}