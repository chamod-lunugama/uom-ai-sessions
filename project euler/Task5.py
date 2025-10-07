def gcd(a,b):
    while b!=0:
        a,b=b,a%b
    return a

def main(a,b):
    return a*b//gcd(a,b)

n=1
for i in range(1,21):
    n=main(n,i)
print(n)