import io
import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, render_template_string, request, send_file
from google import genai
from google.genai import types
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

load_dotenv()
app = Flask(__name__)

# Never hard-code API keys. Set GEMINI_API_KEY in your environment or .env file.
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None
MODEL_CANDIDATES = [
    item.strip() for item in os.getenv(
        "GEMINI_MODELS", "gemini-3.5-flash,gemini-2.5-flash,gemini-2.0-flash"
    ).split(",") if item.strip()
]

# Demonstration inventory only. Replace with a verified live inventory before real use.
INVENTORY = [
    {"name": "Tourniquets", "stock": 12, "unit": "units", "keywords": ["tourniquet"]},
    {"name": "Haemostatic dressings", "stock": 3, "unit": "packs", "keywords": ["haemostatic", "hemostatic"]},
    {"name": "IV fluid kits", "stock": 20, "unit": "kits", "keywords": ["iv fluid", "intravenous fluid"]},
    {"name": "Oxygen kits", "stock": 2, "unit": "kits", "keywords": ["oxygen"]},
    {"name": "Trauma dressing kits", "stock": 8, "unit": "kits", "keywords": ["trauma dressing", "dressing kit"]},
    {"name": "Burn care kits", "stock": 5, "unit": "kits", "keywords": ["burn"]},
]

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MedPod-AI | Smart Emergency Response</title>
<link rel="icon" type="image/svg+xml"
href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23087e82'/%3E%3Cpath d='M32 10v44M10 32h44' stroke='white' stroke-width='9' stroke-linecap='round'/%3E%3C/svg%3E">

<style>
:root{
 --bg:#07141b;
 --panel:#0d2029;
 --panel2:#102934;
 --line:#1c3b47;
 --text:#eef8fa;
 --muted:#91aab3;
 --teal:#21d4c5;
 --teal-dark:#0b9f96;
 --red:#ff5964;
 --yellow:#f4c95d;
 --green:#45d483;
 --white:#fff;
}

*{box-sizing:border-box}

