a = [1,2,3]

def test( a ):
    del a[:]

test( a )
print a
