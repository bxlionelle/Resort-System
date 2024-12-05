home.html
- login/signup
- rooms but no choose room (lockscreen?)

pag magsign up ma get hin:
firstname
lastname
gender
birthday ...
contact number
address
email address
password

tapos after ma get, ma kadto ha login page

pagmakalog-in na makadto hiya ha index.html
- didto ma choose hin rooms
- machoose hin date to check in-out

make choose na ngan ha index.html
- makadto reservation, ipapakita an
firstname
lastname
contact number
address
email

**upod pati an

check in
check out
child
adult
room name 

tapos after confirming ha reservation.html
- makadto ha payment.html
- ig display an:
Name
Room name !!! # dire ma display :-#

after payment.html
- makdto ha receipt ig display an aada ha user_info ngan an guest na list dapat
- tapos may button ha ubos na home where ma redirect ha index.html 

DAPAT DIRE MAG POP AN ACCOUNT HAN CUSTOMER! amo ma import hin global


MAG BUTANG HIN "PROFILE" NA KUAN HA NAVBAR PARA MA KITA NGAN MA MODIFY HAN CUSTOMER AN IYA INFOS !!!







PAN CONNECT HA DB

connection = sqlite3.connect(os.path.join(currentdirectory, "customer.db"))
        cursor = connection.cursor()
        
        query1 = "INSERT INTO customer (firstname, lastname, address, cel_num, check_in, check_out, adults, children, room_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query1, (guest["firstname"], guest["lastname"], guest["address"], guest["cel_num"], guest["check_in"], guest["check_out"], guest["adults"], guest["children"], guest["room_name"]))
        connection.commit()
        connection.close()


        signup

             """
        connection = sqlite3.connect(os.path.join(currentdirectory, "customer.db"), timeout=5)

        cursor = connection.cursor()
        
        query1 = "INSERT INTO Customers_Profile (firstname, lastname, gender, cel_num, address, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query1, (
            customer['firstname'], 
            customer['lastname'], 
            customer['gender'], 
            customer['cel_num'], 
            customer['address'], 
            customer['email'], 
            customer['password']
        ))

        connection.commit()
        connection.close()
        """




---------------------------------------------------------------------------------

1. Signup Process
Inputs: First name, last name, email, gender, phone number, address, password.

Actions:
>> Captures user details via a form.
>> Stores user details in:
    - guestlist (a global list storing all users and their details).
    - session['user_info'] (specific to the currently logged-in user).

Data Usage:
>> guestlist serves as the source of truth for all registered users.
>> session['user_info'] is used for personalized user experiences.

2. Login Process
Inputs: Email, password.

Actions:
>> Validates the entered email and password against entries in guestlist.
>> On successful login:
    - Updates session['user_info'] with the logged-in user's data.

Data Usage:
>> guestlist is used to verify credentials.
>> session['user_info'] is updated to manage the current session for the logged-in user.

3. Profile View
Inputs: None (retrieved directly from session['user_info']).

Actions:
>> Displays user details stored in session['user_info'] on the profile page.

Data Usage:
>> session['user_info'] provides details like name, email, and address.

4. Edit Profile
Inputs: Updated user details (name, phone number, address, etc.).

Actions:
>> Pre-fills the edit form with data from session['user_info'].
>> On submission:
    - Updates the corresponding user entry in guestlist.
    - Updates session['user_info'] with the modified details.

Data Usage:
>> session['user_info'] for pre-filled data.
>> guestlist ensures all changes are saved across the application.

5. Room Reservation
Inputs: Room type, check-in date, check-out date, number of adults, number of children.

Actions:
>> Captures reservation details via a form.
>> Adds reservation details to the user's entry in guestlist.

Data Usage:
>> guestlist stores all reservation details.
>> session['user_info'] is used to identify the logged-in user making the reservation.

6. Payment
Inputs: Payment method (credit card, PayPal, etc.).

Actions:
>> Captures the payment method and associates it with the reservation in guestlist.

Data Usage:
>> guestlist stores payment details linked to the user's reservation.
>> session['user_info'] ensures the correct user is charged.

7. Receipt Generation
Inputs: None (retrieved from guestlist).

Actions:
>> Fetches reservation and payment details from guestlist for the logged-in user.
>> Displays the receipt on the screen.

Data Usage:
>> guestlist retrieves the necessary data for receipt generation.
>> session['user_info'] ensures the receipt is linked to the logged-in user.

Session Management
session['user_info']:
    >> Quick access to the logged-in user's details.
    >> Used for profile, reservation, and payment processes.

guestlist:
    >> The primary data store for all users, their reservations, and payments.

Key Notes
Use session['user_info'] only for the currently logged-in user's session data.

Always update both guestlist and session['user_info'] when modifying user details.

For future scalability, consider replacing guestlist with a database to persist data.


