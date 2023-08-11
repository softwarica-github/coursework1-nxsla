import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

encoded_images = []

def encode_image():
    message = entry_message.get()
    if not message:
        return

    image_file = filedialog.askopenfilename()
    if not image_file:
        return

    image = Image.open(image_file)
    encoded_image = hide_message(image, message)
    
    encoded_images.append(encoded_image)

    encoded_image_file = filedialog.asksaveasfilename(defaultextension=".png",
                                                      filetypes=[("PNG Files", "*.png")])
    if not encoded_image_file:
        return

    encoded_image.save(encoded_image_file)
    tk.messagebox.showinfo("Success", "Image encoded and saved successfully!")

def hide_message(image, message):
    encoded_image = image.copy()
    width, height = image.size

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    message_length = len(binary_message)

    if message_length > width * height * 3:
        tk.messagebox.showerror("Error", "Message is too long to encode in the image.")
        return

    index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(encoded_image.getpixel((x, y)))
            for i in range(3):
                if index < message_length:
                    pixel[i] = pixel[i] & ~1 | int(binary_message[index])
                    index += 1
                else:
                    break
            encoded_image.putpixel((x, y), tuple(pixel))

    return encoded_image

def decode_image():
    image_file = filedialog.askopenfilename()
    if not image_file:
        return

    image = Image.open(image_file)
    decoded_message = reveal_message(image)

    if decoded_message:
        tk.messagebox.showinfo("Decoded Message", decoded_message)
    else:
        tk.messagebox.showinfo("No Message Found", "No hidden message found in the image.")

def reveal_message(image):
    binary_message = ""
    width, height = image.size

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        message += chr(int(byte, 2))

    return message

def show_encoded_image():
    if not encoded_images:
        tk.messagebox.showinfo("No Encoded Images", "You have not encoded any images yet.")
        return
    
    encoded_image = encoded_images[-1]  # Show the last encoded image in the list
    encoded_image_photo = ImageTk.PhotoImage(encoded_image)
    
    encoded_image_window = tk.Toplevel(root)
    encoded_image_window.title("Encoded Image")
    encoded_image_window.geometry(f"{encoded_image.width}x{encoded_image.height}")
    
    encoded_image_label = tk.Label(encoded_image_window, image=encoded_image_photo)
    encoded_image_label.image = encoded_image_photo
    encoded_image_label.pack()


# Create the main GUI window
root = tk.Tk()
root.title("Image Steganography Tool")
root.geometry("700x200")

# Encode
label_message = tk.Label(root, text="Enter message to encode:")
label_message.pack()

entry_message = tk.Entry(root, width=50)
entry_message.pack()

btn_encode = tk.Button(root, text="Encode Image", command=encode_image)
btn_encode.pack()

# Decode
btn_decode = tk.Button(root, text="Decode Image", command=decode_image)
btn_decode.pack()

# Show Encoded Image
btn_show_encoded_image = tk.Button(root, text="Show Encoded Image", command=show_encoded_image)
btn_show_encoded_image.pack()

root.mainloop()
