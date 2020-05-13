import hashlib, binascii, os

### class for DB controling
### It has user add and user athentication functions
class DBControl:
    def __init__(self, cursor):
        self.cursor = cursor

    ### a function for hasing a given password
    def hash_password(password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    ### identify whether the stored and the given passwords are the same
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    ### user add function
    def add_new_user(self, account, pwd, name, email, phone):
        pwd = DBControl.hash_password(pwd)
        confirmed = 0
        confirmed_on = "0000-00-00 00:00:00"

        self.cursor.execute("INSERT INTO sjaws.user ("
                                 "userID,"
                                 "userPWD,"
                                 "userName,"
                                 "userEmail,"
                                 "userPhone,"
                                 "confirmed,"
                                 "confirmed_on) VALUES (%s, %s, %s, %s, %s, %d, %s)",
                                 (account,
                                  pwd,
                                  name,
                                  email,
                                  phone,
                                  confirmed,
                                  confirmed_on
                                  ))
        result = self.cursor.fetchall()

        return result

    ### user athentication function
    def user_athentication(self, account, pwd):
        self.cursor.execute("SELECT userPWD FROM sjaws.user WHERE userID = %s", account)

        result = self.cursor.fetchall()

        ### len(result) == 0 indicates that there is no such user
        if len(result) > 0 and DBControl.verify_password(result[0][0], pwd):
            return True
        else:
            return False
