import json, os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EVENT_FILE = os.path.join(DATA_DIR, "events.json")
REPORT_FILE = "/var/log/ids_report.pdf"

os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------
# Add Event (for Dashboard)
# -------------------------
def add_event(level, msg):
    event = {
        "time": str(datetime.now()),
        "level": level,
        "message": msg
    }

    if not os.path.exists(EVENT_FILE):
        with open(EVENT_FILE, "w") as f:
            json.dump([], f)

    with open(EVENT_FILE, "r+") as f:
        try:
            data = json.load(f)
        except:
            data = []

        data.append(event)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

# -------------------------
# Generate PDF Report
# -------------------------
def generate_report():
    if not os.path.exists(EVENT_FILE):
        return

    with open(EVENT_FILE) as f:
        events = json.load(f)

    doc = SimpleDocTemplate(REPORT_FILE, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>Intrusion Detection System Report</b>", styles["Title"]))
    content.append(Paragraph(f"Generated at: {datetime.now()}", styles["Normal"]))
    content.append(Paragraph("<br/>", styles["Normal"]))

    for e in events:
        line = f"{e['time']} | {e['level']} | {e['message']}"
        content.append(Paragraph(line, styles["Normal"]))

    doc.build(content)
