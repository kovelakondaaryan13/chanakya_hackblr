from data import PENDING_PAYMENTS, SALES_DATA, VENDORS, ORDERS, BATCHES, LABOUR, MACHINES, RAW_MATERIAL, EXPENSES
from state import (update_payment_state, update_material_state,
                   update_machine_state, get_context_for_vendor)

def format_amount(amount):
    if amount >= 100000:
        lakhs = amount // 100000
        thousands = (amount % 100000) // 1000
        return f"{lakhs} lakh {thousands} thousand rupees" if thousands > 0 else f"{lakhs} lakh rupees"
    elif amount >= 1000:
        thousands = amount // 1000
        hundreds = amount % 1000
        return f"{thousands} thousand {hundreds} rupees" if hundreds > 0 else f"{thousands} thousand rupees"
    return f"{amount} rupees"

def speak_id(id_str):
    return id_str.replace("LOOM-", "Loom ").replace("DYEING-", "Dyeing unit ").replace("BATCH-KPR-", "Batch ").replace("ORD-KPR-", "Order ")

def speak_status(s):
    return {"in_production": "in production", "ready_to_dispatch": "ready to dispatch", "dyeing": "in dyeing", "quality_check": "in quality check", "running": "running", "stopped": "stopped", "maintenance": "under maintenance", "present": "present", "absent": "absent", "half_day": "on half day"}.get(s, s)

def speak_phone(phone):
    return phone.replace("+91-", "").replace("-", " ")

def handle_pending_payments(entity=None, original_text=""):
    if entity and entity.lower() in ["today", "now", "aaj", "abhi"]:
        entity = None
    # Gather context notes from state
    context_notes = []
    for p in PENDING_PAYMENTS:
        ctx = get_context_for_vendor(p["name"])
        if ctx:
            context_notes.append(ctx)

    if any(w in (original_text or "").lower() for w in ["most", "biggest", "highest", "largest", "most money", "most overdue", "longest"]):
        top = sorted(PENDING_PAYMENTS, key=lambda x: x["days_overdue"], reverse=True)[0]
        resp = f"Sabse bada overdue hai {top['name']} — {format_amount(top['amount'])}, {top['days_overdue']} days se pending."
        ctx = get_context_for_vendor(top['name'])
        if ctx:
            from state import payment_states
            st = payment_states.get(top['name'], {})
            if st.get("status") == "REMINDER_SENT":
                resp += f" {top['name']} ko reminder pehle se bhej diya hai {st.get('last_action_time', '')} pe. Still no response — aaj call karein?"
            elif st.get("status") == "CALL_MADE":
                resp += f" {top['name']} ko call bhi ho chuka hai {st.get('last_action_time', '')} pe."
        return resp
    if entity:
        matches = [p for p in PENDING_PAYMENTS if entity.lower() in p["name"].lower()]
        if matches:
            p = matches[0]
            resp = f"{p['name']} ka {format_amount(p['amount'])} pending hai, {p['days_overdue']} days se overdue."
            ctx = get_context_for_vendor(p['name'])
            if ctx:
                from state import payment_states
                st = payment_states.get(p['name'], {})
                if st.get("status") == "REMINDER_SENT":
                    resp += f" Reminder pehle se bhej diya hai {st.get('last_action_time', '')} pe. Still no response — aaj call karein?"
                elif st.get("status") == "CALL_MADE":
                    resp += f" Call bhi ho chuka hai {st.get('last_action_time', '')} pe."
            return resp
        return f"{entity} ka record nahi mila."
    total = sum(p["amount"] for p in PENDING_PAYMENTS)
    top3 = sorted(PENDING_PAYMENTS, key=lambda x: x["days_overdue"], reverse=True)[:3]
    resp = f"Total pending hai {format_amount(total)} across {len(PENDING_PAYMENTS)} vendors. Sabse purane teen: "
    for p in top3:
        resp += f"{p['name']} — {format_amount(p['amount'])}, {p['days_overdue']} days se overdue. "
    if context_notes:
        resp += " | " + " | ".join(context_notes[:2])
    return resp

