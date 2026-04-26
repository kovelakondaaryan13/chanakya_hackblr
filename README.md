# Chanakya — AI Copilot for Indian Factory Owners

> Every king had a Chanakya. Every MSME owner has been ruling alone — until now.

Built for HackBlr 2026 · PS-1 Voice-First Knowledge & Workflow Agent

---

## Please ReadMe

This is a fully working voice AI agent. You can talk to it right now using the live Vapi assistant, or set it up yourself from scratch using the instructions below. Every question listed at the bottom of this file has a correct, tested answer.

---

## Live Demo (No Setup Needed)

Backend is already deployed and live:
https://web-production-478c6.up.railway.app

To test instantly — go to the Vapi dashboard, create an assistant using the config below, and click Talk.

---

## What is Chanakya?

Chanakya is a voice-first AI copilot for Indian MSME factory owners. The owner speaks in English or Hinglish. Chanakya responds with real business data — pending payments, production orders, factory floor status, labour attendance, machine health, stock alerts, expenses — all in natural spoken English.

Demo factory: **Sarvoday Textiles, Kolhapur, Maharashtra**

---

## Tech Stack

| Layer | Tool | Role |
|---|---|---|
| Voice I/O | Vapi (Custom LLM mode) | Speech to text, text to speech |
| Intent Classification | Groq llama-3.1-8b-instant | Understands English and Hinglish queries |
| Vector Store | Qdrant Cloud | 77 business documents, semantic search |
| Backend | FastAPI on Railway | Webhook + Custom LLM endpoint |
| Data | Python (data.py) | Mock MSME factory dataset |

---

## Setup Instructions

### Step 1 — Clone and install

```bash
git clone https://github.com/kovelakondaaryan13/chanakya_hackblr
cd chanakya_hackblr
pip install -r requirements.txt
```

### Step 2 — Load data into Qdrant

```bash
python qdrant_setup.py
```

Should print: `Loaded 77 documents into Qdrant`

### Step 3 — Run the backend

```bash
uvicorn main:app --reload --port 8000
```

Test it:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "how much payment is pending today"}'
```

Expected response: Total pending payments across 10 vendors with top 3 overdue.

### Step 4 — Expose locally with ngrok (for Vapi)

```bash
ngrok http 8000
```

Copy the https URL — you will need it in the Vapi setup below.

---

## Vapi Setup Instructions

Follow these steps exactly to connect Chanakya to Vapi.

### Step 1 — Create a Vapi account
Go to [vapi.ai](https://vapi.ai) and sign up. You get $10 free credits — more than enough to test.

### Step 2 — Create a new Assistant
Go to Assistants → Create Assistant → start from blank template.

### Step 3 — Model tab settings

| Field | Value |
|---|---|
| Provider | Custom LLM |
| Custom LLM URL | `https://web-production-478c6.up.railway.app/vapi-llm` |
| Model name | `chanakya` |
| First Message Mode | Assistant speaks first |
| First Message | `Namaste! I am Chanakya — your factory copilot for Sarvoday Textiles. Today Max Fabrics has 1 lakh 85 thousand rupees overdue, 3 materials are on stock alert, and 2 orders are ready to dispatch. What would you like to check?` |
| System Prompt | `You are Chanakya, AI copilot for Sarvoday Textiles. Answer in clear English. Be concise and specific.` |
| Max Tokens | 250 |

> If running locally, replace the Custom LLM URL with your ngrok URL + `/vapi-llm`
> Example: `https://abc123.ngrok-free.app/vapi-llm`

### Step 4 — Voice tab settings

| Field | Value |
|---|---|
| Provider | 11labs |
| Voice | Any clear male Indian-accented voice (e.g. Aditya) |
| Speed | 0.9 |
| Stability | 0.5 |
| Clarity + Similarity | 0.75 |
| Optimize Streaming Latency | On |
| Speaker Boost | On |

### Step 5 — Advanced tab settings

| Field | Value |
|---|---|
| Server URL | `https://web-production-478c6.up.railway.app/vapi-webhook` |
| Server Timeout | 30 seconds |

### Step 6 — Save and Test

Click Save. Then click the green Talk button at the top right. Speak any question from the list below.

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check |
| `/chat` | POST | Direct text test — takes `{"text": "..."}` |
| `/vapi-llm` | POST | Vapi Custom LLM endpoint |
| `/vapi-llm/chat/completions` | POST | OpenAI-compatible endpoint |
| `/vapi-webhook` | POST | Vapi webhook handler |

