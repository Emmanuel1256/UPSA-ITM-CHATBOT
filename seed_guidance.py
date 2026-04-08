#!/usr/bin/env python3
"""
seed_guidance.py — Seeds the UPSA ITM chatbot with Academic Guidance
knowledge base entries covering:
  • Breaking down complex project briefs
  • Prioritizing and planning coding tasks
  • Creating effective study plans
  • Debugging strategies and getting unstuck
  • Time management and deadline management
  • Group project coordination
  • Exam preparation for theoretical subjects

Run from project root with venv active:
    python seed_guidance.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app
from server.extensions import db
from server.models.models import KnowledgeBase

GUIDANCE_DATA = [

# ─────────────────────────────────────────────────────────────────────────
#  PROJECT BRIEF BREAKDOWN
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_break_down_project",
"keywords": [
    "break down project", "understand project brief", "project brief", "project requirements",
    "start project", "how to start", "project scope", "confusing brief", "project unclear",
    "don't know where to start", "no idea where to start", "project too big",
    "overwhelmed by project", "analyse brief", "understand assignment",
    "project plan", "how to plan project", "beginning of project",
],
"response": """
📋 **How to Break Down a Complex Project Brief**

Getting a long project brief and not knowing where to start is one of the most common ITM challenges. Here's a structured approach that works every time.

---

## Step 1 — Read it twice before doing anything
Read the entire brief **once for general understanding**, then **once more with a highlighter** (physical or digital). On the second pass, mark:
- 🎯 **Deliverables** — what exactly must you submit?
- 📅 **Deadlines** — final date AND any milestone dates
- 🔧 **Technical requirements** — specific languages, tools, or platforms mentioned
- ⚠️ **Constraints** — word limits, file formats, what NOT to do

---

## Step 2 — Extract the core questions
Turn the brief into a list of questions the project must answer. For example:

> *"Build a student record management system with login and report generation"*

Becomes:
- What data does the system store?
- Who logs in and what can they do?
- What does the report look like?
- How is data stored (file, database)?
- What language/framework must I use?

This turns vague text into **specific engineering problems**.

---

## Step 3 — Identify the modules
Every ITM project can be split into vertical slices. Common ones:

| Module | What it covers |
|--------|---------------|
| **Authentication** | Login, register, roles, session |
| **Data Layer** | Database schema, file storage, CRUD |
| **Business Logic** | Rules, calculations, processing |
| **User Interface** | Forms, displays, navigation |
| **Reports / Output** | Exports, summaries, print views |

Draw a simple box diagram — one box per module, arrows showing how they connect.

---

## Step 4 — List tasks per module
Under each module, write the individual coding tasks. Keep each task small enough to finish in **one sitting (2–4 hours)**. If a task feels too big, split it.

❌ *"Build the login system"* — too vague  
✅ *"Create the login HTML form"*  
✅ *"Write the password validation function"*  
✅ *"Connect form to database and check credentials"*  
✅ *"Handle failed login and show error message"*  

---

## Step 5 — Sequence the tasks
Some tasks depend on others. Build in this order:
1. **Data layer first** — you can't build anything without somewhere to store data
2. **Core logic second** — the main functionality
3. **Interface third** — connect it all visually
4. **Testing and polish last** — edge cases, error handling, formatting

---

## Step 6 — Estimate and assign time
Be honest. Triple your gut estimate — most students underestimate by 3×. If you think a task takes 1 hour, block 3. Add a **buffer day** before submission.

💡 **Tip:** If anything in the brief is still unclear after this process, ask your lecturer NOW — not the night before submission.
""",
"level": "all"
},

# ─────────────────────────────────────────────────────────────────────────
#  TASK PRIORITIZATION
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_prioritize_tasks",
"keywords": [
    "prioritize tasks", "task priority", "what to do first", "order of tasks",
    "manage tasks", "too many tasks", "stuck on where to begin",
    "task management", "what should i work on", "multiple assignments",
    "many deadlines", "overwhelmed", "juggling assignments",
    "prioritization", "which task first", "coding task order",
    "time management coding", "schedule my work",
],
"response": """
⚡ **How to Prioritize Your Coding Tasks**

