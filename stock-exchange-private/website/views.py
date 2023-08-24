from flask import Blueprint, render_template, request, url_for, flash, redirect
from sqlalchemy import null
from flask_login import login_required, current_user
from website.models import User_Stock_Info
import yfinance as yf
import requests
from . import db
from datetime import datetime
from cachetools import cached, TTLCache
import re

cache = TTLCache(maxsize=256, ttl=3600)


views = Blueprint("views", __name__)


def subscribe_user(email, user_group_email, api_key):

    resp = requests.post(
        f"https://api.mailgun.net/v3/lists/{user_group_email}/members",
        auth=("api", api_key),
        data={"subscribed": True, "address": email},
    )

    print(resp.status_code)

    return resp


@views.route("/", methods=["GET", "POST"])
def home():

    # if user submits the form
    if request.method == "POST":

        email = request.form.get("email")

        subscribe_user(
            email=email,
            user_group_email="newsletter@sandbox19ce4f1055834080aa0b077e71af98f4.mailgun.org",
            api_key="6325dc122ba4abdff8c7bec3d00cc77e-0677517f-7ce70962",
        )

        flash("Tuned in!", category="success")

    return render_template(
        "home.html",
        user=current_user,
        #FB_open=round(FB["Open"][0], 2),
        #FB_high=round(FB["High"][0], 2),
        #FB_close=round(FB["Close"][0], 2),
        #Apple_open=round(Apple["Open"][0], 2),
       #  Apple_high=round(Apple["High"][0], 2),
        # Apple_close=round(Apple["Close"][0], 2),
        # Amazon_open=round(Amazon["Open"][0], 2),
         #Amazon_high=round(Amazon["High"][0], 2),
         # #Amazon_close=round(Amazon["Close"][0], 2),
         #Netflix_open=round(Netflix["Open"][0], 2),
         #Netflix_high=round(Netflix["High"][0], 2),
         #Netflix_close=round(Netflix["Close"][0], 2),
         #Google_open=round(Google["Open"][0], 2),
         #Google_high=round(Google["High"][0], 2),
         #Google_close=round(Google["Close"][0], 2),
         #Nvidia_open=round(Nvidia["Open"][0], 2),
         #Nvidia_high=round(Nvidia["High"][0], 2),
         #Nvidia_close=round(Nvidia["Close"][0], 2),
         #AMD_open=round(AMD["Open"][0], 2),
         #AMD_high=round(AMD["High"][0], 2),
         #AMD_close=round(AMD["Close"][0], 2),
         #Visa_open=round(Visa["Open"][0], 2),
         #Visa_high=round(Visa["High"][0], 2),
         #Visa_close=round(Visa["Close"][0], 2),
         #Mastercard_open=round(MasterCard["Open"][0], 2),
         #Mastercard_high=round(MasterCard["High"][0], 2),
         #Mastercard_close=round(MasterCard["Close"][0], 2),
        #Twitter_open=round(Twitter["Open"][0], 2),
        #Twitter_high=round(Twitter["High"][0], 2),
        #Twitter_close=round(Twitter["Close"][0], 2),
         #Tesla_open=round(Tesla["Open"][0], 2),
         #Tesla_high=round(Tesla["High"][0], 2),
         #Tesla_close=round(Tesla["Close"][0], 2),
         #JP_Morgan_open=round(JP_Morgan["Open"][0], 2),
         #JP_Morgan_high=round(JP_Morgan["High"][0], 2),
         #JP_Morgan_close=round(JP_Morgan["Close"][0], 2),
        # Walmart_open=round(Walmrt["Open"][0], 2),
         #Walmart_high=round(Walmrt["High"][0], 2),
         #Walmart_close=round(Walmrt["Close"][0], 2),
         #Coca_Cola_open=round(Coca_Cola["Open"][0], 2),
         #Coca_Cola_high=round(Coca_Cola["High"][0], 2),
         #Coca_Cola_close=round(Coca_Cola["Close"][0], 2),
    )


