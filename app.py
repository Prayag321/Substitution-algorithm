from flask import Flask, render_template, request

app = Flask(__name__)

def substitution_cipher(text, category_key, key, mode='encrypt'):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''

    # Repeat the category key to match the length of the text
    category_key = (category_key * len(text)).upper()

    for char, category_shift in zip(text, category_key):
        if char.isalpha():
            # Determine whether the character is uppercase or lowercase
            is_upper = char.isupper()

            # Convert the character to uppercase for simplicity
            char = char.upper()

            # Find the index of the character in the alphabet (starting from 1)
            index = alphabet.index(char) + 1

            # Apply the substitution with the key and category shift
            if mode == 'encrypt':
                new_index = (index + alphabet.index(category_shift) + key - 1) % 26 + 1
            else:  # mode == 'decrypt'
                new_index = (index - alphabet.index(category_shift) - key - 1) % 26 + 1

            # Retrieve the new character
            new_char = alphabet[new_index - 1]  # Convert back to 0-25 index

            # Convert back to lowercase if the original character was lowercase
            if not is_upper:
                new_char = new_char.lower()

            # Add the new character to the result
            result += new_char
        else:
            # If the character is not a letter, leave it unchanged
            result += char

    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    plaintext = request.form['plaintext']
    category_key = request.form['category_key']
    numeric_key = int(request.form['numeric_key'])

    # Encrypt the plaintext
    ciphertext = substitution_cipher(plaintext, category_key, numeric_key, mode='encrypt')

    # Decrypt the ciphertext
    decrypted_text = substitution_cipher(ciphertext, category_key, numeric_key, mode='decrypt')

    return render_template('result.html', ciphertext=ciphertext, decrypted_text=decrypted_text)

if __name__ == '__main__':
    app.run(debug=True)
