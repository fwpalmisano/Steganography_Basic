# Steganography_Basic
This program hides a .txt message within a photo by obscuring the binary form of the message in the rgb channels of each pixel in the picture.

Message starts at pixel 0, continues in consecutive rgb channels until a 00000000 is encountered. Message is unencrypted, but is obscured within the information of the picture. Picture remains unchanged to the human eye.
