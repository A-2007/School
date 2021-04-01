from math import *

choice = 0 

while choice != 9 :
 choice = int (input("""
 1 – Find a hypotenuse 

 2 – Find another side 

 9 – Exit 

 Enter an option: """))

 if choice == 1 :
        a = float(input("Please enter first side:  "))
        b = float(input("Please enter second side:  "))
        h = sqrt( (a**2) + (b**2))
        print ("the hypotenuse is : ", str (h))
          
 elif choice == 2:
        a = float(input("Please enter first side:  "))
        h = float(input("Please enter the hypotenuse: "))
        b = sqrt( h**2 - a**2)
        print ("the length of the side is : ", str (b))
        
 elif choice== 9:
   print("Good bye")
 
    
 else:
  print("You must only select either 1 or 2 or press 9 to exit ")
  print("Please try again")


input (' press enter to close program ')