When you have multiple assignments, tasks, or modules pulling at you, this framework cuts through the noise.

---

## The ITM Priority Matrix

Sort every task into one of four boxes:

```
                   URGENT          NOT URGENT
              ┌──────────────┬──────────────────┐
    IMPORTANT │  DO FIRST    │   SCHEDULE IT    │
              │  (deadline   │   (design, docs, │
              │   tomorrow)  │    refactoring)  │
              ├──────────────┼──────────────────┤
 NOT IMPORTANT│  DELEGATE /  │   DROP / LATER   │
              │  BATCH       │   (extra polish, │
              │  (emails,    │    nice-to-haves) │
              │   formatting)│                  │
              └──────────────┴──────────────────┘
```

---

## For a single project — sequence your tasks this way

**1. Foundation tasks first (blockers)**
Anything that other tasks depend on. Usually: database schema, data models, authentication. Nothing else works until these are done.

**2. Core requirement tasks second**
The features the brief explicitly requires and will be marked on. Do these before any extras.

**3. Integration tasks third**
Connecting modules together — frontend talking to backend, functions calling each other.

**4. Error handling and validation**
Input validation, edge cases, meaningful error messages. This is where marks are often lost.

**5. Extras and polish last**
Nice UI touches, bonus features, README. Only if time allows.

---

## The 3-Task Rule
Every morning or work session, pick **exactly 3 tasks** to complete that day. Not 10, not 1 — 3. Write them down before you open your IDE.

At the end of the session, if you finished your 3, you can pick 1 bonus task. This prevents the paralysis of a massive to-do list.

---

## When everything feels equally urgent

**Use the deadline tiebreaker:**
List all tasks, write the submission deadline next to each, and sort by earliest deadline. Work backwards from each deadline — what must be done 3 days before? 1 week before?

**Use the dependency tiebreaker:**
If Task B cannot start until Task A is done, Task A wins regardless of deadline.

---

💡 **Common ITM mistake:** Spending the first 3 days making the UI look perfect before the core logic works. Always build logic first, interface last.
""",
"level": "all"
},

# ─────────────────────────────────────────────────────────────────────────
#  STUDY PLAN
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_create_study_plan",
"keywords": [
    "study plan", "how to study", "study schedule", "revision plan",
    "prepare for exam", "exam preparation", "revision strategy",
    "study tips", "effective study", "study techniques",
    "how to revise", "learning plan", "academic plan",
    "study routine", "study method", "study for theoretical",
    "study for itm", "study programming", "study for test",
    "how to pass", "prepare for test", "study smarter",
],
"response": """
📚 **Creating an Effective Study Plan for ITM**

ITM is split between **theoretical** (concepts, definitions, essays) and **practical** (coding, systems). Your study plan needs to handle both differently.

---

## Step 1 — Audit your subjects

List every course this semester. For each, write:
- Topic areas to cover
- Exam/assignment format (MCQ, essay, code, practical?)
- Your current confidence level (1–5)
- Weeks until exam

---

## Step 2 — Allocate study blocks

**For theoretical subjects** (networking, database theory, IS management):

| Technique | What to do |
|-----------|-----------|
| **Active recall** | Read a section, close the book, write what you remember |
| **Concept mapping** | Draw diagrams connecting ideas — better than re-reading |
| **Past questions** | Find past exam questions and answer them without notes first |
| **Teach it back** | Explain the concept out loud as if teaching someone — gaps appear immediately |

**For practical/coding subjects** (C++, data structures, web dev):

| Technique | What to do |
|-----------|-----------|
| **Code daily** | Even 30 minutes of writing actual code beats 3 hours of reading notes |
| **Redo lab exercises** | Without looking at your solutions — then compare |
| **Break and rebuild** | Take working code, delete sections, rebuild them from memory |
| **Explain the output** | Before running code, predict what it will print and why |

---

## Step 3 — Build your weekly schedule

**Recommended ITM student week:**

```
Monday    │ Hardest subject — fresh mind handles difficulty best
Tuesday   │ Coding practice / lab work
Wednesday │ Theoretical subject — active recall session
Thursday  │ Assignments / project work
Friday    │ Mixed review — weaker topics
Saturday  │ Past questions / mock tests
Sunday    │ REST — no guilt. Burnout kills exam performance.
```

