from typing import Dict, Any, Optional
import time
import hashlib

class SmartContract:
    def __init__(self, owner: str, code: str, initial_state: Dict):
        self.owner = owner
        self.code = code
        self.state = initial_state
        self.created_at = time.time()
        self.contract_id = self._generate_contract_id()
        self.transactions = []

    def _generate_contract_id(self) -> str:
        contract_string = f"{self.owner}{self.code}{self.created_at}"
        return hashlib.sha256(contract_string.encode()).hexdigest()

    def execute(self, method: str, params: Dict, caller: str) -> Dict:
        if not self._validate_caller(caller, method):
            return {"success": False, "error": "Unauthorized"}

        try:
            result = self._execute_method(method, params)
            self.transactions.append({
                "method": method,
                "params": params,
                "caller": caller,
                "timestamp": time.time()
            })
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _validate_caller(self, caller: str, method: str) -> bool:
        if method in ["owner_only"] and caller != self.owner:
            return False
        return True

    def _execute_method(self, method: str, params: Dict) -> Any:
        # Execute the contract method
        method_mapping = {
            "update_state": self._update_state,
            "get_state": self._get_state,
            "owner_only": self._owner_only
        }
        
        if method not in method_mapping:
            raise ValueError(f"Method {method} not found")
            
        return method_mapping[method](params)