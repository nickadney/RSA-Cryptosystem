# RSA-Cryptosystem
This is an academic project completed for an Algorithms course. It utilizes algorithms such as Fermat's Little Theorem, Euclidean Algorithm and the Extended Euclidean Algorithm, and Fast Modular Exponentiation. These are all O(log n) and therefore are highly efficient. 

This program begins by generating a list of possible prime numbers. We then further test the primality using Fermat's Little Theorem. Upon gathering two prime numbers, we can generate a public key, consisting of N and e, used to encrypt a message and authenticate a digital signature. Finding the multiplicative inverse of e allows us to find its counterpart, d. d makes up the private key used to decrypt and create a digital signature. 

The program utilizes a simple CLI to perform. However, the real magic is in the math behind it all. 
