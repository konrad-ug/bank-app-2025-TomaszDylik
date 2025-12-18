from flask import Flask, request, jsonify
from src.personal_account_registry import AccountRegistry
from src.personal_account import PersonalAccount
app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    
    pesel = data["pesel"]
    if registry.pesel_exists(pesel):
        return jsonify({"message": "Account with this PESEL already exists"}), 409
    
    account = PersonalAccount(data["name"], data["surname"], pesel)
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.return_all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.length()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    return jsonify({"name": account.first_name, "surname": account.last_name, "pesel": account.pesel, "balance": account.balance}), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    data = request.get_json()
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    
    return jsonify({"message": "Account updated", "account": {"name": account.first_name, "surname": account.last_name, "pesel": account.pesel}}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    registry.accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def make_transfer(pesel):
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    data = request.get_json()
    amount = data.get("amount")
    transfer_type = data.get("type")
    
    # Validate transfer type
    valid_types = ["incoming", "outgoing", "express"]
    if transfer_type not in valid_types:
        return jsonify({"message": "Invalid transfer type"}), 400
    
    # Handle different transfer types
    if transfer_type == "incoming":
        account.incoming_transfer(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    
    elif transfer_type == "outgoing":
        initial_balance = account.balance
        account.outgoing_transfer(amount)
        # Check if transfer was successful by comparing balance
        if account.balance < initial_balance:
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        else:
            return jsonify({"message": "Insufficient funds"}), 422
    
    elif transfer_type == "express":
        result = account.outgoing_express_transfer(amount)
        if result:
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        else:
            return jsonify({"message": "Insufficient funds"}), 422