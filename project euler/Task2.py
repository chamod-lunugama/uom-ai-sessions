a,b=0,1
total=0
while a<4000000:
    a,b=b,a+b
    if a%2==1:
        total+=a
print(total)
