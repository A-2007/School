def triangle(b,h):
  area = b*h /2
  return area
  
  
base = float(input("Enter the length of the base:  "))
height = float(input("Enter the height:   "))

area = triangle(base,height)

print("The area of this triangle is " + str(area))
