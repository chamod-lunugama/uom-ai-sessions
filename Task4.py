def palindrome(n):
    return str(n)==str(n)[::-1]

largest=0
a,b=0,0
for i in range(100,1000):
    for j in range(i,1000):
        product=i*j
        if palindrome(product) and product>largest:
            largest=product
            a,b=i,j
print(largest)