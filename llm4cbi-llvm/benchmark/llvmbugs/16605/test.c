int a, b, d, e, *f = &b, g, i;
char c;

int
foo (int p1, long long p2)
{
  return p2 == 0 ? 0 : p1 % p2;
}

void
bar (int p)
{
 lbl:
  if (*f)
    g = 0;
  int **l = &f;
  *l = 0;
  for (; i < 1; i++)
    {
      if (i)
	goto lbl;
      if (foo (2, d || p))
	{
	  int **m = &f;
	  *m = &e;
	}
    }
}

int
main ()
{
  bar (&c == (void *)&a);
  return 0;
}
