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
        guest = c.fetchone()  
        
        if guest:
            session.clear()
            
            session['user_info'] = {
                'firstname': guest[1],  
                'lastname': guest[2],   
                'gender': guest[3],     
                'cel_num': guest[4],    
                'address': guest[5],    
                'email': guest[6],      
            }
            session['email'] = guest[6]  # ig check an email 
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

        email = customer['email']
        query = "SELECT * FROM GUEST WHERE email = ?"
        c.execute(query, (email,))
        guest = c.fetchone()

        if guest:
            con.close()
            return render_template('sign_up.html', message="Email already exists. Please use a different email.")
        else:
            # ma proceded dari
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

            # igsession an user_info(customer)
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

        session['user_info'].update(updated_user_info)

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
        
        con = sqlite3.connect(currentdirectory + '\data.db')
        c = con.cursor()

           
        guest_id = session['user_info'].get('guest_id')
        
        query = """
            INSERT INTO BOOKING (guest_id, check_in, check_out, adult_guest, child_guest, room_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        c.execute(query, (guest_id, guest["check_in"], guest["check_out"], guest["adults"], guest["children"], guest["room_name"]))
        con.commit()
        con.close()

        
        #pagkadto reservation, ig shoshow an user_info, tapos an adi. ///
        return render_template("reservationform.html",
            user_info=user_info, 
            guest=guest
        )
        
        #Mag INNER JOIN la ugaring para ma call an common, pero if kung two transactions na in one account, it will only
        #show the first transaction

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
            
            session['guestlist'] = guestlist 

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
