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
    browser_advice = ""
    
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
            
            #check specific scenarios
            if "Safari" not in str(ua_string.browser.family) and "ios" in str(ua_string.os.family.lower()):
                extra_data = "Only Safari is supported on iOS, other browsers do not have WebRTC capability."
            
            # gneral browser version checks
            if "Safari" in str(ua_string.browser.family) and "ios" in str(ua_string.os.family.lower()):
                if float(ua_string.browser.version_string[0:3]) < 11.2:
                    extra_data = "Minimum Safari version for iOS is v11.2 (https://docs.pexip.com/admin/interoperability.htm?Highlight=interoperability#browser)"
            elif "Safari" in str(ua_string.browser.family) and "Mac" in str(ua_string.os.family.lower()):
                if float(ua_string.browser.version_string[0:3]) < 11.1:
                    extra_data = "Minimum Safari version is v11.1 (https://docs.pexip.com/admin/interoperability.htm?Highlight=interoperability#browser)"
            elif "Chrome" in str(ua_string.browser.family):
                if float(ua_string.browser.version_string[0:3]) < 61:
                    browser_advice = "Minimum Chrome version is v61 (https://docs.pexip.com/admin/interoperability.htm?Highlight=interoperability#browser)"
            elif "Firefox" in str(ua_string.browser.family):
                if float(ua_string.browser.version_string[0:3]) < 68:
                    browser_advice = "Minimum Firefox version is v68 (https://docs.pexip.com/admin/interoperability.htm?Highlight=interoperability#browser)"
            elif "Edge" in str(ua_string.browser.family):
                if float(ua_string.browser.version_string[0:3]) < 41:
                    browser_advice = "Minimum Edge version is v41, Chromium or HTML versions (https://docs.pexip.com/admin/interoperability.htm?Highlight=interoperability#browser)"
            elif "Opera" in str(ua_string.browser.family):
                if float(ua_string.browser.version_string[0:3]) < 53:
                    browser_advice = "Minimum Opera version is v53 (https://docs.pexip.com/admin/interoperability.htm?Highlight=interoperability#browser)"
            elif "IE" in str(ua_string.browser.family):
                browser_advice = "Internet Explorer is not supported, please use a modern browser (https://docs.pexip.com/admin/interoperability.htm?Highlight=interoperability#browser)"
            
            
    return render_template("index.html", message=error, browser = browser_data, os = os_data, device = device_data, extra = extra_data, browser_info = browser_advice)


