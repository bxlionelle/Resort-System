from flask import Flask, render_template, request, url_for, redirect, session, flash
import sqlite3
import os

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "hello"

guestlist = []

# Room Management Classes
class Room_Management:
    def __init__(self, room_name, cost, description, more, image, min_guests, max_guests, room_id=None, count=1):
        self.room_id = room_id
        self.room_name = room_name
        self.cost = cost
        self.description = description
        self.more = more
        self.image = image
        self.min_guests = min_guests
        self.max_guests = max_guests
        self.room_count = count
        self.__availability = count

    def room_available(self):
        return self.__availability > 0

    def room_book(self): 
        if self.room_available():
            self.__availability -= 1
        else:
            flash("Room not available!")

    def room_is_checked_out(self):
        if self.__availability < self.room_count:
            self.__availability += 1

#for admin
class Rooms:
    def __init__(self):
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def remove_room(self, room_name):
        self.rooms = [room for room in self.rooms if room.room_name != room_name]

    def get_room(self, room_name):
        for room in self.rooms:
            if room.room_name == room_name:
                return room
        return None

    def list_rooms(self):
        return self.rooms

#------------------------------------------------------------------------------

room_manager = Rooms()
predefined_rooms = {
    "Basic Room": {"price": 500, "description": "1 bed, A/C, Sleeps 2, Free wifi", "more": ["Private bathroom", "Cable channels", "Free toiletries"], "image": "static/images/lily.jpg", "min_guests": 1, "max_guests": 2, "room_count": 10},
    "Deluxe Room": {"price": 1200, "description": "2 beds, A/C, Sleeps 4-5, Free wifi", "more": ["Private bathroom", "Cable channels", "Free toiletries"], "image": "static/images/lily1.jpg", "min_guests": 2, "max_guests": 5, "room_count": 3},
    "Deluxe Twin Room": {"price": 2200, "description": "4 beds, A/C, Sleeps 8, Free wifi", "more": ["Private bathroom", "Cable channels", "Free toiletries"],"image": "static/images/lily4.jpg","min_guests": 2, "max_guests": 8, "room_count": 5},
    "Suite Room": { "price": 6000, "description": "3 double beds, A/C, Sleeps 6, Free wifi", "more": ["Private bathroom", "Cable channels", "Free toiletries"], "image": "static/images/lily3.jpg", "min_guests": 2, "max_guests": 6, "room_count": 5},
}

con = sqlite3.connect(currentdirectory + '\\data.db')
c = con.cursor()

for room_name, room_details in predefined_rooms.items():
    # Check if the room already exists in the ROOMS table
    c.execute("SELECT room_id FROM ROOMS WHERE room_name = ?", (room_name,))
    result = c.fetchone()
        
    if result is not None:
            # If the room already exists, flash a message and redirect
            flash(f"Error: The room '{room_name}' already exists. Please contact support.")
            redirect ('/')
        

    else:
            # Insert only the relevant columns into the ROOMS table
        query = """
        INSERT INTO ROOMS (room_name, room_cost, room_availability,)
        VALUES (?, ?, ?)
        """
        c.execute(query, (room_name, room_details["price"], room_details["room_count"]))

    # Commit changes once after the loop completes
con.commit()
con.close()
    

    # Redirect to the home page after inserting all rooms


    # room_details["min_guests"], room_details["max_guests"]


    #ig insert sa database, pero kun already exist then move on
for name, data in predefined_rooms.items():
    room_manager.add_room(Room_Management(name, data["price"], data["description"], data["more"], data["image"], data["min_guests"], data["max_guests"], count=data["room_count"]))

#------------------------------------------------------------------------------


@app.route("/")
def home():
    rooms = room_manager.list_rooms()
    
    return render_template("home.html", rooms=rooms)



@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    # Fetch the list of bookings from the database to show guest information
    
    con = sqlite3.connect(currentdirectory + '\\data.db')
    c = con.cursor()

    # Query to fetch booking details including guest info and room details
    query = """
        SELECT BOOKING.booking_id, GUEST.guest_id, ROOMS.room_name, ROOMS.check_in, ROOMS.check_out, ROOMS.room_cost
        FROM BOOKING 
        JOIN GUEST ON BOOKING.guest_id = GUEST.guest_id
        JOIN ROOMS ON BOOKING.room_name = ROOMS.room_name
    """
    c.execute(query)
    bookings = c.fetchall()
    con.close()

    return render_template("admin_dashboard.html", bookings=bookings)


