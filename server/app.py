from flask import Flask, render_template, request, jsonify, make_response, send_from_directory, send_file, redirect, url_for
from flask_cors import CORS, cross_origin
from sqlalchemy import or_
import json
import bcrypt
from models import *

app = Flask(__name__, static_folder='build', static_url_path='')
cors = CORS(app)
setup_db(app)

@app.route('/')
def index():
    return "Hey"

@app.route('/users')
def get_users():
    users = User.query.all()
    if users:
        result = []
        for user in users:
            result.append({
                "id":user.id,
                "username": user.username,
                "password": user.password,
            })
        return {"success": True, "users": result}
    else:
        return {"success": False, "users": "No users found"}

@app.route('/transactions')
def get_transactions():
    transactions = Transaction.query.all()
    if transactions:
        result = []
        for transaction in transactions:
            result.append({
                "id":transaction.id,
                "transaction_date": transaction.transaction_date,
                "transaction_added": transaction.transaction_added,
                "users": transaction.users,
                "amount": transaction.amount,
                "user_id": transaction.user_id,
            })
        return {"success": True, "transactions": result}
    else:
        return {"success": False, "transactions": "No users found"}

@app.route('/transactions/<id>')
def get_transaction_by_id(id):
    transaction = Transaction.query.filter(Transaction.user_id==id).all()
    if transaction:
        result = []
        for transaction in transaction:
            result.append({
                "id":transaction.id,
                "transaction_date": transaction.transaction_date,
                "amount": transaction.amount,
                "users": transaction.users
            })
        return {"success": True, "transactions": result}
    else:
        return {"success": False, "transactions": "No accounts found"}

@app.route('/accounts/<id>')
def get_accounts(id):
    accounts = Account.query.filter(or_(Account.lender_id==id, Account.receiver_id==id)).all()
    if accounts:
        result = []
        for account in accounts:
            lender = User.query.filter_by(id=account.lender_id).first()
            receiver = User.query.filter_by(id=account.receiver_id).first()
            result.append({
                "id":account.id,
                "transaction_id": account.transaction_id,
                "transaction_date": account.transaction_date,
                "amount": account.amount,
                "lender": lender.username,
                "receiver": receiver.username
            })
        return {"success": True, "accounts": result}
    else:
        return {"success": False, "accounts": "No accounts found"}


@app.route('/accounts/')
def get_all_accounts():
    accounts = Account.query.all()
    if accounts:
        result = []
        for account in accounts:
            app.logger.info(account)
            result.append({
                "id":account.id,
                "transaction_id": account.transaction_id,
                "transaction_date": account.transaction_date,
                "amount": account.amount,
                "lender_id": account.lender_id,
                "receiver_id": account.receiver_id,
            })
        return {"success": True, "accounts": result}
    else:
        return {"success": False, "accounts": "No accounts found"}


@app.route('/refresh')
def refresh():
    id = request.args.get('id')
    password = request.args.get('password')

    # http://localhost:5000/refresh?id=janmejay16&password=abcdefghij

    if id=="janmejay16" and password=="abcdefghij":
        create_new()
        return "Refreshed"
    else:
        return "Not authorized"
    
@app.route('/register', methods=['POST'])
def register_user():
    username = request.json.get('username',None)
    password = request.json.get('password',None)
    check_username = User.query.filter_by(username=username).first()

    if check_username:
        # return "Username Already Taken!"
        return jsonify({"success":False,"message":"Username Already Taken!"})

    saltedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        new_user = User(username=username,password=saltedPassword.decode('utf8'))
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
            app.logger.error(e)
            db.session.rollback()
            # return "Internal Server Error!"
            return jsonify({"success":False,"message":"Internal Server Error!"})
    else:
        return jsonify({
            "success":True,
            "message":"User Registered",
            "user": {
                "id": new_user.id,
                "username":new_user.username,
                "password":new_user.password
            }
        })

@app.route('/login',methods=["POST"])
def login_user():
    username = request.json.get('username',None)
    password = request.json.get('password',None)
    app.logger.info(password.encode('utf-8'))
    check_username = User.query.filter_by(username=username).first()
    if check_username:
        if bcrypt.checkpw(password.encode('utf-8'),check_username.password.encode('utf-8')):
            return jsonify({
                "success": True,
                "message":"Logged In!",
                "user": {
                    "id": check_username.id,
                    "username":check_username.username,
                    "password":check_username.password
                }
            })
        else:
            return jsonify({"success": False,"message":"Incorrect Password"})
    else:
        return jsonify({"success": False,"message":"Username does not exist"})


@app.route('/transaction', methods=["POST"])
def add_transaction():
    user_id = request.json.get('user_id',None)
    users = request.json.get('users',None)
    amount = request.json.get('amount',None)
    transaction_date = request.json.get('transaction_date',None)
        
    new_transaction = Transaction(
        user_id=user_id, 
        users=users ,
        amount=amount, 
        transaction_date=transaction_date
    )
    try:
        db.session.add(new_transaction)
        db.session.commit()
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        return jsonify({"success": False,"message":"Something went wrong!"})
    
    
    transaction_id = new_transaction.id

    if users:
        users = users.split(",")
    if amount:
        amount = [int(exp) for exp in amount.split(",")]

    contribution = sum(amount)/len(amount)
    diff_array = []

    for amt in amount:
        diff_array.append(amt-contribution)
    
    transactions = []

    for index in range(0,len(diff_array)):
        if(diff_array[index]<0):
            for i in range(0,len(diff_array)):
                transaction_item = {}
                if (diff_array[i] == abs(diff_array[index]) and index!=i and diff_array[i]>0):
                    transaction_item["lender"] = users[index]
                    transaction_item["receiver"] = users[i]
                    transaction_item["amount"] = abs(diff_array[index])
                    diff_array[index] = diff_array[index]+diff_array[i]
                    diff_array[i] =0
                    transactions.append(transaction_item)
                    i+=1
                    continue
                    
                elif (diff_array[i] < abs(diff_array[index]) and index!=i and diff_array[i]>0):
                    transaction_item = {}
                    transaction_item["lender"] = users[index]
                    transaction_item["receiver"] = users[i]
                    transaction_item["amount"] = abs(diff_array[i])
                    diff_array[index] = diff_array[i] + diff_array[index]
                    diff_array[i] =0
                    transactions.append(transaction_item)
                    i+=1
                    continue
                    
                elif (diff_array[i] > abs(diff_array[index]) and index!=i and diff_array[i] > 0):
                    transaction_item = {}
                    transaction_item["lender"] = users[index]
                    transaction_item["receiver"] = users[i]
                    transaction_item["amount"] = abs(diff_array[index])
                    diff_array[index] = 0
                    diff_array[i] =diff_array[i] + diff_array[index]
                    transactions.append(transaction_item)
                    i+=1
                    continue
    app.logger.info(transactions)

    result={
        "message" : "Accounts Added Succsfully",
        "succes": True
    }

    for item in transactions:
        lender_id = User.query.filter_by(username=item["lender"]).first().id
        receiver_id = User.query.filter_by(username=item["receiver"]).first().id
        amount = item["amount"]

        account = Account(
            lender_id=lender_id,
            receiver_id=receiver_id,
            amount=amount,
            transaction_date=transaction_date,
            transaction_id=transaction_id
        )

        try:
            db.session.add(account)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            db.session.rollback()
            # return "Internal Server Error!"
            result["success"]=False
            result["message"]="Internal Server Error!"
            break
        else:
            continue
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
