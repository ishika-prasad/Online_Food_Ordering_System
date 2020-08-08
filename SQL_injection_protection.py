#!/usr/bin/env python
# coding: utf-8

# In[16]:


import time
import MySQLdb


# In[42]:


username = input('Enter username: ')


# In[31]:


try:
    db = MySQLdb.connect(host="127.0.0.1", user="****", passwd="********", db="onlinefoodorderingdb")
    cur = db.cursor()

    cur.execute("SELECT * FROM cust_data_test WHERE username = '%s';" %username)
    for row in cur.fetchall():
        print(row)
    db.close()

except MySQLdb.OperationalError as e:
    print("Exception - OperationalError: ", e)
    
except MySQLdb.ProgrammingError as e:
    print(data)
    print("ProgrammingError:", e)


# In[40]:


try:
    db = MySQLdb.connect(host="127.0.0.1", user="****", passwd="********", db="onlinefoodorderingdb")
    cur = db.cursor()

    cur.execute("SELECT * FROM cust_data_test WHERE username = %s;", (username,))
    for row in cur.fetchall():
        print(row)
    db.close()
    
except MySQLdb.OperationalError as e:
    print("Exception - OperationalError: ", e)
    
except MySQLdb.ProgrammingError as e:
    print("ProgrammingError:", e)


# In[43]:


db = MySQLdb.connect(host="127.0.0.1", user="****", passwd="********", db="onlinefoodorderingdb")
cur = db.cursor()

cur.execute("SELECT * FROM cust_data_test WHERE username = %s;", (username,))
for row in cur.fetchall():
    print(row)
db.close()


# In[ ]:




