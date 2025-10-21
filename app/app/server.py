from flask import Flask, request, jsonify
from app.email_utils import generate_emails, linkedin_query

app = Flask(__name__)

@app.route("/generate", methods=["GET"])
def generate():
    first = request.args.get("first")
    last = request.args.get("last")
    domain = request.args.get("domain")

    if not first or not last or not domain:
        return jsonify({"error": "Missing parameters"}), 400

    results = generate_emails(first, last, domain)
    linkedin_q = linkedin_query(first, last, domain)

    return jsonify({
        "results": results,
        "linkedin_query": linkedin_q
    })

@app.route("/", methods=["GET"])
def home():
    return "<h2>Email Generator & Verifier API</h2><p>Use /generate?first=John&last=Doe&domain=example.com</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
