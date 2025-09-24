for a in range(1,1000):
    for b in range(a,1000):
        c=(a**2+b**2)**0.5
        if c.is_integer():
            if a+b+int(c)==1000:
                print(a*b*int(c))