**Session length:** 45–50 minutes of focused work, then a 10-minute break (Pomodoro technique). Never study more than 3 hours without a proper break.

---

## Step 4 — The 3-week countdown

**3 weeks before exam:**
- Identify ALL topics and which ones you don't understand yet
- Start active recall sessions — no passive re-reading

**2 weeks before:**
- Past questions — do them under timed conditions
- Focus extra time on weak areas identified in week 3

**1 week before:**
- Light review only — you should be consolidating, not learning new material
- Practice writing answers quickly
- Review your own notes and concept maps

**2 days before:**
- Only review your summary notes
- Sleep early — memory consolidates during sleep

**Day before:**
- Light review in the morning only
- Rest in the afternoon
- Prepare your materials (pens, ID, calculator if needed)

---

💡 **Most important rule:** Consistent 45-minute sessions every day outperform an all-night study session every time. Your brain needs sleep to consolidate what you studied.
""",
"level": "all"
},

# ─────────────────────────────────────────────────────────────────────────
#  DEBUGGING STRATEGY
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_debugging_strategy",
"keywords": [
    "stuck on bug", "can't find bug", "debugging", "debug", "how to debug",
    "code not working", "error in code", "fix my code", "code has error",
    "program crashes", "segfault", "segmentation fault", "runtime error",
    "compilation error", "logic error", "infinite loop", "wrong output",
    "code won't compile", "getting errors", "debugging tips",
    "find bug", "troubleshoot code", "debug strategy", "stuck coding",
],
"response": """
🔍 **Debugging Strategy — How to Get Unstuck**

Every programmer gets stuck. The difference between good and great programmers is a systematic approach to finding bugs — not luck.

---

## The 5-Step Debug Process

### Step 1 — Read the error message carefully
Error messages tell you **exactly** what went wrong if you read them fully.

```
error: 'x' was not declared in this scope
         ^~
```
This says: variable `x` doesn't exist where you're trying to use it. Check spelling, scope, or missing declaration.

Common C++ error types:
| Error | Meaning |
|-------|---------|
| `undefined reference` | Function declared but not defined/linked |
| `segmentation fault` | You accessed memory you don't own (bad pointer) |
| `stack overflow` | Infinite recursion |
| `out of range` | Array or vector index too large |
| `use of uninitialized variable` | Forgot to assign a value before using it |

---

### Step 2 — Reproduce the problem consistently
Make sure you can trigger the bug **every time** with the same input. If it's random, it's likely a memory/pointer issue.

---

### Step 3 — Isolate the problem — binary search your code
Don't scan every line. Instead:
1. Comment out the **bottom half** of the suspicious section
2. Does the bug still appear? → problem is in the top half
3. Keep halving until you pinpoint the exact line

This finds bugs in minutes instead of hours.

---

### Step 4 — Add print statements / use a debugger
Before the suspicious line, print every variable involved:

```cpp
cout << "Before function call: x = " << x << ", size = " << size << endl;
```

This tells you **exactly what your program thinks** at that moment — often the value is wrong long before the crash.

---

### Step 5 — Rubber duck debugging
Explain your code **line by line out loud** as if teaching it to someone (or a rubber duck). You will find the bug while explaining. This sounds silly but it works — explaining forces you to question assumptions you've been glossing over.

---

## The "I've been stuck for over 30 minutes" rule

If you've been on the same bug for more than 30 minutes:
1. **Step away** for 10 minutes — walk, drink water, look at something else
2. **Return and re-read** the code as if you're seeing it for the first time
3. **Google the exact error message** — someone has had this before
4. **Ask for help** — show your code and describe what you expected vs what happened

Staring at the same code for 3 hours rarely fixes it. Taking a break does.

---

## Before asking for help — answer these first:
- What **exactly** did you expect the code to do?
- What **exactly** does it do instead?
- Which **specific line** do you think is wrong?
- What have you already tried?

