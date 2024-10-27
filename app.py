from flask import Flask, request, jsonify

app = Flask(__name__)

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

#Return a response with both name and age
    response = {
       "message" : f"Hello , {name}! You are {age} years old.",
       "received_data" : data
}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug = True)