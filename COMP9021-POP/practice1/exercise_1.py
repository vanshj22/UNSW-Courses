# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.
#
# You can assume that vertical_bars() is called with nothing but
# integers at least equal to 0 as arguments (if any).


def vertical_bars(*x):
    '''
    >>> vertical_bars()
    >>> vertical_bars(0, 0, 0)
    >>> vertical_bars(4)
    *
    *
    *
    *
    >>> vertical_bars(4, 4, 4)
    * * *
    * * *
    * * *
    * * *
    >>> vertical_bars(4, 0, 3, 1)
    *
    *   *
    *   *
    *   * *
    >>> vertical_bars(0, 1, 2, 3, 2, 1, 0, 0)
          *
        * * *
      * * * * *
    '''
    max_element = 0 if not x else max(x)
    out = [[] for _ in range(max_element)]

    x=list(x)
    canprint = False
    while sum(x)>0:
      canprint=True

      for i in range (max_element-1,-1,-1):
        for idx,val in enumerate(x):
            if val>0:
              out[i].append("*")
              x[idx]-=1
            else:
              out[i].append(" ") 
      
    if sum(x)==0 and canprint:
      for row in out:
          print(' '.join(row).rstrip())    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
