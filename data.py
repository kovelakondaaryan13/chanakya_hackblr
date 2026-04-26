import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
QDRANT_URL = os.environ.get("QDRANT_URL", "")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", "")
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")

PENDING_PAYMENTS = [
    {"name": "Max Fabrics", "amount": 185000, "days_overdue": 45},
    {"name": "Crown Textiles", "amount": 156000, "days_overdue": 38},
    {"name": "Atlas Machinery", "amount": 134000, "days_overdue": 32},
    {"name": "Blue Star Dyes", "amount": 112000, "days_overdue": 28},
    {"name": "Prime Yarns", "amount": 98000, "days_overdue": 19},
    {"name": "Royal Threads", "amount": 76000, "days_overdue": 14},
    {"name": "Metro Chemicals", "amount": 54000, "days_overdue": 11},
    {"name": "Eagle Exports", "amount": 43000, "days_overdue": 8},
    {"name": "Global Sizing", "amount": 31000, "days_overdue": 6},
    {"name": "Star Traders", "amount": 18000, "days_overdue": 2},
]

SALES_DATA = [
    {"day": "Monday", "total": 178000, "top_item": "Cotton Fabric", "units": 2850, "orders_completed": 5},
    {"day": "Tuesday", "total": 125000, "top_item": "Polyester Blend", "units": 1920, "orders_completed": 3},
    {"day": "Wednesday", "total": 210000, "top_item": "Cotton Fabric", "units": 3200, "orders_completed": 8},
    {"day": "Thursday", "total": 97000, "top_item": "Mixed Fabric", "units": 1450, "orders_completed": 2},
    {"day": "Friday", "total": 185000, "top_item": "Cotton Fabric", "units": 2700, "orders_completed": 6},
    {"day": "Saturday", "total": 85000, "top_item": "Polyester Blend", "units": 800, "orders_completed": 2},
    {"day": "today", "total": 163000, "top_item": "Cotton Fabric", "units": 2400, "orders_completed": 4},
]

ORDERS = [
    {"order_id": "ORD-KPR-041", "client_name": "Reliance Retail", "fabric_type": "Cotton Fabric", "quantity_meters": 5000, "due_date": "April 18", "status": "in_production", "priority": "high"},
    {"order_id": "ORD-KPR-042", "client_name": "Raymond Limited", "fabric_type": "Cotton Fabric", "quantity_meters": 3000, "due_date": "April 20", "status": "dyeing", "priority": "high"},
    {"order_id": "ORD-KPR-043", "client_name": "Arvind Mills", "fabric_type": "Polyester Blend", "quantity_meters": 4200, "due_date": "April 22", "status": "in_production", "priority": "medium"},
    {"order_id": "ORD-KPR-044", "client_name": "Welspun India", "fabric_type": "Mixed Fabric", "quantity_meters": 2500, "due_date": "April 16", "status": "ready_to_dispatch", "priority": "high"},
    {"order_id": "ORD-KPR-045", "client_name": "Vardhman Textiles", "fabric_type": "Cotton Fabric", "quantity_meters": 1800, "due_date": "April 25", "status": "quality_check", "priority": "medium"},
    {"order_id": "ORD-KPR-046", "client_name": "Dollar Industries", "fabric_type": "Cotton Fabric", "quantity_meters": 3500, "due_date": "April 28", "status": "in_production", "priority": "medium"},
    {"order_id": "ORD-KPR-047", "client_name": "Monte Carlo", "fabric_type": "Polyester Blend", "quantity_meters": 500, "due_date": "April 17", "status": "ready_to_dispatch", "priority": "low"},
    {"order_id": "ORD-KPR-048", "client_name": "Bombay Dyeing", "fabric_type": "Cotton Fabric", "quantity_meters": 4000, "due_date": "April 30", "status": "dyeing", "priority": "high"},
]

BATCHES = [
    {"batch_id": "BATCH-KPR-041", "fabric_type": "Cotton Fabric", "meters_produced": 3200, "target_meters": 5000, "machine_id": "LOOM-07", "status": "running"},
    {"batch_id": "BATCH-KPR-042", "fabric_type": "Cotton Fabric", "meters_produced": 1800, "target_meters": 3000, "machine_id": "LOOM-03", "status": "running"},
    {"batch_id": "BATCH-KPR-043", "fabric_type": "Polyester Blend", "meters_produced": 2100, "target_meters": 4200, "machine_id": "LOOM-11", "status": "running"},
    {"batch_id": "BATCH-KPR-044", "fabric_type": "Mixed Fabric", "meters_produced": 900, "target_meters": 1800, "machine_id": "LOOM-05", "status": "stopped"},
    {"batch_id": "BATCH-KPR-045", "fabric_type": "Cotton Fabric", "meters_produced": 4000, "target_meters": 4000, "machine_id": "LOOM-09", "status": "maintenance"},
    {"batch_id": "BATCH-KPR-046", "fabric_type": "Cotton Fabric", "meters_produced": 1200, "target_meters": 3500, "machine_id": "LOOM-02", "status": "running"},
]

