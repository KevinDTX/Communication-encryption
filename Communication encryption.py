# -*- coding: utf-8 -*-
# Date: 20190405
# Author: 一刀流狮子歌歌
# Aim: To encrypt the data and decrypt the data in the keyboard.


import time
import pyperclip
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
from PyCRC.CRC16SICK import CRC16SICK
import sys


# To show the welcome page
def display():
    print(" --------------------- Tool Description ---------------------- ")
    print("| ## This tool is used to encrypt your chat content！         |")
    print("| ## If you close the tool, you will not decrypt the content  |")
    print("| ## which is created by yourself!                            |")
    # print("| ## (2) Private key is to encrypt the content what you want  |")
    print("| ## Version: 1.0.0                                           |")
    print(" -------------------------------------------------------------")

# To encryt the data with the public key which got from others
def data_encryption(plain_text, public_key = b''):
    # To read the public key
    print("| ## 公钥加密开始")
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    # The message must be byte type.
    cipher_text = base64.b64encode(cipher.encrypt(plain_text.encode(encoding="utf-8")))
    # print(type(cipher_text))
    # print(cipher_text)
    print("| ## 公钥加密结束")
    return cipher_text

# To decrypt the cipher test with my private key
def data_decryption(cipher_text, private_key = b''):
    # To load the private key
    print("| ## 私钥解密开始")
    rsakey = RSA.importKey(private_key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    plain_text = cipher.decrypt(base64.b64decode(cipher_text), "ERROR")
    # print(type(plain_text))
    # print(plain_text)
    print("| ## 私钥解密结束")
    return plain_text

# To generate key pair
def generatekeypair():
    random_generator = Random.new().read
    # print(random_generator)
    rsa = RSA.generate(1024, random_generator)
    private_pem = rsa.exportKey()
    public_pem = rsa.publickey().exportKey()
    return private_pem,public_pem

# To monitor the keyboard
def keyboardmonitor():
    cipher_text = pyperclip.paste()
    print(cipher_text)
    # To copy to keyboard
    # pyperclip.copy()
    return cipher_text

# To construct the data to be sent
def send_data(header = '', data = b'', tail = ''):
    s_data = header + bytes.decode(data) + tail
    data = s_data + str(calculate_crc(s_data))
    return data

# To resolve the received data
def receive_data(r_data = ''):
    r_data_len = len(r_data)
    crc_num = r_data.rfind('==', 0, len(r_data)) + 2
    if crc_num == 1 :
        print("## Warning: The cipher data has been tampered!!!")
        print("## Please reenter the correct data!!!")
        return 'null'
    elif r_data[crc_num:] != str(calculate_crc(r_data[:crc_num])):
        print("## Warning: The cipher data has been tampered!!!")
        print("## Please reenter the correct data!!!")
        return 'null'
    else:
        cipher_text = r_data[6:r_data.rfind('/',7,r_data_len)]
        # print('#- Ciphertest is:')
        # print(cipher_text)
        return cipher_text

# To show the options
def show_options():
    print('--------------------- Option selections ----------------------')
    print('| ## Please select the following options:                 ## |')
    print('| ## 1. Show my public key;                               ## |')
    print('| ## 2. Create a cipher text;                             ## |')
    print('| ## 3. Decrypt a cipher message sent from a friend;      ## |')
    print('| ## 4. Add a new friend\'s public key;                    ## |')
    print('| ##                                                      ## |')
    print('| ## Please select the number above;                      ## |')
    print('| ## You could enter \'q\' to exit the process!             ## |')
    print('------------------- Option selections END --------------------')
    print()
    text_number = ''
    while True:
        channel = input('| ## You enter the number: ')
        if channel == '1':
            text_number = text_number + channel
            break
        elif channel == '2':
            text_number = text_number + channel
            break
        elif channel == '3':
            text_number = text_number + channel
            break
        elif channel == 'q':
            text_number = text_number + channel
            break
        elif channel == '4':
            text_number = text_number + channel
            break
        else:
            print('| ## Error number! Please enter again!')
    return text_number

# To calculate the CRC value
def calculate_crc(cipher_text = ''):
    return CRC16SICK().calculate(cipher_text)

# To judge the integrity of the public key
def judge_public_key_integrity(receive_data_str = ''):
    begin_key = receive_data_str.find('-----BEGIN PUBLIC KEY-----',0,len(receive_data_str))
    end_key = receive_data_str.rfind('-----END PUBLIC KEY-----',26,len(receive_data_str))
    key_num = receive_data_str.count('\\n')
    if key_num == 5 and begin_key == 0 and end_key > 0:
        return True
    else:
        return False

# The main function
if __name__ == '__main__':
    # To define the each part of the cipher
    header = 'plmWN/'
    tail = '/JBwsSVasiSB6hnng=='
    display()
    time.sleep(1)
    print('----------------------------Begin----------------------------')
    time.sleep(0.5)
    private_key, public_key = generatekeypair()
    print('| ###############')
    friend_public_key_dict = {}

    while True:
        options = show_options()
        if options == '1':
            print('------------------------ Option 1 -------------------------')
            print('| ## The following is your public key is:')
            public_key_final = str(public_key)[2:str(public_key).rfind('\'',2,len(public_key))]
            print(public_key_final)
            print()
            print('| ## Weather to copy your public key to the paste board?')
            while True:
                public_key_copy = input('| ## (Y/N): ')
                if public_key_copy == 'Y' or public_key_copy == 'y':
                    pyperclip.copy(public_key_final)
                    print('| ## After 10 seconds, the paste board will be clear!')
                    time.sleep(10)
                    pyperclip.copy('Null')
                    break
                elif public_key_copy == 'N' or public_key_copy == 'n':
                    break
                else:
                    print('| ## Please enter \'Y\' or \'N\'!')
            print('----------------------- Option 1 END ----------------------')
            print()
            print()
            print()
            time.sleep(2)
        elif options == '2':
            print('------------------------ Option 2 -------------------------')
            print('| ## Checking the public keys from friends! Waiting! ......')
            if len(friend_public_key_dict) == 0:
                print('| ## There are no public key from others. And add a new friend\'s public key at first!')
            else:
                print('| ## Now choose a friend name:')
                for l in friend_public_key_dict:
                    print('| ## Name: ', l)
                    print('| ## Public key: ', friend_public_key_dict[l])
                    print()
                print('| ## Is there a public key for the friend you want to use? If not, add your friend\'s public key to Option 4.')
                while True:
                    exist_friend_key = input('| ## (Y/N): ')
                    if exist_friend_key == 'Y' or exist_friend_key == 'y':
                        test_public_key = ''
                        while True:
                            test_friend_name = input('| ## Enter the friend name above in the list: ')
                            if test_friend_name in friend_public_key_dict:
                                test_public_key = friend_public_key_dict[test_friend_name]
                                break
                            else:
                                print('| ## You enter the wrong name in the list. Please enter again.')
                        while True:
                            # 此时的test_public_key是string类型
                            # 用他人的公钥对需要加密的内容进行加密
                            test_plain_text = input('| ## Please enter the plaintext you need to encrypt: ')

                            test_public_key_1 = '{begin1}\n{p1}\n{p2}\n{p3}\n{p4}\n{end1}'
                            # test_public_key_2 = input('| ## Please enter someone else\'s public key: ')
                            test_public_key_2 = test_public_key
                            list1 = test_public_key_2.split("\\n")
                            test_public_key_final = ''
                            test_public_key_final = test_public_key_1.format(begin1 = list1[0], p1 = list1[1], p2 = list1[2], p3 = list1[3], p4 = list1[4], end1 = list1[5])
                            test_send_cipher_text = data_encryption(test_plain_text, str.encode(test_public_key_final))
                            test_data = send_data(header, test_send_cipher_text, tail)
                            print('######################################################################')
                            print('| ## Encryption success!!! The encrypted data is:')
                            print(test_data)
                            pyperclip.copy(test_data)
                            print('| ## The ciphertext has been copied to the paste board!')
                            time.sleep(0.5)
                            print('######################################################################')
                            continue_yes_no = input('| ## Whether to continue decryption?(Y/N, or other keywords exit): ')
                            if continue_yes_no == 'Y' or continue_yes_no == 'y':
                                pass
                            else:
                                break
                        break
                    elif exist_friend_key == 'N' or exist_friend_key == 'n':
                        print('| ## All right. You might need to add a new friend\'s public key.')
                        break
                    else:
                        print('| ## Error 2! Enter the right key word!')
            print('----------------------- Option 2 END ----------------------')
            print()
            print()
            print()
            time.sleep(2)
        elif options == '3':
            print('------------------------ Option 3 -------------------------')
            print('| ## Start decrypting encrypted data ## |')
            while True:
                test_receive_cipher_data = ''
                while True:
                    test_receive_cipher_text = input('| ## Please enter ciphertext: ')
                    test_receive_cipher_data = receive_data(test_receive_cipher_text)
                    if test_receive_cipher_data == 'null':
                        print('| ## You enter the wrong ciphertext. Try again!')
                    else:
                        break
                test_receive_plain_text = data_decryption(test_receive_cipher_data, private_key)
                print('| #########################################################')
                print('| ## Original plaintext is: ' + bytes.decode(test_receive_plain_text))
                print('| #########################################################')
                decryption_exit = input('| ## Enter \'Y\' to continue to decrypt the ciphertext.(Y)')
                if decryption_exit == 'Y' or decryption_exit == 'y':
                    print()
                else:
                    print('| ## Now exit!')
                    break
            print('----------------------- Option 3 END ----------------------')
            print()
            print()
            print()
            time.sleep(2)
        elif options == 'q':
            break
        elif options == '4':
            print('------------------------ Option 4 -------------------------')
            print('| ## Start adding a new friend\'s public key ## |')
            confirm_new_name = True
            while confirm_new_name:
                new_friend_name_4 = input('| ## Enter your friend name: ')
                if new_friend_name_4 in friend_public_key_dict:
                    print('| ## The friend name has existed! Please choose another name.')
                    break
                else:
                    print('| ## Confirm to use this name: ' + new_friend_name_4)
                    while True:
                        new_friend_name_Y_N = input('| ## (Y/N): ')
                        if new_friend_name_Y_N == 'Y' or new_friend_name_Y_N == 'y':
                            new_friend_public_key = input('| ## Enter your new friend\'s public key: ')
                            new_friend_public_key_intergrity = judge_public_key_integrity(new_friend_public_key)
                            if new_friend_public_key_intergrity:
                                friend_public_key_dict[new_friend_name_4] = new_friend_public_key
                                print('| ## Adding a new friend\'s public key successfully!')
                                print('| ## Name: ' + new_friend_name_4, end ='    ')
                                print('| ## Public Key: ' + friend_public_key_dict[new_friend_name_4])
                                print()
                                confirm_new_name = False
                                break
                            else:
                                print('| ## Please enter the right public key!!!')
                                print()
                        elif new_friend_name_Y_N == 'N' or new_friend_name_Y_N == 'n':
                            print('| ## Please enter the right name!')
                            print()
                            break
                        else:
                            print('| ## Please enter the \'Y\' or \'N\'!')
                            print()
            print('----------------------- Option 4 END ----------------------')
            print()
            print()
            print()
            time.sleep(2)
        else:
            print('| ## Error 1!')
            time.sleep(2)
    print('---------------------------- END ----------------------------')

