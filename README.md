# Pixel Vault

Pixel Vault is a desktop steganography tool that hides encrypted text messages inside PNG images. It uses **LSB (Least Significant Bit) encoding** to embed data invisibly in pixel values, combined with **XOR-based password encryption** for an extra layer of security.

## Features

- Hide any text message inside a PNG image
- Password-protected encryption before hiding the data
- Extract and decrypt hidden messages from an image
- Simple, dark-themed desktop UI built with Tkinter

## Requirements

- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/)

Install the dependency:

```bash
pip install pillow
```

## Usage

Run the app:

```bash
python pixel_vault.py
```

**To hide a message:**
1. Click **Select PNG Image** and choose a cover image
2. Type your secret message
3. Enter a password
4. Click **Encode Message** and choose where to save the new image

**To reveal a message:**
1. Select the encoded PNG image
2. Enter the same password used to encode it
3. Click **Decode Message**

## How It Works

The message is first encrypted with a password using XOR, then converted to binary. Each bit is written into the least significant bit of the image's red, green, and blue channels, changing pixel values so slightly that the image looks identical to the naked eye. A delimiter marks the end of the hidden data so it can be extracted precisely during decoding.

## License

This project is open source and available for personal or educational use.
