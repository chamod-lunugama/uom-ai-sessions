n=0
total=0
sum_of_squares=0
while n<=100:
    sum_of_squares+=n**2
    total+=n
    n+=1
square_of_sum=total**2
difference=square_of_sum-sum_of_squares
print(difference)
