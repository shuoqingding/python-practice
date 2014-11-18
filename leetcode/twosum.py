
def twoSum( num, target):
    ii = 0
    jj = 0
    for i in num:
        if i > target:
            continue
        for j in num:
            if ii>=jj or j > target:
                continue
            if (i + j) == target:
                return (i,j)
            jj += 1
        ii += 1
    return (0,0)


print twoSum( [1,2,3,4], 5 )