Having answers to these questions often reveals the bug before you even need to ask.
""",
"level": "all"
},

# ─────────────────────────────────────────────────────────────────────────
#  TIME MANAGEMENT & DEADLINES
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_time_management",
"keywords": [
    "time management", "manage time", "deadline", "missed deadline",
    "running out of time", "not enough time", "time pressure",
    "procrastination", "procrastinating", "keep delaying",
    "submission date", "when is deadline", "manage deadlines",
    "assignment due", "late submission", "extension",
    "balance assignments", "too much work", "overwhelmed deadlines",
    "manage workload", "workload too heavy", "behind on work",
],
"response": """
⏰ **Time Management for ITM Students**

Poor time management is the number one reason for last-minute submissions and failed projects — not lack of ability. Here's how to take control.

---

## The Backward Planning Method

Start from your deadline and plan backwards.

**Example:** Assignment due in 3 weeks

```
Week 3 (submission week)
  Mon-Tue  → Final testing and bug fixes
  Wed      → Write report / documentation
  Thu      → Final review and submission
  Fri      → BUFFER (things always take longer)

Week 2 (building week)
  Mon-Tue  → Build module 2
  Wed-Thu  → Build module 3
  Fri      → Integration and first test

Week 1 (setup week)
  Mon      → Read brief, break into tasks
  Tue-Wed  → Design and database setup
  Thu-Fri  → Build module 1
```

Working backwards forces you to see that **you need to start on day 1** — not week 3.

---

## The Procrastination Fix

Procrastination usually comes from a task feeling too large or scary. Fix it by making the first step **ridiculously small**.

❌ *"Work on my project"* — paralyzing  
✅ *"Open my IDE and create the project folder"* — achievable in 2 minutes

Once you've started, momentum takes over. The hardest part is always the beginning.

---

## Protect your productive hours

Track for 3 days when you feel most focused. For most people it's either:
- **Morning (6–10am)** — do hard coding and problem-solving here
- **Evening (8–11pm)** — good for reading and review

Use your peak hours for the hardest tasks. Use low-energy times (after lunch, etc.) for routine tasks like formatting code, writing comments, or organising files.

---

## When you're already behind

Don't panic — triage:

**Step 1:** List every task left with honest time estimates  
**Step 2:** Mark what is **absolutely required** to pass vs what's extra  
**Step 3:** Cut everything non-essential and do the required items first  
**Step 4:** Work in 2-hour focused blocks with short breaks  
**Step 5:** If genuinely stuck or unwell, contact your lecturer **before** the deadline — not after  

---

## The Rule of Three (daily)

Every morning, write down **3 things that, if completed today, would make today a success**. Only 3. Focus on those before anything else.

---

💡 **A note on extensions:** Lecturers are far more sympathetic when you ask for help **before** the deadline than when you submit late without warning. If you're struggling, communicate early.
""",
"level": "all"
},

# ─────────────────────────────────────────────────────────────────────────
#  GROUP PROJECT COORDINATION
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_group_project",
"keywords": [
    "group project", "team project", "group work", "group assignment",
    "team assignment", "coordinate team", "group coordination",
    "team member not working", "group member lazy", "team communication",
    "divide work group", "split tasks group", "group project tips",
    "working in a team", "team roles", "project collaboration",
    "group project problems", "team conflict", "group contribution",
],
"response": """
👥 **Managing a Group Project Successfully**

Group projects are difficult because you're combining technical work with people management. Here's how to set your team up for success from day one.

---

## Day 1 — Set the foundation (don't skip this)

**Hold a kickoff meeting within 48 hours of getting the brief.** Decide together:

| Decision | Why it matters |
|----------|---------------|
| **Team lead** | One person coordinates — not bosses, but keeps things moving |
| **Communication channel** | WhatsApp group, Discord, or email — pick one and use only that |
| **Meeting schedule** | Weekly check-in, same time, same place (physical or virtual) |
| **Task division** | Who owns what — write it down |
| **Version control** | Set up a shared GitHub repo on day 1 |

---

## How to divide the work fairly

Split by **module/feature**, not by type of task. Avoid:
- ❌ "You do all the frontend, I do all the backend"

This creates bottlenecks. Instead:
- ✅ "Member A owns authentication (frontend + backend)"
- ✅ "Member B owns the reporting module (frontend + backend)"

Each person owns a vertical slice — they understand their part fully and there's no waiting.

