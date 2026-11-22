# RSA

p, q, e = 61, 53, 17
n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
print("Public key:", (e, n), " Private key:", (d, n))

m = int(input("Enter integer message (< n): "))
if not 0 <= m < n:
    print("Message must be between 0 and", n - 1)
else:
    c = pow(m, e, n)
    print("Encrypted:", c)
    print("Decrypted:", pow(c, d, n))

# RSA - PSS
import hashlib, os
from sympy import randprime

K = 128


def H(b):
    return hashlib.sha256(b).digest()


def mgf1(seed, length):
    output = b''
    counter = 0
    while len(output) < length:
        output += H(seed + counter.to_bytes(4, 'big'))
        counter += 1
    return output[:length]


def xor(a, b):
    result = b''
    for i in range(len(a)):
        result += bytes([a[i] ^ b[i]])
    return result


def keygen(e=65537):
    while True:
        p = randprime(3 * 2**510, 2**512)
        q = randprime(3 * 2**510, 2**512)
        phi = (p - 1) * (q - 1)
        if p != q and phi % e != 0:
            d = pow(e, -1, phi)
            n = p * q
            return e, d, n


def sign(m, d, n):
    salt = os.urandom(32)
    m_hash = H(m)
    m_dash = bytes(8) + m_hash + salt
    h = H(m_dash)
    ps = bytes(K - 66)
    db = ps + b'\x01' + salt
    masked_db = xor(db, mgf1(h, K - 33))
    first_byte = masked_db[0] & 0x7F
    masked_db = bytes([first_byte]) + masked_db[1:]
    em = masked_db + h + b'\xbc'
    em_int = int.from_bytes(em, 'big')
    return pow(em_int, d, n)


def verify(m, s, e, n):
    em_int = pow(s, e, n)
    em = em_int.to_bytes(K, 'big')
    if em[-1] != 0xbc:
        return False
    masked_db = em[:K - 33]
    h = em[K - 33:K - 1]
    db = xor(masked_db, mgf1(h, K - 33))
    if db[K - 66] != 1:
        return False
    salt = db[-32:]
    m_dash = bytes(8) + H(m) + salt
    return H(m_dash) == h


e, d, n = keygen()
message = input("Enter a message to sign: ").encode()
sig = sign(message, d, n)
print("Signature:", sig)
print("Verified:", verify(message, sig, e, n))

tampered = message + b"!"
print("\nModified message:", tampered.decode())
print("Verified:", verify(tampered, sig, e, n))

# DH - diffie hellman
import random

p, g = 23, 5
a = random.randint(2, p - 2)
b = random.randint(2, p - 2)
A = pow(g, a, p)
B = pow(g, b, p)
print("Public: p =", p, " g =", g)
print("Alice: private a =", a, " public A =", A)
print("Bob : private b =", b, " public B =", B)

K_A = pow(B, a, p)
K_B = pow(A, b, p)
print("Alice's shared key:", K_A)
print("Bob's shared key:", K_B)
print("Keys match:", K_A == K_B)


# MONO ALPHABETIC CIPHER BREAK (Caesar)
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def caesar(text, k):
    result = ''
    for ch in text:
        if ch in A:
            new_pos = (A.index(ch) + k) % 26
            result += A[new_pos]
        else:
            result += ch
    return result

def check(attempt, word, k):
    if attempt == word:
        print("Key", k, ":", attempt, "-> Brute force attempt SUCCEEDED")
        return True
    print("Key", k, ":", attempt, "-> failed")
    return False

def brute_force(cipher, word):
    for k in range(26):
        attempt = caesar(cipher, -k)
        if check(attempt, word, k):
            return k
    return None

word = input("Enter a word: ").upper()

while not any(c in A for c in word):
    word = input("Enter at least one letter: ").upper()

key = 3
cipher = caesar(word, key)
print("Encrypted:", cipher)
found = brute_force(cipher, word)
print("Key found:", found)

# Polyalphabetic cipher break (Vigenere)
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
FREQ = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.2, 0.8, 4.0, 2.4,
        6.7, 7.5, 1.9, 0.1, 6.0, 6.3, 9.1, 2.8, 1.0, 2.4, 0.2, 2.0, 0.1]


def vigenere(text, key, sign=1):
    result = ''
    for i in range(len(text)):
        p = A.index(text[i])
        k = A.index(key[i % len(key)])
        result += A[(p + sign * k) % 26]
    return result


def ic(s):
    N = len(s)
    total = 0
    for ch in A:
        f = s.count(ch)
        total += f * (f - 1)
    return total / (N * (N - 1))


def key_length(c):
    avg_ics = []
    for m in range(1, 13):
        total = 0
        for i in range(m):
            total += ic(c[i::m])
        avg_ics.append(total / m)
    best = max(avg_ics)
    for m in range(1, 13):
        if avg_ics[m - 1] >= 0.9 * best:
            return m


def chi_sq(s):
    N = len(s)
    total = 0
    for i in range(26):
        observed = s.count(A[i])
        expected = N * FREQ[i] / 100
        total += (observed - expected) ** 2 / expected
    return total


def crack(c):
    m = key_length(c)
    key = ''
    for i in range(m):
        col = c[i::m]
        best_shift = 0
        best_score = chi_sq(vigenere(col, A[0], -1))
        for k in range(1, 26):
            score = chi_sq(vigenere(col, A[k], -1))
            if score < best_score:
                best_score = score
                best_shift = k
        key += A[best_shift]
    return key, vigenere(c, key, -1)


TEXT = """Cryptography is the practice of securing communication in the presence of
adversaries. A classical cipher such as the Vigenere cipher uses a repeating keyword
to shift each letter of the message by a different amount. For a long time it was
believed to be unbreakable, but the repetition of the key leaves patterns in the
ciphertext. Once the length of the key is known, the message splits into several
simple shift ciphers, and each of them can be solved by comparing its letter counts
with the normal frequencies of the English language."""

P = ''
for ch in TEXT.upper():
    if ch in A:
        P += ch

raw = input("Enter key (letters, max 12): ").upper()
key = ''
for ch in raw:
    if ch in A:
        key += ch
if key == '':
    key = 'KEY'

C = vigenere(P, key)
print("Ciphertext:", C)

found_key, plain = crack(C)
print("Key length:", len(found_key))
print("Found key:", found_key)
print("Plaintext:", plain)


# ECC Arithmetic Operations

p, a, b = 17, 2, 2
G = (5, 1)


def on_curve(P):
    if P is None:
        return True
    x, y = P
    return (y * y - x ** 3 - a * x - b) % p == 0


def add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        top = 3 * x1 * x1 + a
        bottom = 2 * y1
    else:
        top = y2 - y1
        bottom = x2 - x1
    slope = top * pow(bottom, -1, p) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)


def mul(k, P):
    result = None
    while k > 0:
        if k % 2 == 1:
            result = add(result, P)
        P = add(P, P)
        k = k // 2
    return result


print("p, a, b =", p, a, b, " G =", G)
P = G
Q = add(G, G)
print("P = G:", P)
print("Q = 2P:", Q)
print("P + Q:", add(P, Q))
print("3G == P + Q:", mul(3, G) == add(P, Q))

k = int(input("Enter scalar k: "))
R = mul(k, G)
print("k * G =", R, " on curve:", on_curve(R))


# ECDH (Elliptic Curve Diffie Hellman)
import random

p, a, b = 10007, 2, 30
G = (1, 283)
n = 10091


def add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        top = 3 * x1 * x1 + a
        bottom = 2 * y1
    else:
        top = y2 - y1
        bottom = x2 - x1
    slope = top * pow(bottom, -1, p) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)


def mul(k, P):
    result = None
    while k > 0:
        if k % 2 == 1:
            result = add(result, P)
        P = add(P, P)
        k = k // 2
    return result


dA = random.randint(1, n - 1)
dB = random.randint(1, n - 1)
QA = mul(dA, G)
QB = mul(dB, G)
print("p, a, b =", p, a, b, " G =", G, " n =", n)
print("Alice: private d_A =", dA, " public Q_A =", QA)
print("Bob: private d_B =", dB, " public Q_B =", QB)

SA = mul(dA, QB)
SB = mul(dB, QA)
print("Alice's shared key:", SA)
print("Bob's shared key:", SB)
print("keys match:", sa == sb)

