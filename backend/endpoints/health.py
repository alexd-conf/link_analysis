import flask


health_endpoint = flask.Blueprint('health_endpoint', __name__)

@health_endpoint.route("/api/health", methods=['GET'])
def health():
    notes = ["The metrics delivered reflect loading the web page at the resolution 1920x1080 with no further interaction, during the reported elapsed time.",
        "Rendering the page at a different resolution, interacting with it or staying on the page past the elapsed time may elicit different behavior, from what is reported by this tool, for the hypertext retrieved from the given URL.",
        "Additionally, specific Iframe URLs may change between visits, whether via a web browser, this tool or other methods of retrieving hypertext from a URL (a visit).",
        "And web page content, hypertext delivered from accessing a given URL, may change at the whim of the owner of the given URL's web page."]
    response = {"status": 0, "data": [{"category": "Welcome", "content": notes}]}

    return flask.jsonify(response)