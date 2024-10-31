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
    if not name or not isinstance(age, int) or age < 0:
       return jsonify({"error": "Please provide a valid name and age"}), 400
    
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

@app.route('/search', methods=['GET'])
def search_user():
    name_query = request.args.get('name')
    if not name_query:
        return jsonify({"error": "Please provide a name to search"}), 400
    
    users = User.query.filter(User.name.ilike(f"%{name_query}")).all()
    if not users:
        return jsonify({"message": "No users found with that name"}), 404
    
    user_list = [{"id": user.id, "name": user.name, "age": user.age} for user in users]
    return jsonify(user_list), 200
    

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all() #Query all users from the database
    user_list = [{"id": user.id, "name": user.name, "age": user.age} for user in users]
    return jsonify(user_list), 200

@app.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if 'name' in data:
        user.name = data['name']
    if 'age' in data:
        user.age = data['age']

    with app.app_context():
        db.session.commit()

    return jsonify({"message": "User updated successfully!"}), 200

@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    with app.app_context():
        db.session.delete(user)
        db.session.commit()

    return jsonify({"message": "User deleted successfully!"}), 200

if __name__ == '__main__':
    with app.app_context(): 
       db.create_all() #Create database tables
    app.run(debug = True)