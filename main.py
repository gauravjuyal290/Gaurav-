import random
import string
import jwt
import psycopg2
from flask import Flask, request, jsonify
from twilio.rest import Client
import datetime




conn=psycopg2.connect(database="assignment", user='postgres', password='Gaurav@321', host='127.0.0.1', port= '5432')
cursor = conn.cursor()


app=Flask(__name__)
app.config['SECRET_KEY']="thisissecretkey"



#API
@app.route("/signup",methods=["POST"])
def sendOtp():
    data=request.get_json()
    number=data["number"]
    id=random.randrange(0,45122)
    a = datetime.datetime(100, 1, 1, 11, 34, 59)
    b = a + datetime.timedelta(0, 15)
    End=b.time()
    start=a.time()
    otp = getOTPApi("+91"+number)
    try:
        cursor.execute("insert into table1 values(%s, %s, %s, %s, %s)", (id, number, otp, End, start))
        conn.commit()
    except:
        conn.rollback()
    return jsonify({"Status":1003 ,"Message":"Verification OTP Sent on the Mobile Number"})

@app.route("/verify",methods=["POST"])
def verifyOtp():
    data=request.get_json()
    id = random.randrange(0, 45122)
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(10))
    mobile=data["number"]
    otp=data["otp"]
    cursor.execute("""select * from table1 where "Mobile_Number"=%s and "OTP"=%s """, (mobile, otp))
    c = cursor.fetchone()
    token = jwt.encode({'user': mobile},app.config['SECRET_KEY'])
    if c:
        try:
            cursor.execute("""select * from table2 where "Mobile"=%s """, (mobile, ))
            f = cursor.fetchone()
            if not f:
                cursor.execute("""insert into table2("ID","Name","Mobile") values(%s, %s, %s)""", (id, name, mobile))
                conn.commit()
                return jsonify({"Status": 1002,"Token": token})
            else:
                return jsonify({"Status": 1001,"Token": token})
        except Exception as error:
            conn.rollback()

    return jsonify({'token':token})


@app.route("/profileUpload/<string:phone>",methods=["POST"])
def profileUpload(phone):
    data=request.get_json()
    token2=data['token']
    image=data['image']
    id=random.randrange(1,54564)
    token = jwt.encode({'user': phone}, app.config['SECRET_KEY'])
    if token==token2:
        cursor.execute("""select * from table2 where "Mobile"=%s  """, (phone,))
        c = cursor.fetchone()
        customer_id=c[0]
        try:
            cursor.execute("""insert into table6("id","cusromerId","Image") values(%s, %s, %s)""", (id, customer_id, image))
            conn.commit()
            return jsonify({"Status":1005,"Message":"Profile image Updated Successfully"})
        except:
            conn.rollback()

@app.route("/booktradesman/<string:number>")
def booktradesman(number):
    data = request.get_json()
    token2 = data['token']
    Trademan_id = data['tradesman']
    date=data['date']
    time=data['time']
    id = random.randrange(1, 54564)
    token = jwt.encode({'user': number}, app.config['SECRET_KEY'])
    if token == token2:
        cursor.execute("""select * from table3 where "status"=%s  """, ('Active',))
        c = cursor.fetchone()
        customer_id = c[0]
        try:
            cursor.execute("""insert into table5("id","customerId","TraderID","Date","time") values(%s, %s, %s,%s,%s)""",
                           (id, customer_id, Trademan_id,date,time))
            conn.commit()
            return jsonify({"Status":1004,"Message":"Request Added Successfully"})
        except:
            conn.rollback()



@app.route("/valid/<string:phone>",methods=["POST"])
def valid(phone):
    data = request.get_json()
    token2 = data['token']
    token = jwt.encode({'user': phone}, app.config['SECRET_KEY'])
    if token == token2:
        cursor.execute("""select * from table2 where "Mobile"=%s  """, (phone,))
        c = cursor.fetchone()
        return jsonify({'Status': 1006, 'Data': {'id': c[0], 'Name': c[1], 'DOB': c[2], 'Email': c[3], 'Phone': c[4]}})






#Function
def getOtp():
    return random.randrange(100000,999999)

def getOTPApi(number):
    account_sid='ACaa3b0a9bfac4be358bac6cf85db57e62'
    auth_token='4fb279373f18d32e883271adf54ba41a'
    client = Client(account_sid, auth_token)
    otp=getOtp()
    body="your OTP is " +str(otp)
    message=client.messages.create(
                              from_='+18586021529',
                              body =body,
                              to =number
                          )
    return int(otp)





if __name__=="__main__":
    app.run(debug=True)