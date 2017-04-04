# ## Problem 2:  steganography
#
# This question asks you to write two functions, likely with some helper functions, that will enable you
# to embed arbitrary text (string) messages into an image (if there is
# enough room!)
import numpy as np
from matplotlib import pyplot as plt
import cv2


# For extra credit, the challenge is to be
# able to extract/embed an image into another image...

#
# You'll want to borrow from hw7pr1 for
#  + opening the file
#  + reading the pixels
#  + create some helper functions!
#  + also, check out the slides :-)
#
# Happy steganographizing, everyone!
#

# Hid the text of Romeo and Juliet inside of a picture of Romeo and Juliet
# Find it by calling desteg_image('stegged.png')



# Part A: here is a signature for the decoding
# remember - you will want helper functions!
def desteg_string(image_name):
    """ this function takes in an image name, examines the bits, and returns
        any hidden (nonencrypted) messages
    """
    raw_image = cv2.imread(image_name, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)

    num_rows, num_cols, num_chans = image.shape
    message_bits = []
    letter = ''
    for row in range(num_rows):                     #iterate through every pixel
        for col in range(num_cols):
            r, g, b = image[row, col]
            bits_to_strip = []                      # put binary rgb colors into this list

            r_binary_string = str(bin(r))           # convert red to binary
            bits_to_strip.append(r_binary_string)

            g_binary_string = str(bin(g))           # convert green to binary
            bits_to_strip.append(g_binary_string)

            b_binary_string = str(bin(b))           # convert blue to binary
            bits_to_strip.append(b_binary_string)

            for bit in bits_to_strip:               # strip off the last bit
                if len(letter) < 8:                 # construct it into an 8 long string that represents each character
                    letter += bit[-1]
                else:
                    message_bits.append(int(letter))    # if letter is 8 long, append that letter to message list, create a new letter
                    letter = ''
                    letter += bit[-1]

    message_desteg = ''                             # string where destegged message will be constructed
    for bit in message_bits:
        if bit == 00000000:                         # end message
            break
        else:
            ascii_character = int(str(bit), 2)      # convert 8 long binary letters into decimal integers
            letter = chr(ascii_character)           # convert numbers into corresponding ascii characters
            message_desteg += letter                # append character to message string

    return message_desteg


# Part B: here is a signature for the encoding/embedding
# remember - you will want helper functions!
def steganographize(image_name, message_text_file_name):
    """ this function takes in an image name and a message, and hides the message in the
        lowest bits of the image's pixel channels
    """
    raw_image = cv2.imread(image_name, cv2.IMREAD_COLOR)        # read in the image
    image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)
    stegged_image = image.copy()                                # make a copy to stegify

    f = open(message_text_file_name, "r", encoding = "latin1")  # latin1 is a very safe encoding
    data = f.read()

    # get all of the bits from the picture
    num_rows, num_cols, num_chans = image.shape
    picture_bits = []                                           # store all info from picture here (in binary)
    for row in range(num_rows):
        for col in range(num_cols):                             # iterate through everu pixel
            r, g, b = image[row, col]

            r_binary_string = str(bin(r))                       # get color info and convert to binary
            g_binary_string = str(bin(g))
            b_binary_string = str(bin(b))

            pixel_bits = [r_binary_string, g_binary_string, b_binary_string]    # assemble binary color info
            picture_bits.append(pixel_bits)                     # append binary color info to picture_bits

    # encode message in binary
    message_in_binary = []                                      # list to store binary message
    for letter in data:
        ascii_code = ord(letter)                                # convert characters to ascii codes
        binary_letter = bin(ascii_code)                         # convert ascii codes to binary
        binary_letter_clean = binary_letter[2:]                 # clean binary codes          
        binary_letter_str = str(binary_letter_clean)
        length_binary_code = len(binary_letter_str)             
        if length_binary_code < 8:                              # make sure every binary character code is 8 long
            elongater = 8 - length_binary_code
            appropriate_length_binary_str = elongater * '0'
            appropriate_length_binary_str += binary_letter_str

        message_in_binary.append(appropriate_length_binary_str) # append character to binary message list
    message_in_binary.append('00000000')                        # end message

    # start bringing message and image together and changing bits
    # need to collapse the message into one string and put it into the image
    
    message_in_binary_concated = ''

    for bit in message_in_binary:                               # collapse the message into a single long string
        message_in_binary_concated += bit

    count = 0
    photo_with_message_list = []                                # list to store info for all pixels
    for rgb_bin_list in picture_bits:                           # iterate through picture info
        color_list = []                                         # list to store info for one pixel
        for bit in rgb_bin_list:
            if count < len(message_in_binary_concated):         # while message is being encoded
                short_bit = bit[:-1]                            # take off lowest bit
                short_bit += message_in_binary_concated[count]  # change to appropriate bit
                bit_to_appened = int(short_bit, 2)              # convert to base 10
                color_list.append(bit_to_appened)
                count += 1
            else:                                               # if message is finished
                color_list.append(int(bit, 2))                  # leave as is (but convert to base 10)
        photo_with_message_list.append(color_list)              # append pixel to list with all info

    # at this point you have a list of pixel info with message stored inside @ photo_with_message_list

    # now going to modify pixels in image to be saved with message
    count = 0                                                   # going through the list containing pixel info for pic containing message
    num_rows, num_cols, num_chans = image.shape
    for row in range(num_rows):                                 # iterating through info for original picture
        for col in range(num_cols):
            r, g, b = image[row, col]

            r = photo_with_message_list[count][2]               # change original picture info to reflect changes made previously
            g = photo_with_message_list[count][1]
            b = photo_with_message_list[count][0]

            stegged_image[row, col] = [r, g, b]                 # apply changes to copy of original images
            count += 1

    before = ''                                                 # create modified name for encoded image
    after = ''
    for character in range(len(image_name)):
        if image_name[character] != '.':
            before += image_name[character]
        else:
            after += image_name[character:]
            break

    cv2.imwrite('stegged.png', stegged_image)                   # save encoded image

