from __future__ import annotations
 
import os
from tkinter import (
    Tk, Frame, Label, Text, Entry, Button,
    filedialog, messagebox, END, StringVar
)
from PIL import Image
 
BG_DARK = "#1e1f29"
BG_PANEL = "#282a36"
ACCENT = "#8be9fd"
ACCENT_GREEN = "#50fa7b"
ACCENT_ORANGE = "#ffb86c"
TEXT_LIGHT = "#f8f8f2"
TEXT_MUTED = "#6272a4"
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_BODY = ("Segoe UI", 10)
 
DELIMITER = "#####"
 
 
def xor_cipher(text: str, key: str) -> str:
    if not key:
        raise ValueError("Password must not be empty.")
    return "".join(
        chr(ord(char) ^ ord(key[i % len(key)]))
        for i, char in enumerate(text)
    )
 
 
def encode_image(image_path: str, message: str, password: str, save_path: str) -> None:
    img = Image.open(image_path).convert("RGB")
 
    payload = xor_cipher(message, password) + DELIMITER
    bits = "".join(format(ord(char), "08b") for char in payload)
 
    capacity = img.width * img.height * 3
    if len(bits) > capacity:
        raise ValueError("Message is too long to fit inside this image.")
 
    pixels = img.load()
    bit_index = 0
 
    for y in range(img.height):
        for x in range(img.width):
            if bit_index >= len(bits):
                break
 
            r, g, b = pixels[x, y]
 
            if bit_index < len(bits):
                r = (r & ~1) | int(bits[bit_index]); bit_index += 1
            if bit_index < len(bits):
                g = (g & ~1) | int(bits[bit_index]); bit_index += 1
            if bit_index < len(bits):
                b = (b & ~1) | int(bits[bit_index]); bit_index += 1
 
            pixels[x, y] = (r, g, b)
 
    img.save(save_path)
 
 
def decode_image(image_path: str, password: str) -> str:
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
 
    bits = []
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            bits.append(str(r & 1))
            bits.append(str(g & 1))
            bits.append(str(b & 1))
    bits = "".join(bits)
 
    chars = []
    for i in range(0, len(bits) - 7, 8):
        byte = bits[i:i + 8]
        chars.append(chr(int(byte, 2)))
        if "".join(chars).endswith(DELIMITER):
            break
    else:
        raise ValueError("No hidden message found in this image.")
 
    encrypted_message = "".join(chars)[: -len(DELIMITER)]
    return xor_cipher(encrypted_message, password)
 
 
