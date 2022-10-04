import random
import math

#Create the possible prime number candidates between 1M and 10M 
#These will be used as input in fermats_theorem
def create_candidates(n = 1000000):
    candidates = []
    x = 0
    for i in range(100):
        x = random.randint(n, n * 10)
        if x%2 != 0 and x%3 != 0 and x%5 != 0 and x%7 != 0 and x%11 != 0:
            candidates.append(x)
    return candidates

#Fermat's Little theorem that accepts a list of possible prime numbers
def fermats_theorem(candidates = []):
    primes = []
    n = 10

    while len(primes) < n:
        for i in candidates:
            for k in range(20): #performs Fermat's test 20 times
                a = random.randint(2, i//2) #Find an 'a' to perform Fermat's Theorem
                while math.gcd(a, i) != 1: #if gcd is not one, the 'a' and 'i' are not relatively prime
                    a = random.randint(2, i//2)
                if pow(a , i - 1, i) == 1: #if the number passes Fermat's Test then add it to primes
                    primes.append(i)
                break
    
    #Set our p and q to our two prime numbers and return them
    p = primes[0]
    q = primes[1]
    return(p, q)

#the requirements for e are that it must be less than phi and it must be relatively prime to phi
def generate_e(phi):
    e_is_empty = True
    while(e_is_empty):
        x = random.randint(2, phi-1) #e must be in the range of phi
        if math.gcd(x, phi) == 1: #if e and phi are relatively prime, they're gcd must be 1
            e_ = x
            e_is_empty = False
        else:
            continue

    return e_

#Euclid's extended algorithm that uses mod inverse
def eeagcd(a, b):
    if a == 0:
            return (b, 0, 1)
    (g, x1, y1) = eeagcd(b % a, a)
    x = y1 - (b//a) * x1
    y = x1

    return g,x,y

#Modular inverse
def modular_inverse(a,b):
    g,x,y = eeagcd(a,b)
    if g != 1:
        raise Exception("No modular inverse")
    else: 
        return x % b    

#uses eeagcd to create the private key
def generate_d(phi,e):
    d = modular_inverse(e,phi)
    return d

#this takes each individual character and finds its ASCII correspondence
#it then adds it to the list message_in_ascii
def message_to_ascii(message_in_char):
    message_in_ascii = []
    message_in_char = message_in_char.upper()
    for i in message_in_char:
        message_in_ascii.append(ord(i))

    return message_in_ascii

#M is the message (in ASCII) to encrypt
#N and e are the public key
def encrypt(M, e, N):
    encryted_message = []
    for i in M:
        encryted_message.append(pow(i, e, N))

    return encryted_message

#C is a ciphered message in the form of a list
#it first decrpyts the element in ASCII and then changes it to its associated char
def decrypt(C, d, N):
    decrypted_message = ""
    for i in C:
        element_in_ascii = (pow(i, d, N))
        decrypted_message += chr(element_in_ascii)

    return decrypted_message

#M is the message (in ASCII) to encrypt
#N and d are used as keys 
#d must be kept private
def create_digital_signature(M, d, N):
    encryted_message = []
    for i in M:
        encryted_message.append(pow(i, d, N))

    return encryted_message
        
#Authenticates the digital signature 
#Accepts the encrypted signature, e, N, the plaintext and the representative number(index) of the chosen signature
def authenticate_signature(encrypted_signature, e, N, plaintext, index):

    #send our encrypted signature into our decrypt function
    decrypted_signature = decrypt(encrypted_signature[index - 1], e, N)
    #Text we are comparing our decrytped signature to
    text_to_compare = plaintext[index - 1]

    #If decrypted signature matches our plaintext message then we return True, else return False
    if decrypted_signature == text_to_compare.upper():
        return True
    else: 
        return False


#Create our list of possible candidate prime numbers
candidates = create_candidates()

#Assign our return variables to p and q as they should be
p, q = fermats_theorem(candidates)

#Create our N
N = p*q

#Create our phi
phi = (p-1)*(q-1)

#Create our e
e = generate_e(phi)

#Generate our public keys
public_key = [N, e]

#Generate d
d = generate_d(phi, e)

#Our frontend begins here
a = True
encryption_list = []
plaintext_signature_list = []
signature_list = []
signature_validity = True
print("RSA Keys Have Been Generated.")

#While a is true display our prompt for the user which controls the outside most loop
while(a):
    print("\nPlease Select Your User Type:")
    print("\t1. A public user")
    print("\t2. The owner of the keys")
    print("\t3. Exit program")
    print("Enter Your Choice: ", end = '')

    choice = int(input())

    #Match choice tree that allows for the selection of the proper choice from the previous prompt
    match choice:

        #Case 1 is for the public user
        case 1:
            b = True
            
            #Second while loop that controls the loop for the public user
            while(b):
                
                print("\nAs a public user, what would you like to do?")
                print("\t1. Send an encrypted message " )
                print("\t2. Authenticate a digital signature ")
                print("\t3. Exit")
                print("Choose One: ", end = "")
                choice_case_1 = int(input())

                #Match choice tree that allows for the selection of the proper choice from the public user prompt
                match choice_case_1:

                        #Send encrypted message
                        case 1:
                            our_string = (input("Enter a message: "))
                            message_to_encrypt = message_to_ascii(our_string) #the inputted string is transformed to ASCII 
                            encryption_list.append(encrypt(message_to_encrypt,e,N)) #message encrypted
                            print("Message encrypted and sent")

                        #Authenticate the digital signatures
                        case 2:
                            if len(plaintext_signature_list) == 0: #if no signatures tell the user
                                print("There are no signatures to authenticate.")
                            else:
                                print("The following messages are available: ")#print the messages the user can authenticate
                                for i in range(len(plaintext_signature_list)):
                                    print(str(i + 1) + ". " + str(plaintext_signature_list[i]))
                                print("Choose One: ", end = "")
                                choose_message = int(input())
                                signature_validity = authenticate_signature(signature_list, e, N, plaintext_signature_list, choose_message)
                                    
                                #notify the user of the signature validity
                                if signature_validity == True:
                                    print("Signature is valid.")
                                else:
                                    print("Signature is not valid")

                        #exit the public user loop
                        case 3:
                            b = False

        #Case 2 is for the owner of the keys
        case 2:

            c = True
            
            #While the user is the owner of the keys continue allowing for the choice to use the below actions
            while(c):
                print("\nAs the owner of the keys, what would you like to do?")
                print("\t1. Decrypt a received message " )
                print("\t2. Digitally sign a message ")
                print("\t3. Exit")
                print("Choose One: ", end = "")
                choice_case_2 = int(input())
                

                match choice_case_2:

                    #Case 1: Decrypt the received message
                    case 1:
                        print("\nThe following messages are available")
                        for i in range(len(encryption_list)): #print the list of the encrypted messages and their length
                            print(str(i + 1) + ". " + "length = " + str(len(encryption_list[i])))
                        
                        print("Choose One: ", end = "")
                        choose_message = int(input())

                        for i in range(len(encryption_list)): #allow for the decryption of the chosen message and print it
                            if choose_message == i + 1:
                                decrypted_message = decrypt(encryption_list[i], d, N)
                                print("Decrypted Message: " + decrypted_message)
                    
                    #Case 2: Create a Digital Signature
                    case 2:
                        message = input("Enter a message: ") #allow for input of our message
                        plaintext_signature_list.append(message) #append our plaintext message to the plaintext signature list
                        message = message_to_ascii(message) #convert our plaintext message to ASCII
                        signature_list.append(create_digital_signature(message, d, N)) #append our digital signature to our list of digital signatures
                        print("Message signed and sent")

                    #Exit the owner of the keys loop
                    case 3:
                        c = False

        #Case 3: Exit the entire program
        case 3:
            print("Bye for Now!")
            a = False
