import hashlib
import pyfiglet


def hash_cracker():
    ascii_banner = pyfiglet.figlet_format("Ciph3r-360")
    print(ascii_banner)

    print("Algorithms available: MD5 | SHA1 | SHA224 | SHA512 | SHA384")

    while True:
        hash_type = input("What's the hash type? ")
        if hash_type.lower() in ['quit', 'exit']:
            print("Exiting...")
            break

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
                    if hash_type == "MD5":
                        hash_object = hashlib.md5(word.encode('utf-8'))
                    elif hash_type == "SHA1":
                        hash_object = hashlib.sha1(word.encode('utf-8'))
                    elif hash_type == "SHA224":
                        hash_object = hashlib.sha224(word.encode('utf-8'))
                    elif hash_type == "SHA512":
                        hash_object = hashlib.sha512(word.encode('utf-8'))
                    elif hash_type == "SHA384":
                        hash_object = hashlib.sha384(word.encode('utf-8'))
                    else:
                        print("Please choose from the given options.")
                        break

                    hashed = hash_object.hexdigest()
                    if hash_value == hashed:
                        print("\033[1;32mHASH FOUND:", word, "\n")
                        break
                else:
                    print("Hash not found in the wordlist.")

        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print("An error occurred:", e)
        finally:
            exit_option = input("Do you want to exit? (Type 'quit' or 'exit' to exit, or press Enter to continue): ")
            if exit_option.lower() in ['quit', 'exit']:
                print("Exiting...")
                break


# if __name__ == "__main__":
#     hash_cracker()