body{
 margin:0;
 background:
 radial-gradient(circle at 15% 0%,#123843 0,transparent 35%),
 radial-gradient(circle at 90% 20%,#10322f 0,transparent 30%),
 var(--bg);
 color:var(--text);
 font:15px/1.55 Inter,Segoe UI,Arial,sans-serif;
}

header{
 border-bottom:1px solid var(--line);
 background:rgba(7,20,27,.9);
 backdrop-filter:blur(12px);
 position:sticky;
 top:0;
 z-index:10;
}

.nav{
 max-width:1180px;
 margin:auto;
 padding:17px 22px;
 display:flex;
 align-items:center;
 justify-content:space-between;
 gap:20px;
}

.brand{
 display:flex;
 align-items:center;
 gap:12px;
}

.logo{
 width:40px;
 height:40px;
 border-radius:11px;
 background:linear-gradient(135deg,var(--teal),#087e82);
 display:flex;
 align-items:center;
 justify-content:center;
 color:#062126;
 font-weight:900;
 font-size:20px;
}

.brand-name{
 font-size:20px;
 font-weight:800;
 letter-spacing:.2px;
}

.brand-sub{
 font-size:11px;
 color:var(--muted);
}

.status{
 border:1px solid #23604f;
 background:#0c3029;
 color:var(--green);
 padding:6px 11px;
 border-radius:20px;
 font-size:11px;
 font-weight:700;
}

main{
 max-width:1180px;
 margin:35px auto;
 padding:0 22px;
}

.hero{
 display:flex;
 justify-content:space-between;
 align-items:flex-end;
 gap:25px;
 margin-bottom:30px;
}

.eyebrow{
 color:var(--teal);
 font-size:11px;
 font-weight:800;
 letter-spacing:1.5px;
 text-transform:uppercase;
 margin-bottom:7px;
}

h1{
 margin:0;
 font-size:36px;
 line-height:1.1;
 letter-spacing:-1px;
}

.hero p{
 color:var(--muted);
 max-width:650px;
 margin:10px 0 0;
}

.track{
 border:1px solid var(--line);
 background:var(--panel);
 padding:13px 16px;
 border-radius:12px;
 min-width:245px;
}

.track-label{
 font-size:10px;
 color:var(--muted);
 text-transform:uppercase;
 letter-spacing:1px;
}

.track strong{
 display:block;
 margin-top:3px;
 color:#dffaf7;
 font-size:13px;
}

.steps{
 display:grid;
 grid-template-columns:repeat(3,1fr);
 gap:12px;
 margin-bottom:20px;
}

.step{
 background:var(--panel);
 border:1px solid var(--line);
 border-radius:12px;
 padding:13px 15px;
 display:flex;
 align-items:center;
 gap:11px;
}

.step-num{
 width:30px;
 height:30px;
 border-radius:9px;
 background:#173640;
 color:var(--teal);
 display:flex;
 align-items:center;
 justify-content:center;
 font-size:11px;
 font-weight:800;
}

.step strong{
 display:block;
 font-size:13px;
}

.step span{
 color:var(--muted);
 font-size:11px;
}

.layout{
 display:grid;
 grid-template-columns:1.05fr .95fr;
 gap:18px;
}

.card{
 background:rgba(13,32,41,.94);
 border:1px solid var(--line);
 border-radius:16px;
 padding:22px;
 box-shadow:0 15px 40px rgba(0,0,0,.16);
}

.card-title{
 display:flex;
 justify-content:space-between;
 align-items:center;
 margin-bottom:18px;
}

.card-title h2{
 margin:0;
 font-size:17px;
}

.tag{
 background:#12363e;
 color:var(--teal);
 border-radius:20px;
 padding:4px 9px;
 font-size:10px;
 font-weight:800;
}

.field{
 margin-bottom:16px;
}

label{
 display:block;
 font-size:12px;
 font-weight:700;
 margin-bottom:7px;
 color:#d9e9ed;
}

input,textarea{
 width:100%;
 padding:12px 13px;
 border:1px solid #294651;
 border-radius:9px;
 background:#091a22;
 color:var(--text);
 font:inherit;
 outline:none;
}

input:focus,textarea:focus{
 border-color:var(--teal);
 box-shadow:0 0 0 3px rgba(33,212,197,.08);
}

textarea{
 min-height:150px;
 resize:vertical;
}

.hint{
 color:var(--muted);
 font-size:11px;
 margin-top:6px;
}

button,.btn{
 border:0;
 border-radius:9px;
 background:linear-gradient(135deg,var(--teal),var(--teal-dark));
 color:#03191d;
 padding:12px 18px;
 font-weight:800;
 font-size:13px;
 cursor:pointer;
 text-decoration:none;
 display:inline-block;
}

button:hover,.btn:hover{
 filter:brightness(1.08);
}

.inventory-grid{
 display:grid;
 grid-template-columns:1fr 1fr;
 gap:10px;
}

.inventory-item{
 background:#091b23;
 border:1px solid #1c3b46;
 border-radius:11px;
 padding:13px;
}

.inventory-name{
 font-size:12px;
 font-weight:700;
 margin-bottom:6px;
}

.inventory-bottom{
 display:flex;
 justify-content:space-between;
 align-items:center;
}

.stock{
 font-size:18px;
 font-weight:800;
}

.unit{
 color:var(--muted);
 font-size:10px;
}

.available{
 color:var(--green);
 font-size:10px;
 font-weight:800;
}

.low{
 color:var(--yellow);
 font-size:10px;
 font-weight:800;
}

.result{
 margin-top:18px;
}

.result-header{
 display:flex;
 justify-content:space-between;
 align-items:flex-start;
 gap:15px;
 border-bottom:1px solid var(--line);
 padding-bottom:17px;
 margin-bottom:17px;
}

.severity{
 background:#321b20;
 border:1px solid #70323b;
 color:#ff8990;
 border-radius:20px;
 padding:6px 11px;
 font-size:11px;
 font-weight:800;
}

.metrics{
 display:grid;
 grid-template-columns:repeat(3,1fr);
 gap:10px;
 margin:15px 0;
}

.metric{
 background:#091b23;
 border:1px solid #1c3b46;
 border-radius:10px;
 padding:13px;
}

.metric-label{
 color:var(--muted);
 font-size:10px;
 text-transform:uppercase;
}

.metric-value{
 font-size:21px;
 font-weight:800;
 margin-top:3px;
}

.report-section{
 margin-top:20px;
}

.report-section h3{
 font-size:13px;
 margin:0 0 9px;
}

.report-section p{
 color:#c9d9dd;
 margin:0;
}

.equipment{
 display:flex;
 flex-wrap:wrap;
 gap:7px;
}

.equipment span{
 background:#12343b;
 color:#bcefeb;
 border:1px solid #20545a;
 padding:6px 9px;
 border-radius:7px;
 font-size:11px;
}

.supply-table{
 width:100%;
 border-collapse:collapse;
 font-size:12px;
}

.supply-table th,
.supply-table td{
 text-align:left;
 padding:10px 7px;
 border-bottom:1px solid var(--line);
}

.supply-table th{
 color:var(--muted);
 font-size:10px;
 text-transform:uppercase;
}

.notmatched{
 color:var(--muted);
 font-weight:700;
}

.notice{
 margin-top:18px;
 padding:11px 13px;
 border:1px solid #66552b;
 background:#292516;
 color:#d8c891;
 border-radius:9px;
 font-size:11px;
}

.error{
 background:#35191d;
 border:1px solid #733139;
 color:#ff9ba1;
 border-radius:9px;
 padding:12px;
 margin-bottom:18px;
}

.actions{
 display:flex;
 flex-wrap:wrap;
 gap:9px;
 margin-top:20px;
}

.secondary{
 background:#18303a;
 color:#d9e9ed;
}

footer{
 max-width:1180px;
 margin:25px auto 35px;
 padding:0 22px;
 color:#607982;
 font-size:10px;
 text-align:center;
}

@media(max-width:800px){
 .hero{flex-direction:column;align-items:flex-start}
 .layout{grid-template-columns:1fr}
 .steps{grid-template-columns:1fr}
 .inventory-grid{grid-template-columns:1fr}
 h1{font-size:29px}
}

@media(max-width:500px){
 main{padding:0 13px}
 .nav{padding:14px}
 .metrics{grid-template-columns:1fr}
}
</style>
</head>

<body>

<header>
 <div class="nav">
  <div class="brand">
   <div class="logo">
    <svg viewBox="0 0 64 64" width="28" height="28"
         xmlns="http://www.w3.org/2000/svg">
        <path d="M32 10v44M10 32h44"
              stroke="white"
              stroke-width="9"
              stroke-linecap="round"
              fill="none"/>
    </svg>
</div>
   <div>
    <div class="brand-name">MedPod-AI</div>
    <div class="brand-sub">Emergency Intelligence Platform</div>
   </div>
  </div>
  <div class="status">● SYSTEM ONLINE</div>
 </div>
</header>

<main>

 <section class="hero">
  <div>
   <div class="eyebrow">Smart Health & Supply Chain Resilience</div>
   <h1>Emergency Response Intelligence</h1>
   <p>
    AI-assisted incident triage with resource identification and
    simulated supply availability analysis for rapid emergency response.
   </p>
  </div>

  <div class="track">
   <div class="track-label">Hackathon Track</div>
   <strong>Smart Health & Supply Chain Resilience</strong>
  </div>
 </section>

 <div class="steps">
  <div class="step">
   <div class="step-num">01</div>
   <div>
    <strong>Incident Intake</strong>
    <span>Capture emergency details</span>
   </div>
  </div>

  <div class="step">
   <div class="step-num">02</div>
   <div>
    <strong>Supply Resilience</strong>
    <span>Check required resources</span>
   </div>
  </div>

  <div class="step">
   <div class="step-num">03</div>
   <div>
    <strong>AI Triage Report</strong>
    <span>Generate response guidance</span>
   </div>
  </div>
 </div>

 {% if error %}
 <div class="error">{{ error }}</div>
 {% endif %}

 <div class="layout">

  <section class="card">

   <div class="card-title">
    <h2>Emergency Incident Intake</h2>
    <span class="tag">AI TRIAGE</span>
   </div>

   <form method="post" action="/triage">

    <div class="field">
     <label for="incident">INCIDENT DESCRIPTION *</label>
     <textarea
      id="incident"
      name="incident"
      required
      placeholder="Describe the incident, reported injuries and relevant circumstances..."
     >{{ incident or "" }}</textarea>
     <div class="hint">Use synthetic information for demonstration purposes.</div>
    </div>

    <div class="field">
     <label for="location">INCIDENT LOCATION</label>
     <input
      id="location"
      name="location"
      value="{{ location or '' }}"
      placeholder="e.g. Highway junction, Sector 4"
     >
    </div>

    <div class="field">
     <label for="people">PEOPLE AFFECTED</label>
     <input
      id="people"
      name="people"
      type="number"
      min="1"
      max="1000"
      value="{{ people or '' }}"
      placeholder="e.g. 2"
     >
    </div>

    <button type="submit">Generate AI Triage Report →</button>

   </form>

   <div class="notice">
    <strong>Prototype safety notice:</strong>
    MedPod-AI is a hackathon demonstration and is not a medical device,
    diagnostic system or emergency dispatch service.
   </div>

  </section>

  <section class="card">

   <div class="card-title">
    <h2>Supply Resilience Monitor</h2>
    <span class="tag">RESOURCE MONITOR</span>
   </div>

   <p style="color:var(--muted);font-size:11px;margin-top:-8px;margin-bottom:15px;">
    Resource availability monitor for emergency response planning.
</p>

   <div class="inventory-grid">

    {% for item in inventory %}
    <div class="inventory-item">
     <div class="inventory-name">{{ item.name }}</div>

     <div class="inventory-bottom">
      <div>
       <span class="stock">{{ item.stock }}</span>
       <span class="unit">{{ item.unit }}</span>
      </div>

      {% if item.stock <= 3 %}
      <span class="low">● LOW STOCK</span>
      {% else %}
      <span class="available">● AVAILABLE</span>
      {% endif %}
     </div>
    </div>
    {% endfor %}

   </div>

   <div class="notice">
    Inventory is simulated for the hackathon prototype and is not connected
    to a real hospital, warehouse or procurement system.
   </div>

  </section>

 </div>

 {% if result %}

 <section class="card result" id="generated-report">

  <div class="result-header">
   <div>
    <div class="eyebrow">Generated Response</div>
    <h2 style="margin:0;font-size:22px;">Emergency Intelligence Report</h2>
    <div style="color:var(--muted);font-size:11px;margin-top:4px;">
     Model: {{ model }}
    </div>
   </div>

   {% if result.severity %}
   <div class="severity">{{ result.severity }}</div>
   {% endif %}
  </div>

  <div class="metrics">

   <div class="metric">
    <div class="metric-label">Priority</div>
    <div class="metric-value">{{ result.severity or "Unclear" }}</div>
   </div>

   <div class="metric">
    <div class="metric-label">Resources Identified</div>
    <div class="metric-value">{{ equipment|length }}</div>
   </div>

   <div class="metric">
    <div class="metric-label">Supply Checks</div>
    <div class="metric-value">{{ stock_check|length }}</div>
   </div>

  </div>

  <div class="report-section">
   <h3>INCIDENT</h3>
   <p>{{ incident }}</p>
  </div>

  {% if location %}
  <div class="report-section">
   <h3>LOCATION</h3>
   <p>{{ location }}</p>
  </div>
  {% endif %}

  {% if people %}
  <div class="report-section">
   <h3>PEOPLE AFFECTED</h3>
   <p>{{ people }}</p>
  </div>
  {% endif %}

  {% if result.primary_injuries %}
  <div class="report-section">
   <h3>REPORTED / ASSESSED CONCERNS</h3>
   <p>{{ result.primary_injuries }}</p>
  </div>
  {% endif %}

  {% if equipment %}
  <div class="report-section">
   <h3>AI-IDENTIFIED RESOURCES</h3>
   <div class="equipment">
    {% for eq in equipment %}
    <span>{{ eq }}</span>
    {% endfor %}
   </div>
  </div>
  {% endif %}

  {% if result.dispatch_action %}
  <div class="report-section">
   <h3>SUGGESTED RESPONSE ACTION</h3>
   <p>{{ result.dispatch_action }}</p>
  </div>
  {% endif %}

  <div class="report-section">
   <h3>SUPPLY CHAIN RESILIENCE CHECK</h3>

   <table class="supply-table">
    <thead>
     <tr>
      <th>Requested Resource</th>
      <th>Inventory Match</th>
      <th>Status</th>
     </tr>
    </thead>

    <tbody>
     {% for row in stock_check %}
     <tr>
      <td>{{ row.requested }}</td>
      <td>{{ row.match }}</td>
      <td>
       {% if row.status == 'Low stock' %}
       <span class="low">LOW STOCK</span>
       {% elif row.status == 'Available' %}
       <span class="available">AVAILABLE</span>
       {% else %}
       <span class="notmatched">NOT MATCHED</span>
       {% endif %}
      </td>
     </tr>
     {% endfor %}
    </tbody>
   </table>
  </div>

  <div class="actions">

   <form method="post" action="/report.pdf">
    <input type="hidden" name="payload" value="{{ pdf_payload }}">
    <button type="submit">↓ Download PDF Report</button>
   </form>

   <button class="secondary" type="button" onclick="window.print()">
    Print / Save Report
   </button>

  </div>

  <div class="notice">
   AI-generated output and simulated inventory matches require qualified
   human review. They do not authorize treatment, procurement or dispatch.
  </div>

 </section>

 {% endif %}

</main>

<footer>
 MedPod-AI · Hackathon Prototype · AI-assisted Emergency Triage &
 Supply Chain Resilience
</footer>

{% if result %}
<script>
document.addEventListener("DOMContentLoaded", function () {
    const report = document.getElementById("generated-report");
    if (report) {
        setTimeout(function () {
            report.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }, 200);
    }
});
</script>
{% endif %}

</body>
</html>
"""

def parse_equipment(value):
    if isinstance(value, list):
        return [str(x) for x in value]
    if value is None:
        return []
    return [str(value)]

def check_inventory(equipment):
    rows = []
    for requested in equipment:
        text = requested.lower()
        match = next((item for item in INVENTORY
                      if item["name"].lower() in text
                      or any(keyword in text for keyword in item["keywords"])), None)
        if match:
            rows.append({
                "requested": requested,
                "match": f'{match["name"]} ({match["stock"]} {match["unit"]})',
                "status": "Low stock" if match["stock"] <= 3 else "Available"
            })
        else:
            rows.append({"requested": requested, "match": "No inventory mapping", "status": "Not matched"})
    return rows

def make_pdf(payload):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SmallNote", parent=styles["BodyText"], fontSize=8, leading=11, textColor=colors.HexColor("#555555")))
    story = [Paragraph("MedPod-AI Emergency & Supply Report", styles["Title"]), Spacer(1, 5*mm)]
    story.append(Paragraph(f'Generated: {payload.get("generated_at","")}', styles["SmallNote"]))
    story.append(Spacer(1, 4*mm))
    for label, value in [("Incident", payload.get("incident","")), ("Location", payload.get("location","Not provided")), ("People affected", payload.get("people","Not provided"))]:
        story.append(Paragraph(f"<b>{label}:</b> {str(value).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')}", styles["BodyText"]))
        story.append(Spacer(1, 2*mm))
    result = payload.get("result", {})
    for key, label in [("severity","AI-assessed severity"),("primary_injuries","Primary injuries / concerns"),("dispatch_action","Suggested dispatch action")]:
        if result.get(key):
            value = str(result[key]).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            story.append(Paragraph(f"<b>{label}:</b> {value}", styles["BodyText"]))
            story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Suggested equipment", styles["Heading2"]))
    equipment = payload.get("equipment", [])
    story.append(Paragraph("• " + "<br/>• ".join(str(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;") for x in equipment) if equipment else "Not specified", styles["BodyText"]))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Demonstration inventory check", styles["Heading2"]))
    data = [["Suggested resource", "Inventory match", "Status"]]
    for row in payload.get("stock_check", []):
        data.append([row["requested"], row["match"], row["status"]])
    table = Table(data, repeatRows=1, colWidths=[58*mm, 65*mm, 35*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e7f5f4")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#17343c")),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8),
        ("GRID",(0,0),(-1,-1),.4,colors.HexColor("#ccd8dc")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6)
    ]))
    story.extend([table, Spacer(1, 5*mm), Paragraph(
        "IMPORTANT: AI-generated demonstration output only. Not a medical diagnosis, treatment instruction, "
        "verified inventory record, or dispatch authorization. Seek qualified clinical review and contact "
        "local emergency services for real emergencies.", styles["SmallNote"])])
    doc.build(story)
    buffer.seek(0)
    return buffer

@app.route("/", methods=["GET"])
def home():
    return render_template_string(PAGE, inventory=INVENTORY, result=None, error=None,
                                  incident="", location="", people="")

@app.route("/triage", methods=["POST"])
def triage():
    incident = (request.form.get("incident") or "").strip()
    location = (request.form.get("location") or "").strip()
    people = (request.form.get("people") or "").strip()
    if not incident:
        return render_template_string(PAGE, inventory=INVENTORY, result=None,
                                      error="Please enter an incident description.",
                                      incident=incident, location=location, people=people), 400
    if not client:
        return render_template_string(PAGE, inventory=INVENTORY, result=None,
                                      error="GEMINI_API_KEY is not configured. Add it to your .env file and restart.",
                                      incident=incident, location=location, people=people), 500
    prompt = f"""You are supporting an emergency-response demonstration. This is not a medical device.
Analyze the incident text and return ONLY valid JSON with exactly these keys:
severity, primary_injuries, required_equipment, dispatch_action.
severity must be one of P1-Critical, P2-Urgent, P3-Stable, or Unclear.
primary_injuries should be a short string. required_equipment must be an array of short strings.
dispatch_action should be a cautious, non-authoritative suggestion for qualified human review.
Do not invent patient facts. If details are insufficient, say so and recommend contacting emergency services.
Incident: {incident}
Location: {location or "Not provided"}
People affected: {people or "Not provided"}"""
    last_error = None
    for model_name in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model_name, contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            result = json.loads(response.text or "{}")
            equipment = parse_equipment(result.get("required_equipment"))
            stock_check = check_inventory(equipment)
            payload = {
                "incident": incident, "location": location, "people": people,
                "result": result, "equipment": equipment, "stock_check": stock_check,
                "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                "model": model_name
            }
            return render_template_string(PAGE, inventory=INVENTORY, result=result,
                                          model=model_name, equipment=equipment,
                                          stock_check=stock_check,
                                          pdf_payload=json.dumps(payload),
                                          error=None, incident=incident,
                                          location=location, people=people)
        except Exception as exc:
            last_error = str(exc)
    return render_template_string(PAGE, inventory=INVENTORY, result=None,
                                  error=f"Gemini request failed for the configured models: {last_error}",
                                  incident=incident, location=location, people=people), 502

@app.route("/report.pdf", methods=["POST"])
def report_pdf():
    try:
        payload = json.loads(request.form.get("payload", "{}"))
        pdf = make_pdf(payload)
        return send_file(pdf, mimetype="application/pdf", as_attachment=True,
                         download_name="medpod-ai-emergency-report.pdf")
    except Exception:
        return "Could not generate the PDF. Please generate the report again.", 400

@app.route("/health", methods=["GET"])
def health():
    return {"status": "online", "project": "MedPod-AI Triage Engine"}

if __name__ == "__main__":
    app.run(debug=False, port=5000)
