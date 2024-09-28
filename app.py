from flask import Flask, render_template, request, url_for, redirect
import uuid

app = Flask(__name__)

guestlist = []
rooms = {
    "Basic Room": {
        "price": 500,
        "description": "1 bed, A/C, Sleeps 2, Free wifi",
        "more": ["Private bathroom", "Cable channels", "Free toiletries"]
    },
    "Deluxe Room": { 
        "price": 1200,
        "description": "2 beds, A/C, Sleeps 4-5, Free wifi",
        "more": ["Private bathroom", "Cable channels", "Free toiletries"]
    },
    "Deluxe Twin Room": {
        "price": 2200,
        "description": "4 beds, A/C, Sleeps 8, Free wifi",
        "more": ["Private bathroom", "Cable channels", "Free toiletries"]
    },
    "Suite Room": {
        "price": 6000,
        "description": "3 double beds, A/C, Sleeps 6, Free wifi",
        "more": ["Private bathroom", "Cable channels", "Free toiletries"]
    }
}

@app.route("/", methods=["GET", "POST"])
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
        return render_template("reservationform.html", 
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
            
        guest = {
            "firstname": request.form.get("firstname"),
            "lastname": request.form.get("lastname"),
            "address": request.form.get("address"),
            "cel_num": request.form.get("cel-number"),
            "check_in": request.form.get("check_in"),
            "check_out": request.form.get("check_out"),
            "adults": request.form.get("adults"),
            "children": request.form.get("children"), 
            "room_name": request.form.get("room_type"),
            "customer_id": str(uuid.uuid4())  # parahan id
        }
        guestlist.append(guest)
        return redirect(url_for('payment', guest_index=len(guestlist) - 1))
    
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out" )
    adults = request.args.get("adults")
    children = request.args.get("children")
    room_type = request.args.get("room_name")

    return render_template("reservationform.html", 
        check_in=check_in, 
        check_out=check_out, 
        adults=adults, 
        children=children, 
        room_type=room_type)

@app.route("/payment/<int:guest_index>", methods=['GET', 'POST'])
def payment(guest_index):
    if request.method == "POST":
        guest = guestlist[guest_index]
        
        guest['payment_method'] = request.form.get('payment-method')
        return redirect(url_for('receipt', guest_index=guest_index))
    
    guest = guestlist[guest_index]
    return render_template("payment.html", guest=guest)


@app.route("/receipt/<int:guest_index>")
def receipt(guest_index):
    guest = guestlist[guest_index]
    return render_template("receipt.html", guest=guest)

@app.route("/admin")
def admin():
    return render_template("admin.html", guestlist=guestlist)

if __name__ == "__main__":
    app.run(debug=True)
