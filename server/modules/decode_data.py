def decode_data(data_to_decode):
    databyte = bytearray(data_to_decode)
    datalen = (0x7F & databyte[1])
    data_from_client = data_to_decode
    if(datalen > 0):
        mask_key = databyte[2:6]
        masked_data = databyte[6:(6+datalen)]
        unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
        data_from_client = str(bytearray(unmasked_data))
    return data_from_client

# def decode_data(stringStreamIn):

#     # Turn string values into opererable numeric byte values
#     byteArray = [ord(character) for character in stringStreamIn]
#     datalength = byteArray[1] & 127
#     indexFirstMask = 2

#     if datalength == 126:
#         indexFirstMask = 4
#     elif datalength == 127:
#         indexFirstMask = 10

#     # Extract masks
#     masks = [m for m in byteArray[indexFirstMask : indexFirstMask+4]]
#     indexFirstDataByte = indexFirstMask + 4

#     # List of decoded characters
#     decodedChars = []
#     i = indexFirstDataByte
#     j = 0

#     # Loop through each byte that was received
#     while i < len(byteArray):

#         # Unmask this byte and add to the decoded buffer
#         decodedChars.append( chr(byteArray[i] ^ masks[j % 4]) )
#         i += 1
#         j += 1

#     # Return the decoded string
#     return decodedChars

