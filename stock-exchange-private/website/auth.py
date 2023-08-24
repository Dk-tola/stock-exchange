from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .twoFA import authentication
import time
import re


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session["email"] = email
                return redirect(url_for("auth.sendCode"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/twoFactorAuthentication", methods=["GET", "POST"])
def twoFactorAuthentication():
    # Put here 2 factor auth
    start = time.time()
    # while time.time() - start < 60: # 60 secs.
    if request.method == "POST":
        submittedCode = str(request.form.get("code"))
        print("SUBMITTED CODE: ", submittedCode)
        if submittedCode == session.get("code", None):
            user = User.query.filter_by(email=session.get("email", None)).first()
            # flash("Logged in successfully!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.portfolio"))
        else:
            flash("Code is Invalid, try again.")
    return render_template("codeverification.html", user=current_user)


@auth.route("/sendCode")
def sendCode():
    my_var = session.get("email", None)
    print(my_var)
    print("Hello")
    verificationCode = authentication(my_var)
    session["code"] = verificationCode
    print("VERIFICATION CODE: ", verificationCode)
    flash("A code has been sent to your email")
    return redirect(url_for("auth.twoFactorAuthentication"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        address = request.form.get("address")
        city = request.form.get("city")
        zipcode = request.form.get("zipcode")
        phonenumber = request.form.get("phonenumber")
        bankaccount = request.form.get("bankaccount")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        SpecialSym = [
            "$",
            "@",
            "#",
            "%",
            "^",
            "&",
            "*",
            "?",
            "~",
            "`",
            "!",
        ]

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Account by the following email already exists!", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater then 1 character.", category="error")
        elif len(last_name) < 2:
            flash("Last name must be greater then 1 character.", category="error")
        elif len(address) < 4:
            flash("Address must be greater than 3 characters.", category="error")
        elif len(city) < 2:
            flash("City must be greater then 1 character.", category="error")
        elif len(zipcode) < 4:
            flash("Zip code must be greater then 3 characters.", category="error")
        elif len(phonenumber) < 6:
            flash("Last name must be greater then 5 characters.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be atleast 7 characters.", category="error")
        elif re.search("[0-9]", password1) is None:
            flash("Make sure your password has a number in it", category="error")
        elif re.search("[A-Z]", password1) is None:
            flash(
                "Make sure your password has a capital letter in it", category="error"
            )
        elif not any(char in SpecialSym for char in password1):
            flash(
                "Make sure your password has a special character in it $@#!",
                category="error",
            )
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                address=address,
                city=city,
                zipcode=zipcode,
                phonenumber=phonenumber,
                bankaccount=bankaccount,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully.", category="success")
            # return redirect(url_for("views.home"))
            return redirect(url_for("auth.logout"))

    return render_template("sign_up.html", user=current_user)


@auth.route("/contactus", methods=["GET", "POST"])
def contactus():

    return render_template("contactus.html", user=current_user)
