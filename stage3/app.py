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
    

@app.route('/create_rule', methods=['POST'])
def create_rule():
    try:
        json_policy_identifier = {"id": request.json['policy_id']}
        json_rule_input = request.json['rule_input']
        rule_id = policy_api.create_rule(json.dumps(json_policy_identifier), json.dumps(json_rule_input))
        return jsonify({"rule_id": rule_id}), 201
    except ValueError as e:
        return str(e), 400


@app.route('/read_rule', methods=['GET'])
def read_rule():
    try:
        json_policy_id = json.dumps({"id": request.args.get('policy_id')})
        json_rule_id = json.dumps({"id": request.args.get('rule_id')})
        json_identifier = json.dumps({'policyID': json_policy_id, 'ruleID': json_rule_id})
        rule_data = policy_api.read_rule(json_identifier)
        return jsonify(json.loads(rule_data)), 200
    except ValueError as e:
        return str(e), 400


@app.route('/update_rule', methods=['PUT'])
def update_rule():
    try:
        json_policy_id = json.dumps({"id": request.args.get('policy_id')})
        json_rule_id = json.dumps({"id": request.args.get('rule_id')})
        json_identifier = json.dumps({'policyID': json_policy_id, 'ruleID': json_rule_id})
        json_rule_input = request.json['rule_input']
        policy_api.update_rule(json_identifier, json.dumps(json_rule_input))
        return '', 204
    except ValueError as e:
        return str(e), 400


@app.route('/delete_rule', methods=['DELETE'])
def delete_rule():
    try:
        json_policy_id = json.dumps({"id": request.args.get('policy_id')})
        json_rule_id = json.dumps({"id": request.args.get('rule_id')})
        json_identifier = json.dumps({'policyID': json_policy_id, 'ruleID': json_rule_id})
        policy_api.delete_rule(json_identifier)
        return '', 204
    except ValueError as e:
        return str(e), 400


@app.route('/list_rules', methods=['GET'])
def list_rules():
    try:
        print(request.args.get('policy_id'))
        json_policy_id = {"id": request.args.get('policy_id')}
        rule_list = policy_api.list_rules(json.dumps(json_policy_id))
        print(rule_list)
        return rule_list, 200
    except ValueError as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)
