from flask import Flask, redirect, render_template, request
from user_agents import parse

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    error = ""
    user_agent_string = ""
    ua_string = ""
    ua_short = ""
    browser_data = ""
    os_data = ""
    device_data = ""
    extra_data = ""

    if request.method == 'POST':
        user_agent_string = request.form['user_agent']
        if len(user_agent_string) == 0:
            error = "Please enter a user agent string!"
        else:
            ua_string = parse(user_agent_string)
            #ua_short = str(ua_string)
            browser_data = str(ua_string.browser.family) + " " + str(ua_string.browser.version_string)
            os_data = str(ua_string.os.family) + " " + str(ua_string.os.version_string)
            device_data = str(ua_string.device.brand) + " " + str(ua_string.device.family) + " (" + str(ua_string.device.model) + ")"

            if "IE" in str(ua_string.browser.family):
                extra_data = "Internet Explorer is not supported, please use a modern browser."
            elif "Safari" not in str(ua_string.browser.family) and "ios" in str(ua_string.os.family.lower()):
                extra_data = "Only Safari browser is supported on iOS, other browsers do not have WebRTC capability."

    return render_template("index.html", message=error, browser = browser_data, os = os_data, device = device_data, extra = extra_data)


