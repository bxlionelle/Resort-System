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
            
            guestlist.append(customer) # ig susulod an customer ha guestlist
            return redirect(url_for('login'))
        else:
            return render_template('sign_up.html')


    @app.route('/login', methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            login_email = request.form.get("email")
            login_password = request.form.get("password")
            valid = False
            
            for customer in guestlist: 
                if login_email == customer['email'] and login_password == customer['password']:
                    valid = True #ig set hiya as true
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
                session['email'] = login_email
                return render_template("index.html", rooms=rooms)
            else:
                return render_template('login.html', message="Invalid credentials")
        
        return render_template('login.html')

    @app.route("/profile", methods=["GET", "POST"])
    def profile():
        user_info = session.get('user_info')
        
        if request.method == "POST":
            updated_info = {
                'firstname': request.form.get("first-name"),
                'lastname': request.form.get("last-name"),
                'gender': request.form.get("gender"),
                'cel_num': request.form.get("cel-number"),
                'address': request.form.get("address"),
                'email': request.form.get("email"),
            }
            
            connection = sqlite3.connect(os.path.join(currentdirectory, "Resort.db"), timeout=5)
            cursor = connection.cursor()
            
            query = """
            UPDATE Customers_Profile
            SET firstname = ?, lastname = ?, gender = ?, cel_num = ?, address = ?, email = ?
            WHERE email = ?
            """
            cursor.execute(query, (
                updated_info['firstname'], 
                updated_info['lastname'], 
                updated_info['gender'], 
                updated_info['cel_num'], 
                updated_info['address'], 
                updated_info['email'],
                user_info['email'] 
            ))

            connection.commit()

            session['user_info'] = updated_info
            connection.close()

            flash("Profile updated successfully!", "success")
            return render_template("profile.html", message="Profile updated successfully!", user_info=updated_info)

        return render_template('profile.html', user_info=user_info)


    
    @app.route("/logout")
    def logout():
        session.pop('email', None)

        flash("You have been logged out.", "info")
        return redirect(url_for('login'))


class Index(Customers):
    @app.route("/index", methods=["GET", "POST"])
    def index():
        if 'email' not in session:
            return redirect(url_for('login'))
        
        if request.method == "POST":
            check_in = request.form.get("check_in")
            check_out = request.form.get("check_out")
            adults = int(request.form.get("adult-count"))
            children = int(request.form.get("child-count"))
            room_name = request.form.get("room-name")


            if room_name in rooms:
                min_guests = rooms[room_name]['min_guests']
                max_guests = rooms[room_name]['max_guests']
                total_guests = adults + children

                if total_guests < min_guests or total_guests > max_guests:
                    flash(f"The number of guests must be between {min_guests} and {max_guests}.", "danger")
                    return redirect(url_for('index'))

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
