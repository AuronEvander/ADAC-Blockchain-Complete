class SmartContract:
    def __init__(self):
        self.state = {}
        self.owner = None

    def deploy(self, owner_address):
        self.owner = owner_address

    def execute(self, sender, function_name, params):
        if not hasattr(self, function_name):
            raise Exception(f"Function {function_name} not found")

        function = getattr(self, function_name)
        return function(sender, *params)

    def validate_owner(self, sender):
        if sender != self.owner:
            raise Exception("Only contract owner can perform this action")