------------------------------------------------




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
        
        con=sqlite3.connecct('data.db')
        c=con.cursor()
        
        if request.method=='POST':
            if(request.form["email"]!="" and request.form["password"]!=""):
                email = request.form["name"]
                password = request.form["password"]
                query1 = f"SELECT * from data WHERE email='{email}' AND password='{password}';"
                c.execute(query1)
                guest=c.fetchone()
                if guest:
                    return render_template("sign_up.html", message= "Email already exist")
                else:
                    if not guest:
                        c.execute("INSERT INTO Customers_Profile (firstname, lastname, gender, cel_num, address, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)")
                        con.commit()
                        con.close
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
----------------------------------------------------------------------------------

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

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        get_email = request.form.get("email")
        get_password = request.form.get("password")
        con = sqlite3.connect(currentdirectory + '\data.db')
        c = con.cursor()
        query1 = "SELECT * FROM GUEST WHERE email = ? AND password = ?"
        c.execute(query1, (get_email, get_password))
        guest = c.fetchone()  # Fetch the guest record if credentials are valid
        
        if guest:
            # Clear any previous session data
            session.clear()
            
            # Store the logged-in user's information in the session
            session['user_info'] = {
                'firstname': guest[1],  # Assuming the second column is firstname
                'lastname': guest[2],   # Assuming the third column is lastname
                'gender': guest[3],     # Assuming the fourth column is gender
                'cel_num': guest[4],    # Assuming the fifth column is cel_num
                'address': guest[5],    # Assuming the sixth column is address
                'email': guest[6],      # Assuming the seventh column is email
            }
            session['email'] = guest[6]  # Use email as a unique identifier
            con.close()
            return redirect(url_for("index"))
        else:
            con.close()
            return render_template('login.html', message="Invalid email or password")
    else:
        return render_template('login.html')

    
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

        con = sqlite3.connect(currentdirectory + '\data.db')
        c = con.cursor()

        # Check if email already exists in the database
        email = customer['email']
        query = "SELECT * FROM GUEST WHERE email = ?"
        c.execute(query, (email,))
        guest = c.fetchone()

        if guest:
            # If the email already exists, return an error message
            con.close()
            return render_template('sign_up.html', message="Email already exists. Please use a different email.")
        else:
            # If email does not exist, insert the new user into the database
            query = """
                INSERT INTO GUEST (firstname, lastname, gender, cel_num, address, email, password) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            c.execute(query, (
                customer['firstname'], 
                customer['lastname'], 
                customer['gender'], 
                customer['cel_num'], 
                customer['address'], 
                customer['email'], 
                customer['password']
            ))
            con.commit()
            con.close()

            # Log in the user by saving their information in the session
            session['user_info'] = customer
            return redirect(url_for('login'))
    else:
        return render_template('sign_up.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if 'user_info' not in session:
        flash("You need to log in to edit your profile.")
        return redirect(url_for('login'))

    user_info = session['user_info']

    if request.method == "POST":
        updated_user_info = {
            "firstname": request.form.get("first-name"),
            "lastname": request.form.get("last-name"),
            "address": request.form.get("address"),
            "email": request.form.get("email"),
            "cel_num": request.form.get("cel-number"),
        }

        # Update session data
        session['user_info'].update(updated_user_info)

        # Update database
        con = sqlite3.connect(currentdirectory + '\data.db')
        c = con.cursor()
        query = """
            UPDATE GUEST
            SET firstname = ?, lastname = ?, address = ?, cel_num = ?, email = ?
            WHERE email = ?
        """
        c.execute(query, (
            updated_user_info["firstname"],
            updated_user_info["lastname"],
            updated_user_info["address"],
            updated_user_info["cel_num"],
            updated_user_info["email"],
            user_info["email"]
        ))
        con.commit()
        con.close()

        flash("Profile updated successfully!")
        return redirect(url_for('profile'))

    return render_template("edit.html", user_info=user_info)


@app.route('/profile', methods=["GET"])
def profile():
    if 'user_info' not in session:
        flash("You need to log in to view your profile.")
        return redirect(url_for('login'))

    # Retrieve the latest data from the database
    user_email = session['user_info']['email']
    con = sqlite3.connect(currentdirectory + '\data.db')
    c = con.cursor()
    query = "SELECT firstname, lastname, gender, cel_num, address, email FROM GUEST WHERE email = ?"
    c.execute(query, (user_email,))
    updated_info = c.fetchone()
    con.close()

    if updated_info:
        session['user_info'] = {
            "firstname": updated_info[0],
            "lastname": updated_info[1],
            "gender": updated_info[2],
            "cel_num": updated_info[3],
            "address": updated_info[4],
            "email": updated_info[5],
        }

    return render_template("profile.html", user_info=session['user_info'])



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



con = sqlite3.connect(currentdirectory + '\\data.db')
            c = con.cursor()
            
            # Update payment method and status (Pending -> Paid)
            query = """
                UPDATE BOOKING
                SET payment_method = ?, status = "Paid"
                WHERE guest_id = ? AND room_name = ? AND check_in = ? AND check_out = ?
            """
            
            c.execute(query, (
                payment-method,
                session['user_info']['email'],
                guest['room_name'],
                guest['check_in'],
                guest['check_out']
            ))
            
            con.commit()
            con.close()