---

## Version control for teams (GitHub)

```bash
# Each member works on their own branch
git checkout -b feature/login-module

# Commit regularly (at minimum after each working session)
git add .
git commit -m "Add password validation function"

# Push and create a pull request when feature is complete
git push origin feature/login-module
```

**Rule:** Never push directly to `main`. Always branch → work → pull request → review → merge.

---

## When a team member isn't contributing

1. **First:** Have a direct, private conversation — they may be struggling with something
2. **Second:** Document the conversation (WhatsApp message is fine)
3. **Third:** Redistribute tasks clearly in writing — "By Thursday, you will complete X"
4. **If unresolved:** Inform your lecturer **before** submission, not after. Most lecturers will adjust marks based on contribution evidence

---

## Weekly check-in agenda (15 minutes)

1. What did each person finish this week?
2. Is anyone blocked on anything?
3. What does each person commit to completing next week?
4. Any integration work needed between modules?

---

💡 **Most important rule:** Over-communicate in a group project. Silence breeds assumptions. A 2-minute WhatsApp update saves hours of confusion.
""",
"level": "all"
},

# ─────────────────────────────────────────────────────────────────────────
#  EXAM PREPARATION — THEORETICAL
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_exam_prep_theory",
"keywords": [
    "exam preparation", "prepare for exam", "exam tips", "pass exam",
    "theory exam", "theoretical exam", "written exam", "exam revision",
    "exam strategy", "how to answer exam", "exam technique",
    "multiple choice tips", "essay exam", "short answer",
    "exam tomorrow", "exam next week", "exam next month",
    "study for exam", "revision tips", "exam advice",
    "past questions", "past papers", "exam questions",
],
"response": """
📝 **Exam Preparation for ITM Theory Exams**

ITM theory exams test your understanding of concepts, frameworks, and their application — not just memorisation. Here's how to prepare effectively.

---

## Know your exam format first

Before studying, find out:
- **MCQ, Short Answer, or Essay?** — each needs a different approach
- **Open book or closed book?** — affects what to memorise vs understand
- **Topics covered** — get the official list from your course outline
- **Marks allocation** — spend revision time proportional to marks available

---

## Effective revision techniques

### For definitions and concepts
**Flashcard method:** Write the concept on one side, the definition + example on the other. Test yourself — if you can't explain it in your own words, you don't know it yet.

### For frameworks and models
**Diagram + label from memory:** Draw the framework (SDLC, OSI model, ER diagram) without looking at notes. Then check and correct. Repeat until perfect.

### For application questions
**Past question practice:** Find past exam questions. Answer them under timed conditions, then compare to model answers. Focus on *why* the answer is what it is, not just what it is.

---

## Answering exam questions

**For MCQ:**
- Read every option before choosing
- Eliminate obviously wrong answers first
- If unsure between two, choose the more specific/technical one
- Never leave a question blank (usually no negative marking)

**For short answer (5–10 marks):**
- Answer directly in the first sentence — don't warm up
- Use bullet points or numbered lists where appropriate
- Include an example to demonstrate understanding
- Check you've addressed every part of the question

**For essays (15–25 marks):**
- Spend 2 minutes planning before writing
- Structure: Introduction → Main argument (3–4 points with evidence) → Conclusion
- Each paragraph should make one clear point
- Use course terminology — show you know the subject language

---

## The night before

✅ Review your summary notes only — no new content  
✅ Pack your materials (pen, student ID, calculator if needed)  
✅ Know the exam location and time  
✅ Sleep at least 7 hours — memory consolidates during sleep  
✅ Eat breakfast on exam day — brain needs fuel  

❌ Don't pull an all-nighter — it impairs recall  
❌ Don't learn new topics the night before  
❌ Don't discuss the paper with anxious classmates right before going in  

---

💡 **In the exam room:** Read through the entire paper for 5 minutes before writing anything. This primes your memory and helps you sequence your answers by what you know best.
""",
"level": "all"
},

# ─────────────────────────────────────────────────────────────────────────
#  HOW TO START CODING A PROJECT (from scratch)
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_start_coding_project",
"keywords": [
    "how to start coding", "start a project", "begin project",
    "project setup", "set up project", "first steps project",
    "don't know how to code project", "where to begin coding",
    "start programming project", "project structure", "folder structure",
    "set up development environment", "github setup project",
    "initialise project", "initialize project", "scaffold project",
    "code project from scratch", "new project setup",
],
"response": """
🚀 **How to Start a Coding Project from Scratch**

