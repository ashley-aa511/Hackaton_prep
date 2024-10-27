from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #Database file
db = SQLAlchemy(app)
CORS(app)    #Enamble CORS for all routes

#Define a model for your data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    return "Hackathon manenoz!"

#Define a route "/submit" whete it accepts json data and returns a response
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.get_json() #Extract JSON data 
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    name = data.get("name")
    age = data.get("age")

#Check if both name and age are provided
    if not name or not age:
       return jsonify({"error": "Please provide both name and age"}), 400
    
    #Create a new user instance and add to the database
    new_user = User(name=name, age=age)

    #Wrap database operations in an application context
    with app.app_context():
       db.session.add(new_user)
       db.session.commit()

#Return a response with both name and age
    response = {
       "message" : f"Hello , {name}! You are {age} years old.",
       "received_data" : data
}
    return jsonify(response), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all() #Query all users from the database
    user_list = [{"id": user.id, "name": user.name, "age": user.age} for user in users]
    return jsonify(user_list), 200

if __name__ == '__main__':
    with app.app_context(): 
       db.create_all() #Create database tables
    app.run(debug = True)