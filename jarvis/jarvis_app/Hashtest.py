import hashlib
import pyfiglet
import subprocess


def hash_cracker():
    ascii_banner = pyfiglet.figlet_format("Ciph3r-360")
    print(ascii_banner)

    print("Algorithms available: MD5 | SHA1 | SHA224 | SHA256 | SHA384 | SHA512 | WinZip | PDF_RC4_40 | PDF_RC4_128 | PDF_AES_128 | PDF_AES_256 | ZIP_Legacy | ZIP_AES | RAR_Legacy | RAR_AES")

    while True:
        hash_type = input("What's the hash type? ")
        if hash_type.lower() in ['quit', 'exit']:
            print("Exiting...")
            break

        if hash_type.lower() == 'winzip':
            # WinZip hash cracking
            zip_file = input("Enter the path to the encrypted ZIP file: ")
            if zip_file.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            password_list = input("Enter the path to the password list: ")
            if password_list.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            try:
                # Use subprocess to execute the WinZip command-line tool to test passwords
                result = subprocess.run(['wzzip', '-t', '-s', password_list, zip_file], capture_output=True)
                if result.returncode == 0:
                    print("\033[1;32mPassword found!\033[0m")
                    print(result.stdout.decode())
                else:
                    print("\033[1;31mPassword not found.\033[0m")

            except FileNotFoundError:
                print("WinZip command-line tool 'wzzip' not found.")
            except Exception as e:
                print("An error occurred:", e)

        elif hash_type.lower() in ['pdf_rc4_40', 'pdf_rc4_128', 'pdf_aes_128', 'pdf_aes_256']:
            # PDF hash cracking
            pdf_file = input("Enter the path to the PDF file: ")
            if pdf_file.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            password_list = input("Enter the path to the password list: ")
            if password_list.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            try:
                # Use subprocess to execute the pdf2john.py script to extract hash
                result = subprocess.run(['pdf2john.py', pdf_file], capture_output=True)
                hash_output = result.stdout.decode()

                if hash_type.lower() in hash_output.lower():
                    print("\033[1;32mHash type identified.\033[0m")

                    # Now, perform hash cracking using the appropriate method based on hash type
                    # (e.g., use hashcat or John the Ripper)
                    # Implementation depends on the specific tools and methods available for each hash type

                else:
                    print("\033[1;31mHash type not found in PDF file.\033[0m")

            except FileNotFoundError:
                print("pdf2john.py script not found.")
            except Exception as e:
                print("An error occurred:", e)

        elif hash_type.lower() in ['zip_legacy', 'zip_aes']:
            # ZIP hash cracking
            zip_file = input("Enter the path to the ZIP file: ")
            if zip_file.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            password_list = input("Enter the path to the password list: ")
            if password_list.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            try:
                # Use subprocess to execute the ZIP cracking tool (e.g., hashcat or John the Ripper)
                # Implementation depends on the specific tools and methods available for each hash type
                pass  # Placeholder for ZIP cracking tool execution

            except FileNotFoundError:
                print("ZIP cracking tool not found.")
            except Exception as e:
                print("An error occurred:", e)

        elif hash_type.lower() in ['rar_legacy', 'rar_aes']:
            # RAR hash cracking
            rar_file = input("Enter the path to the RAR file: ")
            if rar_file.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            password_list = input("Enter the path to the password list: ")
            if password_list.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            try:
                # Use subprocess to execute the RAR cracking tool (e.g., hashcat or John the Ripper)
                # Implementation depends on the specific tools and methods available for each hash type
                pass  # Placeholder for RAR cracking tool execution

            except FileNotFoundError:
                print("RAR cracking tool not found.")
            except Exception as e:
                print("An error occurred:", e)

        else:
            # For other hash types (MD5, SHA1, SHA224, SHA256, SHA384, SHA512), perform regular hash cracking
            wordlist_location = input("Enter wordlist location: ")
            if wordlist_location.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            hash_value = input("Enter hash: ")
            if hash_value.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            try:
                with open(wordlist_location, 'r', encoding='latin-1') as wordlist_file:
                    word_list = wordlist_file.readlines()

                    for word in word_list:
                        word = word.strip()  # Remove leading/trailing whitespace
                        if hash_type.lower() == "md5":
                            hash_object = hashlib.md5(word.encode('utf-8'))
                        elif hash_type.lower() == "sha1":
                            hash_object = hashlib.sha1(word.encode('utf-8'))
                        elif hash_type.lower() == "sha224":
                            hash_object = hashlib.sha224(word.encode('utf-8'))
                        elif hash_type.lower() == "sha256":
                            hash_object = hashlib.sha256(word.encode('utf-8'))
                        elif hash_type.lower() == "sha384":
                            hash_object = hashlib.sha384(word.encode('utf-8'))
                        elif hash_type.lower() == "sha512":
                            hash_object = hashlib.sha512(word.encode('utf-8'))
                        else:
                            print("Please choose from the given options.")
                            break

                        hashed = hash_object.hexdigest()
                        if hash_value == hashed:
                            print("\033[1;32mHASH FOUND:", word, "\033[0m")
                            break
                    else:
                        print("Hash not found in the wordlist.")

            except FileNotFoundError:
                print("File not found.")
            except Exception as e:
                print("An error occurred:", e)

        exit_option = input("Do you want to exit? (Type 'quit' or 'exit' to exit, or press Enter to continue): ")
        if exit_option.lower() in ['quit', 'exit']:
            print("Exiting...")
            break


if __name__ == "__main__":
    hash_cracker()