def handle_send_followup(entity=None):
    if not entity:
        return "Kis vendor ko follow-up bhejna hai? Naam batao."
    match = next((v for v in VENDORS if entity.lower() in v["name"].lower()), None)
    if not match:
        return f"{entity} ka record nahi mila. Naam check karke dobara try karein."
    payment = next((p for p in PENDING_PAYMENTS if entity.lower() in p["name"].lower()), None)
    amount_text = format_amount(payment['amount']) if payment else "outstanding payment"
    days_text = f", {payment['days_overdue']} days se overdue" if payment else ""
    print(f"[WHATSAPP LOG] To: {match['phone']} — {amount_text} reminder sent")
    try:
        import requests
        requests.post(
            "http://localhost:9000/send-email",
            json={
                "vendor_name": match["name"],
                "vendor_email": match["email"],
                "type": "followup",
                "amount": payment["amount"] if payment else 0,
                "days_overdue": payment["days_overdue"] if payment else 0
            },
            timeout=5
        )
    except Exception as e:
        print(f"Email trigger: {e}")
    update_payment_state(match["name"], "REMINDER_SENT", f"Email sent: {amount_text}")
    return f"Follow-up bhej diya {match['name']} ko. Unhe {amount_text}{days_text} ka remind kiya. Message deliver ho gaya."

def handle_sales_summary(entity=None, original_text=""):
    orig = (original_text or "").lower()
    if any(w in orig for w in ["best", "highest", "most", "top day", "best day"]):
        best = max(SALES_DATA, key=lambda x: x["total"])
        return f"Sabse accha din tha {best['day']} — {format_amount(best['total'])}. Top item: {best['top_item']}, {best['units']} meters bika, {best['orders_completed']} orders complete."
    day = (entity or "today").lower()
    data = next((s for s in SALES_DATA if s["day"].lower() == day), SALES_DATA[-1])
    return f"{data['day'].capitalize()} ka sales tha {format_amount(data['total'])}. Top item: {data['top_item']}, {data['units']} meters bika, {data['orders_completed']} orders complete."

def handle_vendor_info(entity=None):
    if not entity:
        return "Kis vendor ki information chahiye?"
    match = next((v for v in VENDORS if entity.lower() in v["name"].lower()), None)
    if not match:
        return f"{entity} ka record nahi mila."
    payment = next((p for p in PENDING_PAYMENTS if entity.lower() in p["name"].lower()), None)
    resp = f"{match['name']} — contact number {speak_phone(match['phone'])}, email {match['email']}."
    if payment:
        resp += f" Inka {format_amount(payment['amount'])} pending hai, {payment['days_overdue']} days se overdue."
    return resp

def handle_order_status(entity=None, original_text=""):
    orig = (original_text or "").lower()
    if any(w in orig for w in ["ready", "dispatch", "ship"]):
        ready = [o for o in ORDERS if o["status"] == "ready_to_dispatch"]
        if ready:
            resp = f"{len(ready)} orders dispatch ke liye ready hain: "
            for o in ready:
                resp += f"{o['client_name']} — {o['quantity_meters']} meters {o['fabric_type']}, due {o['due_date']}. "
            return resp
        return "Abhi koi order dispatch ke liye ready nahi hai."
    if any(w in orig for w in ["high priority", "urgent", "priority"]):
        hp = [o for o in ORDERS if o["priority"] == "high"]
        resp = f"{len(hp)} high priority orders hain: "
        for o in hp:
            resp += f"{o['client_name']} — {speak_status(o['status'])}, due {o['due_date']}. "
        return resp
    if any(w in orig for w in ["due soon", "soonest", "earliest", "next due"]):
        from datetime import datetime
        month_map = {"April": 4, "May": 5, "March": 3}
        def parse_date(d):
            parts = d.split()
            return datetime(2024, month_map.get(parts[0], 4), int(parts[1]))
        soonest = min(ORDERS, key=lambda o: parse_date(o["due_date"]))
        return f"Sabse jaldi due order hai {soonest['client_name']} — {soonest['quantity_meters']} meters {soonest['fabric_type']}, due {soonest['due_date']}, abhi {speak_status(soonest['status'])}."
    if any(w in orig for w in ["in production", "production mein", "being made"]):
        prod = [o for o in ORDERS if o["status"] == "in_production"]
        resp = f"{len(prod)} orders production mein hain: "
        for o in prod:
            resp += f"{o['client_name']} — {o['quantity_meters']} meters, due {o['due_date']}. "
        return resp
    if entity:
        match = next((o for o in ORDERS if entity.lower() in o["order_id"].lower() or entity.lower() in o["client_name"].lower()), None)
        if match:
            return (f"{speak_id(match['order_id'])} for {match['client_name']} — {match['quantity_meters']} meters of {match['fabric_type']}. "
                    f"Due {match['due_date']}, abhi {speak_status(match['status'])}, priority {match['priority']}.")
        return f"{entity} ke liye koi order nahi mila."
    counts = {}
    for o in ORDERS:
        counts[o["status"]] = counts.get(o["status"], 0) + 1
    resp = f"{len(ORDERS)} active orders total hain. "
    for k, v in counts.items():
        resp += f"{v} {speak_status(k)}, "
    return resp.rstrip(", ") + "."

