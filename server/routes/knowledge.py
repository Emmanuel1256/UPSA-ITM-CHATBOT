# ═══════════════════════════════════════════════════════════
# server/routes/knowledge.py
# Knowledge Base CRUD Routes
# READ: any authenticated user
# WRITE (create/update/delete): lecturer only
# FR-4.2 Knowledge Base Editor
# ═══════════════════════════════════════════════════════════

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.extensions import db
from server.models.models import KnowledgeBase, User

kb_bp = Blueprint("knowledge", __name__, url_prefix="/api/knowledge")

VALID_LEVELS = ("all", "100", "200", "300")


def _require_lecturer():
    """Returns (user, None) if authorized, (None, error_response) if not."""
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)
    if not user or user.role != "lecturer":
        return None, (jsonify({"error": "Lecturer access required."}), 403)
    return user, None


# ─── GET ALL ─────────────────────────────────────────────────
@kb_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    items = KnowledgeBase.query.order_by(KnowledgeBase.id.asc()).all()
    return jsonify({"items": [i.to_dict() for i in items]}), 200


# ─── GET ONE ─────────────────────────────────────────────────
@kb_bp.route("/<int:item_id>", methods=["GET"])
@jwt_required()
def get_one(item_id):
    item = KnowledgeBase.query.get_or_404(item_id)
    return jsonify({"item": item.to_dict()}), 200


# ─── CREATE ──────────────────────────────────────────────────
@kb_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    user, err = _require_lecturer()
    if err:
        return err

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided."}), 400

    intent_name   = (data.get("intent_name")   or "").strip()
    keywords      = (data.get("keywords")      or "").strip()
    response_text = (data.get("response_text") or "").strip()
    level         = (data.get("level")         or "all").strip()
    resource_url  = (data.get("resource_url")  or "").strip() or None

    if not intent_name:
        return jsonify({"error": "Intent name is required."}), 400
    if not keywords:
        return jsonify({"error": "At least one keyword is required."}), 400
    if not response_text:
        return jsonify({"error": "Response text is required."}), 400
    if level not in VALID_LEVELS:
        return jsonify({"error": f"Level must be one of: {', '.join(VALID_LEVELS)}"}), 400

    intent_name = intent_name.lower().replace(" ", "_")

    if KnowledgeBase.query.filter_by(intent_name=intent_name).first():
        return jsonify({"error": f"An intent named '{intent_name}' already exists."}), 409

    item = KnowledgeBase(
        intent_name=intent_name,
        keywords=keywords,
        response_text=response_text,
        level=level,
        resource_url=resource_url,
        created_by=user.id,
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Intent created.", "item": item.to_dict()}), 201


# ─── UPDATE ──────────────────────────────────────────────────
@kb_bp.route("/<int:item_id>", methods=["PUT"])
@jwt_required()
def update(item_id):
    _, err = _require_lecturer()
    if err:
        return err

    item = KnowledgeBase.query.get_or_404(item_id)
    data = request.get_json(silent=True) or {}

    if "intent_name" in data:
        new_name = data["intent_name"].strip().lower().replace(" ", "_")
        existing = KnowledgeBase.query.filter_by(intent_name=new_name).first()
        if existing and existing.id != item_id:
            return jsonify({"error": f"Intent name '{new_name}' already exists."}), 409
        item.intent_name = new_name

    if "keywords" in data:
        kw = data["keywords"].strip()
        if not kw:
            return jsonify({"error": "Keywords cannot be empty."}), 400
        item.keywords = kw

    if "response_text" in data:
        rt = data["response_text"].strip()
        if not rt:
            return jsonify({"error": "Response text cannot be empty."}), 400
        item.response_text = rt

    if "level" in data:
        if data["level"] not in VALID_LEVELS:
            return jsonify({"error": "Invalid level."}), 400
        item.level = data["level"]

    if "resource_url" in data:
        item.resource_url = (data["resource_url"] or "").strip() or None

    db.session.commit()
    return jsonify({"message": "Intent updated.", "item": item.to_dict()}), 200


# ─── DELETE ──────────────────────────────────────────────────
@kb_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete(item_id):
    _, err = _require_lecturer()
    if err:
        return err

    item = KnowledgeBase.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Intent deleted."}), 200
