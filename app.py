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

class Home: #independent
    @app.route("/")
    def home():
        return render_template('home.html', rooms=rooms)

class Customers:
    def __init__(self,firstname, lastname, gender, cel_num, address, email, password ):
        super().__init__(firstname,lastname, gender, cel_num, address, email, password)
    
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
        

        session['user_info'] = customer
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
        
        user_info = session.get('user_info')
        
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
                break
        
        if valid:
            session['email'] = get_email
            return render_template("index.html", rooms=rooms, user_info=user_info)
        else:
            return render_template('login.html', message="Invalid credentials")
    
    return render_template('login.html')

    
@app.route("/edit")
def edit():
    
    user_info = session.get('user_info')
      
    return render_template ('edit.html', user_info=user_info)    
        

@app.route("/index", methods=["GET", "POST"])
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    
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

    return render_template("index.html", rooms=rooms, user_info=user_info)
            

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
                "customer_id": id_gen.generate_id()
            }



            guestlist.append(guest)
            
            return redirect(url_for('payment', guest_index=len(guestlist) - 1, guest=guest))

        check_in = request.args.get("check_in")
        check_out = request.args.get("check_out")
        adults = request.args.get("adults")
        children = request.args.get("children")
        room_name = request.args.get("room_name")
        
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

    @app.route("/receipt/<int:guest_index>")
    def receipt(guest_index):
        guest = guestlist[guest_index]
        user_info = session.get('user_info')
        return render_template("receipt.html", guest=guest, user_info=user_info)



if __name__ == "__main__":
    app.run(debug=True)
