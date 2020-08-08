#!/usr/bin/env python
# coding: utf-8

# In[4]:


import random
import mysql.connector
import time
import datetime
from faker import Factory
from dateutil.parser import parse

fake = Factory.create()


# In[5]:


def generate_card_no():
    t2 = '4605'
    t1 = (random.randrange(10209781, 99201719))
    t4 = (random.randrange(1624, 9276))
    t3 = t2 + str(t1) + str(t4)
    return t3


# In[6]:


def generateSSN() :
    return fake.ssn()


# In[7]:


def generate_uuid() :
    fake = Factory.create()
    uuid = fake.uuid4()
    uuid = uuid.replace("-", "").upper()
    return uuid


# In[8]:


def generate_password():
    return fake.password(length=12)


# In[9]:


def generateAddress() :
    address = {}
    fullAddress = fake.address()
    addressParts = fullAddress.splitlines()
    address["address"] = addressParts[0]
    if "," in addressParts[1] :
        cityStateZip = addressParts[1].split(",")
        stateZip = cityStateZip[1].split()
        address["city"] = cityStateZip[0]
        address["state"] = stateZip[0]
        address["postalCode"] = stateZip[1]
    else :
        cityStateZip = addressParts[1].split()
        address["city"] = cityStateZip[0]
        address["state"] = cityStateZip[1]
        address["postalCode"] = cityStateZip[2]
    return address


# In[10]:


def generateName(gender=None):
    name = {}
    if gender is None:
        name['firstName'] = fake.first_name()
    else :
        if gender == 'Male':
            name['firstName'] = fake.first_name_male()
            name['gender'] = 'Male'
        else:
            name['firstName'] = fake.first_name_female()
            name['gender'] = 'Female'
    name["lastName"] = fake.last_name()
    return name


# In[11]:


def generateContact() :
    contact = {}
    contact["email"] = fake.email()
    contact["phone"] = fake.phone_number()
    return contact


# In[12]:


def generate_random_data(gender):
    uuid = generate_uuid()
    ssn = generateSSN()
    address = generateAddress()
    name = generateName(gender)
    contact = generateContact()
    masked_credit_data = mask_credit_card()
    return uuid, ssn, address, name, contact


# In[13]:


def generate_employee_record(uuid, ssn, address, name, contact):
    member = {}
    member['emp_id'] = uuid
    member['ssn'] = ssn
    member['firstName'] = name['firstName']
    member['lastName'] = name['lastName']
    member['gender'] = name['gender']
    member['address'] = address["address"]
    member['city'] =  address["city"]
    member['state'] = address["state"]
    member['postalCode'] = address["postalCode"]
    member["phone"] = contact["phone"]
    member["email"] = contact["email"]
    member["salary"] = round(random.uniform(3000, 9200), 2)
    return member


# In[14]:


def generate_customer_record(address, name, contact):
    customer = {}
    customer['username'] = fake.user_name()
    customer['firstName'] = name['firstName']
    customer['lastName'] = name['lastName']
    customer['password'] = generate_password()
    customer['gender'] = name['gender']
    customer['address'] = address["address"]
    customer['city'] =  address["city"]
    customer['state'] = address["state"]
    customer['postalCode'] = address["postalCode"]
    customer["phone"] = contact["phone"]
    customer["email"] = contact["email"]
    customer["creditCard"] = generate_card_no()
    customer["paymentID"] = random.randrange(129483, 981924)
    customer["orderID"] = random.randrange(1723, 9328)
    return customer


# # Masking

# In[86]:


def mask_credit_card(get_credit_cards_no):
    length = len(get_credit_cards_no)
    card_no_new = "X" * (length - 4) + get_credit_cards_no[length - 4:]
    return card_no_new


# In[65]:


def mask_SSN(ssn):
    #ssn = generateSSN()
    masked_ssn = "X" * (len(ssn) - 8) + ssn[3] + "X" * (len(ssn[len(ssn) - 7:len(ssn) - 5])) + ssn[6] +                 "X" * len((ssn[len(ssn) - 4:len(ssn) - 2])) + ssn[-2:]
        
    return masked_ssn


# # MySQL Connections

# In[82]:


def create_cust_tables():
    cnx = mysql.connector.connect(user='****', password='*********', host='127.0.0.1',
                                  database='onlinefoodorderingdb', auth_plugin='mysql_native_password')

    cursor = cnx.cursor()

    cursor.execute("DROP TABLE IF EXISTS CUSTOMER_MASKED_DATA")

    sql ='''CREATE TABLE CUSTOMER_MASKED_DATA(
       username VARCHAR(255) NOT NULL,
       firstName VARCHAR(100),
       lastName VARCHAR(100),
       gender VARCHAR(100),
       address VARCHAR(255),
       city VARCHAR(100),
       state VARCHAR(100),
       postalCode VARCHAR(100),
       phone VARCHAR(100),
       email VARCHAR(100),
       creditCard_masked VARCHAR(100),
       paymentID INT(100),
       orderID INT(100)
    )'''
    cursor.execute(sql)

    cnx.close()


# In[57]:


def create_emp_tables():
    cnx = mysql.connector.connect(user='****', password='*********', host='127.0.0.1',
                                  database='onlinefoodorderingdb', auth_plugin='mysql_native_password')

    cursor = cnx.cursor()

    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE_MASKED_DATA")

    
    sql ='''CREATE TABLE EMPLOYEE_MASKED_DATA(
       emp_id VARCHAR(255) NOT NULL,
       masked_ssn VARCHAR(100),
       firstName VARCHAR(100),
       lastName VARCHAR(100),
       gender VARCHAR(100),
       address VARCHAR(255),
       city VARCHAR(100),
       state VARCHAR(100),
       postalCode VARCHAR(100),
       phone VARCHAR(100),
       email VARCHAR(100),
       salary VARCHAR(100)
    )'''
    cursor.execute(sql)

    cnx.close()


