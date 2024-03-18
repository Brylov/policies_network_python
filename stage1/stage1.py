import json

class PolicyAPI:
    def __init__(self) -> None:
        self.policies =[]

    def create_policy(self, json_input: str) -> str:
        try:
            policy = json.loads(json_input)
            name = policy['name']
            description = policy['description']
            if len(name) > 32 or not name.isalnum():
                raise ValueError("Policy name must be at most 32 alphanumeric characters and underscores")
            if any(existing_policy['name'] == name for existing_policy in self.policies):
                raise ValueError("Policy name must be unique")
            self.policies.append(policy)
            return json.dumps({"id": len(self.policies) - 1})  # returning the index as identifier
        except KeyError:
            raise ValueError("Policy JSON must contain 'name' and 'description' fields")

    def list_policies(self) -> str:      
        return json.dumps(self.policies)
