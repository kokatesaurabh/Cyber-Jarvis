from PIL import Image


def steganography():
    class LSBSteganography:
        @staticmethod
        def encode_image(image_path, message):
            """Encodes a message into an image using LSB steganography.

            Args:
                image_path (str): Path to the image file to use as the cover.
                message (str): The message to be hidden within the image.

            Raises:
                ValueError: If the message is too long to be hidden in the image.
            """

            img = Image.open(image_path).convert('RGB')
            width, height = img.size

            binary_message = ''.join(format(ord(char), '08b') for char in message)
            message_with_delimiter = binary_message + "11111111"  # Add delimiter

            if len(message_with_delimiter) > width * height * 3:
                raise ValueError("Message too long to encode in the given image.")

            encoded_pixels = img.load()
            index = 0

            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))

                    if index < len(message_with_delimiter):
                        r = r & ~1 | int(message_with_delimiter[index])
                        index += 1
                    if index < len(message_with_delimiter):
                        g = g & ~1 | int(message_with_delimiter[index])
                        index += 1
                    if index < len(message_with_delimiter):
                        b = b & ~1 | int(message_with_delimiter[index])
                        index += 1

                    encoded_pixels[x, y] = (r, g, b)

            output_path = 'encoded_' + image_path
            img.save(output_path)
            print(f"Message encoded successfully in the image: {output_path}")

        @staticmethod
        def decode_image(image_path):
            """Decodes a hidden message from an image using LSB steganography.

            Args:
                image_path (str): Path to the image containing the hidden message.

            Returns:
                str: The decoded message extracted from the image.
            """

            img = Image.open(image_path).convert('RGB')
            width, height = img.size

            binary_message = ""

            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    binary_message += str(r & 1)
                    binary_message += str(g & 1)
                    binary_message += str(b & 1)

            # Remove only the delimiter, not trailing zeros
            delimiter_index = binary_message.find("11111111")
            if delimiter_index != -1:
                binary_message = binary_message[:delimiter_index]

            bytes_list = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
            decoded_message = ''.join(chr(int(byte, 2)) for byte in bytes_list if byte and len(byte) == 8)
            return decoded_message

    def main():
        while True:
            print("\nSteganography Menu:")
            print("1. Encode message into an image")
            print("2. Decode message from an image")
            print("3. Exit")
            choice = input("Enter your choice (1/2/3): ")

            if choice == '1':
                image_path = input("Enter the path of the image: ")
                message = input("Enter the message to encode: ")
                try:
                    LSBSteganography.encode_image(image_path, message)
                except ValueError as e:
                    print("Error:", e)

            elif choice == '2':
                image_path = input("Enter the path of the encoded image: ")
                try:
                    decoded_message = LSBSteganography.decode_image(image_path)
                    print("Decoded message:", decoded_message)
                except FileNotFoundError:
                    print("Error: Image file not found.")
                except Exception as e:  # Catch other potential errors
                    print("Error:", e)

            elif choice == '3':
                print("Exiting...")
                break  # Exit the loop

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    main()


# if __name__ == "__main__":
#     steganography()