# In[101]:


def insert_data():
    cnx = mysql.connector.connect(user='****', password='*********', host='127.0.0.1',
                                  database='onlinefoodorderingdb', auth_plugin='mysql_native_password')

    cursor = cnx.cursor()
    
    
    add_employee_record = ("INSERT INTO employee_data "
                          "(emp_id, ssn, firstName, lastName, gender, address, city, state, postalCode, phone, email, salary)"
                          "VALUES (%(emp_id)s, %(ssn)s, %(firstName)s, %(lastName)s, %(gender)s, %(address)s, %(city)s,\
                          %(state)s, %(postalCode)s, %(phone)s, %(email)s, %(salary)s)")

    
    add_customer_record = ("INSERT INTO customer_data "
                          "(username, firstName, lastName, password, gender, address, city, state, postalCode, phone, email,\
                          creditCard,paymentID, orderID)"
                          "VALUES (%(username)s, %(firstName)s, %(lastName)s, %(password)s, %(gender)s, %(address)s, %(city)s,\
                          %(state)s, %(postalCode)s, %(phone)s, %(email)s, %(creditCard)s, %(paymentID)s, %(orderID)s)")
    
    list_gender = ['Male', 'Female', 'Male', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Male', 'Female',
                  'Female', 'Male', 'Female', 'Female', 'Male', 'Male', 'Male', 'Female', 'Male', 'Male', 'Female', 'Female',
                   'Male',]
    
    
    for i in list_gender:
        uuid, ssn, address, name, contact = generate_random_data(i)
        record = generate_employee_record(uuid, ssn, address, name, contact)
        cursor.execute(add_employee_record, record)
 
    
    for i in list_gender:
        uuid, ssn, address, name, contact = generate_random_data(i)
        record = generate_customer_record(address, name, contact)
        cursor.execute(add_customer_record, record)
        
    
    cnx.commit()
    cursor.close()
    cnx.close()


# In[78]:


def select_emp_query():
    cnx = mysql.connector.connect(user='****', password='*********', host='127.0.0.1',
                                  database='onlinefoodorderingdb', auth_plugin='mysql_native_password')

    cursor = cnx.cursor(buffered=True)
    query = ("SELECT * FROM employee_data")
    cursor.execute(query)
    
    add_maskedemployee_record = ("INSERT INTO employee_masked_data "
                          "(emp_id, masked_ssn, firstName, lastName, gender, address, city, state, postalCode, phone, email, salary)"
                          "VALUES (%(emp_id)s, %(masked_ssn)s, %(firstName)s, %(lastName)s, %(gender)s, %(address)s, %(city)s,\
                          %(state)s, %(postalCode)s, %(phone)s, %(email)s, %(salary)s)")
    
    cursor1 = cnx.cursor()
    
    for row in cursor:
        member_masked = {}
        member_masked['emp_id'] = row[0]
        member_masked['masked_ssn'] = mask_SSN(row[1])
        member_masked['firstName'] = row[2]
        member_masked['lastName'] = row[3]
        member_masked['gender'] = row[4]
        member_masked['address'] = row[5]
        member_masked['city'] =  row[6]
        member_masked['state'] = row[7]
        member_masked['postalCode'] = row[8]
        member_masked["phone"] = row[9]
        member_masked["email"] = row[10]
        member_masked["salary"] = row[11]
        cursor1.execute(add_maskedemployee_record, member_masked)
        
        
    cnx.commit()
    cursor.close()
    cursor1.close()
    cnx.close()


# In[84]:


def select_cust_query():
    cnx = mysql.connector.connect(user='****', password='*******', host='127.0.0.1',
                                  database='onlinefoodorderingdb', auth_plugin='mysql_native_password')

    cursor = cnx.cursor(buffered=True)
    query = ("SELECT * FROM customer_data")
    cursor.execute(query)
    
    add_maskedcustomer_record = ("INSERT INTO customer_masked_data "
                              "(username, firstName, lastName, gender, address, city, state, postalCode, phone, email,\
                              creditCard_masked,paymentID, orderID)"
                              "VALUES (%(username)s, %(firstName)s, %(lastName)s, %(gender)s, %(address)s, %(city)s,\
                              %(state)s, %(postalCode)s, %(phone)s, %(email)s, %(creditCard_masked)s, %(paymentID)s,\
                              %(orderID)s)")
    cursor1 = cnx.cursor()
    
    for row in cursor:
        customer_masked = {}
        customer_masked['username'] = row[0]
        customer_masked['firstName'] = row[1]
        customer_masked['lastName'] = row[2]
        customer_masked['gender'] = row[3]
        customer_masked['address'] = row[4]
        customer_masked['city'] =  row[5]
        customer_masked['state'] = row[6]
        customer_masked['postalCode'] = row[7]
        customer_masked["phone"] = row[8]
        customer_masked["email"] = row[9]
        customer_masked["creditCard_masked"] = mask_credit_card(row[10])
        customer_masked["paymentID"] = row[11]
        customer_masked["orderID"] = row[12]
        cursor1.execute(add_maskedcustomer_record, customer_masked)
        
        
    cnx.commit()
    cursor.close()
    cursor1.close()
    cnx.close()


# In[87]:


def main():
    create_cust_tables()
    create_emp_tables()
    insert_data()
    select_emp_query()
    select_cust_query()


# In[1]:


if "__name__" == "__main__":
    main()

