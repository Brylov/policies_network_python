import json
from flask import Flask, request, jsonify, render_template
from policy_api import PolicyAPI

app = Flask(__name__)
policy_api = PolicyAPI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_policy', methods=['POST'])
def create_policy():
    try:
        json_input = request.json
        policy_id = policy_api.create_policy(json.dumps(json_input))
        return jsonify({"policy_id": policy_id}), 201
    except ValueError as e:
        return str(e), 400

@app.route('/list_policies', methods=['GET'])
def list_policies():
    try:
        return policy_api.list_policies(), 200
    except ValueError as e:
        return str(e), 400
    
@app.route('/update_policy', methods=['PUT'])
def update_policy():
    try:
        json_identifier = {"id": request.args.get('id')} 
        json_input = request.json
        policy_api.update_policy((json.dumps(json_identifier)), json.dumps(json_input))
        return "Policy updated successfully", 200
    except ValueError as e:
        return str(e), 400

@app.route('/read_policy', methods=['GET'])
def read_policy():
    try:
        json_identifier = {"id": request.args.get('id')} 
        policy_data = policy_api.read_policy(json.dumps(json_identifier))
        return policy_data, 200
    except ValueError as e:
        return str(e), 400

@app.route('/delete_policy', methods=['DELETE'])
def delete_policy():
    try:
        json_identifier = {"id": request.args.get('id')} 
        policy_api.delete_policy(json.dumps(json_identifier))
        return "Policy deleted successfully", 200
    except ValueError as e:
        return str(e), 400



if __name__ == '__main__':
    app.run(debug=True)
