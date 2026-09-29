import requests

url = "http://127.0.0.1:5000/api/triage"
payload = {
    "report": (
        "Major collision on NH-27 near Guwahati bypass, heavy traffic,"
        " unconscious passenger with severe bleeding."
    )
}

print("Sending emergency report to Gemini AI Triage Engine...")
response = requests.post(url, json=payload)
print("\nResponse from Server:")
print(response.json())