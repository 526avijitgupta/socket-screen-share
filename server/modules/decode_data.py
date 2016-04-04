def decode_data(data_to_decode):
    databyte = bytearray(data_to_decode)
    datalen = (0x7F & databyte[1])
    if(datalen > 0):
        mask_key = databyte[2:6]
        masked_data = databyte[6:(6+datalen)]
        unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
        data_from_client = str(bytearray(unmasked_data))
    return data_from_client or data_to_decode

