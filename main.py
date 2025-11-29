import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def encrypt_image(img_path, key):
    img = Image.open(img_path)
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            pixels[x, y] = ((r + key) % 256, (g + key) % 256, (b + key) % 256)
    output_path = "encrypted_image.png"
    img.save(output_path)
    return output_path

def decrypt_image(img_path, key):
    img = Image.open(img_path)
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            pixels[x, y] = ((r - key) % 256, (g - key) % 256, (b - key) % 256)
    output_path = "decrypted_image.png"
    img.save(output_path)
    return output_path

def run_app():
    window = tk.Tk()
    window.title("Pixel Manipulation Image Encryption Tool")

    img_label = tk.Label(window)
    img_label.pack(pady=10)

    key_var = tk.IntVar(value=123)  # default key

    def show_image(img_path):
        try:
            img = Image.open(img_path)
            img.thumbnail((400, 400))
            img_tk = ImageTk.PhotoImage(img)
            img_label.img_tk = img_tk
            img_label.config(image=img_tk)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot display image: {e}")

    def upload_img():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            window.img_path = file_path
            show_image(file_path)

    def encrypt_img():
        if not hasattr(window, 'img_path'):
            messagebox.showerror("Error", "Please upload an image first.")
            return
        key = key_var.get()
        output_path = encrypt_image(window.img_path, key)
        show_image(output_path)
        messagebox.showinfo("Encrypted", f"Encrypted image saved as {output_path}")

    def decrypt_img():
        if not hasattr(window, 'img_path'):
            messagebox.showerror("Error", "Please upload an image first.")
            return
        key = key_var.get()
        output_path = decrypt_image(window.img_path, key)
        show_image(output_path)
        messagebox.showinfo("Decrypted", f"Decrypted image saved as {output_path}")

    tk.Button(window, text="Upload Image", command=upload_img).pack(pady=5)
    tk.Label(window, text="Encryption Key:").pack()
    tk.Entry(window, textvariable=key_var).pack(pady=5)
    tk.Button(window, text="Encrypt", command=encrypt_img).pack(pady=5)
    tk.Button(window, text="Decrypt", command=decrypt_img).pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    run_app()
