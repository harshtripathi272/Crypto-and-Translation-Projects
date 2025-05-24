# Cryptography Research Notes

This document provides foundational notes on key cryptography concepts explored during the initial phase of the internship. Understanding these principles is crucial for secure data handling and communication.

---

## Table of Contents

1.  [Introduction to Cryptography, Cryptanalysis, and Cryptology](#1-introduction-to-cryptography-cryptanalysis-and-cryptology)
2.  [Network Security Fundamentals](#2-network-security-fundamentals)
3.  [Core Principles of Cryptography](#3-core-principles-of-cryptography)
4.  [Symmetric-key Cryptography](#4-symmetric-key-cryptography)
    * [Advanced Encryption Standard (AES)](#advanced-encryption-standard-aes)
5.  [Asymmetric-key Cryptography (Public-key Cryptography)](#5-asymmetric-key-cryptography-public-key-cryptography)
    * [RSA Algorithm](#rsa-algorithm)
6.  [Hashing Algorithms](#6-hashing-algorithms)
    * [SHA-256 (Secure Hash Algorithm 256)](#sha-256-secure-hash-algorithm-256)
7.  [Digital Signatures](#7-digital-signatures)
8.  [Key Exchange](#8-key-exchange)
    * [Diffie-Hellman Key Exchange](#diffie-hellman-key-exchange)
9.  [References](#9-references)

---

## 1. Introduction to Cryptography, Cryptanalysis, and Cryptology

* **Cryptology:** The overarching field encompassing both cryptography and cryptanalysis. It is the study of secure communications.
* **Cryptography:** The art and science of concealing messages. It involves techniques for encryption (making messages unintelligible) and decryption (recovering the original message).
* **Cryptanalysis:** The art and science of breaking cryptosystems. It involves finding weaknesses in cryptographic algorithms to decrypt messages without the key.

---

## 2. Network Security Fundamentals

Network security involves protecting a network and its resources from unauthorized access, use, disclosure, disruption, modification, or destruction. It's a broad field where cryptographic principles are applied.

**Key Concepts in Network Security:**

* **Threats and Vulnerabilities:** Understanding common attacks (e.g., eavesdropping, tampering, spoofing, denial-of-service) and system weaknesses that adversaries can exploit.
* **Security Services:** How cryptographic primitives are combined to provide security services like:
    * **Authentication:** Verifying the identity of users, devices, or services.
    * **Access Control:** Restricting access to resources based on identity.
    * **Data Confidentiality:** Protecting data from unauthorized disclosure.
    * **Data Integrity:** Ensuring data has not been altered.
    * **Non-repudiation:** Preventing parties from denying actions.
* **Protocols (e.g., SSL/TLS):** Secure Sockets Layer (SSL) and its successor Transport Layer Security (TLS) are cryptographic protocols designed to provide communication security over a computer network. They are fundamental for securing web traffic (HTTPS), email, and other network applications.
    * **How they integrate cryptography:** TLS uses a combination of asymmetric cryptography (for key exchange and authentication), symmetric cryptography (for bulk data encryption), and hashing (for integrity checks).
* **Socket Programming (Networking Context):** Sockets are endpoints for communication between two programs on a network. While sockets themselves do not provide security, they are the underlying mechanism upon which secure communication protocols (like TLS) are built.
    * **Role in Cryptography:** When implementing cryptographic communication, socket programming is used to establish the raw connection, over which encrypted data is then sent and received. Libraries like `ssl` in Python wrap standard sockets to provide TLS functionality.

---

## 3. Core Principles of Cryptography

Cryptography is the practice and study of techniques for secure communication in the presence of adversarial behavior. Its primary goals are:

* **Confidentiality (Secrecy):** Ensuring that information is accessible only to those authorized to have access. (Achieved through encryption).
* **Integrity:** Ensuring that information has not been altered or destroyed in an unauthorized manner. (Achieved through hashing and digital signatures).
* **Authentication:** Ensuring that the origin of information or the identity of a user is genuine. (Achieved through digital signatures, passwords, certificates).
* **Non-repudiation:** Ensuring that a party cannot deny having performed an action. (Achieved through digital signatures).

---

## 4. Symmetric-key Cryptography

In symmetric-key cryptography, the same secret key is used for both encryption and decryption. Both the sender and receiver must possess this identical key.

**Characteristics:**

* **Speed:** Generally much faster than asymmetric-key algorithms.
* **Simplicity:** Simpler to implement.
* **Key Distribution Problem:** The biggest challenge is securely distributing the shared secret key to all authorized parties before any communication can begin.

### Advanced Encryption Standard (AES)

* **Description:** AES is a block cipher, meaning it encrypts data in fixed-size blocks (128 bits). It supports key sizes of 128, 192, or 256 bits. It is the current encryption standard adopted by the U.S. government and widely used worldwide.
* **Algorithm:** AES uses a series of substitutions, transpositions, and mixing operations (mix columns, shift rows, sub bytes) over multiple rounds to scramble the plaintext.
* **Strengths:** Highly secure when implemented correctly with appropriate key management. Very efficient in software and hardware.
* **Use Cases:** Encrypting files, database encryption, SSL/TLS (for bulk data encryption after key exchange), VPNs.

---

## 5. Asymmetric-key Cryptography (Public-key Cryptography)

In asymmetric-key cryptography, two different but mathematically linked keys are used: a **public key** and a **private key**.

* The **public key** can be shared with anyone.
* The **private key** must be kept secret by its owner.

**Characteristics:**

* **Key Pair:** Each participant has a unique public/private key pair.
* **Functionality:** If data is encrypted with a public key, it can only be decrypted with the corresponding private key. Conversely, if data is signed with a private key, it can be verified with the corresponding public key.
* **Solves Key Distribution:** Eliminates the need for pre-sharing a secret key.
* **Speed:** Slower than symmetric-key algorithms.

### RSA Algorithm

* **Description:** RSA (Rivest–Shamir–Adleman) is one of the first public-key cryptosystems and is widely used for secure data transmission. It relies on the computational difficulty of factoring large integers.
* **Algorithm:**

    1.  **Key Generation:** Involves selecting two large prime numbers, calculating their product ($n$), and finding a pair of exponents ($e$ and $d$) such that $(e \cdot d) \pmod{\phi(n)} = 1$, where $\phi(n)$ is Euler's totient function.

        * Public Key: $(e, n)$
        * Private Key: $(d, n)$
    2.  **Encryption:** Ciphertext $C = M^e \pmod{n}$, where $M$ is the plaintext.
    3.  **Decryption:** Plaintext $M = C^d \pmod{n}$.
* **Strengths:** Widely adopted, proven security (assuming sufficiently large key sizes). Can be used for both encryption and digital signatures.
* **Use Cases:** Secure email (PGP/GPG), digital signatures, key exchange (to securely exchange symmetric keys for bulk data encryption in protocols like SSL/TLS).

---

## 6. Hashing Algorithms

A hashing algorithm takes an input (or 'message') and returns a fixed-size string of bytes, typically a hexadecimal number, called a **hash value**, **hash code**, **digest**, or **fingerprint**.

**Characteristics:**

* **One-Way Function:** It's computationally infeasible to reverse the process (i.e., to find the original input from the hash value).
* **Deterministic:** The same input will always produce the same hash value.
* **Fixed Output Size:** The output hash has a fixed length, regardless of the input size.
* **Collision Resistance:** It should be computationally infeasible to find two different inputs that produce the same hash value (a "collision").

### SHA-256 (Secure Hash Algorithm 256)

* **Description:** SHA-256 is a member of the SHA-2 (Secure Hash Algorithm 2) family. It produces a 256-bit (32-byte) hash value.
* **Strengths:** Widely considered secure for most applications, computationally efficient.
* **Weaknesses:** Not vulnerable to pre-image or second pre-image attacks for practical purposes. Collisions are theoretically possible but extremely difficult to find. MD5 is considered cryptographically broken.
* **Use Cases:**

    * **Data Integrity:** Verifying that a file has not been altered (e.g., software downloads).
    * **Password Storage:** Storing hashes of passwords instead of plaintext passwords.
    * **Blockchain/Cryptocurrencies:** Fundamental to Bitcoin and other cryptocurrencies for linking blocks and verifying transactions.

---

## 7. Digital Signatures

Digital signatures provide authentication, integrity, and non-repudiation. They are analogous to handwritten signatures but are cryptographically secure.

**How it works:**

1.  **Hashing:** The sender computes a hash of the message.
2.  **Encryption (with Private Key):** The sender encrypts this hash value using their *private key*. This encrypted hash is the digital signature.
3.  **Sending:** The sender sends the original message along with the digital signature.
4.  **Verification:** The receiver:

    * Computes a hash of the received message.
    * Decrypts the received digital signature using the sender's *public key*.
    * Compares their computed hash with the decrypted hash. If they match, the message's integrity is confirmed, and the sender's authenticity is verified (non-repudiation).

**Strengths:** Provides strong assurances about message origin and integrity.
**Use Cases:** Software distribution (verifying integrity of downloaded files), secure email, verifying digital certificates.

---

## 8. Key Exchange

Key exchange is the process of securely exchanging cryptographic keys between two parties who wish to communicate privately.

### Diffie-Hellman Key Exchange

* **Description:** The Diffie-Hellman (DH) key exchange protocol allows two parties to establish a shared secret key over an insecure communication channel without ever directly exchanging the key itself. It is not an encryption method but a key agreement protocol.
* **Algorithm (Simplified):**

    1.  **Public Parameters:** Alice and Bob agree on two public numbers: a large prime number ($p$) and a base ($g$).
    2.  **Private Selections:**

        * Alice chooses a secret integer ($a$).
        * Bob chooses a secret integer ($b$).
    3.  **Public Computations:**

        * Alice computes $A = g^a \pmod{p}$ and sends $A$ to Bob.
        * Bob computes $B = g^b \pmod{p}$ and sends $B$ to Alice.
    4.  **Shared Secret Computation:**

        * Alice computes $S = B^a \pmod{p}$.
        * Bob computes $S = A^b \pmod{p}$.
        * Crucially, $B^a \pmod{p} = (g^b)^a \pmod{p} = g^{ab} \pmod{p}$ and $A^b \pmod{p} = (g^a)^b \pmod{p} = g^{ab} \pmod{p}$. Thus, Alice and Bob arrive at the same shared secret $S$.
* **Strengths:** Allows secure key establishment without prior shared secrets.
* **Weaknesses:** Susceptible to a "man-in-the-middle" (MITM) attack if the public values ($A$ and $B$) are not authenticated. Often used in conjunction with digital signatures or certificates to prevent MITM.
* **Use Cases:** Widely used in SSL/TLS, SSH, and VPNs to establish the session key for symmetric encryption.

---

## 9. References

This section lists the key resources utilized for understanding and implementing the cryptographic concepts.

* **Book:**
    * `Cryptography and Network Security - Principles and Practice (Stallings William)` (Covers various cryptographic algorithms, network security protocols like SSL/TLS, and principles of secure communication.)
    * `SSL and TSL Essentials - Securing the Web (Stephen A. Thomas)` (Focuses specifically on the practical application of cryptography in securing web communication.)
* **Key Topics Explored (from video resources):**
    * **Cryptography and Network Security Concepts:** Including topics like Message Authentication Codes (MAC), detailed explanations of AES and RSA algorithms, and Diffie-Hellman key exchange.
    * **Python Socket Programming:** Understanding the foundational aspects of network communication, including client-server models, sending/receiving data, and establishing connections, which forms the basis for building secure communication channels.
* **Online Documentation/Tutorials:**
    * **The Python Cryptography Authority (PyCA) Documentation:** Essential for understanding the `cryptography` library. [https://cryptography.io/en/latest/](https://cryptography.io/en/latest/)
    * **OpenSSL Project Documentation:** For broader context on cryptographic standards and tools. [https://www.openssl.org/docs/](https://www.openssl.org/docs/)
    * **Khan Academy - Cryptography:** Provides accessible explanations of foundational concepts. [https://www.khanacademy.org/computing/computer-science/cryptography](https://www.khanacademy.org/computing/computer-science/cryptography)
    * **GeeksforGeeks - Cryptography:** Numerous articles on specific algorithms and concepts. [https://www.geeksforgeeks.org/cryptography-basics/](https://www.geeksforgeeks.org/cryptography-basics/)