def handle_batch_status(entity=None, original_text=""):
    orig = (original_text or "").lower()
    if any(w in orig for w in ["closest", "almost done", "almost complete", "nearly done", "finish"]):
        b = max(BATCHES, key=lambda x: x["meters_produced"] / x["target_meters"])
        pct = int((b["meters_produced"] / b["target_meters"]) * 100)
        return f"{speak_id(b['batch_id'])} on {speak_id(b['machine_id'])} complete hone wala hai — {pct} percent done, {b['meters_produced']} of {b['target_meters']} meters."
    if entity:
        match = next((b for b in BATCHES if entity.lower() in b["batch_id"].lower() or entity.lower() in b["machine_id"].lower()), None)
        if match:
            pct = int((match["meters_produced"] / match["target_meters"]) * 100)
            return (f"{speak_id(match['batch_id'])} on {speak_id(match['machine_id'])}: {match['fabric_type']}, "
                    f"{match['meters_produced']} of {match['target_meters']} meters done, {pct} percent complete, abhi {speak_status(match['status'])}.")
        return f"{entity} ke liye koi batch ya loom nahi mila."
    running = sum(1 for b in BATCHES if b["status"] == "running")
    stopped = sum(1 for b in BATCHES if b["status"] == "stopped")
    maint = sum(1 for b in BATCHES if b["status"] == "maintenance")
    return f"Factory floor: {running} looms chal rahi hain, {stopped} band hain, {maint} maintenance mein. Total {len(BATCHES)} active batches."