---

## Every Question You Can Ask

All of these have been tested and return correct answers.

### Payments
- How much payment is pending today?
- Who owes us the most money?
- What is Crown Textiles pending amount?
- How long has Max Fabrics been overdue?
- What is Atlas Machinery pending amount?
- What is Blue Star Dyes pending amount?
- What is Prime Yarns pending amount?
- Total outstanding amount?

### Follow-up Actions
- Send a follow-up to Max Fabrics
- Send a follow-up to Crown Textiles
- Send a follow-up to Atlas Machinery
- Send a follow-up to Blue Star Dyes
- Send a follow-up to Prime Yarns
- Send a follow-up to Royal Threads
- Send a follow-up to Metro Chemicals
- Send a follow-up to Eagle Exports
- Send a follow-up to Global Sizing
- Send a follow-up to Star Traders

### Sales
- What are today's sales?
- How much did we sell on Monday?
- How much did we sell on Wednesday?
- How much did we sell on Friday?
- What was our best day this week?
- What is our top selling fabric?
- How many orders were completed today?

### Orders
- Which orders are ready to dispatch?
- Which orders are high priority?
- Which order is due soonest?
- How many orders are in production?
- What is the status of the Reliance Retail order?
- What is the status of the Raymond Limited order?
- What is the status of the Arvind Mills order?
- What is the status of the Welspun India order?
- What is the status of the Vardhman Textiles order?
- What is the status of the Dollar Industries order?
- What is the status of the Monte Carlo order?
- What is the status of the Bombay Dyeing order?

### Factory Floor and Batches
- Which batch is almost complete?
- How much has Loom 07 produced?
- How much has Loom 03 produced?
- How much has Loom 02 produced?
- What is the status of Batch 041?
- What is the status of Batch 042?
- What is the status of Batch 043?

### Machines
- Which machines are stopped?
- Is Loom 01 running?
- Is Loom 03 running?
- Is Loom 04 running?
- Is Loom 05 running?
- Is Loom 06 running?
- Is Dyeing unit 01 running?
- Is Dyeing unit 02 running?
- What is the efficiency of Loom 04?
- What is the efficiency of Dyeing unit 02?
- Which machine has the lowest efficiency?
- When was Loom 03 last serviced?
- When was Loom 01 last serviced?
- Who operates Loom 06?
- Who operates Dyeing unit 01?

### Labour and Attendance
- How many workers came today?
- Who is absent today?
- Who took half day today?
- How much salary is due this month?
- How many workers are on morning shift?
- Who is the supervisor?
- What is Ravi Kumar's attendance?
- What is Priya Sharma's attendance?
- What is Rajesh Nair's attendance?
- What is Neha Kulkarni's attendance?
- What is Sanjay Pawar's attendance?

### Raw Material and Stock
- Which materials are running low?
- How much Cotton Yarn is left?
- How much Polyester Fibre is left?
- How many days will Red Dye last?
- How many days will Blue Dye last?
- How many days will Sizing Chemical last?
- Is Blue Dye stock okay?
- What needs urgent reorder?

### Expenses
- How much did we spend this week?
- What was our biggest expense?
- How much did we spend on maintenance?
- What was the electricity bill?
- How much did labour cost this week?
- How much did we spend on transport?
- How much did we spend on raw material?
- Who approved the most expenses?

### Vendor Info
- What is Max Fabrics contact number?
- What is Crown Textiles contact number?
- What is Atlas Machinery contact number?
- What is Blue Star Dyes contact number?
- What is Prime Yarns contact number?

### Open Ended
- Should I be worried about anything today?
- What needs my attention right now?
- Give me a summary of the factory today
- Any urgent issues today?
- Thank you Chanakya

---

## About

Built by **Aryan Kovelakonda**, founder of **Svayantra Tech** — building India's first AI-native ERP for ops and management.

Chanakya is not a hackathon side project. It is the voice interface layer of Svayantra, built in one night as a live demo of what the full platform can do. Every intent — payments, machines, labour, stock — is a module that exists in the product. The voice layer is the add-on that ties it all together.

**Chanakya — Every king had one. Now every MSME owner can.**