def styled_button(parent, text, command, bg, fg="#1e1f29"):
    btn = Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=fg,
        activeforeground=bg,
        font=FONT_LABEL,
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=8,
        borderwidth=0,
    )
 
    def on_enter(_e):
        btn.config(bg=TEXT_LIGHT)
 
    def on_leave(_e):
        btn.config(bg=bg)
 
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn
 
 
class PixelVaultApp:
    def __init__(self, root: Tk):
        self.root = root
        self.selected_image_path = ""
 
        root.title("Pixel Vault")
        root.geometry("520x640")
        root.resizable(False, False)
        root.configure(bg=BG_DARK)
 
        self._build_header()
        self._build_image_picker()
        self._build_message_box()
        self._build_password_field()
        self._build_actions()
        self._build_footer()
 
    def _build_header(self):
        header = Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", pady=(28, 10))
 
        Label(
            header, text="🔒 PIXEL VAULT", font=FONT_TITLE, bg=BG_DARK, fg=ACCENT
        ).pack()
 
        Label(
            header,
            text="Hide encrypted messages inside images",
            font=FONT_SUBTITLE,
            bg=BG_DARK,
            fg=TEXT_MUTED,
        ).pack(pady=(4, 0))
 
    def _build_image_picker(self):
        panel = Frame(self.root, bg=BG_PANEL)
        panel.pack(fill="x", padx=24, pady=12)
 
        inner = Frame(panel, bg=BG_PANEL)
        inner.pack(fill="x", padx=16, pady=16)
 
        styled_button(
            inner, "📁  Select PNG Image", self.select_image, ACCENT
        ).pack(side="left")
 
        self.image_status = StringVar(value="No image selected")
        Label(
            inner,
            textvariable=self.image_status,
            font=FONT_BODY,
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            wraplength=260,
            justify="left",
        ).pack(side="left", padx=12)
 
    def _build_message_box(self):
        panel = Frame(self.root, bg=BG_PANEL)
        panel.pack(fill="x", padx=24, pady=(0, 12))
 
        inner = Frame(panel, bg=BG_PANEL)
        inner.pack(fill="both", padx=16, pady=16)
 
        Label(
            inner, text="SECRET MESSAGE", font=FONT_LABEL, bg=BG_PANEL, fg=ACCENT
        ).pack(anchor="w")
 
        self.message_text = Text(
            inner,
            height=8,
            width=40,
            bg=BG_DARK,
            fg=TEXT_LIGHT,
            insertbackground=TEXT_LIGHT,
            relief="flat",
            font=FONT_BODY,
            padx=10,
            pady=10,
        )
        self.message_text.pack(fill="x", pady=(8, 0))
 
    def _build_password_field(self):
        panel = Frame(self.root, bg=BG_PANEL)
        panel.pack(fill="x", padx=24, pady=(0, 12))
 
        inner = Frame(panel, bg=BG_PANEL)
        inner.pack(fill="x", padx=16, pady=16)
 
        Label(
            inner, text="PASSWORD", font=FONT_LABEL, bg=BG_PANEL, fg=ACCENT
        ).pack(anchor="w")
 
        self.password_entry = Entry(
            inner,
            show="•",
            width=30,
            bg=BG_DARK,
            fg=TEXT_LIGHT,
            insertbackground=TEXT_LIGHT,
            relief="flat",
            font=FONT_BODY,
        )
        self.password_entry.pack(fill="x", pady=(8, 0), ipady=6)
 
    def _build_actions(self):
        panel = Frame(self.root, bg=BG_DARK)
        panel.pack(fill="x", padx=24, pady=(4, 12))
 
        styled_button(
            panel, "🔐  Encode Message", self.encode_message, ACCENT_GREEN
        ).pack(fill="x", pady=(0, 8))
 
        styled_button(
            panel, "🔓  Decode Message", self.decode_message, ACCENT_ORANGE
        ).pack(fill="x")
 
    def _build_footer(self):
        Label(
            self.root,
            text="Mini Project · Pixel Vault",
            font=("Segoe UI", 9),
            bg=BG_DARK,
            fg=TEXT_MUTED,
        ).pack(side="bottom", pady=14)
 
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select PNG Image",
            filetypes=[("PNG Images", "*.png")],
        )
        if file_path:
            self.selected_image_path = file_path
            self.image_status.set(os.path.basename(file_path))
 
    def encode_message(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select an image.")
            return
 
        message = self.message_text.get("1.0", END).strip()
        password = self.password_entry.get()
 
        if not message or not password:
            messagebox.showerror("Error", "Enter a message and a password.")
            return
 
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Images", "*.png")],
            title="Save Encoded Image",
        )
        if not save_path:
            return
 
        try:
            encode_image(self.selected_image_path, message, password, save_path)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return
 
        messagebox.showinfo("Success", "Message encoded and image saved successfully!")
 
    def decode_message(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select an encoded image.")
            return
 
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Enter the password.")
            return
 
        try:
            hidden_message = decode_image(self.selected_image_path, password)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return
 
        messagebox.showinfo("Decoded Message", f"Hidden Message:\n\n{hidden_message}")
 
 
if __name__ == "__main__":
    root = Tk()
    app = PixelVaultApp(root)
    root.mainloop()
 
