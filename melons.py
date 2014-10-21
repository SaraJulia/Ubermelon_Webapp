from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    session["customer"] = session.get("customer", None)
    print session["customer"]
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
    # print session["cart"]

    create_melon_dict()
    melon_dict = session['melon_dict']
    total = total_price()

    # print "Melon dict is:", melon_dict

    # print "Melon dict is now (line 49):", melon_dict

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
    
    if "melon_dict" not in session:
        session["melon_dict"] = {}
    cart_list = session.get("cart", [])
    if cart_list is not None:
        for id in cart_list:
            if id not in melon_dict:
                new_melon = model.get_melon_by_id(id)
                melon_info = [new_melon.common_name, float(new_melon.price), 1, new_melon.price*1.00]
                melon_dict[id] = melon_info
            else:
                melon_dict[id][2] += 1
                melon_dict[id][3] = melon_dict[id][1] * melon_dict[id][2]
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
    return redirect("/cart")

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    if session.get("customer", None) is not None:
        flash("Log out before logging in again!")
        return redirect("/login")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        customer = model.get_customer_by_email(email)
        if customer is None:
            flash("You don't exist!")
            return redirect("/login")
        if password == customer.password: #successful login case
            flash("Welcome, %s!" % customer.givenname)
            session["customer"] = (customer.givenname, customer.email, customer.password)
            return redirect("/melons")
        else:
            flash("Incorrect email or password.")
            return redirect("/login")

@app.route("/logout")
def logout():
    # for key in session.keys():
    #     del session[key]
    session.clear()
    # session["customer"] = session.get("customer", None)
    session["customer"] = None
    flash("You have logged out!")
    return redirect("/login")

@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
