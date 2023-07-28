from flask import Blueprint, request, Response, jsonify

authentication = Blueprint("authentication", __name__)

from utils import (
    validate_user_input,
    generate_salt,
    generate_hash,
    db_write,
    validate_user,
    verify_jwt_token,
    get_user_by_id,
)


@authentication.route("/register", methods=["POST"])
def register_user():
    print(request.json)
    user_email = request.json["email"]
    user_password = request.json["password"]
    user_confirm_password = request.json["confirm_password"]
    print(
        user_email,
        user_password,
        user_confirm_password,
        user_password == user_confirm_password,
    )
    print(
        validate_user_input("authentication", email=user_email, password=user_password)
    )
    if user_password == user_confirm_password and validate_user_input(
        "authentication", email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)

        if db_write(
            "INSERT INTO users (email, password_salt, password_hash) VALUES (%s, %s, %s)",
            (user_email, password_salt, password_hash),
        ):
            return Response(status=201)
        else:
            return Response(status=409)
    else:
        return Response(status=400)


@authentication.route("/login", methods=["POST"])
def login_user():
    user_email = request.json["email"]
    user_password = request.json["password"]

    user_token = validate_user(user_email, user_password)
    print("Valided", user_token)

    if user_token:
        # return jsonify({"jwt_token": "asda"})
        return jsonify({"jwt_token": user_token})
    else:
        return Response(status=401)
        # print("asda")
        # return jsonify({"jwt_token": "asda"})


@authentication.route("/verify_user", methods=["POST"])
def verify_user():
    token = request.json["token"]
    data = verify_jwt_token(token)
    user = get_user_by_id(data["id"])
    return jsonify({"data": user})