@views.route("/deposit")
@login_required
def deposit():
    return render_template("deposit.html", user=current_user)


@views.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit2():
    deposit_amount = request.form["amount"]
    cvv = request.form["CVV"]

    if not isValidCVVNumber(cvv):
        flash("CVV is invalid", category="error")
        return render_template("deposit.html", user=current_user)

    if is_valid_float(deposit_amount) and isValidCVVNumber(cvv):
        if float(deposit_amount) > 0:
            current_user.balance += float(deposit_amount)
            db.session.commit()
            flash("Deposit successful!", category="success")
            return render_template("deposit.html", user=current_user)
        else:
            flash("Deposit amount must be greater than 0", category="error")
            return render_template("deposit.html", user=current_user)
    return render_template("deposit.html", user=current_user)


@views.route("/withdraw")
@login_required
def withdraw():
    return render_template("withdraw.html", user=current_user)


@views.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw2():
    withdraw_amount = request.form["amount"]
    ban = request.form["BAN"]

    if int(ban) < 0:
        flash("Enter a valid bank account number", category="error")
        return render_template("withdraw.html", user=current_user)

    if is_valid_float(withdraw_amount) and int(ban) > 0:
        if (
            float(withdraw_amount) > 0
            and float(withdraw_amount) <= current_user.balance
        ):
            current_user.balance -= float(withdraw_amount)
            db.session.commit()
            flash("Withdrawal successful!", category="success")
            return render_template("withdraw.html", user=current_user)
        else:
            flash(
                "Withdrawal amount must be greater than 0 and less than your balance",
                category="error",
            )
            return render_template("withdraw.html", user=current_user)
    return render_template("withdraw.html", user=current_user)


@views.route("/termsofservice")
def termsofservice():
    return render_template("termsofservice.html", user=current_user)


@views.route("/privacy")
def privacy():
    return render_template("privacy.html", user=current_user)


recent_transactions = []


@views.route("/portfolio")
def portfolio():
    sum_ = 0
    all_stocks = []

    for i in User_Stock_Info.query.filter_by(user_id=current_user.id):
        sum_ += float(i.stock_price) * float(i.quantity)

        if i.quantity > 0:
            all_stocks.append(i)

    new_list = sorted(
        all_stocks, key=lambda x: float(x.stock_price) * float(x.quantity), reverse=True
    )

    actual_new_list = []
    for i in new_list:
        actual_new_list.append(
            [round(float(i.stock_price), 2), float(i.quantity), i.stock_id]
        )

    for i in actual_new_list:
        if float(i[1]) == float(0):
            actual_new_list.remove(i)

    our_users_list = []
    for i in recent_transactions:
        if i[0] == current_user.id:
            our_users_list.append(i)

    print(our_users_list)

    return render_template(
        "portfolio.html",
        user=current_user,
        account_balance=round(current_user.balance, 2),
        account_profit=round(current_user.profit, 2),
        account_holdings=round(sum_, 2),
        most_valuable=actual_new_list,
        recent=our_users_list,
    )


@views.route("/newsandinsights")
def newsandinsights():
    return render_template("newsandinsights.html", user=current_user)


@views.route("/lawsandpolicies")
def lawsandpolicies():
    return render_template("lawsandpolicies.html", user=current_user)


@views.route("/stockists")
def stockists():
    return render_template("stockists.html", user=current_user)


@views.route("/newsAndInsights")
def news():
    articles = Article.query.all()
    return render_template("newsAndInsights.html", events=articles)


@views.route("/event/<int:id>")
def event(id):
    event = Article.query.get_or_404(id)
    return render_template("event.html", event=event)


@views.route("/viewportfolio")
def view_portfolio():
    return render_template("viewportfolio.html", user=current_user)


@views.route("/buy")
@login_required
def buy():
    return render_template("buy.html", user=current_user)


