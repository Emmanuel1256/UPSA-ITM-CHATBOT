# ═══════════════════════════════════════════════════════════
# server/routes/analytics.py
# Analytics and Report Generation Routes — Lecturer only
# FR-4.1 Query Analytics | FR-4.3 Automated Reporting
# ═══════════════════════════════════════════════════════════

import io
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.models.models import User
from server.services import report_service

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")


def _require_lecturer():
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)
    if not user or user.role != "lecturer":
        return None, (jsonify({"error": "Lecturer access required."}), 403)
    return user, None


# ─── FULL ANALYTICS SUMMARY ──────────────────────────────────
@analytics_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    _, err = _require_lecturer()
    if err:
        return err
    data = report_service.get_analytics_data()
    return jsonify(data), 200


# ─── UNANSWERED QUERIES ──────────────────────────────────────
@analytics_bp.route("/unanswered", methods=["GET"])
@jwt_required()
def unanswered():
    _, err = _require_lecturer()
    if err:
        return err

    from server.models.models import UnansweredQuery
    queries = (
        UnansweredQuery.query
        .order_by(UnansweredQuery.date.desc())
        .limit(50)
        .all()
    )
    return jsonify({"queries": [q.to_dict() for q in queries]}), 200


# ─── PDF REPORT ──────────────────────────────────────────────
@analytics_bp.route("/report/pdf", methods=["GET"])
@jwt_required()
def report_pdf():
    _, err = _require_lecturer()
    if err:
        return err

    semester      = request.args.get("semester", "1")
    academic_year = request.args.get("year", "2024/25")

    try:
        pdf_bytes = report_service.generate_pdf(semester, academic_year)
    except Exception as e:
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500

    filename = f"UPSA_ITM_Report_Sem{semester}_{academic_year.replace('/', '-')}.pdf"
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


# ─── CSV EXPORT ──────────────────────────────────────────────
@analytics_bp.route("/report/csv", methods=["GET"])
@jwt_required()
def report_csv():
    _, err = _require_lecturer()
    if err:
        return err

    try:
        csv_str = report_service.generate_csv()
    except Exception as e:
        return jsonify({"error": f"CSV generation failed: {str(e)}"}), 500

    return send_file(
        io.BytesIO(csv_str.encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="UPSA_ITM_Engagement_Data.csv",
    )