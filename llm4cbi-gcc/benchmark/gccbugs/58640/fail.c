int a;
int b;
int c;
int d = 1;
int e;





static signed char
foo ()
{
  int f;
  int g = a;

  for (f = 1; f < 3; f++)
  {
    for (; b < 1; b++)
      {
        if (d)
        {
          for (c = 0; c < 4; c++)
          {
            for (f = 0; f < 3; f++)
              {
                for (e = 0; e < 1; e++)
                {
                  a = g;
                }
                if (f)
                {
                  break;
                }
              }
          }
        }
        else if (f)
        {
          continue;
        }
        return 0;
      }
  }
  return 0;
}

int
main ()
{
  foo ();
  return 0;
}