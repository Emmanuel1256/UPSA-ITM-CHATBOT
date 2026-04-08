# ═══════════════════════════════════════════════════════════
# server/services/report_service.py
# Analytics data aggregation, PDF and CSV generation
# FR-4.3 Automated Reporting
# ═══════════════════════════════════════════════════════════

import io
import csv
from datetime import datetime, timedelta
from sqlalchemy import func

from server.extensions import db
from server.models.models import ChatMessage, IntentLog, UnansweredQuery, User


def get_analytics_data() -> dict:
    """Aggregate all analytics data including impact metrics."""

    total            = ChatMessage.query.filter_by(role="user").count()
    unanswered_count = UnansweredQuery.query.count()
    answered_count   = total - unanswered_count

    # Response (answer) rate
    response_rate = round((answered_count / total * 100), 1) if total > 0 else 0.0

    # Unique students who have used the system
    from server.models.models import KnowledgeBase
    unique_students = (
        db.session.query(func.count(func.distinct(ChatMessage.user_id)))
        .filter(ChatMessage.role == "user")
        .scalar() or 0
    )

    # Average messages per student
    avg_per_student = round(total / unique_students, 1) if unique_students > 0 else 0.0

    # Knowledge base size
    kb_count = KnowledgeBase.query.count()

    # Top 7 intents by frequency
    top_intents_raw = (
        db.session.query(IntentLog.intent_name, func.count(IntentLog.id).label("count"))
        .group_by(IntentLog.intent_name)
        .order_by(func.count(IntentLog.id).desc())
        .limit(7)
        .all()
    )
    top_intents = [{"intent": r[0], "count": r[1]} for r in top_intents_raw]

    # Last 7 days of daily interaction counts
    today  = datetime.utcnow().date()
    weekly = []
    for i in range(6, -1, -1):
        day   = today - timedelta(days=i)
        count = ChatMessage.query.filter(
            ChatMessage.role == "user",
            func.date(ChatMessage.timestamp) == day,
        ).count()
        weekly.append({"day": day.strftime("%a"), "count": count})

    # Interactions grouped by student level
    level_raw = (
        db.session.query(User.level, func.count(ChatMessage.id).label("count"))
        .join(ChatMessage, ChatMessage.user_id == User.id)
        .filter(ChatMessage.role == "user", User.level.isnot(None))
        .group_by(User.level)
        .all()
    )
    by_level = {r[0]: r[1] for r in level_raw}

    # Most engaged level
    most_engaged_level = max(by_level, key=by_level.get) if by_level else "N/A"

    # Latest 10 unanswered queries for display
    unanswered_list = [
        q.to_dict()
        for q in UnansweredQuery.query.order_by(UnansweredQuery.date.desc()).limit(10).all()
    ]

    # Most asked topic
    most_asked = top_intents[0]["intent"].replace("_", " ").title() if top_intents else "N/A"

    return {
        "total_interactions":   total,
        "answered_count":       answered_count,
        "unanswered_count":     unanswered_count,
        "response_rate":        response_rate,
        "unique_students":      unique_students,
        "avg_per_student":      avg_per_student,
        "kb_count":             kb_count,
        "most_asked":           most_asked,
        "most_engaged_level":   most_engaged_level,
        "top_intents":          top_intents,
        "weekly_engagement":    weekly,
        "by_level":             by_level,
        "unanswered_list":      unanswered_list,
    }