@views.route("/buy", methods=["POST", "GET"])
@login_required
def buy2():
    # symbol
    text = request.form["text"].upper()
    print(bool(get_ticker(text) == None))

    if (yf.Ticker(text).info)["regularMarketPrice"] == None:
        flash("Please enter a valid stock symbol", category="error")
        return render_template("buy.html", user=current_user)

    # quantity
    text2 = request.form["text2"]

    if is_valid_float(text2) == False:
        flash("Please enter a valid quantity", category="error")
        return render_template("buy.html", user=current_user)
    # Want to see if row in database already exists with user_id and stock_id, returns true if it exists
    if bool(
        User_Stock_Info.query.filter_by(user_id=current_user.id, stock_id=text).first()
    ):
        print("yee")

        user_row = User_Stock_Info.query.filter_by(
            user_id=current_user.id, stock_id=text
        ).first()

        print(user_row)

        if current_user.balance >= get_current_price(text) * float(text2):
            old_quantity = user_row.quantity
            new_quantity = float(old_quantity) + float(text2)
            old_profit = current_user.profit
            new_profit = float(old_profit) - (
                float(get_current_price(text)) * float(text2)
            )
            print(new_profit)
            user_row.quantity = new_quantity
            current_user.profit = new_profit
            db.session.commit()
            current_user.balance -= get_current_price(text) * float(text2)
            db.session.commit()

            print("found existing row and updated quantity")
            flash("Stocks Bought successfully!", category="success")

            recent_transactions.append(
                [
                    current_user.id,
                    user_row.stock_id,
                    text2,
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "+",
                ]
            )

            return render_template("buy.html", user=current_user)
        else:
            print("found existing row but not enough money")
            flash("Not enough money", category="error")
            return render_template("buy.html", user=current_user)
    else:
        print("noooo")
        tracker = 0
        if User_Stock_Info.query.filter_by().first():
            last = User_Stock_Info.query.order_by(
                User_Stock_Info.transaction_id.desc()
            ).first()
            tracker = int(last.transaction_id)
        else:
            tracker = 0

        if current_user.balance >= get_current_price(text) * float(text2):

            added_row = User_Stock_Info(
                transaction_id=tracker + 1,
                stock_id=text,
                stock_price=get_current_price(text),
                user_id=current_user.id,
                quantity=text2,
            )
            db.session.add(added_row)
            db.session.commit()

            current_user.balance -= get_current_price(text) * float(text2)
            old_profit = current_user.profit
            new_profit = float(old_profit) - float(get_current_price(text)) * float(
                text2
            )
            print(new_profit)
            current_user.profit = new_profit
            db.session.commit()
            recent_transactions.append(
                [
                    current_user.id,
                    added_row.stock_id,
                    text2,
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "+",
                ]
            )

            print("added new row and updated balance")
            flash("Stocks Bought successfully!", category="success")
            return render_template("buy.html", user=current_user)
        else:
            print("not enough money")
            flash("Not enough money", category="danger")

            return render_template("buy.html", user=current_user)


@views.route("/sell")
@login_required
def sell():
    return render_template("sell.html", user=current_user)


@views.route("/sell", methods=["POST", "GET"])
@login_required
def sell2():
    # symbol
    text = request.form["text"].upper()
    # quantity
    text2 = request.form["text2"]
    print(text2)
    print(type(text2))

    if is_valid_float(text2) == False:
        flash("Please enter a valid quantity", category="error")
        return render_template("sell.html", user=current_user)
    print(text)
    print(text2)
    # Want to see if row in database already exists with user_id and stock_id, returns true if it exists
    if bool(
        User_Stock_Info.query.filter_by(user_id=current_user.id, stock_id=text).first()
    ):
        user_row = User_Stock_Info.query.filter_by(
            user_id=current_user.id, stock_id=text
        ).first()
        if user_row.quantity >= float(text2):
            old_quantity = user_row.quantity
            new_quantity = float(old_quantity) - float(text2)
            old_profit = current_user.profit
            new_profit = float(old_profit) + float(get_current_price(text)) * float(
                text2
            )

            user_row.quantity = new_quantity
            db.session.commit()
            current_user.profit = new_profit
            current_user.balance += get_current_price(text) * float(text2)
            db.session.commit()

            print("found existing row and updated quantity")
            flash("Stocks Sold successfully!", category="success")
            recent_transactions.append(
                [
                    current_user.id,
                    user_row.stock_id,
                    text2,
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "-",
                ]
            )
            return render_template("sell.html", user=current_user)

        else:
            print("here")
            print(text2)
            print(user_row.quantity)
            flash("Not enough stocks to sell", category="error")
            print("found existing row but not enough stocks")
            return render_template("sell.html", user=current_user)
    else:
        flash("You do not own the stock you are trying to sell!", category="error")
        print("you dont own the stock ur trying to sell idiot")
        return render_template("sell.html", user=current_user)