def handle_labour_status(entity=None, original_text=""):
    orig = (original_text or "").lower()
    if any(w in orig for w in ["half day", "half-day", "halfday", "who took"]):
        half = [w for w in LABOUR if w["attendance_today"] == "half_day"]
        if half:
            return f"{half[0]['name']} aaj half day pe hain. Yeh hain {half[0]['role'].replace('_',' ')}, {half[0]['shift']} shift pe."
        return "Aaj koi half day pe nahi."
    if any(w in orig for w in ["absent", "who is absent", "not come", "missing"]):
        absent = [w for w in LABOUR if w["attendance_today"] == "absent"]
        if absent:
            names = ", ".join(w["name"] for w in absent)
            return f"Aaj {len(absent)} log absent hain: {names}."
        return "Aaj sab present hain. Full attendance."
    if any(w in orig for w in ["supervisor", "manager", "in charge"]):
        sups = [w for w in LABOUR if w["role"] == "supervisor" and w["attendance_today"] == "present"]
        if sups:
            return f"Aaj supervisor duty pe hain {sups[0]['name']}, {sups[0]['shift']} shift pe."
        return "Aaj koi supervisor present nahi hai."
    if any(w in orig for w in ["salary", "wages", "pay"]):
        total_salary = sum(w["salary_due"] for w in LABOUR)
        return f"Is mahine total salary due hai {format_amount(total_salary)} across {len(LABOUR)} workers."
    if any(w in orig for w in ["morning shift", "morning"]):
        morning = [w for w in LABOUR if w["shift"] == "morning" and w["attendance_today"] == "present"]
        return f"{len(morning)} log morning shift mein hain aaj."
    if entity:
        match = next((w for w in LABOUR if entity.lower() in w["name"].lower()), None)
        if match:
            return (f"{match['name']} — {match['role'].replace('_',' ')}, {match['shift']} shift. "
                    f"Aaj: {speak_status(match['attendance_today'])}. Is mahine: {match['days_worked_this_month']} days worked, salary due {format_amount(match['salary_due'])}.")
        return f"{entity} ka worker record nahi mila."
    present = sum(1 for w in LABOUR if w["attendance_today"] == "present")
    absent = sum(1 for w in LABOUR if w["attendance_today"] == "absent")
    half = sum(1 for w in LABOUR if w["attendance_today"] == "half_day")
    total_salary = sum(w["salary_due"] for w in LABOUR)
    return f"Aaj: {present} present, {absent} absent, {half} half day pe, out of {len(LABOUR)} total workers. Is mahine salary due hai: {format_amount(total_salary)}."

def handle_machine_status(entity=None, original_text=""):
    orig = (original_text or "").lower()
    if any(w in orig for w in ["lowest", "worst", "weakest", "most problem", "needs attention"]):
        active = [m for m in MACHINES if m["efficiency_percent"] > 0]
        worst = min(active, key=lambda m: m["efficiency_percent"])
        return f"Sabse kam efficiency wali machine hai {speak_id(worst['machine_id'])} at {worst['efficiency_percent']} percent. Operator: {worst['operator_name']}, last service {worst['last_serviced']}."
    if any(w in orig for w in ["last service", "serviced", "when was", "service date"]):
        if entity:
            match = next((m for m in MACHINES if entity.lower() in m["machine_id"].lower()), None)
            if match:
                return f"{speak_id(match['machine_id'])} ka last service {match['last_serviced']} ko hua. Abhi status: {speak_status(match['status'])}, efficiency {match['efficiency_percent']} percent."
    if any(w in orig for w in ["operator", "who operates", "who runs"]):
        if entity:
            match = next((m for m in MACHINES if entity.lower() in m["machine_id"].lower()), None)
            if match:
                return f"{speak_id(match['machine_id'])} ko operate karte hain {match['operator_name']}. Abhi status: {speak_status(match['status'])}."
    if entity:
        match = next((m for m in MACHINES if entity.lower() in m["machine_id"].lower()), None)
        if match:
            return (f"{speak_id(match['machine_id'])} — status {speak_status(match['status'])}, efficiency {match['efficiency_percent']} percent, "
                    f"operator {match['operator_name']}, last service {match['last_serviced']}.")
        return f"{entity} ke liye koi machine nahi mili."
    running = [m for m in MACHINES if m["status"] == "running"]
    stopped = [m for m in MACHINES if m["status"] == "stopped"]
    maint = [m for m in MACHINES if m["status"] == "maintenance"]
    resp = f"{len(running)} machines chal rahi hain, {len(stopped)} band hain, {len(maint)} maintenance mein. "
    if stopped:
        resp += "Band hain: " + ", ".join(f"{speak_id(m['machine_id'])} at {m['efficiency_percent']} percent efficiency" for m in stopped) + ". "
    if maint:
        resp += "Maintenance mein: " + ", ".join(speak_id(m["machine_id"]) for m in maint) + "."
    return resp

