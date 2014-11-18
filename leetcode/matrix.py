a = [1,1,1,1,1]
b = [ [], [], [], [], [] ]


for i in range(5):
    for j in range(5):
        b[i].append(None)

for i in range(5):
    sum = a[i]
    for j in range(i+1,5):
        sum = sum + a[j]
        b[i][j] = sum

print b