# @views.route("/quote", methods=["POST", "GET"])
# def my_form_post():
#     text = request.form["text"]
#     processed_text = str(round(get_current_price(text), 4))
#     comp_name = company_name(text)
#     ticker_symbol = get_ticker(text)
#     return render_template(
#         "stockpage.html",
#         user=current_user,
#         text=processed_text,
#         text2=comp_name,
#         text3=ticker_symbol,
#     )


@views.route("/quote", methods=["POST", "GET"])
@login_required
def quote():
    if request.method == "POST":
        text = request.form["text"].upper()
        if (yf.Ticker(text).info)["regularMarketPrice"] == None:
            flash("Please enter a valid stock symbol", category="error")
            return render_template("quote.html", user=current_user)
        return redirect(url_for("views.my_form_post", stockticker=text))
    else:
        return render_template(
            "quote.html",
            user=current_user,
            tesla=round(Tesla["Close"][0], 2),
            apple=round(Apple["Close"][0], 2),
            amazon=round(Amazon["Close"][0], 2),
            google=round(Google["Close"][0], 2),
            microsoft=round(Microsoft["Close"][0], 2),
            facebook=round(FB["Close"][0], 2),
            nvidia=round(Nvidia["Close"][0], 2),
            intel=round(Intel["Close"][0], 2),
            netflix=round(Netflix["Close"][0], 2),
        )


@views.route("/<stockticker>")
def my_form_post(stockticker):
    text = stockticker
    processed_text = str(round(get_current_price(text), 4))
    comp_name = company_name(text)
    ticker_symbol = get_ticker(text)
    return render_template(
        "stockpage.html",
        user=current_user,
        text=processed_text,
        text2=comp_name,
        text3=ticker_symbol,
    )


def get_ticker(symbol):
    ticker = symbol
    return symbol


def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period="1d")
    return todays_data["Close"][0]


@cached(cache)
def get_data(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period="1d")
    return todays_data


def company_name(symbol):
    ticker = yf.Ticker(symbol)
    company_name = ticker.info["longName"]
    return company_name


def is_valid_float(element: str) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def isValidCVVNumber(str):
    # Regex to check valid
    # CVV number.
    regex = "^[0-9]{3,4}$"

    # Compile the ReGex
    p = re.compile(regex)

    # If the string is empty
    # return false
    if str == None:
        return False

    # Return if the string
    # matched the ReGex
    if re.search(p, str):
        return True
    else:
        return False


@views.route("/stockpage")
@login_required
def stockpage():
    return render_template("stockpage.html", user=current_user)


"""FB = get_data("FB")
Apple = get_data("AAPL")
Amazon = get_data("AMZN")
Netflix = get_data("NFLX")
Google = get_data("GOOG")
Nvidia = get_data("NVDA")
AMD = get_data("AMD")
Visa = get_data("V")
MasterCard = get_data("MC")
Twitter = get_data("TWTR")
Tesla = get_data("TSLA")
JP_Morgan = get_data("JPM")
Walmrt = get_data("WMT")
Coca_Cola = get_data("KO")
Microsoft = get_data("MSFT")
Intel = get_data("INTC")"""
