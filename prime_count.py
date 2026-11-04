 def prime_count(n):
     if n<= 1 :
         return False
     i = 2
     while i < n:
         if n % i == 0:
             return False
         i+= 1
     return f'{n} is prime number'
