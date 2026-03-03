# ═══════════════════════════════════════════════════════════
# server/seed.py
# Database Seeder — called once inside app context after db.create_all()
# Populates KnowledgeBase and Motivation tables if empty
# ═══════════════════════════════════════════════════════════

from server.extensions import db
from server.models.models import KnowledgeBase, Motivation


SEED_KNOWLEDGE = [
    {
        "intent_name":   "loops_cpp",
        "keywords":      "loop, for, while, c++, cpp, iteration, iterate, repeat",
        "response_text": (
            "In C++, loops allow repeated execution of code blocks. "
            "A for loop is ideal when the number of iterations is known: for(int i=0; i<n; i++). "
            "A while loop runs as long as a condition is true. "
            "Use do-while when you need the block to execute at least once. "
            "Always ensure your loop has a termination condition to avoid infinite loops."
        ),
        "level": "100",
    },
    {
        "intent_name":   "osi_model",
        "keywords":      "osi, model, layer, network, protocol, seven, layers",
        "response_text": (
            "The OSI model has 7 layers: "
            "(1) Physical – raw bit transmission, "
            "(2) Data Link – error detection/framing, "
            "(3) Network – routing & IP addressing, "
            "(4) Transport – reliable delivery (TCP/UDP), "
            "(5) Session – session management, "
            "(6) Presentation – data encoding/encryption, "
            "(7) Application – end-user protocols (HTTP, FTP). "
            "Each layer serves the layer above it."
        ),
        "level": "200",
    },
    {
        "intent_name":   "assignment_deadline",
        "keywords":      "assignment, deadline, due, submit, submission, hand in, when",
        "response_text": (
            "Assignment deadlines are listed in your Reminders tab. "
            "Typically assignments are due 2 weeks after issue. "
            "Always confirm with your course lecturer for the exact date. "
            "Submitting late without prior approval may attract penalties per UPSA academic policy."
        ),
        "level": "all",
    },
    {
        "intent_name":   "database_normalization",
        "keywords":      "normalization, normal form, 1nf, 2nf, 3nf, database, redundancy, dependency",
        "response_text": (
            "Database normalization eliminates redundancy and ensures data integrity. "
            "1NF: all values must be atomic, no repeating groups. "
            "2NF: no partial dependencies on the primary key (applies to composite keys). "
            "3NF: no transitive dependencies — non-key attributes should not depend on other non-key attributes. "
            "Higher forms (BCNF, 4NF) exist for special cases."
        ),
        "level": "200",
    },
    {
        "intent_name":   "exam_schedule",
        "keywords":      "exam, test, schedule, timetable, date, when, final, end of semester, mid-semester, midsem",
        "response_text": (
            "Exam schedules are posted on the UPSA student portal and in your Reminders tab. "
            "Mid-semester exams are usually held around Week 7–8, and end-of-semester exams in Weeks 14–15. "
            "Always check the official timetable as dates may shift. "
            "Bring your student ID card and arrive 15 minutes early."
        ),
        "level": "all",
    },
    {
        "intent_name":   "python_basics",
        "keywords":      "python, variable, function, def, print, syntax, indentation, script",
        "response_text": (
            "Python is designed for readability. "
            "Variables need no explicit declaration: x = 5. "
            "Functions are defined with def: def greet(name): return 'Hello, ' + name. "
            "Indentation is mandatory — it defines code blocks. "
            "Use print() for output. Python supports: int, float, str, list, dict, tuple, and set."
        ),
        "level": "100",
    },
    {
        "intent_name":   "data_structures",
        "keywords":      "stack, queue, linked list, tree, array, data structure, binary, heap, graph",
        "response_text": (
            "Key data structures: Arrays offer O(1) random access but fixed size. "
            "Linked Lists allow dynamic size with O(n) access. "
            "Stacks follow Last-In-First-Out (LIFO) — used in function calls. "
            "Queues follow First-In-First-Out (FIFO) — used in scheduling. "
            "Binary Search Trees enable O(log n) search. "
            "Graphs model networks and relationships."
        ),
        "level": "200",
    },
    {
        "intent_name":   "gpa_calculation",
        "keywords":      "gpa, grade, credit, cgpa, calculate, point, cumulative",
        "response_text": (
            "CGPA = Σ(Credit Hours × Grade Points) ÷ Σ(Credit Hours). "
            "Grade scale: A=4.0, B+=3.5, B=3.0, C+=2.5, C=2.0, D=1.0, F=0. "
            "Example: a 3-credit A and a 2-credit B gives CGPA = (3×4 + 2×3) ÷ 5 = 3.6. "
            "Maintain above 2.5 for good academic standing and 3.5 for Dean's List recognition."
        ),
        "level": "all",
    },
    {
        "intent_name":   "software_engineering",
        "keywords":      "software engineering, sdlc, agile, waterfall, scrum, sprint, requirements",
        "response_text": (
            "Software Engineering covers the full SDLC: "
            "Requirements → Design → Implementation → Testing → Deployment → Maintenance. "
            "Key methodologies: Waterfall (sequential, document-heavy) and Agile (iterative, flexible). "
            "Scrum uses sprints (2-week cycles), daily standups, and backlogs. "
            "UML diagrams model system design before coding."
        ),
        "level": "300",
    },
    {
        "intent_name":   "computer_architecture",
        "keywords":      "cpu, processor, memory, cache, bus, architecture, fetch, decode, execute, registers",
        "response_text": (
            "Computer architecture describes how hardware components interact. "
            "The CPU contains: ALU (arithmetic/logic), Control Unit (instruction management), "
            "and Registers (fast temporary storage). "
            "The fetch-decode-execute cycle drives all computation. "
            "Cache memory (L1/L2/L3) bridges the speed gap between CPU and RAM. "
            "Von Neumann architecture stores both data and instructions in the same memory."
        ),
        "level": "100",
    },
]

SEED_MOTIVATIONS = [
    "You're closer to your goals than you think. Keep pushing! 🎯",
    "Consistency beats intensity. Small daily efforts compound into great results. 📈",
    "Every expert was once a beginner. Your struggles today are building tomorrow's expertise. 💡",
    "The ITM journey is tough, but so are you. You've got this! 💪",
    "Progress, not perfection. One concept at a time. 🚀",
    "Your effort today is an investment in your future. Keep going! 🌟",
    "Difficult roads often lead to beautiful destinations. Stay the course. 🛤️",
]


def seed_database():
    """Seed initial data. Safe to call multiple times — skips existing records."""
    seeded = 0

    for kb_data in SEED_KNOWLEDGE:
        if not KnowledgeBase.query.filter_by(intent_name=kb_data["intent_name"]).first():
            db.session.add(KnowledgeBase(**kb_data))
            seeded += 1

    for msg in SEED_MOTIVATIONS:
        if not Motivation.query.filter_by(message=msg).first():
            db.session.add(Motivation(message=msg))
            seeded += 1

    db.session.commit()
    if seeded:
        print(f"[Seeder] Added {seeded} records to the database.")
    else:
        print("[Seeder] Database already seeded — nothing to add.")