VENDORS = [
    {"name": "Max Fabrics", "phone": "+91-9822011001", "email": "max.fabrics@gmail.com"},
    {"name": "Crown Textiles", "phone": "+91-9822011002", "email": "crown.textiles@gmail.com"},
    {"name": "Atlas Machinery", "phone": "+91-9822011003", "email": "atlas.machinery@gmail.com"},
    {"name": "Blue Star Dyes", "phone": "+91-9822011004", "email": "bluestar.dyes@gmail.com"},
    {"name": "Prime Yarns", "phone": "+91-9822011005", "email": "prime.yarns@gmail.com"},
    {"name": "Royal Threads", "phone": "+91-9822011006", "email": "royal.threads@gmail.com"},
    {"name": "Metro Chemicals", "phone": "+91-9822011007", "email": "metro.chemicals@gmail.com"},
    {"name": "Eagle Exports", "phone": "+91-9822011008", "email": "eagle.exports@gmail.com"},
    {"name": "Global Sizing", "phone": "+91-9822011009", "email": "global.sizing@gmail.com"},
    {"name": "Star Traders", "phone": "+91-9822011010", "email": "star.traders@gmail.com"},
]

LABOUR = [
    {"name": "Ravi Kumar", "role": "loom_operator", "shift": "morning", "attendance_today": "present", "days_worked_this_month": 22, "salary_due": 18500},
    {"name": "Sunil Patil", "role": "loom_operator", "shift": "morning", "attendance_today": "present", "days_worked_this_month": 20, "salary_due": 16800},
    {"name": "Amit Singh", "role": "loom_operator", "shift": "evening", "attendance_today": "present", "days_worked_this_month": 24, "salary_due": 20200},
    {"name": "Priya Sharma", "role": "loom_operator", "shift": "evening", "attendance_today": "absent", "days_worked_this_month": 14, "salary_due": 11800},
    {"name": "Deepak More", "role": "dyer", "shift": "morning", "attendance_today": "present", "days_worked_this_month": 21, "salary_due": 19200},
    {"name": "Kavita Rao", "role": "dyer", "shift": "evening", "attendance_today": "present", "days_worked_this_month": 23, "salary_due": 21000},
    {"name": "Rajesh Nair", "role": "dyer", "shift": "night", "attendance_today": "half_day", "days_worked_this_month": 18, "salary_due": 15500},
    {"name": "Anita Desai", "role": "quality_inspector", "shift": "morning", "attendance_today": "present", "days_worked_this_month": 25, "salary_due": 22800},
    {"name": "Vikas Joshi", "role": "quality_inspector", "shift": "evening", "attendance_today": "present", "days_worked_this_month": 19, "salary_due": 17400},
    {"name": "Neha Kulkarni", "role": "supervisor", "shift": "morning", "attendance_today": "present", "days_worked_this_month": 26, "salary_due": 28500},
    {"name": "Sanjay Pawar", "role": "supervisor", "shift": "night", "attendance_today": "absent", "days_worked_this_month": 16, "salary_due": 18000},
    {"name": "Meera Iyer", "role": "loom_operator", "shift": "night", "attendance_today": "present", "days_worked_this_month": 1, "salary_due": 850},
]

MACHINES = [
    {"machine_id": "LOOM-01", "type": "loom", "status": "running", "last_serviced": "April 8", "efficiency_percent": 92, "operator_name": "Ravi Kumar"},
    {"machine_id": "LOOM-02", "type": "loom", "status": "running", "last_serviced": "April 5", "efficiency_percent": 87, "operator_name": "Sunil Patil"},
    {"machine_id": "LOOM-03", "type": "loom", "status": "running", "last_serviced": "April 10", "efficiency_percent": 95, "operator_name": "Amit Singh"},
    {"machine_id": "LOOM-04", "type": "loom", "status": "stopped", "last_serviced": "March 28", "efficiency_percent": 62, "operator_name": "Priya Sharma"},
    {"machine_id": "LOOM-05", "type": "loom", "status": "maintenance", "last_serviced": "April 12", "efficiency_percent": 0, "operator_name": "Meera Iyer"},
    {"machine_id": "LOOM-06", "type": "loom", "status": "running", "last_serviced": "April 9", "efficiency_percent": 98, "operator_name": "Amit Singh"},
    {"machine_id": "DYEING-01", "type": "dyeing_vat", "status": "running", "last_serviced": "April 6", "efficiency_percent": 88, "operator_name": "Deepak More"},
    {"machine_id": "DYEING-02", "type": "dyeing_vat", "status": "stopped", "last_serviced": "March 30", "efficiency_percent": 60, "operator_name": "Kavita Rao"},
]

