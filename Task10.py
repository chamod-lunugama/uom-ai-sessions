def prime(n):
    if n<2:
        return False
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True

total=0
n=0
while n<=2000000:
    if prime(n):
        total+=n
    n+=1
print(total)



