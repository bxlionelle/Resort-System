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