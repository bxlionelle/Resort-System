from flask import Flask, render_template, request, url_for, redirect, session, flash
import sqlite3
import os

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "hello"

guestlist = []
rooms = {
    "Basic Room": {
        "price": 500,
        "description": "1 bed, A/C, Sleeps 2, Free wifi",
        "more": ["Private bathroom", "Cable channels", "Free toiletries"],
        "image": "static/images/lily.jpg",
        "min_guests": 1,
        "max_guests": 2
    },
    "Deluxe Room": {
        "price": 1200,
        "description": "2 beds, A/C, Sleeps 4-5, Free wifi",
        "more": ["Private bathroom", "Cable channels", "Free toiletries"],
        "image": "static/images/lily1.jpg",
        "min_guests": 2,
        "max_guests": 5
    },
    "Deluxe Twin Room": {
        "price": 2200,
        "description": "4 beds, A/C, Sleeps 8, Free wifi",
        "more": ["Private bathroom", "Cable channels", "Free toiletries"],
        "image": "static/images/lily4.jpg",
        "min_guests": 2,
        "max_guests": 8
    },
    "Suite Room": {
        "price": 6000,
        "description": "3 double beds, A/C, Sleeps 6, Free wifi",
        "more": ["Private bathroom", "Cable channels", "Free toiletries"],
        "image": "static/images/lily3.jpg",
        "min_guests": 2,
        "max_guests": 6
    }
}

class Home:
    @app.route("/")
    def home():
        return render_template('home.html', rooms=rooms)
    
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        customer = {
            'firstname': request.form.get("first-name"),
            'lastname': request.form.get("last-name"),
            'gender': request.form.get("gender"),
            'cel_num': request.form.get("cel-number"),
            'address': request.form.get("address"),
            'email': request.form.get("email"),
            'password': request.form.get("password")
        }

        guestlist.append(customer)
        session['guestlist'] = guestlist  # Update session with the latest guestlist
        
        session['user_info'] = customer  # Log in the user
        print(guestlist)
        
        return redirect(url_for('login'))
    else: 
        return render_template('sign_up.html')



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        get_email = request.form.get("email")
        get_password = request.form.get("password")
        valid = False
        
        user_info = session.get('user_info') #kuwaon an nakadto sulod han session var which is user_info(customer)
        
        for customer in guestlist: 
           if get_email == customer['email'] and get_password == customer['password']:
                valid = True
                session['user_info'] = {
                    'firstname': customer['firstname'],
                    'lastname': customer['lastname'],
                    'gender': customer['gender'],
                    'cel_num': customer['cel_num'],
                    'address': customer['address'],
                    'email': customer['email'],
                }
                session['email'] = get_email
                break
        
        if valid:
            session['email'] = get_email
            return render_template("index.html", rooms=rooms, user_info=user_info)
        else:
            return render_template('login.html', message="Invalid credentials")
    
    return render_template('login.html')

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        updated_user_info = {
            "firstname": request.form.get("first-name"),
            "lastname": request.form.get("last-name"),
            "address": request.form.get("address"),
            "email": request.form.get("email"),
            "cel_num": request.form.get("cel-number"),
        }

        # Update session data
        session['user_info'] = updated_user_info #ig convert niya an updated_user_info tikadto ha session var na user_info(customer)

        # Update the corresponding user in guestlist
        for user in guestlist:
            if user['email'] == session['user_info']['email']:
                user.update(updated_user_info)
                break

        return redirect(url_for('profile'))

    return render_template("edit.html", user_info=session.get('user_info'))

@app.route('/profile', methods=["GET"])
def profile():
    if 'user_info' not in session:
        flash("You need to log in to view your profile.")
        return redirect(url_for('login'))
    
    user_info = session.get('user_info') #ig show info nga nakadto to user_info(customer) nga in session
    
    #AN TRANSACTIONS NALA, LIKE MAKITA HIRA KUN ANO AN IRA GIN BOOK
    return render_template("profile.html", user_info=user_info)


@app.route("/index", methods=["GET", "POST"])
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    user_info = session.get('user_info')
    
    if request.method == "POST":
        
        guest = {
            'check_in' : request.form.get("check_in"),
            'check_out' : request.form.get("check_out"),
            'adults' : request.form.get("adult-count"),
            'children' : request.form.get("child-count"),
            'room_name' : request.form.get("room-name")
        }
        
        #ig sulod an adi ha guestlist
        guestlist.append(guest)
    
        #Ig shoshow ha registration
        user_info = session.get('user_info')
        
        #pagkadto reservation, ig shoshow an user_info, tapos an adi. ///
        return render_template("reservationform.html",
            user_info=user_info, 
            guest=guest
        )

    return render_template("index.html", rooms=rooms, guestlist=guestlist, user_info=user_info)
            
class Rent:
    @app.route("/reservationform", methods=['GET', 'POST'])
    def reservationform():
        if request.method == "POST":
            
            check_in = request.args.get("check_in")
            check_out = request.args.get("check_out")
            adults = request.args.get("adults")
            room_name = request.args.get("room_name")
            children = request.args.get("children")
            
            user_info = session.get('user_info')
            
            session['guestlist'] = guestlist  # Update the session with the modified guestlist

            return redirect(url_for('payment', guest_index=len(guestlist) - 1))

        
        return render_template("reservationform.html", user_info=user_info, 
            check_in=check_in, 
            check_out=check_out, 
            room_name=room_name,
            adults=adults, 
            children=children
        )

    @app.route("/payment/<int:guest_index>", methods=['GET', 'POST'])
    def payment(guest_index):
        if request.method == "POST":
            guest = guestlist[guest_index]
            
            guest['payment_method'] = request.form.get('payment-method')
            return redirect(url_for('receipt', guest_index=guest_index, guest=guest))
        
        guest = guestlist[guest_index]
        
        user_info = session.get('user_info')
        
        check_in = request.args.get("check_in")
        check_out = request.args.get("check_out")
        adults = request.args.get("adults")
        children = request.args.get("children")
        room_name = request.args.get("room-name")
            
        return render_template("payment.html", guest=guest, user_info=user_info,
            check_in=check_in, 
            check_out=check_out, 
            adults=adults, 
            children=children, 
            room_name=room_name)

    @app.route("/receipt/<int:guest_index>")
    def receipt(guest_index):
        guest = guestlist[guest_index]
        user_info = session.get('user_info')
        
        
        return render_template("receipt.html", guest=guest, user_info=user_info)
    
    
    
@app.route('/logout')
def logout():
    if 'user_info' in session:
        session['user_info'] = {key: session['user_info'][key] for key in session['user_info'] if key not in ['email']}
    session.pop('email', None)
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True)
