from flask import Flask, request, make_response

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
@app.route("/lost-cookie")
def lost_cookie():
    if request.cookies.get("staff") == "true":
        return "Welcome staff member.<br>Flag: uthractf{cookie_trust_is_bad}"
    else:
        return "Access denied. Staff only."
@app.route("/physical-trace")
def physical_trace():
    return """
    <h2>UTHRA Venue Trace</h2>
    <p>You found the physical clue inside the venue.</p>
    <p>Flag: uthractf{physical_trace_found}</p>
    """



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

