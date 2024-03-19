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
            raise ValueError("Policy JSON must contain 'name' ,'description' and 'type' fields")

    def read_policy(self, json_identifier: str) -> str:
        try:
            policy_index = self.get_policy(json_identifier)
            policy = self.policies[policy_index]

            return json.dumps(policy)
        except (ValueError, IndexError):
            raise ValueError("Invalid policy identifier")

    def update_policy(self, json_identifier: str, json_input: str) -> None:
        try:
            policy_index = self.get_policy(json_identifier)
            policy = self.policies[policy_index]
            update_policy = json.loads(json_input) 
            update_policy['id'] = policy['id']
            print("Updated Policy Data:", update_policy)
            if self.check_valid_data(update_policy, index=policy_index):
                self.policies[policy_index] = update_policy
        except (ValueError, IndexError):
            raise ValueError("Invalid policy identifier")

    def delete_policy(self, json_identifier: str) -> None:
        try:
            policy_index = self.get_policy(json_identifier)
            policy = self.policies[policy_index]
            del self.policies[policy_index]
        except (ValueError, IndexError):
            raise ValueError("Invalid policy identifier")

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
        

    def list_policies(self) -> str:     
        return json.dumps(self.policies)
    
    def check_valid_data(self, policy, index=-1):
        name = policy['name']
        description = policy['description']
        type = str(policy['type'])
        if type.lower() != "arupa" and type.lower() != "frisco":
            raise ValueError("type can be only Arupa or Frisco")
        if len(name) > 32 or not name.isalnum():
            raise ValueError("Policy name must be at most 32 alphanumeric characters and underscores")
        if any(existing_policy['name'] == name and existing_policy['type'].lower() == "arupa" and self.policies.index(existing_policy) != index for existing_policy in self.policies):
            raise ValueError("Policy name of Arupa types must be unique")
        return True



        