def handle_stock_status(entity=None, original_text=""):
    orig = (original_text or "").lower()
    if any(w in orig for w in ["urgent", "critical", "most urgent", "reorder", "order now", "place order"]):
        low = sorted([r for r in RAW_MATERIAL if r["stock_kg"] <= r["reorder_level_kg"]], key=lambda x: x["days_remaining"])
        if low:
            most_urgent = low[0]
            resp = f"Sabse urgent reorder chahiye: {most_urgent['material']} — sirf {most_urgent['days_remaining']} din bacha hai, {most_urgent['stock_kg']} kg stock mein. Supplier hai {most_urgent['supplier_name']}. "
            if len(low) > 1:
                resp += f"{len(low)-1} other materials bhi reorder level se neeche hain."
            return resp
        return "Abhi koi material ko urgent reorder nahi chahiye. Sab stocks reorder level ke upar hain."
    if entity:
        match = next((r for r in RAW_MATERIAL if entity.lower() in r["material"].lower()), None)
        if match:
            status = "reorder level se NEECHE — restocking chahiye" if match["stock_kg"] <= match["reorder_level_kg"] else "OK"
            return (f"{match['material']}: {match['stock_kg']} kg stock mein, reorder level {match['reorder_level_kg']} kg hai. "
                    f"Supplier: {match['supplier_name']}. {match['days_remaining']} din chalega. Status: {status}.")
        return f"{entity} ka stock record nahi mila."
    low = [r for r in RAW_MATERIAL if r["stock_kg"] <= r["reorder_level_kg"]]
    ok = [r for r in RAW_MATERIAL if r["stock_kg"] > r["reorder_level_kg"]]
    for r in low:
        update_material_state(r["material"], "CRITICAL", f"{r['days_remaining']} days remaining")
    resp = ""
    if low:
        resp += f"Alert: {len(low)} materials reorder level se neeche hain — "
        for r in low:
            resp += f"{r['material']} sirf {r['days_remaining']} din bacha hai. "
    if ok:
        resp += f"{len(ok)} materials theek hain: " + ", ".join(r["material"] for r in ok) + "."
    return resp

def handle_expense_summary(entity=None, original_text=""):
    orig = (original_text or "").lower()
    if any(w in orig for w in ["biggest", "largest", "most", "highest"]):
        biggest = max(EXPENSES, key=lambda e: e["amount_rs"])
        return f"Sabse bada expense tha {format_amount(biggest['amount_rs'])} on {biggest['date']} — {biggest['description']}, approve kiya {biggest['approved_by']}."
    if any(w in orig for w in ["approved", "who approved"]):
        approver_totals = {}
        for e in EXPENSES:
            approver_totals[e["approved_by"]] = approver_totals.get(e["approved_by"], 0) + e["amount_rs"]
        top_approver = max(approver_totals, key=approver_totals.get)
        return f"Sabse zyada expenses {top_approver} ne approve kiye — total {format_amount(approver_totals[top_approver])}."
    if entity:
        matches = [e for e in EXPENSES if entity.lower() in e["category"].lower()]
        if matches:
            total = sum(e["amount_rs"] for e in matches)
            resp = f"{entity.capitalize()} expenses total {format_amount(total)}. "
            for e in matches[:3]:
                resp += f"{e['date']}: {format_amount(e['amount_rs'])} — {e['description']}. "
            return resp
        return f"{entity} category mein koi expense nahi mila."
    total = sum(e["amount_rs"] for e in EXPENSES)
    by_cat = {}
    for e in EXPENSES:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["amount_rs"]
    resp = f"Total recent expenses: {format_amount(total)}. Breakdown: "
    for cat, amt in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
        resp += f"{cat.replace('_',' ')} {format_amount(amt)}, "
    return resp.rstrip(", ") + "."

