from flask import Flask, request, make_response
import jwt


app = Flask(__name__)

# -----------------------------
# Challenge 1 – Open Gate
# -----------------------------
@app.route("/open-gate")
def open_gate():
    return """
    <h2>UTHRA Event Portal</h2>
    <p>Welcome to the UTHRA event site.</p>

    <!-- TODO: remove debug endpoint before deployment -->
    <!-- /open-gate/debug -->
    """

@app.route("/open-gate/debug")
def open_gate_debug():
    return "Debug panel active.<br>flag = uthractf{open_gate_leak}"


# -----------------------------
# Challenge 2 – Lost Cookie
# -----------------------------
@app.route("/lost-cookies")
def lostcookies():
    # Normal-looking student info page
    resp = make_response("""
        <h1>Uthra Student Information</h1>
        <p>This portal contains details and resources for students of Uthra.</p>
        <p>Students can view announcements, schedules, and updates here.</p>
    """)
    # Set a cookie named "role" with value "student"
    resp.set_cookie("role", "student")
    
    # Check cookie value
    if request.cookies.get("role") == "staff":
        return """
            <h2>Welcome staff member</h2>
            <p>Flag: uthractf{cookie_trust_is_bad}</p>
            <p>Staff have access to confidential information.</p>
        """
    else:
        return resp



@app.route("/physical-trace")
def physical_trace():
    return """
    <h2>UTHRA Venue Trace</h2>
    <p>You found the physical clue inside the venue.</p>
    <p>Flag: uthractf{physical_trace_found}</p>
    """
# -----------------------------
# Challenge 9 – Broken Login
# -----------------------------
@app.route("/broken-login", methods=["GET"])
def broken_login_form():
    return """
    <h3>UTHRA Staff Login</h3>
    <form action="/broken-login" method="post">
      Username: <input name="username"><br>
      Password: <input name="password" type="password"><br>
      <button type="submit">Login</button>
    </form>
    """

from flask import request

@app.route("/broken-login", methods=["POST"])
def broken_login():
    user = request.form.get("username", "")
    pwd = request.form.get("password", "")

    # ❌ logic bug on purpose
    if user == "admin" or pwd == "uthra2026":
        return "Welcome staff!<br>Flag: uthractf{L0G1C_0R_L0G1N}"
    else:
        return "Invalid credentials"

# -----------------------------
# Challenge 10 – Ticket Portal (IDOR)
# -----------------------------
@app.route("/ticket", methods=["GET", "POST"])
def ticket_portal():
    tickets = {
        "1001": "Ticket for Arun - General entry",
        "1002": "Ticket for Meera - VIP entry",
        "1003": "Internal staff ticket - placeholder",
        "1004": "Ticket for Ravi - General entry",
        "1005": "Ticket for Sneha - VIP entry",
        "1006": "Ticket for Karthik - General entry",
        "1007": "Ticket for Priya - VIP entry",
        "1008": "Ticket for Anil - General entry",
        "1009": "Internal staff ticket - flag: uthractf{IDOR_Leak_I$_B@S|C}",
        "1010": "Ticket for Divya - VIP entry"
    }

    if request.method == "POST":
        tid = request.form.get("id", "")
        if tid in tickets:
            return tickets[tid]
        else:
            return "Ticket not found"

    # Default GET request shows the form
    return """
    <h3>Ticket Portal</h3>
    <form action="/ticket" method="post">
      Ticket ID: <input name="id" value="1001"><br>
      <button type="submit">View Ticket</button>
    </form>
    <p>Example input: try <b>1001</b></p>
    """
# -----------------------------
# Challenge 13 – Bad Token
# -----------------------------
@app.route("/bad-token")
def bad_token():
    token = request.args.get("token")

    if not token:
        return "Provide token as ?token="

    try:
        payload = jwt.decode(
            token,
            "uthra_secret",      # intentionally weak
            algorithms=["HS256"]
        )

        if payload.get("role") == "admin":
            return "Welcome admin<br>Flag: uthractf{JWT_s3cr3t_|S_we@k}"
        else:
            return "Not an admin"

    except Exception as e:
        return "Invalid token"
        
# -----------------------------
# Challenge 16 – Admin Shadow (HARD)
# -----------------------------
@app.route("/staff-panel")
def staff_panel():
    return """
    <h3>UTHRA Staff Panel</h3>
    <p>Restricted internal interface.</p>

    <!--
    internal proxy note:
    X-Uthra-Internal must be base64(true)
    auth cookie name: uthra_auth
    -->
    """

@app.route("/staff-panel/admin")
def staff_panel_admin():

    header_val = request.headers.get("X-Uthra-Internal")
    cookie_val = request.cookies.get("uthra_auth")

    expected = base64.b64encode(b"true").decode()

    if header_val == expected and cookie_val == "shadow_access":
        return "Admin function unlocked.<br>Flag: uthractf{S#aD0W3D_$t@FF_P@n3L}"
    else:
        # misleading response on purpose
        return "404 - page not found"

@app.route("/ghost-trail-tn", methods=["GET", "POST"])
def ghost_trail_tn():
    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()

        if code == "MAA":
            return "Recovered trace:<br>uthractf{tn_cyber_ghost_trail}"
        else:
            return "No matching trace found."

    # GET request – show simple form
    return """
    <h3>Ghost Trail Investigation</h3>
    <form method="post">
        Enter airport code:
        <input type="text" name="code" required>
        <input type="submit" value="Submit">
    </form>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)














