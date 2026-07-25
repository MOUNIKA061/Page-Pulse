import os
from flask import Flask, render_template, request, jsonify
from website_parser import analyze_website

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()

    if not url:
        return jsonify({"error": "Please enter a website URL."}), 400

    result = analyze_website(url)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)