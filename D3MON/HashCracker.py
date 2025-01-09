import hashlib
import pyfiglet
import threading
import queue
from tqdm import tqdm


def hash_cracker():
    ascii_banner = pyfiglet.figlet_format("Ciph3r-360")
    print(ascii_banner)

    algorithms = ["MD5", "SHA1", "SHA224", "SHA256", "SHA512", "SHA384", "SHA3_256", "SHA3_512"]
    print("Algorithms available:", " | ".join(algorithms))

    def hash_word(word, hash_type):
        word = word.strip()
        if hash_type == "MD5":
            hash_object = hashlib.md5(word.encode('utf-8'))
        elif hash_type == "SHA1":
            hash_object = hashlib.sha1(word.encode('utf-8'))
        elif hash_type == "SHA224":
            hash_object = hashlib.sha224(word.encode('utf-8'))
        elif hash_type == "SHA256":
            hash_object = hashlib.sha256(word.encode('utf-8'))
        elif hash_type == "SHA512":
            hash_object = hashlib.sha512(word.encode('utf-8'))
        elif hash_type == "SHA384":
            hash_object = hashlib.sha384(word.encode('utf-8'))
        elif hash_type == "SHA3_256":
            hash_object = hashlib.sha3_256(word.encode('utf-8'))
        elif hash_type == "SHA3_512":
            hash_object = hashlib.sha3_512(word.encode('utf-8'))
        else:
            return None
        return hash_object.hexdigest()

    def worker(queue, hash_type, hash_value, found_event, progress_bar):
        while not queue.empty() and not found_event.is_set():
            word = queue.get()
            if hash_value == hash_word(word, hash_type):
                found_event.set()
                print("\033[1;32mHASH FOUND:", word, "\n")
                with open("cracked_hashes.txt", 'a') as f:
                    f.write(f"Hash: {hash_value} - Word: {word}\n")
            queue.task_done()
            progress_bar.update(1)

    while True:
        hash_type = input("What's the hash type? ").upper()
        if hash_type in ['QUIT', 'EXIT']:
            print("Exiting...")
            break

        if hash_type not in algorithms:
            print("Invalid hash type. Please choose from the given options.")
            continue

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
                word_queue = queue.Queue()
                for word in word_list:
                    word_queue.put(word)

                found_event = threading.Event()
                threads = []

                # Initialize the progress bar
                with tqdm(total=len(word_list), desc="Progress", ncols=100, bar_format="\033[92m{l_bar}{bar}| {n_fmt}/{total_fmt}\033[0m") as progress_bar:
                    for _ in range(10):  # Number of threads
                        thread = threading.Thread(target=worker, args=(word_queue, hash_type, hash_value, found_event, progress_bar))
                        thread.start()
                        threads.append(thread)

                    for thread in threads:
                        thread.join()

                if not found_event.is_set():
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