RAW_MATERIAL = [
    {"material": "Cotton Yarn", "stock_kg": 1200, "reorder_level_kg": 500, "supplier_name": "Max Fabrics", "days_remaining": 8},
    {"material": "Polyester Fibre", "stock_kg": 350, "reorder_level_kg": 400, "supplier_name": "Prime Yarns", "days_remaining": 3},
    {"material": "Red Dye", "stock_kg": 45, "reorder_level_kg": 50, "supplier_name": "Blue Star Dyes", "days_remaining": 2},
    {"material": "Blue Dye", "stock_kg": 120, "reorder_level_kg": 50, "supplier_name": "Blue Star Dyes", "days_remaining": 12},
    {"material": "Sizing Chemical", "stock_kg": 80, "reorder_level_kg": 100, "supplier_name": "Global Sizing", "days_remaining": 4},
    {"material": "Finishing Agent", "stock_kg": 900, "reorder_level_kg": 600, "supplier_name": "Metro Chemicals", "days_remaining": 6},
]

EXPENSES = [
    {"date": "April 14", "category": "electricity", "amount_rs": 42000, "description": "Factory power bill first half April", "approved_by": "Neha Kulkarni"},
    {"date": "April 13", "category": "raw_material", "amount_rs": 185000, "description": "Cotton Yarn 2000kg from Max Fabrics", "approved_by": "Neha Kulkarni"},
    {"date": "April 12", "category": "maintenance", "amount_rs": 15500, "description": "LOOM-05 bearing replacement", "approved_by": "Sanjay Pawar"},
    {"date": "April 11", "category": "labour", "amount_rs": 95000, "description": "Weekly wages Week 2 April", "approved_by": "Neha Kulkarni"},
    {"date": "April 10", "category": "transport", "amount_rs": 12000, "description": "Fabric dispatch to Welspun India", "approved_by": "Neha Kulkarni"},
    {"date": "April 9", "category": "raw_material", "amount_rs": 36500, "description": "Dyes bulk order from Blue Star Dyes", "approved_by": "Sanjay Pawar"},
    {"date": "April 8", "category": "maintenance", "amount_rs": 8500, "description": "DYEING-02 valve repair", "approved_by": "Sanjay Pawar"},
    {"date": "April 7", "category": "electricity", "amount_rs": 5200, "description": "Generator diesel top-up", "approved_by": "Neha Kulkarni"},
    {"date": "April 6", "category": "transport", "amount_rs": 18000, "description": "Raw material pickup from Mumbai", "approved_by": "Neha Kulkarni"},
    {"date": "April 5", "category": "labour", "amount_rs": 92000, "description": "Weekly wages Week 1 April", "approved_by": "Neha Kulkarni"},
]

DOCUMENTS = (
    [f"Pending payment from {p['name']}: Rs {p['amount']} overdue by {p['days_overdue']} days" for p in PENDING_PAYMENTS] +
    [f"Sales on {s['day']}: Rs {s['total']} total, top item {s['top_item']}, {s['units']} meters sold, {s['orders_completed']} orders completed" for s in SALES_DATA] +
    [f"Order {o['order_id']} for {o['client_name']}: {o['quantity_meters']}m of {o['fabric_type']}, due {o['due_date']}, status {o['status']}, priority {o['priority']}" for o in ORDERS] +
    [f"Batch {b['batch_id']} on {b['machine_id']}: {b['fabric_type']}, {b['meters_produced']}/{b['target_meters']}m produced, status {b['status']}" for b in BATCHES] +
    [f"Vendor {v['name']}: phone {v['phone']}, email {v['email']}" for v in VENDORS] +
    [f"Worker {w['name']}: {w['role']}, {w['shift']} shift, attendance {w['attendance_today']}, {w['days_worked_this_month']} days worked, salary due Rs {w['salary_due']}" for w in LABOUR] +
    [f"Machine {m['machine_id']}: {m['type']}, status {m['status']}, efficiency {m['efficiency_percent']}%, operator {m['operator_name']}, last serviced {m['last_serviced']}" for m in MACHINES] +
    [f"Raw material {r['material']}: {r['stock_kg']}kg in stock, reorder at {r['reorder_level_kg']}kg, supplier {r['supplier_name']}, {r['days_remaining']} days remaining" for r in RAW_MATERIAL] +
    [f"Expense on {e['date']}: {e['category']} Rs {e['amount_rs']}, {e['description']}, approved by {e['approved_by']}" for e in EXPENSES]
)