The blank editor screen is the most intimidating moment in any project. Here's the exact sequence to go from nothing to a running foundation.

---

## Step 1 — Set up version control first (before writing any code)

```bash
# Create project folder
mkdir MyProject
cd MyProject

# Initialise git
git init

# Create a .gitignore immediately (prevents uploading junk files)
# For C++ projects, add:
echo "*.exe\n*.o\n*.out\nbuild/\n.vscode/\n" > .gitignore

# First commit
git add .gitignore
git commit -m "Initial commit — project setup"
```

If it's a group project, create a GitHub repo and share it now.

---

## Step 2 — Design your file/folder structure

Before writing logic, decide where things live:

**C++ project structure:**
```
MyProject/
├── src/           ← all .cpp source files
│   ├── main.cpp
│   ├── student.cpp
│   └── database.cpp
├── include/       ← all .h header files
│   ├── student.h
│   └── database.h
├── data/          ← input/output files
├── docs/          ← documentation
└── Makefile       ← or CMakeLists.txt
```

---

## Step 3 — Write the skeleton, not the logic

Create all your files with empty functions. Write function signatures and comments describing what each function will do — but don't implement them yet.

```cpp
// student.h
class Student {
public:
    Student(string name, int id);
    void displayInfo();      // prints student details
    void updateGrade(float grade);  // updates the student's grade
private:
    string name;
    int id;
    float grade;
};
```

This lets you see the whole architecture before committing to any implementation.

---

## Step 4 — Build and test the skeleton first

Make sure your project **compiles with empty functions** before adding any logic. This catches structural errors early.

```cpp
// main.cpp — just test it compiles and runs
int main() {
    cout << "Project skeleton running successfully." << endl;
    return 0;
}
```

**Compile and run it.** If it works, you have a solid foundation.

---

## Step 5 — Implement one function at a time

Pick the most fundamental function (usually creating/initialising your main data structure). Implement it, test it with a simple `cout` statement, then move to the next.

**Never implement multiple functions at once** — you won't know which one caused a bug.

---

## Step 6 — Commit after every working feature

```bash
git add .
git commit -m "Add Student class with constructor and displayInfo"
```

Small, frequent commits mean you can always go back to a working state if something breaks.

---

💡 **The golden rule:** Get a tiny, ugly, working version done first. Then improve it. A working ugly program beats a beautiful broken one every time.
""",
"level": "all"
},

# ─────────────────────────────────────────────────────────────────────────
#  CHOOSING THE RIGHT TECHNOLOGY / APPROACH
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_choose_technology",
"keywords": [
    "which language to use", "which technology", "choose technology",
    "what language should i use", "best language for project",
    "which framework", "which database", "choose database",
    "should i use", "technology choice", "pick technology",
    "right approach", "right tool", "best approach",
    "which tool is best", "language choice", "platform choice",
],
"response": """
🛠️ **How to Choose the Right Technology for Your Project**

One of the most common mistakes is spending days choosing tools instead of building. Here's how to decide quickly and confidently.

---

## The ITM project decision framework

Ask these questions in order:

### 1. Does the brief specify the technology?
**If yes** — use exactly what was specified. Don't be creative here. Marks are lost by using a different language or database than instructed.

### 2. Does your team have experience with it?
Using a new language under deadline pressure is high-risk. Familiarity beats novelty.

### 3. Does it fit the project type?

| Project type | Recommended |
|-------------|-------------|
| Console/CLI application | C++, Python, Java |
| Web application | Python (Flask/Django), Node.js, PHP |
| Database-heavy system | Any language + MySQL or SQLite |
| Data processing / analysis | Python |
| Mobile | React Native, Flutter |
| Systems-level / embedded | C++ |

---

## Database choice

