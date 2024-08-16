from flask import Flask, jsonify, render_template, redirect, url_for, request

app = Flask(__name__)

received_messages = []

@app.route("/", methods=["POST"])
def sms():
    data = request.json
    message_content = data.get("message")
    sender = data.get("sender", "VF-Cash")
    received_messages.append({"sender": sender, "content": message_content})

    #-------- Split Messages
    global list_sms
    list_sms = str(data.get("message")).split()

    return jsonify({"status": "Message received"}), 200

@app.route("/", methods=["GET"])
def login():
    return render_template("login.html",messages=received_messages)

@app.route("/messages")
def get_messages():
    return jsonify({"messages": received_messages})


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    if username == "user" and password == "pass":
        return redirect(url_for("protected"))
    else:
        return "Invalid username or password", 401

@app.route("/protected")
def protected():
    return app.send_static_file("protected.html")

@app.route("/balance", methods=["GET"])
def get_balance():
    balancee = 200000 #Max Money Transaction in the Month
    transaction_amount = float(list_sms[2])
    if transaction_amount < balancee:
        new_balance = balancee - transaction_amount
    return jsonify({"balance": new_balance})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