def generate_pdf(semester: str = "1", academic_year: str = "2024/25") -> bytes:
    """Generate UPSA-branded PDF semester report. Returns raw bytes."""

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer,
        Table, TableStyle, HRFlowable,
    )

    NAVY  = colors.HexColor("#0B1E3F")
    GOLD  = colors.HexColor("#C5A100")
    LIGHT = colors.HexColor("#F4F6F8")

    data   = get_analytics_data()
    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )

    styles   = getSampleStyleSheet()
    elements = []

    # ── Header banner
    header_content = Paragraph(
        f"<font color='#C5A100'><b>UPSA ITM</b></font> — Academic Counseling System<br/>"
        f"<font size='9' color='grey'>Semester {semester} | Academic Year {academic_year} | "
        f"Generated: {datetime.utcnow().strftime('%d %b %Y, %H:%M UTC')}</font>",
        ParagraphStyle("hdr", fontName="Helvetica", fontSize=13, textColor=colors.white, leading=18),
    )
    hdr_table = Table([[header_content]], colWidths=[17 * cm])
    hdr_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("PADDING",    (0, 0), (-1, -1), 14),
    ]))
    elements.append(hdr_table)
    elements.append(Spacer(1, 0.5 * cm))

    title_style = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, textColor=NAVY, spaceAfter=6)
    h2_style    = ParagraphStyle("h2",    fontName="Helvetica-Bold", fontSize=12, textColor=NAVY, spaceBefore=14, spaceAfter=6)
    body_style  = ParagraphStyle("body",  fontName="Helvetica",      fontSize=10, textColor=colors.HexColor("#374151"), leading=14)

    elements.append(Paragraph("Semester Engagement Report", title_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=GOLD))
    elements.append(Spacer(1, 0.3 * cm))

    # ── 1. System Impact Summary
    elements.append(Paragraph("1. System Impact Summary", h2_style))

    impact_data = [
        ["Impact Metric",                    "Value"],
        ["Total Student Interactions",        str(data["total_interactions"])],
        ["Successfully Answered Queries",     str(data["answered_count"])],
        ["Unanswered / Flagged Queries",      str(data["unanswered_count"])],
        ["Query Response Rate",               f"{data['response_rate']}%"],
        ["Unique Students Served",            str(data["unique_students"])],
        ["Avg. Interactions per Student",     str(data["avg_per_student"])],
        ["Knowledge Base Intents Configured", str(data["kb_count"])],
        ["Most Asked Topic",                  data["most_asked"]],
        ["Most Engaged Level",                f"Level {data['most_engaged_level']}"],
    ]
    impact_table = Table(impact_data, colWidths=[10 * cm, 7 * cm])
    impact_table.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID",           (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("PADDING",        (0, 0), (-1, -1), 8),
        # Highlight response rate row in gold if >= 70%
        ("TEXTCOLOR",      (1, 4), (1, 4),
         colors.HexColor("#15803d") if data["response_rate"] >= 70 else colors.HexColor("#b45309")),
        ("FONTNAME",       (1, 4), (1, 4), "Helvetica-Bold"),
    ]))
    elements.append(impact_table)
    elements.append(Spacer(1, 0.2 * cm))

    # Impact interpretation paragraph
    rate = data["response_rate"]
    if rate >= 80:
        interp = f"The system is performing <b>excellently</b>, answering {rate}% of all student queries. The Knowledge Base is well-configured and covering student needs effectively."
    elif rate >= 60:
        interp = f"The system is performing <b>adequately</b>, answering {rate}% of queries. Consider expanding the Knowledge Base to cover the flagged unanswered topics below."
    else:
        interp = f"The system answered {rate}% of queries. <b>Significant improvement</b> is possible by adding intents for the unanswered topics flagged below."
    elements.append(Paragraph(interp, body_style))

    # ── 2. Engagement by Level
    elements.append(Paragraph("2. Engagement by Level", h2_style))
    stats_data = [
        ["Metric",                "Value"],
        ["Engagement — Level 100", str(data["by_level"].get("100", 0))],
        ["Engagement — Level 200", str(data["by_level"].get("200", 0))],
        ["Engagement — Level 300", str(data["by_level"].get("300", 0))],
    ]
    stats_table = Table(stats_data, colWidths=[10 * cm, 7 * cm])
    stats_table.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID",           (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("PADDING",        (0, 0), (-1, -1), 8),
    ]))
    elements.append(stats_table)

    # ── 2. Top Intents
    elements.append(Paragraph("3. Top 5 Query Intents", h2_style))
    if data["top_intents"]:
        intent_rows = [["Rank", "Intent", "Query Count"]]
        for i, item in enumerate(data["top_intents"][:5], 1):
            intent_rows.append([
                str(i),
                item["intent"].replace("_", " ").title(),
                str(item["count"]),
            ])
        intent_table = Table(intent_rows, colWidths=[2 * cm, 10 * cm, 5 * cm])
        intent_table.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (-1, 0),  GOLD),
            ("TEXTCOLOR",      (0, 0), (-1, 0),  NAVY),
            ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",       (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
            ("GRID",           (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
            ("PADDING",        (0, 0), (-1, -1), 8),
            ("ALIGN",          (0, 0), (-1, -1), "CENTER"),
            ("ALIGN",          (1, 1), (1, -1),  "LEFT"),
        ]))
        elements.append(intent_table)
    else:
        elements.append(Paragraph("No intent data recorded yet.", body_style))

    # ── 3. Unanswered Queries
    elements.append(Paragraph("4. Unanswered / Flagged Queries", h2_style))
    if data["unanswered_list"]:
        ua_rows = [["#", "Question", "Level", "Date"]]
        for i, q in enumerate(data["unanswered_list"], 1):
            ua_rows.append([
                str(i),
                Paragraph(q["question"], body_style),
                q.get("student_level", "—"),
                q["date"][:10],
            ])
        ua_table = Table(ua_rows, colWidths=[1 * cm, 10 * cm, 2.5 * cm, 3.5 * cm])
        ua_table.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (-1, 0),  colors.HexColor("#b45309")),
            ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",       (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fffbeb")]),
            ("GRID",           (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
            ("PADDING",        (0, 0), (-1, -1), 7),
            ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(ua_table)
    else:
        elements.append(Paragraph("No unanswered queries logged.", body_style))

    # ── Footer
    elements.append(Spacer(1, 1 * cm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=GOLD))
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(Paragraph(
        "University of Professional Studies, Accra (UPSA) — ITM Department | Confidential Academic Report",
        ParagraphStyle("footer", fontName="Helvetica", fontSize=8, textColor=colors.grey, alignment=1),
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()


def generate_csv() -> str:
    """Generate CSV export of raw engagement data. Returns a UTF-8 string."""

    data   = get_analytics_data()
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["UPSA ITM — Engagement Data Export"])
    writer.writerow(["Generated", datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")])
    writer.writerow([])

    writer.writerow(["=== SUMMARY ==="])
    writer.writerow(["Total Interactions", data["total_interactions"]])
    writer.writerow(["Unanswered Queries", data["unanswered_count"]])
    writer.writerow([])

    writer.writerow(["=== TOP INTENTS ==="])
    writer.writerow(["Rank", "Intent", "Count"])
    for i, item in enumerate(data["top_intents"], 1):
        writer.writerow([i, item["intent"], item["count"]])
    writer.writerow([])

    writer.writerow(["=== ENGAGEMENT BY LEVEL ==="])
    writer.writerow(["Level", "Interactions"])
    for level, count in data["by_level"].items():
        writer.writerow([f"Level {level}", count])
    writer.writerow([])

    writer.writerow(["=== WEEKLY ENGAGEMENT (last 7 days) ==="])
    writer.writerow(["Day", "Interactions"])
    for d in data["weekly_engagement"]:
        writer.writerow([d["day"], d["count"]])
    writer.writerow([])

    writer.writerow(["=== UNANSWERED QUERIES ==="])
    writer.writerow(["Question", "Level", "Date"])
    for q in data["unanswered_list"]:
        writer.writerow([q["question"], q.get("student_level", "—"), q["date"][:10]])

    return output.getvalue()
