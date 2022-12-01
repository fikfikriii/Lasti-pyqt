import re
import sqlite3

import bcrypt

# conn = sqlite3.connect("fitpal.db")
# c = conn.cursor()
# c.execute("SELECT * FROM workout_history")
# print(c.fetchall())
arr = []
def emailValidation(email):
      #example@gmail.com
      #13520029@std.stei.itb.ac.id
      validEmail = r"[A-Za-z0-9._]+@[A-Za-z0-9.]+\.[A-Z|a-z]{2,}"
      if re.match(validEmail, email):
          print("MASUK BOS")
      else:
          print("email is invalid")

def hashPassword(password):
    bytePass = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashedPass = bcrypt.hashpw(bytePass, salt)
    print(salt, bytePass, hashedPass)
    return hashedPass

while True:
    print(arr)
    inp = input()
    temp = hashPassword(inp)
    print(temp.decode())
    print(bcrypt.checkpw(inp.encode('utf-8'), temp))
    arr.append(temp)