# ECDSA (Elliptic curve digital signature algorithm)
import random, hashlib

p, a, b = 10007, 2, 30
G = (1, 283)
n = 10091


def add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        top = 3 * x1 * x1 + a
        bottom = 2 * y1
    else:
        top = y2 - y1
        bottom = x2 - x1
    slope = top * pow(bottom, -1, p) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)


def mul(k, P):
    result = None
    while k > 0:
        if k % 2 == 1:
            result = add(result, P)
        P = add(P, P)
        k = k // 2
    return result


def H(m):
    hex_digest = hashlib.sha256(m.encode()).hexdigest()
    return int(hex_digest, 16) % n


def sign(m, d):
    while True:
        k = random.randint(1, n - 1)
        point = mul(k, G)
        r = point[0] % n
        s = pow(k, -1, n) * (H(m) + d * r) % n
        if r != 0 and s != 0:
            return r, s


def verify(m, r, s, Q):
    if not (0 < r < n and 0 < s < n):
        return False
    w = pow(s, -1, n)
    u1 = H(m) * w % n
    u2 = r * w % n
    X = add(mul(u1, G), mul(u2, Q))
    if X is None:
        return False
    return X[0] % n == r


d = random.randint(1, n - 1)
Q = mul(d, G)
print("Private key d:", d, " Public key Q:", Q)

message = input("Enter a message to sign: ")
r, s = sign(message, d)
print("Signature (r, s):", (r, s))
print("Verified:", verify(message, r, s, Q))

tampered = message + "!"
print("\nModified message:", tampered)
print("Verified:", verify(tampered, r, s, Q))

# Bilinear Pairing

q, p, g, P = 1019, 2039, 4, 7


def e(X, Y):
    return pow(g, X * Y % q, p)


a = int(input("Enter a: "))
b = int(input("Enter b: "))
X, Y = a * P % q, b * P % q
print("aP =", X, " bP =", Y)
print("e(P, P) =", e(P, P))
print("e(aP, bP) =", e(X, Y))
print("e(P, P)^(ab) =", pow(e(P, P), a * b, p))

print("Bilinear:", e(X, Y) == pow(e(P, P), a * b, p))
print("Additive:", e((X + Y) % q, P) == e(X, P) * e(Y, P) % p)
print("Symmetric:", e(X, Y) == e(Y, X))
print("Non-degenerate:", e(P, P) != 1)


# IBE (Identity Based Encryption)

import random, hashlib

q, p, g, P = 1019, 2039, 4, 7


def e(X, Y):
    return pow(g, X * Y % q, p)


def H1(ID):
    hex_digest = hashlib.sha256(ID.encode()).hexdigest()
    return int(hex_digest, 16) % (q - 1) + 1


def H2(x, length):
    return hashlib.shake_256(str(x).encode()).digest(length)


def xor(a, b):
    result = b''
    for i in range(len(a)):
        result += bytes([a[i] ^ b[i]])
    return result


def extract(ID, s):
    Q_ID = H1(ID)
    return s * Q_ID % q


def encrypt(M, ID, P_pub):
    r = random.randint(1, q - 1)
    Q_ID = H1(ID)
    pairing_value = e(Q_ID, P_pub)
    K = pow(pairing_value, r, p)
    U = r * P % q
    keystream = H2(K, len(M))
    V = xor(M, keystream)
    return U, V


def decrypt(U, V, d):
    K = e(d, U)
    keystream = H2(K, len(V))
    return xor(V, keystream)


s = random.randint(1, q - 1)
P_pub = s * P % q
print("Setup: master key s =", s, "P_pub =", P_pub)

ID = input("Enter receiver's ID: ")
d_ID = extract(ID, s)
print("Extract: Q_ID =", H1(ID), "d_ID =", d_ID)

M = input("Enter message: ").encode()
U, V = encrypt(M, ID, P_pub)
print("Encrypt: U =", U, "V =", V)
print("Decrypt:", decrypt(U, V, d_ID).decode())
d_eve = extract("eve@example.com", s)
print("\nDecrypt with Eve's key:", decrypt(U, V, d_eve))

