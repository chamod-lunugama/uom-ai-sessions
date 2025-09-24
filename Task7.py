def prime(n):
    if n<2:
        return False
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True

count=0
n=0
while count<10001:
    n+=1
    if prime(n):
        count+=1
print(n)