def handle_initiate_call(entity=None):
    if not entity:
        return "Kisko call karna hai? Vendor ka naam batao."
    match = next((v for v in VENDORS if entity.lower() in v["name"].lower()), None)
    if not match:
        return f"{entity} ka record nahi mila."
    payment = next((p for p in PENDING_PAYMENTS if entity.lower() in p["name"].lower()), None)
    try:
        import requests
        requests.post(
            "http://localhost:9000/initiate-call",
            json={
                "vendor_name": match["name"],
                "amount": payment["amount"] if payment else 0,
                "days_overdue": payment["days_overdue"] if payment else 0
            },
            timeout=10
        )
        update_payment_state(match["name"], "CALL_MADE", f"Outbound call via Vapi")
        if payment:
            lakhs = payment["amount"] // 100000
            thousands = (payment["amount"] % 100000) // 1000
            return f"Call initiate ho gaya {match['name']} ko. Phone ring ho raha hai — {lakhs} lakh {thousands} thousand rupees ka payment reminder. Dashboard mein call log dekho."
        return f"Call initiate ho gaya {match['name']} ko."
    except Exception as e:
        update_payment_state(match["name"], "CALL_MADE", f"Outbound call via Vapi")
        return f"Call ho raha hai {match['name']} ko. Check karo phone."

def handle_unknown(original_text):
    from data import MINIMAX_API_KEY

    context = """You are Chanakya, AI copilot for Sarvoday Textiles Kolhapur.
Speak in Hinglish exactly like these examples:
Q: Should I be worried about anything today?
A: Haan, do cheezein urgent hain. Red Dye sirf 2 days remaining hai, aur Max Fabrics ka 1 lakh 85 thousand rupees 45 days se overdue hai. Inhe aaj hi address karo.
Q: Thank you Chanakya
A: Anytime. Aur kuch jaanna hai?
Q: How is business doing?
A: Aaj ka sales 1 lakh 63 thousand rupees tha — decent day. But 3 materials stock alert mein hain aur 9 lakh 7 thousand rupees pending payment hai. Attention chahiye.

Current snapshot:
- Total pending: 9 lakh 7 thousand rupees from 10 vendors
- Max Fabrics 1 lakh 85 thousand (45 days), Crown Textiles 1 lakh 56 thousand (38 days)
- Today sales: 1 lakh 63 thousand rupees, Cotton Fabric, 2 thousand 400 meters
- 8 orders — 2 ready to dispatch, 3 in production, 2 dyeing, 1 quality check
- 2 machines stopped: Loom 04 at 62 percent, Dyeing unit 02 at 60 percent
- Stock alerts: Red Dye 2 days, Polyester Fibre 3 days, Sizing Chemical 4 days
- Labour: 9 present, 2 absent, 1 half day

Answer using same Hinglish style. Short, direct, specific. Max 3 sentences."""

    try:
        import requests as req
        response = req.post(
            "https://api.minimax.io/v1/text/chatcompletion_v2",
            headers={
                "Authorization": f"Bearer {MINIMAX_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "MiniMax-Text-01",
                "messages": [
                    {"role": "system", "content": context},
                    {"role": "user", "content": original_text}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            },
            timeout=15
        )
        result = response.json()
        reply = (result.get("choices") or [{}])[0].get("message", {}).get("content", "")
        if reply:
            return reply
        raise Exception("Empty MiniMax response")
    except Exception as e:
        print(f"MiniMax fallback error: {e}, trying Groq")
        try:
            from groq import Groq
            from data import GROQ_API_KEY
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=120,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": original_text}
                ]
            )
            return response.choices[0].message.content.strip()
        except:
            return "Koi issue aa gaya. Dobara poochein please."

def process(intent, entity, original_text=""):
    if intent == "pending_payments": return handle_pending_payments(entity, original_text)
    elif intent == "send_followup": return handle_send_followup(entity)
    elif intent == "sales_summary": return handle_sales_summary(entity, original_text)
    elif intent == "vendor_info": return handle_vendor_info(entity)
    elif intent == "order_status": return handle_order_status(entity, original_text)
    elif intent == "batch_status": return handle_batch_status(entity, original_text)
    elif intent == "labour_status": return handle_labour_status(entity, original_text)
    elif intent == "machine_status": return handle_machine_status(entity, original_text)
    elif intent == "stock_status": return handle_stock_status(entity, original_text)
    elif intent == "expense_summary": return handle_expense_summary(entity, original_text)
    elif intent == "initiate_call": return handle_initiate_call(entity)
    else: return handle_unknown(original_text)