# Route to add a new room
@app.route("/add_room", methods=["GET", "POST"])
def add_room():
    if request.method == "POST":
        room_name = request.form.get("room_name")
        cost = request.form.get("cost")
        description = request.form.get("description")
        more = request.form.getlist("more")
        image = request.form.get("image")
        min_guests = request.form.get("min_guests")
        max_guests = request.form.get("max_guests")
        room_count = request.form.get("room_count")

        # Create a new Room_Management object and add it to the room manager
        new_room = Room_Management(
            room_name, float(cost), description, more, image, int(min_guests), int(max_guests), count=int(room_count)
        )
        room_manager.add_room(new_room)

        # Insert the room into the database
        con = sqlite3.connect(currentdirectory + '\\data.db')
        c = con.cursor()
        query = """
            INSERT INTO ROOMS (room_name, room_cost, room_availability)
            VALUES (?, ?, ?)
        """
        c.execute(query, (room_name, float(cost), int(room_count)))
        con.commit()
        con.close()

        flash(f"Room '{room_name}' added successfully!")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_room.html")


# Route to update room information
@app.route("/update_room/<room_name>", methods=["GET", "POST"])
def update_room(room_name):
    room = room_manager.get_room(room_name)
    if not room:
        flash("Room not found!")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        room.room_name = request.form.get("room_name")
        room.cost = float(request.form.get("cost"))
        room.description = request.form.get("description")
        room.more = request.form.getlist("more")
        room.image = request.form.get("image")
        room.min_guests = int(request.form.get("min_guests"))
        room.max_guests = int(request.form.get("max_guests"))
        room.room_count = int(request.form.get("room_count"))
        room.__availability = int(request.form.get("room_count"))

        # Update room details in the database
        con = sqlite3.connect(currentdirectory + '\\data.db')
        c = con.cursor()
        query = """
            UPDATE ROOMS
            SET room_name = ?, room_cost = ?, room_availability = ?
            WHERE room_name = ?
        """
        c.execute(query, (room.room_name, room.cost, room.room_count, room_name))
        con.commit()
        con.close()

        flash(f"Room '{room.room_name}' updated successfully!")
        return redirect(url_for("admin_dashboard"))

    return render_template("update_room.html", room=room)


# Route to remove a room
@app.route("/remove_room/<room_name>", methods=["POST"])
def remove_room(room_name):
    room_manager.remove_room(room_name)

    # Remove room from the database
    con = sqlite3.connect(currentdirectory + '\\data.db')
    c = con.cursor()
    query = "DELETE FROM ROOMS WHERE room_name = ?"
    c.execute(query, (room_name,))
    con.commit()
    con.close()

    flash(f"Room '{room_name}' removed successfully!")
    return redirect(url_for("admin_dashboard"))


@app.route("/book_room/<room_name>", methods=["POST"])
def book_room(room_name):
    room = room_manager.get_room(room_name)
    if room:
        room.room_book()
        flash(f"Room '{room_name}' booked successfully!" if room.room_available() else "No availability left for this room!")
    else:
        flash("Room not found!")
    return redirect(url_for("home"))


#////////////////////////////////////////////
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

#Priorities, Not Ambiguities
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
#////////////////////////////////////////////


@app.route("/index", methods=["GET", "POST"])
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    user_info = session.get('user_info')
    
    if request.method == "POST":
        # Collect guest information from the form
        guest = {
            'check_in': request.form.get("check_in"),
            'check_out': request.form.get("check_out"),
            'adults': request.form.get("adult-count"),
            'children': request.form.get("child-count"),
            'room_name': request.form.get("room-name")
        }
        
        """
        

        if room_name and its availabilty is not available anymore then flash a message that "Room is not available"
        else  proceed to 
        
        """
        
        
        # Append guest information to the guestlist (if needed)
        guestlist.append(guest)
        
        # Connect to the database
        con = sqlite3.connect(currentdirectory + '\\data.db')
        c = con.cursor()

        # Retrieve the guest_id using the logged-in user's email
        user_email = session['user_info']['email']
        c.execute("SELECT guest_id FROM GUEST WHERE email = ?", (user_email,))
        guest_id_row = c.fetchone()
        
        if guest_id_row:
            guest_id = guest_id_row[0]  # Extract the guest_id from the query result

            #make a condition if the room_name / room_id is available, if yes proceed
            # if no print a flash message and try again
            
            # Insert booking information into the BOOKING table
            query = """
                INSERT INTO BOOKING (guest_id, check_in, check_out, adult_guest, child_guest, room_name)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            
            
            c.execute(query, (guest_id, guest["check_in"], guest["check_out"], guest["adults"], guest["children"], guest["room_name"]))
            con.commit()
        else:
            con.close()
            flash("Error: Could not find the guest ID. Please contact support.")
            return redirect(url_for('index'))
        
        con.close()

        # Render the reservation form with the user and booking details
        return render_template(
            "reservationform.html",
            user_info=user_info,
            guest=guest
        )
    rooms = room_manager.list_rooms() #new way para ma call an rooms
    return render_template("index.html", rooms=rooms, guestlist=guestlist, user_info=user_info)

            
class Rent:
    #IG DISPLAY LA NIYA AN INPUTS HA INDEX
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
