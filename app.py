from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/") # Підключаємося до MongoDB (mongo - це назва контейнера для MongoDB)

db = client["mydatabase"]
collection = db["customers"]

@app.route("/")
def home():
    return "Привіт, це мій додаток з MongoDB на Kubernetes!"

@app.route("/customers", methods=["GET"])
def get_customers():
    customers = []
    for customer in collection.find():
        customers.append({"name": customer["name"], "email": customer["email"]})
    return jsonify(customers)

@app.route("/customer", methods=["POST"])
def add_customer():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    customer = {"name": name, "email": email}
    collection.insert_one(customer)
    return "Клієнт додано успішно!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
