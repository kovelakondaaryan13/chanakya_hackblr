from collections import defaultdict
from datetime import datetime

# Payment states
payment_states = {}
for p in ["Max Fabrics", "Crown Textiles", "Atlas Machinery",
          "Blue Star Dyes", "Prime Yarns", "Royal Threads",
          "Metro Chemicals", "Eagle Exports", "Global Sizing",
          "Star Traders"]:
    payment_states[p] = {
        "status": "OVERDUE",
        "reminder_count": 0,
        "last_action": None,
        "last_action_time": None,
        "history": []
    }

# Material states
material_states = {}
for m in ["Cotton Yarn", "Polyester Fibre", "Red Dye",
          "Blue Dye", "Sizing Chemical", "Finishing Agent"]:
    material_states[m] = {
        "status": "OK",
        "order_placed": False,
        "order_time": None,
        "history": []
    }

# Machine states
machine_states = {}
for m in ["LOOM-01", "LOOM-02", "LOOM-03", "LOOM-04",
          "LOOM-05", "LOOM-06", "DYEING-01", "DYEING-02"]:
    machine_states[m] = {
        "status": "running",
        "maintenance_requested": False,
        "history": []
    }

# Order states - mirrors data.py but trackable
order_states = {
    "ORD-KPR-041": {"status": "in_production", "history": []},
    "ORD-KPR-042": {"status": "dyeing", "history": []},
    "ORD-KPR-043": {"status": "in_production", "history": []},
    "ORD-KPR-044": {"status": "ready_to_dispatch", "history": []},
    "ORD-KPR-045": {"status": "quality_check", "history": []},
    "ORD-KPR-046": {"status": "in_production", "history": []},
    "ORD-KPR-047": {"status": "ready_to_dispatch", "history": []},
    "ORD-KPR-048": {"status": "dyeing", "history": []},
}

def update_payment_state(vendor_name, action, details=""):
    if vendor_name in payment_states:
        state = payment_states[vendor_name]
        old_status = state["status"]

        if action == "REMINDER_SENT":
            state["reminder_count"] += 1
            state["status"] = "REMINDER_SENT"
            if state["reminder_count"] >= 2:
                state["status"] = "ESCALATED"
        elif action == "CALL_MADE":
            state["status"] = "CALL_MADE"
        elif action == "PAYMENT_RECEIVED":
            state["status"] = "PAYMENT_RECEIVED"

        state["last_action"] = action
        state["last_action_time"] = datetime.now().strftime("%H:%M:%S")
        state["history"].append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "action": action,
            "details": details,
            "from_status": old_status,
            "to_status": state["status"]
        })
        return True
    return False

def update_material_state(material_name, action, details=""):
    for key in material_states:
        if material_name.lower() in key.lower():
            state = material_states[key]
            old_status = state["status"]

            if action == "ORDER_PLACED":
                state["status"] = "ORDER_PLACED"
                state["order_placed"] = True
                state["order_time"] = datetime.now().strftime("%H:%M:%S")
            elif action == "CRITICAL":
                if not state["order_placed"]:
                    state["status"] = "CRITICAL"

            state["history"].append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "action": action,
                "details": details,
                "from_status": old_status,
                "to_status": state["status"]
            })
            return True
    return False

def update_machine_state(machine_id, action, details=""):
    machine_id_upper = machine_id.upper()
    if machine_id_upper in machine_states:
        state = machine_states[machine_id_upper]
        old_status = state["status"]

        if action == "MAINTENANCE_REQUESTED":
            state["maintenance_requested"] = True
            state["status"] = "maintenance_requested"
        elif action == "RUNNING":
            state["status"] = "running"
            state["maintenance_requested"] = False

        state["history"].append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "action": action,
            "details": details,
            "from_status": old_status,
            "to_status": state["status"]
        })
        return True
    return False

def get_all_states():
    return {
        "payments": payment_states,
        "materials": material_states,
        "machines": machine_states,
        "orders": order_states
    }

def get_context_for_vendor(vendor_name):
    if vendor_name in payment_states:
        state = payment_states[vendor_name]
        if state["status"] == "REMINDER_SENT":
            return f"Note: {state['reminder_count']} reminder(s) already sent to {vendor_name}. Last action at {state['last_action_time']}."
        elif state["status"] == "ESCALATED":
            return f"Note: {vendor_name} is ESCALATED — {state['reminder_count']} reminders sent, no response."
        elif state["status"] == "CALL_MADE":
            return f"Note: Call was made to {vendor_name} at {state['last_action_time']}."
    return ""
