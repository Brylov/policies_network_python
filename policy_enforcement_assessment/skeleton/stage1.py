class PolicyAPI:
    def __init__(self) -> None:
        pass

    def create_policy(self, json_input: str) -> str:
        raise NotImplementedError

    def list_policies(self) -> str:
        raise NotImplementedError
