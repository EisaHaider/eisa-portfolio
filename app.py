import os
import json
from html import escape
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import Flask, jsonify, render_template, request


from dotenv import load_dotenv  # استيراد المكتبة
load_dotenv()  # تحميل المتغيرات من ملف .env
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/contact")
def contact():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"ok": False, "message": "Missing required fields."}), 400

    # القراءة السليمة من متغيرات البيئة
    resend_api_key = os.environ.get("RESEND_API_KEY")
    mail_to = os.environ.get("CONTACT_EMAIL", "kuwait10@msn.com")
    mail_from = os.environ.get("RESEND_FROM", "onboarding@resend.dev")

    if not resend_api_key:
        return jsonify({"ok": False, "message": "Email service is not configured."}), 500

    safe_name = escape(name)
    safe_email = escape(email)
    safe_phone = escape(phone or "Not provided")
    safe_message = escape(message).replace("\n", "<br>")

    html = (
        f"<p><strong>Name:</strong> {safe_name}</p>"
        f"<p><strong>Email:</strong> {safe_email}</p>"
        f"<p><strong>Phone:</strong> {safe_phone}</p>"
        f"<hr>"
        f"<p>{safe_message}</p>"
    )

    payload = {
        "from": mail_from,
        "to": [mail_to],
        "reply_to": [email],
        "subject": f"Portfolio Inquiry: {safe_name}",
        "html": html,
    }

    request_data = json.dumps(payload).encode("utf-8")

    resend_request = Request(
        "https://api.resend.com/emails",
        data=request_data,
        headers={
            "Authorization": f"Bearer {resend_api_key.strip()}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        },
        method="POST",
    )

    try:
        with urlopen(resend_request, timeout=15) as response:
            if response.status >= 400:
                raise RuntimeError(f"Resend returned status {response.status}")
    except HTTPError as e:
        error_response = e.read().decode("utf-8")
        app.logger.error(f"Resend API Error ({e.code}): {error_response}")
        return jsonify({"ok": False, "message": f"Resend Error: {error_response}"}), 500
    except (URLError, RuntimeError) as e:
        app.logger.exception("Failed to send contact form email")
        return jsonify({"ok": False, "message": "Message could not be sent."}), 500

    return jsonify({"ok": True, "message": "Message sent successfully."})


if __name__ == "__main__":
    app.run(debug=True)