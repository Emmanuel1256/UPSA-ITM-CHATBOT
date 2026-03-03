# ═══════════════════════════════════════════════════════════
# run.py — Application Entry Point
# Run:  python run.py
# ═══════════════════════════════════════════════════════════

from server.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)