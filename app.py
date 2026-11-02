from flask import Flask, abort, jsonify, render_template

app = Flask(__name__)

PAGES = {
    "our-story": {"title": "Our Story", "description": "The grandfather, the repair bench, and the legacy behind Grandpa's Drum."},
    "donate": {"title": "Donate an Instrument", "description": "Learn about donating drums and percussion equipment to Grandpa's Drum in the Hudson Valley."},
    "request": {"title": "Request an Instrument", "description": "Learn how Grandpa's Drum intends to help individuals, schools and organizations access instruments."},
    "impact": {"title": "Our Impact", "description": "Follow the instruments and restoration stories of Grandpa's Drum as the initiative grows."},
    "get-involved": {"title": "Get Involved", "description": "Explore ways to help Grandpa's Drum restore and redistribute musical instruments."},
}


@app.get("/health")
def health():
    return jsonify(status="ok", application="grandpasdrum")


@app.get("/")
def index():
    return render_template("index.html", title="Every Drum Has a Story", description="Grandpa's Drum collects, restores, and redistributes donated percussion instruments, beginning in New York's Hudson Valley.")


@app.get("/<slug>")
def information_page(slug):
    page = PAGES.get(slug)
    if page is None:
        abort(404)
    return render_template("page.html", slug=slug, **page)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", title="Page Not Found", description="That page could not be found."), 404
