#!/usr/bin/env python
# coding: utf-8

# In[53]:


import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import mysql.connector
import base64
import os


# In[54]:


key = Fernet.generate_key()
file = open('key.key', 'wb') 
file.write(key)
file.close()


# In[66]:


file = open('key.key', 'rb')
key = file.read()
file.close()


def encrypt_data():
    cnx = mysql.connector.connect(user='****', password='********', host='127.0.0.1',
                                  database='onlinefoodorderingdb', auth_plugin='mysql_native_password')

    cursor = cnx.cursor()
    query = ("SELECT * FROM customer_data limit 1;")
    cursor.execute(query)
    
    myresult = cursor.fetchall()
    
    with open('credit_card_demo.txt', 'w') as f:
        for row in myresult:
            f.write(str(row))
            print("Data to be Encrypted: ", row, "\n")
        
    with open('credit_card_demo.txt', 'rb') as f:
        data = f.read()
        
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    
    print("Encrypted Data: ", encrypted_data, "\n")
    
    with open('credit_card_demo.txt.encrypted', 'wb') as f:
        f.write(encrypted_data)
    
    cursor.close()
    cnx.close()


# In[67]:


def decrypt_data():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()

    with open('credit_card_demo.txt.encrypted', 'rb') as f:
            data = f.read()

    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(data)

    print("Decrypted Data: ", decrypted_data)

    with open('credit_card_demo.txt.encrypted', 'wb') as f:
        f.write(decrypted_data)


# In[68]:


if '__name__' == '__main__':
    encrypt_data()
    decrypt_data()


# In[ ]:




