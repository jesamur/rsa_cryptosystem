import secrets
import time
from typing import Dict, Tuple


def gcd(a: int, b: int) -> int:
    """Calcula el máximo común divisor usando el algoritmo de Euclides."""
    while b:
        a, b = b, a % b
    return a


def is_prime(n: int, k: int = 16) -> bool:
    """Verifica si un número es primo usando la prueba de Miller-Rabin."""
    if n < 2:
        return False

    # Rechaza rápidamente múltiplos de pequeños primos.
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n % p == 0:
            return n == p

    # Descompone n-1 en 2^r * d.
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Ejecuta k rondas de la prueba.
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int) -> int:
    """Genera un número primo de tamaño aproximado en bits."""
    while True:
        candidate = secrets.randbits(bits) | 1 | (1 << (bits - 1))
        if is_prime(candidate):
            return candidate


def modinv(a: int, m: int) -> int:
    """Calcula el inverso modular de a con respecto a m."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("El inverso modular no existe")
    return x % m


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Aplica el algoritmo extendido de Euclides para obtener el inverso modular."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def generate_keypair(bits: int = 1024) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Genera un par de claves RSA público y privado."""
    if bits < 16:
        raise ValueError("El tamaño de clave debe ser al menos 16 bits")

    half_bits = bits // 2
    p = generate_prime(half_bits)
    q = generate_prime(bits - half_bits)
    while p == q:
        q = generate_prime(bits - half_bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    # El exponente público e se elige comúnmente como 65537.
    e = 65537
    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2

    d = modinv(e, phi)
    return (e, n), (d, n)


def encrypt(public_key: Tuple[int, int], plaintext: str) -> int:
    """Cifra un mensaje de texto usando la clave pública RSA."""
    e, n = public_key
    message_bytes = plaintext.encode("utf-8")
    message_int = int.from_bytes(message_bytes, "big")
    if message_int >= n:
        raise ValueError("El mensaje es demasiado grande para la clave RSA")
    return pow(message_int, e, n)


def decrypt(private_key: Tuple[int, int], ciphertext: int) -> str:
    """Descifra un texto cifrado usando la clave privada RSA."""
    d, n = private_key
    message_int = pow(ciphertext, d, n)
    message_bytes = message_int.to_bytes((message_int.bit_length() + 7) // 8, "big")
    return message_bytes.decode("utf-8")


def evaluate_key_sizes(key_sizes: Tuple[int, ...], message: str = "RSA test") -> Dict[int, Dict[str, float]]:
    """Evalúa tiempos de generación, cifrado y descifrado para varios tamaños de clave."""
    results: Dict[int, Dict[str, float]] = {}
    for size in key_sizes:
        start = time.perf_counter()
        public_key, private_key = generate_keypair(size)
        keygen_time = time.perf_counter() - start

        start = time.perf_counter()
        ciphertext = encrypt(public_key, message)
        encrypt_time = time.perf_counter() - start

        start = time.perf_counter()
        plaintext = decrypt(private_key, ciphertext)
        decrypt_time = time.perf_counter() - start

        if plaintext != message:
            raise AssertionError("Descifrado no coincide con el mensaje original")

        results[size] = {
            "keygen": keygen_time,
            "encrypt": encrypt_time,
            "decrypt": decrypt_time,
        }
    return results


def main() -> None:
    """Ejecuta una evaluación rápida con tamaños de clave predefinidos."""
    key_sizes = (512, 768, 1024)
    print("Evaluando RSA para distintos tamaños de clave")
    for size, metrics in evaluate_key_sizes(key_sizes).items():
        print(f"\nTamaño de clave: {size} bits")
        print(f"  Generación: {metrics['keygen']:.4f} s")
        print(f"  Cifrado:    {metrics['encrypt']:.6f} s")
        print(f"  Descifrado: {metrics['decrypt']:.6f} s")


if __name__ == "__main__":
    main()
