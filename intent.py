from groq import Groq
import json
from data import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM = """You are an intent classifier for a voice assistant for an Indian textile factory.
Return ONLY valid JSON. No explanation. No markdown. No backticks.
Format: {"intent": "...", "entity": "..."}
Intents: pending_payments, send_followup, sales_summary, vendor_info, order_status, batch_status, labour_status, machine_status, stock_status, expense_summary, initiate_call, unknown
Entity is the specific name, ID, day, or material mentioned. Use null if none.

"how much payment is pending" -> {"intent": "pending_payments", "entity": null}
"who owes us the most" -> {"intent": "pending_payments", "entity": null}
"how long has Max Fabrics been overdue" -> {"intent": "pending_payments", "entity": "Max Fabrics"}
"what is Crown Textiles pending amount" -> {"intent": "pending_payments", "entity": "Crown Textiles"}
"send a follow-up to Crown Textiles" -> {"intent": "send_followup", "entity": "Crown Textiles"}
"send a reminder to Atlas Machinery" -> {"intent": "send_followup", "entity": "Atlas Machinery"}
"what are today's sales" -> {"intent": "sales_summary", "entity": "today"}
"how much did we sell on Friday" -> {"intent": "sales_summary", "entity": "Friday"}
"what was our best day this week" -> {"intent": "sales_summary", "entity": null}
"what is our top selling fabric" -> {"intent": "sales_summary", "entity": null}
"which orders are ready to dispatch" -> {"intent": "order_status", "entity": null}
"what is the status of Reliance Retail order" -> {"intent": "order_status", "entity": "Reliance Retail"}
"which orders are high priority" -> {"intent": "order_status", "entity": null}
"which order is due soonest" -> {"intent": "order_status", "entity": null}
"how many orders are in production" -> {"intent": "order_status", "entity": null}
"is Loom 07 running" -> {"intent": "batch_status", "entity": "LOOM-07"}
"is Loom 5 running" -> {"intent": "batch_status", "entity": "LOOM-05"}
"which batch is almost complete" -> {"intent": "batch_status", "entity": null}
"how much has Loom 07 produced" -> {"intent": "batch_status", "entity": "LOOM-07"}
"how many workers came today" -> {"intent": "labour_status", "entity": null}
"who is absent today" -> {"intent": "labour_status", "entity": null}
"who took half day today" -> {"intent": "labour_status", "entity": null}
"how much salary is due" -> {"intent": "labour_status", "entity": null}
"who is the supervisor" -> {"intent": "labour_status", "entity": null}
"how many workers on morning shift" -> {"intent": "labour_status", "entity": null}
"which machines are stopped" -> {"intent": "machine_status", "entity": null}
"is Loom 05 running" -> {"intent": "machine_status", "entity": "LOOM-05"}
"what is the efficiency of Loom 04" -> {"intent": "machine_status", "entity": "LOOM-04"}
"when was Loom 03 last serviced" -> {"intent": "machine_status", "entity": "LOOM-03"}
"who operates Loom 06" -> {"intent": "machine_status", "entity": "LOOM-06"}
"which machine has lowest efficiency" -> {"intent": "machine_status", "entity": null}
"how much cotton yarn is left" -> {"intent": "stock_status", "entity": "Cotton Yarn"}
"which materials are running low" -> {"intent": "stock_status", "entity": null}
"how many days will Red Dye last" -> {"intent": "stock_status", "entity": "Red Dye"}
"is Blue Dye stock okay" -> {"intent": "stock_status", "entity": "Blue Dye"}
"what needs urgent reorder" -> {"intent": "stock_status", "entity": null}
"place an order for materials" -> {"intent": "stock_status", "entity": null}
"how much did we spend this week" -> {"intent": "expense_summary", "entity": null}
"what was our biggest expense" -> {"intent": "expense_summary", "entity": null}
"how much did we spend on maintenance" -> {"intent": "expense_summary", "entity": "maintenance"}
"what was the electricity bill" -> {"intent": "expense_summary", "entity": "electricity"}
"how much did labour cost" -> {"intent": "expense_summary", "entity": "labour"}
"who approved the most expenses" -> {"intent": "expense_summary", "entity": null}
"should I be worried about anything" -> {"intent": "unknown", "entity": null}
"give me a summary of the factory" -> {"intent": "unknown", "entity": null}
"what needs my attention today" -> {"intent": "unknown", "entity": null}
"thank you" -> {"intent": "unknown", "entity": null}
"how much payment is pending today" -> {"intent": "pending_payments", "entity": null}
"how much is pending today" -> {"intent": "pending_payments", "entity": null}
"total pending today" -> {"intent": "pending_payments", "entity": null}
"pending payments today" -> {"intent": "pending_payments", "entity": null}
"call Crown Textiles" -> {"intent": "initiate_call", "entity": "Crown Textiles"}
"call Max Fabrics" -> {"intent": "initiate_call", "entity": "Max Fabrics"}
"call Atlas Machinery" -> {"intent": "initiate_call", "entity": "Atlas Machinery"}
"make a call to the vendor" -> {"intent": "initiate_call", "entity": null}
"call them" -> {"intent": "initiate_call", "entity": null}"""

def parse_intent(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=100,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": text}
            ]
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Intent error: {e}")
        return {"intent": "unknown", "entity": None}
