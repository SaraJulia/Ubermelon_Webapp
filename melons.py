from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

melon_dict = {}

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    print session["cart"]

    create_melon_dict()
    melon_dict = session['melon_dict']
    total = total_price()

    print "Melon dict is:", melon_dict

    print "Melon dict is now (line 49):", melon_dict

    return render_template("cart.html", melon_dict = melon_dict, total = total)

def total_price():
    melon_dict = session['melon_dict']
    total = 0

    for melon in melon_dict.values():
        print "Adding melon: ", melon
        print "The total is now:", total
        total = total + melon[3]

    return total        


def create_melon_dict():
    melon_dict = {}
    
    if "melon_dict" in session:
        for id in session["cart"]:
            if id not in melon_dict:
                new_melon = model.get_melon_by_id(id)
                melon_info = [new_melon.common_name, new_melon.price, 1, new_melon.price*1]
                melon_dict[id] = melon_info
            else:
                melon_dict[id][2] += 1
                melon_dict[id][3] += melon_dict[id][3] + melon_dict[id][2]
    else:
        session["melon_dict"] = {}
        for id in session["cart"]:
            if id not in melon_dict:
                new_melon = model.get_melon_by_id(id)
                melon_info = [new_melon.common_name, new_melon.price, 1, new_melon.price*1]
                melon_dict[id] = melon_info
            else:
                melon_dict[id][2] += 1
                melon_dict[id][3] += melon_dict[id][3] + melon_dict[id][2]
    
    session["melon_dict"] = melon_dict

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    if "cart" in session.keys():
       session["cart"].append(id)
    else:
        session["cart"] = [id]

    flash("Successfully added to cart!")
    return render_template("/cart.html", melon_dict = melon_dict)

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
