from flask import Flask, render_template, request, url_for, redirect, session
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
        "image": "static/images/lily.jpg" ,
        "min_guests": 1,
        "max_guests": 2
        
        
    },
    "Deluxe Room": { 
        "price": 1200,
        "description": "2 beds, A/C, Sleeps 4-5, Free wifi",
        "more": ["Private bathroom", "Cable channels", "Free toiletries"],
        "image": "static/images/lily1.jpg" ,
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
        "max_guests": 6#adi kay naka-assign an pictures, tapos ha line 89 ha index.html didto hiya tatawagon
    }
}

@app.route("/")
def home():
    return render_template ('home.html', rooms=rooms)
    
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        customer = []
        firstname = request.form.get("first-name")
        lastname = request.form.get("last-name")
        gender = request.form.get("gender")
        cel_num = request.form.get("cel-number")
        address = request.form.get("address")
        email = request.form.get("email")
        password = request.form.get("password")
        
        session['user_info'] = {
            'firstname': firstname,
            'lastname': lastname,
            'gender': gender,
            'cel_num': cel_num,
            'address': address,
            'email': email,
            'password': password
        }
        
        customer.append(firstname)
        customer.append(lastname)
        customer.append(gender)
        customer.append(cel_num)
        customer.append(address)
        customer.append(email)
        customer.append(password)
        
        guestlist.append(customer)
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
        
        for customer in guestlist:
            if get_email == customer[5] and get_password == customer[6]:
                valid = True
                session['user_info'] = {
                    'firstname': customer[0],
                    'lastname': customer[1],
                    'gender': customer[2],
                    'cel_num': customer[3],
                    'address': customer[4],
                    'email': customer[5],
                }
                break
        
        if valid:
            session['email'] = get_email
            return render_template("index.html", rooms=rooms)
        else:
            return render_template('login.html', message="Invalid")
    
    return render_template('login.html')
    
    
        

@app.route("/index", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        check_in = request.form.get("check_in")
        check_out = request.form.get("check_out")
        adults = request.form.get("adult-count")
        children = request.form.get("child-count")
        room_name = request.form.get("room-name")
        
        guestlist.append(check_in)
        guestlist.append(check_out)
        guestlist.append(adults)
        guestlist.append(children)
        guestlist.append(room_name)
    
        #Ig shoshow ha registration
        user_info = session.get('user_info')
        
        return render_template("reservationform.html",
            user_info=user_info, 
            check_in=check_in, 
            check_out=check_out, 
            adults=adults, 
            children=children, 
            room_name=room_name
        )

    return render_template("index.html", rooms=rooms)
            

@app.route("/reservationform", methods=['GET', 'POST'])
def reservationform():
    if request.method == "POST":
        
        class IDGenerator:
            def __init__(self, start_id=2024001):
                self.current_id = start_id

            def generate_id(self):
                generated_id = self.current_id
                self.current_id += 1
                return generated_id
        id_gen = IDGenerator()
        
        guest = {
            "check_in": request.form.get("check_in"),
            "check_out": request.form.get("check_out"),
            "adults": request.form.get("adults"),
            "children": request.form.get("children"), 
            "room_name": request.form.get("room_name"),
            "customer_id": id_gen.generate_id()  # ID GENERATOR :#
        }

        # DB PURPOSES, DO NOT TOUCH UNLESS ASSIGNED TO YOU
        connection = sqlite3.connect(os.path.join(currentdirectory, "customer.db"))
        #cursor = connection.cursor()
        
        connection.commit()
        connection.close()

        guestlist.append(guest)
        
        return redirect(url_for('payment', guest_index=len(guestlist) - 1, guest=guest))

    # para adi ha db, WAG GALAWIN
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")
    adults = request.args.get("adults")
    children = request.args.get("children")
    room_name = request.args.get("room_name")
    
    # An info na gin filled up ha signup
    user_info = session.get('user_info')
    
    return render_template("reservationform.html", user_info=user_info, 
        check_in=check_in, 
        check_out=check_out, 
        adults=adults, 
        children=children, 
        room_name=room_name
    )


@app.route("/payment/<int:guest_index>", methods=['GET', 'POST'])
def payment(guest_index):
    if request.method == "POST":
        guest = guestlist[guest_index]
        
        guest['payment_method'] = request.form.get('payment-method')
        return redirect(url_for('receipt', guest_index=guest_index))
    
    guest = guestlist[guest_index]
    user_info = session.get('user_info')
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")
    adults = request.args.get("adults")
    children = request.args.get("children")
    room_name = request.args.get("room_name")
        

    return render_template("payment.html", guest=guest, user_info=user_info,
        check_in=check_in, 
        check_out=check_out, 
        adults=adults, 
        children=children, 
        room_name=room_name)
    #room name di ko ma get




@app.route("/receipt/<int:guest_index>")
def receipt(guest_index):
    guest = guestlist[guest_index]
    user_info = session.get('user_info')
    return render_template("receipt.html", guest=guest, user_info=user_info)

@app.route("/admin", methods=["GET"])
def admin():
    try:
        if request.method == "GET":
            firstname = request.args.get("firstname")
            lastname = request.args.get("lastname")
            address = request.args.get("address")
            room_type = request.args.get("room_type")
            cel_num = request.args.get("cel_num")
            check_in = request.args.get("check_in")
            check_out = request.args.get("check_out")
            adults = request.args.get("adults")
            children = request.args.get("children")

            # Validate that required fields are filled
            if not firstname or not lastname or not address or not room_type:
                return render_template("admin.html", error="First name, last name, address, and room type are required.")
            
            # Database connection
            connection = sqlite3.connect(os.path.join(currentdirectory, "customer.db"))
            cursor = connection.cursor()
            
            # Update SQL query to include additional fields
            query = """
                SELECT * FROM customer 
                WHERE firstname=? AND lastname=? AND address=? 
                AND room_name=? AND cel_num=? AND check_in=? 
                AND check_out=? AND adults=? AND children=?
            """
            cursor.execute(query, (firstname, lastname, address, room_type, cel_num, check_in, check_out, adults, children))
            results = cursor.fetchall()  # Fetch all matching records
            
            connection.close()  # Close the connection
            
            return render_template("admin.html", guestlist=results)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return render_template("admin.html", error="Database error occurred.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template("admin.html", error="An unexpected error occurred.")


    

if __name__ == "__main__":
    app.run(debug=True)