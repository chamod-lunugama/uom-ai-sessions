no=600851475143
divisor=2
x=[]
while no>1:
    while no%divisor==0:
        x.append(divisor)
        no/=divisor
    divisor+=1
print(max(x))
