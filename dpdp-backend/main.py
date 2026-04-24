from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

import os
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from services.scoring_engine import analyze_compliance
from services.report_generator import generate_pdf_report


app = FastAPI(title="DPDP Compliance Checker API")

LAST_REPORT_PATH = None

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ensure reports folder exists
if not os.path.exists("reports"):
    os.makedirs("reports")


# Serve generated files (charts, reports)
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# Serve frontend static files when available
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


# ==========================
# Root Route - API Status
# ==========================
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "DPDP Compliance Checker API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze_policy": "/analyze-policy",
            "analyze_url": "/analyze-url",
            "download_report": "/download-report",
            "reports_history": "/reports-history"
        }
    }


# ==========================
# Analyze Privacy Policy (File Upload)
# ==========================
@app.post("/analyze-policy")
async def analyze_policy(file: UploadFile = File(...)):

    # Read uploaded file
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    # Run AI compliance analysis
    result = analyze_compliance(text)

    # Save Report History
    save_report(file.filename, result)

    # Generate and save PDF report
    global LAST_REPORT_PATH
    LAST_REPORT_PATH = generate_pdf_report(result, file.filename)

    return result


# ==========================
# URL Input Model
# ==========================
class URLRequest(BaseModel):
    url: str


# ==========================
# Analyze Privacy Policy from URL
# ==========================
@app.post("/analyze-url")
def analyze_url(data: URLRequest):

    try:
        response = requests.get(
            data.url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            },
            timeout=15,
        )

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Failed to fetch URL: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract main policy content
        policy_section = soup.find("main") or soup.find("article") or soup.find("div")

        if policy_section:
            text = policy_section.get_text(separator=" ")
        else:
            text = soup.get_text(separator=" ")

        # Run AI analysis
        result = analyze_compliance(text)

        save_report(data.url, result)

        global LAST_REPORT_PATH
        LAST_REPORT_PATH = generate_pdf_report(result, data.url)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================
# Legacy compatibility route
# ==========================
@app.post("/check-compliance/")
async def check_compliance(website_url: str = Form(...)):
    """Compatibility alias for legacy frontend or external clients."""
    return analyze_url(URLRequest(url=website_url))


# ==========================
# Save Report History
# ==========================
def save_report(source, result):

    report = {
        "filename": source,
        "score": result["overall_score"],
        "risk": result["risk_level"],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    reports_file = "reports/report_history.json"

    if os.path.exists(reports_file):
        with open(reports_file, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(report)

    with open(reports_file, "w") as f:
        json.dump(history, f, indent=2)


# ==========================
# Download PDF Report
# ==========================
@app.get("/download-report")
def download_report():
    global LAST_REPORT_PATH
    if LAST_REPORT_PATH and os.path.exists(LAST_REPORT_PATH):
        return FileResponse(
            LAST_REPORT_PATH,
            media_type="application/pdf",
            filename="dpdp_compliance_report.pdf"
        )
    raise HTTPException(status_code=404, detail="Report not found.")


# ==========================
# Get Report History
# ==========================
@app.get("/reports-history")
def get_reports():

    reports_file = "reports/report_history.json"

    if not os.path.exists(reports_file):
        return []

    with open(reports_file, "r") as f:
        history = json.load(f)

    return history


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# ==========================
# Alias for history endpoint
# ==========================
@app.get("/history/")
def get_history():
    """Alias endpoint for /reports-history for frontend compatibility"""
    reports_file = "reports/report_history.json"
    
    if not os.path.exists(reports_file):
        return []
    
    try:
        with open(reports_file, "r") as f:
            history = json.load(f)
        return history
    except Exception as e:
        print(f"Error reading history: {e}")
        return []


# ==========================
# Export compliance history to CSV
# ==========================
@app.get("/export-csv/")
def export_csv():
    """Export compliance history as CSV file"""
    import csv
    from io import StringIO
    
    reports_file = "reports/report_history.json"
    
    if not os.path.exists(reports_file):
        return {"error": "No history to export"}
    
    try:
        with open(reports_file, "r") as f:
            history = json.load(f)
        
        # Create CSV content
        output = StringIO()
        if history:
            writer = csv.DictWriter(output, fieldnames=history[0].keys())
            writer.writeheader()
            for record in history:
                writer.writerow(record)
        
        csv_content = output.getvalue()
        
        return {
            "filename": f"compliance-history-{datetime.now().strftime('%Y-%m-%d')}.csv",
            "content": csv_content
        }
    except Exception as e:
        return {"error": f"Failed to export CSV: {str(e)}"}
