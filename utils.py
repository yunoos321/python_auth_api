from hashlib import pbkdf2_hmac
from settings import JWT_SECRET_KEY

# from app import mydb
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", user="root", password="root", database="python_auth"
)


import os
import jwt


def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False


def generate_salt():
    salt = os.urandom(16)
    return salt.hex()


def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()


def db_write(query, params):
    print(query, params)
    # return True
    # cursor = mydb.connection.cursor()

    mycursor = mydb.cursor(dictionary=True)

    # try:
    mycursor.execute(query, params)
    mydb.commit()
    # cursor.execute(query, params)
    # db.connection.commit()
    # cursor.close()

    return True

    # except MySQLdb._exceptions.IntegrityError:
    #     cursor.close()
    #     return False


def db_read(query, params=None):
    print(query, params)
    mycursor = mydb.cursor(dictionary=True)

    # cursor = db.connection.cursor()
    if params:
        # cursor.execute(query, params)
        mycursor.execute(query, params)
    else:
        # cursor.execute(query)
        mycursor.execute(query)

    # entries = cursor.fetchall()
    entries = mycursor.fetchall()
    # cursor.close()

    content = []

    for entry in entries:
        content.append(entry)
    return content


def generate_jwt_token(content):
    print("generate_jwt_token - 1", content)
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    print("generate_jwt_token - 2", encoded_content, JWT_SECRET_KEY)
    # token = str(encoded_content).split("'")
    token = encoded_content
    print("generate_jwt_token - 3", token)
    return token


def verify_jwt_token(token):
    print("verify_jwt_token - 1", token)
    decoded_token = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[
            "HS256",
        ],
    )
    print("verify_jwt_token - 2", decoded_token, JWT_SECRET_KEY)
    # token = str(decoded_token).split("'")
    decoded_token
    print("verify_jwt_token - 3", decoded_token)
    return decoded_token


def validate_user(email, password):
    print(email, password)
    current_user = db_read("SELECT * FROM users WHERE email = %s", (email,))
    print("asdfasd", current_user)

    if len(current_user) == 1:
        print(current_user[0])
        saved_password_hash = current_user[0]["password_hash"]
        print("Step2")
        saved_password_salt = current_user[0]["password_salt"]
        print("Step3")
        password_hash = generate_hash(password, saved_password_salt)
        print("Step4")

        if password_hash == saved_password_hash:
            user_id = current_user[0]["id"]
            print("Step5", user_id)
            jwt_token = generate_jwt_token({"id": user_id})
            print("jwt_token", jwt_token)
            return jwt_token
        else:
            print("Step5 Else")
            return False

    else:
        return False


def get_user_by_id(id):
    print(id)
    current_user = db_read("SELECT * FROM users WHERE id = %s", (id,))
    return current_user