| Database | When to use |
|----------|-------------|
| **SQLite** | Single-user desktop apps, prototypes, small systems |
| **MySQL / PostgreSQL** | Multi-user web apps, production systems |
| **File-based (CSV/text)** | Only if databases aren't required — very limited |

For most ITM student projects, **SQLite** is the right choice — no server setup, works everywhere, still proper SQL.

---

## The "good enough" rule

You don't need the best tool. You need a tool that:
- Works for the problem size
- You can use competently under time pressure
- Produces a working, demonstrable result

Pick familiar over perfect. A working project in a known language scores higher than a broken project in a trendy one.

---

💡 **If genuinely unsure:** Ask your lecturer what they recommend. They've seen hundreds of student projects and can save you days of wrong choices.
""",
"level": "all"
},

# ─────────────────────────────────────────────────────────────────────────
#  WRITING TECHNICAL REPORTS
# ─────────────────────────────────────────────────────────────────────────
{
"intent": "guide_technical_report",
"keywords": [
    "write technical report", "project report", "technical report",
    "project documentation", "write documentation", "system documentation",
    "how to write report", "report writing", "project write-up",
    "project write up", "technical writing", "project document",
    "user manual", "system manual", "project proposal writing",
    "write project proposal", "report structure", "report format",
],
"response": """
📄 **How to Write a Technical Report for ITM Projects**

A strong technical report proves you understand what you built and why. Lecturers read reports to assess understanding — not just to see what you submitted.

---

## Standard ITM project report structure

### 1. Title Page
Project title, names, student IDs, course, supervisor, date.

### 2. Table of Contents
Include page numbers. Update it last.

### 3. Abstract / Executive Summary (1 page)
What the system does, why it was built, what technologies were used, what the outcome was. Write this LAST even though it appears first.

### 4. Introduction
- Background context — why is this system needed?
- Problem statement — what problem does it solve?
- Objectives — what specifically will the system achieve?
- Scope — what's included and what's deliberately excluded?

### 5. Literature Review / Background Research
What existing solutions or research relate to your project? How does your approach compare?

### 6. Methodology / System Design
- Development approach used (Agile, waterfall, etc.) and why
- System architecture diagram (show the components and how they connect)
- Database design (ER diagram or schema)
- User interface mockups or wireframes

### 7. Implementation
- Tools and technologies used (and justification for each)
- Key features implemented
- Sample code snippets for important/complex sections
- Challenges encountered and how they were resolved

### 8. Testing
- Test cases (what you tested, expected result, actual result)
- User Acceptance Testing summary
- Known bugs or limitations

### 9. Results and Discussion
What did the system achieve? Does it meet the objectives? Evidence (screenshots, output samples).

### 10. Conclusion and Recommendations
Summary of what was accomplished. What would you do differently? What could be added in future?

### 11. References
Every source cited in the report. Use the required referencing style (usually APA for ITM).

### 12. Appendices
Full code listings, additional screenshots, survey results, user manual.

---

## Writing tips

- **Write daily** — don't leave the report for the last 2 days
- **Use screenshots** — one well-captioned screenshot is worth three paragraphs
- **Be specific** — "The system uses SQLite" not "The system uses a database"
- **Explain decisions** — not just what you did but WHY you chose that approach
- **Proofread** — grammatical errors reduce perceived technical competence

---

💡 **Quickest improvement:** Read your report aloud. Every sentence that sounds awkward when spoken should be rewritten.
""",
"level": "all"
},

]

# ═══════════════════════════════════════════════════════════════════════════
# SEED RUNNER
# ═══════════════════════════════════════════════════════════════════════════

def seed_guidance():
    app = create_app()
    with app.app_context():
        added = 0
        skipped = 0
        for entry in GUIDANCE_DATA:
            if KnowledgeBase.query.filter_by(intent_name=entry["intent"]).first():
                skipped += 1
                continue
            kb = KnowledgeBase(
                intent_name=entry["intent"],
                keywords=", ".join(entry["keywords"]),
                response_text=entry["response"].strip(),
                level=entry.get("level", "all"),
            )
            db.session.add(kb)
            added += 1

        db.session.commit()
        print(f"✅ Guidance seed complete — {added} entries added, {skipped} already existed.")

if __name__ == "__main__":
    seed_guidance()
