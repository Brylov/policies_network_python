import ipaddress
import json
import re

class PolicyAPI:
    def __init__(self) -> None:
        self.policies =[]

    def create_policy(self, json_input: str) -> str:
        try:
            policy = json.loads(json_input)
            self.check_valid_data_policy(policy)
            self.policies.append(policy)
            policy['id'] = str(len(self.policies) - 1 ) 
            policy['rules'] = []
            return json.dumps({"id": policy['id']})  # returning the index as identifier
        except KeyError:
            raise ValueError("Policy JSON must contain 'name', 'description', and 'type' fields")


    def read_policy(self, json_identifier: str) -> str:
        try:
            policy_index = self.get_policy(json_identifier)
            policy = self.policies[policy_index]
            return json.dumps(policy)
        except ValueError as e:
            raise e

    def update_policy(self, json_identifier: str, json_input: str) -> None:
        try:
            policy_index = self.get_policy(json_identifier)
            policy = self.policies[policy_index]
            update_policy = json.loads(json_input) 
            update_policy['id'] = policy['id']
            if self.check_valid_data_policy(update_policy, index=policy_index):
                self.policies[policy_index] = update_policy
        except ValueError as e:
            raise e      

    def delete_policy(self, json_identifier: str) -> None:
        try:
            policy_index = self.get_policy(json_identifier)
            policy = self.policies[policy_index]
            del self.policies[policy_index]
        except ValueError as e:
            raise e

    def list_policies(self) -> str:
        return json.dumps(self.policies)
    
    def check_valid_data_policy(self, policy, index=None):
        name = policy['name']
        description = policy['description']
        type = policy['type']
        if type.lower() != "arupa" and type.lower() != "frisco":
            raise ValueError("type can be only Arupa or Frisco")
        if len(name) > 32 or not name.isalnum():
            raise ValueError("Policy name must be at most 32 alphanumeric characters and underscores")
        if any(existing_policy['name'] == name and existing_policy['type'].lower() == "arupa" and self.policies.index(existing_policy) != index for existing_policy in self.policies):
            raise ValueError("Policy name of Arupa types must be unique")
        return True
    
    def get_policy(self, json_identifier):
        try:
            identifier_dict = json.loads(json_identifier)
            policy_id = identifier_dict['id']
            for index, policy in enumerate(self.policies):
                if policy.get('id') == policy_id:
                    return index
            raise ValueError("Policy with ID {} not found".format(policy_id))
        except ValueError:
            raise ValueError("Invalid policy identifier")
    
    def check_valid_data_rule(self, policy, json_rule, old_rule=None):
        name = json_rule['name']
        ip_proto = json_rule['ip_proto']
        source_port = json_rule['source_port']
        if ip_proto.lower() not in ['tcp', 'udp', 'icmp']:
            raise ValueError("IP Protocol is Invalid - select tcp/udp/icmp")
        if not 0 <= int(source_port) <= 65535:
            raise ValueError("Source port Invalid - select between 0 - 65535")
        if policy['type'].lower() == 'arupa':
            source_subnet = json_rule['source_subnet']
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$', source_subnet):     
                raise ValueError("Source subnet Invalid - i.e. 10.0.0.0/16")       
        

        for rule in policy.get('rules', []):
            # Skip validation for old_rule if provided
            if old_rule and rule == old_rule:
                continue
            if rule['name'] == name:
                raise ValueError("Rule name is already exist in this policy") # Name already exists, rule is not valid
                
        if policy['type'].lower() == 'frisco':
            source_ip = json_rule.get('source_ip')  # source_ip is only for Frisco rules
            destination_ip = json_rule.get('destination_ip')  # destination_ip is only for Frisco rules
            try:
                ipaddress.ip_address(source_ip)
            except ValueError:
                raise ValueError("source_ip is Invalid")
            try:
                ipaddress.ip_address(destination_ip)
            except ValueError:
                raise ValueError("source_ip is Invalid")
            # Iterate through all policies
            # Iterate through Frisco policies only
            for other_policy in self.policies:
                if other_policy['type'].lower() == 'frisco' and other_policy != policy:
                    # Check if the name already exists in the other policy's rules
                    for rule in other_policy.get('rules', []):
                        if rule['name'] == name:
                            raise ValueError("Rule name already exists in another Frisco policy") # Name already exists, rule is not valid
        return True

    def get_rule(self, json_identifier):
        try:
            identifier_dict = json.loads(json_identifier)
            policy_id = int(json.loads(identifier_dict['policyID'])['id'])
            rule_id = int(json.loads(identifier_dict['ruleID'])['id'])
            policy_index = ''
            for index, policy in enumerate(self.policies):
                if int(policy.get('id')) == policy_id:
                    policy = self.policies[index]
                    policy_index = index      
            rules = policy.get('rules', [])
            for index, rule in enumerate(rules):
                if rule.get('id') == rule_id:
                    return policy_index, index
                else:
                    raise ValueError("Rule not Found")
            raise ValueError("Rule with ID {} not found in policy with ID {}".format(rule_id, policy_id))
        except ValueError:
            raise ValueError("Invalid rule identifier")

    def create_rule(self, json_policy_identifier: str, json_rule_input: str) -> str:
        try:
            policy_index = self.get_policy(json_policy_identifier)
            policy = self.policies[policy_index]
            json_rule = json.loads(json_rule_input)
            self.check_valid_data_rule(policy, json_rule)
            rule_id = len(policy['rules'])  # Assign a unique ID to the rule
            json_rule['id'] = rule_id
            policy['rules'].append(json_rule)
            return json.dumps({"id": rule_id})  # Return the ID of the created rule
        except ValueError as e:
            raise e

    def read_rule(self, json_identifier: str) -> str:
        try:
            policy_index, rule_id = self.get_rule(json_identifier)
            policy = self.policies[policy_index]
            rule = policy['rules'][rule_id]
            return json.dumps(rule)
        except ValueError as e:
            raise e

    def update_rule(self, json_identifier: str, json_rule_input: str) -> None:
        try:
            policy_index, rule_id = self.get_rule(json_identifier)
            policy = self.policies[policy_index]
            rule = policy['rules'][rule_id]
            update_rule = json.loads(json_rule_input) 
            update_rule['id'] = rule['id']
            if self.check_valid_data_rule(policy, update_rule, old_rule=rule):
                self.policies[policy_index]['rules'][rule_id] = update_rule
                self.policies[policy_index] = policy
        except ValueError as e:
            raise e 

    def delete_rule(self, json_identifier: str) -> None:
        try:
            policy_index, rule_index = self.get_rule(json_identifier)
            policy = self.policies[policy_index]
            del policy['rules'][rule_index]
        except ValueError as e:
            raise e

    def list_rules(self, json_policy_identifier: str) -> str:
        try:
            policy = self.policies[self.get_policy(json_policy_identifier)]
            return json.dumps(policy['rules'])
        except ValueError as e:
            raise e
