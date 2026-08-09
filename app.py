import os
import json
from datetime import date
from html import escape
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import Flask, Response, jsonify, redirect, render_template, request, url_for


from dotenv import load_dotenv  # استيراد المكتبة
load_dotenv()  # تحميل المتغيرات من ملف .env
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


def canonical_url(path="/"):
    if not path.startswith("/"):
        path = f"/{path}"

    site_url = os.environ.get("SITE_URL", "").strip().rstrip("/")
    if site_url:
        return f"{site_url}{path}"

    return f"{request.url_root.rstrip('/')}{path}"


@app.get("/sitemap.xml")
def sitemap():
    lastmod = os.environ.get("SITEMAP_LASTMOD", date.today().isoformat())
    pages = [
        {
            "loc": canonical_url("/"),
            "lastmod": lastmod,
            "changefreq": "monthly",
            "priority": "1.0",
        }
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        xml.append("  <url>")
        xml.append(f"    <loc>{escape(page['loc'])}</loc>")
        xml.append(f"    <lastmod>{page['lastmod']}</lastmod>")
        xml.append(f"    <changefreq>{page['changefreq']}</changefreq>")
        xml.append(f"    <priority>{page['priority']}</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")

    return Response("\n".join(xml), mimetype="application/xml")


@app.get("/robots.txt")
def robots():
    content = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {canonical_url('/sitemap.xml')}\n"
    )

    return Response(content, mimetype="text/plain")


@app.get("/whatsapp")
def whatsapp():
    whatsapp_url = os.environ.get("WHATSAPP_URL")
    if not whatsapp_url:
        return redirect("/")

    return redirect(whatsapp_url)


@app.post("/contact")
def contact():
    data = request.get_json(silent=True) if request.is_json else request.form
    data = data or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    message = (data.get("message") or "").strip()

    def contact_response(payload, status=200):
        if request.is_json:
            return jsonify(payload), status

        heading = "Message Sent" if payload.get("ok") else "Message Not Sent"
        text = escape(payload.get("message", ""))
        return (
            "<!doctype html>"
            "<html lang='en' dir='ltr'>"
            "<head>"
            "<meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>{heading} | Eisa Haider</title>"
            "<style>"
            "body{margin:0;min-height:100vh;display:grid;place-items:center;"
            "font-family:system-ui,-apple-system,Segoe UI,sans-serif;"
            "background:#0f172a;color:#fff;padding:24px}"
            "main{max-width:520px;border:1px solid #334155;border-radius:18px;"
            "padding:28px;background:#111827}"
            "a{color:#60a5fa}"
            "</style>"
            "</head>"
            "<body>"
            f"<main><h1>{heading}</h1><p>{text}</p>"
            "<p><a href='/#contact'>Back to contact</a></p></main>"
            "</body></html>"
        ), status

    if not name or not email or not message:
        return contact_response({"ok": False, "message": "Missing required fields."}, 400)

    # القراءة السليمة من متغيرات البيئة
    resend_api_key = os.environ.get("RESEND_API_KEY")
    mail_to = os.environ.get("CONTACT_EMAIL", "kuwait10@msn.com")
    mail_from = os.environ.get("RESEND_FROM", "onboarding@resend.dev")

    if not resend_api_key:
        return contact_response({"ok": False, "message": "Email service is not configured."}, 500)

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
        return contact_response({"ok": False, "message": "Message could not be sent."}, 500)
    except (URLError, RuntimeError) as e:
        app.logger.exception("Failed to send contact form email")
        return contact_response({"ok": False, "message": "Message could not be sent."}, 500)

    return contact_response({"ok": True, "message": "Message sent successfully."})


if __name__ == "__main__":
    # هذا الجزء سيُنفذ فقط عند التشغيل المحلي المباشر عبر (python app.py)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
