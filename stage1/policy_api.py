import json

class PolicyAPI:
    def __init__(self) -> None:
        self.policies =[]

    def create_policy(self, json_input: str) -> str:
        try:
            policy = json.loads(json_input)
            self.check_valid_data(policy)
            self.policies.append(policy)
            policy['id'] = str(len(self.policies) - 1 ) 
            return json.dumps({"id": policy['id']})  # returning the index as identifier
        except KeyError:
            raise ValueError("Policy JSON must contain 'name' ,'description'")

    def list_policies(self) -> str: 
        return json.dumps(self.policies)
    
    def check_valid_data(self, policy):
        name = policy['name']
        description = policy['description']
        if len(name) > 32 or not name.isalnum():
            raise ValueError("Policy name must be at most 32 alphanumeric characters and underscores")
        if any(existing_policy['name'] == name for existing_policy in self.policies):
            raise ValueError("Policy name already exist")
        return True
