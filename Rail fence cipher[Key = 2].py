import math


print (' Would you like to decrypt or encrypt a message?')


process = input().lower()
toprail = ''
bottomrail = ''


def decrypt(ciphertext):
 middle = math.ceil(len(ciphertext)/2)
 
 toprail = ciphertext[:middle]
 bottomrail =  ciphertext[middle:]

 plaintext = ''
 for  index in range(len(ciphertext)):
    if index %2 == 0:
      plaintext += (toprail[index // 2])

    else:
        plaintext += (bottomrail[index // 2 ])

 print(' your plaintext message is  ' + plaintext )

 
if process == "encrypt":

 print (' Please enter your plain text message ')
 plaintext =  input().lower()


 for character in plaintext:
     if not character.isalnum():
          plaintext = plaintext.replace(character, '')


 plaintext =''.join(plaintext.split(' '))

 toprail = ''
 bottomrail = ''

 for index in range (len(plaintext)):
    if  index %2 == 0:
          toprail += plaintext [index]

    else:
        bottomrail += plaintext [index]


 ciphertext = toprail + bottomrail

 print ('Your Cipher Text message is  ' + ciphertext)

   
elif process == "decrypt":

 print (' Please enter your cipher text message ')
 ciphertext =  input().lower()
 decrypt(ciphertext)

else:
    print ('invalid choice')


input ("press enter to exit")
