"""Маршруты Flask: форма и JSON API."""

from flask import Blueprint, render_template, request, jsonify

from app.services import RequestAnalyzerService


def register_routes(app, analyzer_service: RequestAnalyzerService) -> None:
    """Зарегистрировать маршруты на экземпляре Flask app."""

    @app.route("/", methods=["GET"])
    def index():
        return render_template(
            "index.html",
            text="",
            label=None,
            confidence=None,
            summary=None,
            fields=None,
        )

    @app.route("/analyze", methods=["POST"])
    def analyze_form():
        text = request.form.get("text") or ""
        result = analyzer_service.analyze(text, save=True)
        if "error" in result:
            return render_template("index.html", error=result["error"])
        return render_template(
            "index.html",
            text=text,
            label=result.get("label"),
            confidence=result.get("confidence"),
            summary=result.get("summary"),
            fields=result.get("fields"),
        )

    @app.route("/api/analyze", methods=["POST"])
    def api_analyze():
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")
        result = analyzer_service.analyze(text, save=True)
        if "error" in result:
            return jsonify({"error": result["error"]}), 400
        return jsonify({
            "id": result.get("id"),
            "label": result.get("label"),
            "confidence": result.get("confidence"),
            "summary": result.get("summary"),
            "fields": result.get("fields"),
        })
