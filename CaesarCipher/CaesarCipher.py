def read_txt_file():
    with open("input.txt", "r", encoding="utf-8") as file:
        text = file.read()
    return text

def cipher_string(text, shift):
    encrypted = []

    for c in text:
        if c.isalpha():
            if c.islower():
                base = ord('a')
            else:
                base = ord('A')
            
            shifted = (ord(c) - base + shift) % 26
            new_c = chr(base + shifted)
            encrypted.append(new_c)
        else:
            encrypted.append(c)
    return ''.join(encrypted)


def write_encrypted(text):
    with open("encrypted.txt", "w", encoding="utf-8") as file:
        file.write(text)



write_encrypted(cipher_string(read_txt_file(), 3))


