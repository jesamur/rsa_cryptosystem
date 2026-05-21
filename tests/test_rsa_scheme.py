import pytest
from src.rsa_scheme import decrypt, encrypt, evaluate_key_sizes, generate_keypair


def test_keypair_generation():
    public_key, private_key = generate_keypair(256)
    assert len(public_key) == 2
    assert len(private_key) == 2
    assert public_key[1] == private_key[1]


def test_encrypt_decrypt_roundtrip():
    public_key, private_key = generate_keypair(256)
    message = "Prueba RSA"
    ciphertext = encrypt(public_key, message)
    decrypted = decrypt(private_key, ciphertext)
    assert decrypted == message


def test_evaluate_key_sizes():
    key_sizes = (256,)
    results = evaluate_key_sizes(key_sizes, message="OK")
    assert 256 in results
    assert results[256]["keygen"] > 0
    assert results[256]["encrypt"] >= 0
    assert results[256]["decrypt"] >= 0
