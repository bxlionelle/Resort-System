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
