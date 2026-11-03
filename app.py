from flask import Flask, abort, jsonify, render_template, Response
from xml.etree.ElementTree import Element, SubElement, tostring

app = Flask(__name__)
SITE_URL = "https://grandpasdrum.com"

PAGES = {
    "our-story": {"title": "Our Story", "description": "Learn how a grandfather's generosity inspired Grandpa's Drum to restore and redistribute used percussion instruments in New York's Hudson Valley."},
    "donate": {"title": "Donate Used Drums in the Hudson Valley", "description": "Learn how to offer used drums, cymbals and percussion equipment to Grandpa's Drum for restoration and future redistribution in the Hudson Valley."},
    "request": {"title": "Request a Percussion Instrument", "description": "Grandpa's Drum is preparing to provide restored percussion instruments to students, schools and community programs in New York's Hudson Valley."},
    "impact": {"title": "Restoration Stories & Impact", "description": "Follow Grandpa's Drum as we begin documenting drum restorations, instrument donations and community impact in the Hudson Valley."},
    "get-involved": {"title": "Get Involved", "description": "Learn how musicians, repair technicians, educators and neighbors can help Grandpa's Drum restore and redistribute percussion instruments."},
}


@app.context_processor
def seo_context():
    from flask import request
    canonical_path = request.path if request.path == "/" else request.path.rstrip("/")
    return {"canonical_url": SITE_URL + canonical_path, "site_url": SITE_URL}


@app.get("/robots.txt")
def robots():
    return Response("User-agent: *\\nAllow: /\\nSitemap: " + SITE_URL + "/sitemap.xml\\n", mimetype="text/plain")


@app.get("/sitemap.xml")
def sitemap():
    root = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for path in ["/", "/our-story", "/donate", "/request", "/impact", "/get-involved", "/privacy"]:
        SubElement(SubElement(root, "url"), "loc").text = SITE_URL + path
    return Response(tostring(root, encoding="utf-8", xml_declaration=True), mimetype="application/xml")


@app.get("/health")
def health():
    return jsonify(status="ok", application="grandpasdrum")


@app.get("/")
def index():
    return render_template("index.html", title="Every Drum Has a Story", description="Grandpa's Drum collects, restores, and redistributes donated percussion instruments, beginning in New York's Hudson Valley.")


@app.get("/privacy")
def privacy():
    return render_template("privacy.html", title="Privacy & Transparency", description="Learn how Grandpa\'s Drum approaches visitor privacy and its current operating status.")


@app.get("/<slug>")
def information_page(slug):
    page = PAGES.get(slug)
    if page is None:
        abort(404)
    return render_template("page.html", slug=slug, **page)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", title="Page Not Found", description="That page could not be found.", noindex=True), 404
