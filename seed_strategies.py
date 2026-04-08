#!/usr/bin/env python3
"""
seed_strategies.py
Predefined 13-week academic counseling strategies for all ITM courses.

Courses  : Programming | Database Management | Networking
Levels   : 100 | 200 | 300
Students : Regular (day) | Evening (working students)

Programming tracks:
  L100 → C++ Basics
  L200 → C++ Intermediate
  L300 → Visual Basic (Basics + Intermediate)

Each entry has:
  strategy    — practical, actionable advice for regular students
  evening_tip — adapted strategy for evening/working students

Run once from project root with venv active:
    python seed_strategies.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app
from server.extensions import db
from server.models.strategy import WeeklyStrategy

# ═══════════════════════════════════════════════════════════════════════════
#  HELPER
# ═══════════════════════════════════════════════════════════════════════════

def s(course, level, week, topic, activity, strategy, evening_tip=""):
    return dict(course=course, level=level, week=week, topic=topic,
                activity=activity, strategy=strategy.strip(),
                evening_tip=evening_tip.strip())


# ═══════════════════════════════════════════════════════════════════════════
#  PROGRAMMING — LEVEL 100  (C++ Basics)
# ═══════════════════════════════════════════════════════════════════════════
PROG_100 = [
s("programming","100",1,
  "Introduction to C++ and Development Environment Setup","lecture",
  """Your goal this week is to get your environment working and write one line of code that compiles — nothing more.

Install a C++ compiler (MinGW on Windows or g++ on Linux/Mac) and a code editor like VS Code. The moment you see "Hello, World!" print on screen, you have crossed the most important barrier of this entire course.

Real-world parallel: Setting up your dev environment is like a carpenter building their workbench before making furniture. You do it once properly so every job after is easier.

Strategy:
• Install your tools on day 1 — do not postpone this to the night before the lab
• Type every example yourself — do not copy-paste. Your fingers need to learn the syntax
• When you get an error, read the full message before searching. The answer is often right there
• Keep a notebook of every error you solve this week — these will repeat""",
  "Install your compiler during lunch break using a phone hotspot if lab access is limited. VS Code works on low-spec machines. If you cannot install on a personal device this week, arrive 20 minutes before the first lab session to set up on lab computers."),

s("programming","100",2,
  "Variables, Data Types, and Input/Output (cin/cout)","lab",
  """This week is the foundation everything else is built on. A variable is just a labelled box — int holds whole numbers, float holds decimals, string holds text.

The winning strategy is to connect every data type to something physical:
  int students = 45;        → number of students in your class
  float gpa = 3.75;         → your GPA
  string name = "Emmanuel"; → your name on your ID card

Practice drill (do this every day):
  1. Write a program that asks for your name and age
  2. Run it, give it your real information
  3. Print a sentence using those inputs
  4. Change the data type of age to float — what changes?

Lab strategy: Do not move to the next exercise until the current one compiles AND gives correct output. Speed is not the goal — correctness is.""",
  "On your commute, mentally trace what data type fits everyday things around you (bus number = int, distance = float, destination = string). This trains your mind without a laptop. Do the practice drill during your 30-minute lab session — prioritise exercises 1 and 2 only if time is short."),

s("programming","100",3,
  "Operators and Expressions","lecture",
  """Operators are the actions — addition, comparison, logic. The most common trap students fall into this week is confusing = (assignment) with == (comparison).

Memory trick: = is giving, == is asking.
  x = 5;    → give x the value 5
  x == 5    → asking: is x equal to 5?

Real-world practice: Write a program that calculates your total phone credit after adding GHS 5 and spending GHS 2.50. Use arithmetic operators. Then check if your remaining credit is enough for a call (comparison operator).

Common mistake to avoid: Dividing two integers gives an integer result.
  7 / 2 = 3  (not 3.5!)
  7.0 / 2 = 3.5  ← use float if you need the decimal

Write 5 short programs this week — one per operator type. Small focused programs teach more than one large messy one.""",
  "Study the operator table from your notes for 15 minutes before sleeping — no laptop needed. On lab day, focus on getting the arithmetic and comparison programs working. If you finish early, try the bonus: write a program that calculates overtime pay (hours × rate, with a condition for hours > 8)."),

s("programming","100",4,
  "Conditional Statements (if / else / switch)","lab",
  """Conditionals are the decision-making brain of your program. Every ATM, every traffic light, every login system uses this logic.

Real-world example: An ATM's logic is exactly:
  if (pin_correct && balance >= amount)
      dispense cash
  else if (pin_correct && balance < amount)
      print "insufficient funds"
  else
      print "wrong PIN"

This week's practice challenge — build a grade classifier:
  Input a score (0-100)
  Output: "A" (80+), "B" (70-79), "C" (60-69), "D" (50-59), "F" (below 50)

This one program exercises every concept: input, variables, if/else if/else, comparison operators, output.

Strategy: Write the logic in plain English FIRST (pseudocode), then translate to C++. Students who code directly without planning make more errors than those who spend 3 minutes planning.""",
  "Write the pseudocode for your grade classifier on paper or your phone notes during your commute. When you reach the lab, your only job is translating what you already planned. This cuts a 2-hour lab down to 40 minutes of actual coding."),

s("programming","100",5,
  "Loops (for / while / do-while)","lab",
  """Loops are where most Level 100 students lose confidence. The key insight: all three loop types do the same thing — repeat code. The difference is only in when you check the condition.

Use this mental model:
  for loop    → when you know EXACTLY how many times (print 13 weekly topics)
  while loop  → when you repeat UNTIL something happens (keep asking for password until correct)
  do-while    → when you need to run at LEAST once (show a menu, then check if user wants to exit)

Practice ladder (do in this order):
  Level 1: Print numbers 1 to 10 (for loop)
  Level 2: Print even numbers 1 to 20 (for loop + condition)
  Level 3: Keep asking for a password until the user gets it right (while loop)
  Level 4: Show a menu and repeat until user chooses "Exit" (do-while)

The most common bug: infinite loops. If your program freezes, your loop condition is never becoming false. Press Ctrl+C to stop it and re-check your condition.""",
  "Before lab: trace the Level 1 and Level 2 programs by hand on paper (write what the variable equals at each step). Tracing manually prevents the infinite loop bug. In lab, complete levels 1-3. Level 4 is your bonus challenge if time allows."),

s("programming","100",6,
  "Functions","lecture",
  """Functions are the single most important concept in this course. Every professional program is built from functions. A function is simply a named block of code you can call repeatedly.

Real-world parallel: A function is like your campus printer. You press Print (call the function), give it a document (parameter), and it returns a printed page (return value). You don't need to know how it works internally — you just use it.

This week's core challenge — rewrite your grade classifier from Week 4 using functions:
  float getScore()                → asks user for input, returns the float
  string getGrade(float score)    → takes a score, returns the grade letter
  void displayResult(string grade)→ prints the final result

Split programs like this until it becomes automatic. Every time you write more than 20 lines in main(), ask: should this be its own function?

Common mistake: forgetting the return statement. Your function promises to return something — keep that promise.""",
  "On your commute: mentally split real tasks into functions. 'Making breakfast': getIngredients(), cookEggs(int minutes), servePlate(). This builds function-thinking without a laptop. In lab: focus on getting the grade classifier refactored — it's the same code you already wrote, just reorganised."),

s("programming","100",7,
  "Arrays","lab",
  """An array is a row of boxes, each with a number. Think of your class attendance sheet — 45 rows, each holding a student's score. That's an array.

  float scores[45];  → 45 boxes, each holding a float

The most common bug: going out of bounds.
  scores[45] does not exist in a 45-element array.
  The last valid index is scores[44].

Memory trick: arrays START at 0, not 1. A class of 45 students uses indices 0 to 44.

Practice program — Student Grade Book:
  1. Create an array of 5 student scores
  2. Fill it using a for loop (ask for each score)
  3. Calculate the average
  4. Find the highest and lowest score
  5. Print all scores with their index number

This single program uses: arrays, loops, functions, conditionals — everything from the past 6 weeks.""",
  "The grade book program is your lab target. If you only finish steps 1-3, that's fine — calculating the average proves you understand arrays and loops working together. Steps 4-5 are extensions. Evening students: pair up if possible for this lab — explaining your logic to a partner reveals bugs faster than staring at the screen."),

s("programming","100",8,
  "Strings and String Manipulation","lecture",
  """A string in C++ is a sequence of characters. Think of it as an array of letters. The string class gives you powerful tools to work with text without managing memory manually.

Essential string operations to master this week:
  string name = "Emmanuel";
  name.length()           → 8 (how many characters)
  name.substr(0, 3)       → "Emm" (first 3 characters)
  name.find("man")        → 2 (position where "man" starts)
  name + " Asante"        → "Emmanuel Asante" (concatenation)

Real-world application: Every login form that checks if a username contains "@" or a password is "at least 8 characters" uses string operations.

Practice challenge: Write a program that takes a full name, splits it into first and last name, and prints a formal greeting: "Good morning, Mr/Ms [Last Name]". This uses substr(), find(), and length() in one program.""",
  "Read through the string methods list before lab and mark the 4 you don't yet understand. Focus your lab time specifically on those 4. Evening students often already use string logic at work (data entry, name formatting) — connect what you're coding to what you do daily."),

s("programming","100",9,
  "Pointers and References (Introduction)","lab",
  """Pointers are the concept most Level 100 students fear. The fear is unearned — a pointer is simply a variable that stores a memory address instead of a value.

  int x = 10;
  int* ptr = &x;   → ptr holds the address WHERE x lives in memory
  *ptr             → the value at that address (10)

Best analogy: Your physical address is a pointer. It doesn't hold you — it tells the postman WHERE to find you. &x is "give me the address of x". *ptr is "go to that address and get what's there."

Strategy for this week:
  Step 1: Draw it on paper. A box labelled x holding 10. An arrow from ptr to that box.
  Step 2: Write the code to match your drawing.
  Step 3: Print both the address (&x) and the value (*ptr) using cout.
  Step 4: Change x to 20 and print *ptr again. Did it change? Why?

Work through these 4 steps before attempting any lab exercise. Students who draw first write correct code faster.""",
  "Spend 10 minutes drawing the pointer diagram (box → arrow → box) before lab. This 10-minute investment prevents the confusion that causes other students to waste the entire session. In lab, focus on getting steps 1-3 working. Step 4 is the 'aha' moment — do not miss it."),

s("programming","100",10,
  "Structures (struct)","lecture",
  """A struct groups related variables under one name. Think of a student record: every student has a name, ID number, and GPA. Instead of three separate variables, a struct holds all three together.

  struct Student {
      string name;
      int id;
      float gpa;
  };

Real-world parallel: Every database record, every contact in your phone, every row in an Excel sheet is essentially a struct. You are building the mental model for database tables this week.

This week's practice — Student Registry:
  Create a Student struct
  Build an array of 5 students
  Fill each student's details using a loop
  Write a function that prints a student's record
  Write a function that finds the student with the highest GPA

If you can write this program, you are fully ready for the Object-Oriented Programming coming next semester.""",
  "The student registry program directly mirrors the kind of system you will build in your final project. Invest fully in this lab. Evening students who work in admin roles — think of your employer's staff database. You're coding the backend logic of what that system does."),

s("programming","100",11,
  "File Handling (Reading and Writing to Files)","lab",
  """File handling lets your program remember data after it closes. Every system that saves data — your phone contacts, a bank's transaction history — uses file input/output.

  ofstream outFile("students.txt");   → open file for writing
  outFile << name << " " << gpa;      → write to file
  outFile.close();

  ifstream inFile("students.txt");    → open file for reading
  inFile >> name >> gpa;              → read from file
  inFile.close();

Practice strategy: Combine with your Week 10 struct program.
  1. Save 3 student records to a file
  2. Close the program completely
  3. Re-open and read the records back
  4. Print them to the screen

If the data survives the program closing and re-opening, you've succeeded. That's the entire goal of file handling.""",
  "Evening students: file handling is directly relevant to office work — saving reports, reading data files. Think of ofstream as 'Save As' and ifstream as 'Open'. In lab, focus on getting the save-and-read cycle working with at least one student record. Three records is the full target."),

s("programming","100",12,
  "Project Work and Code Review","project",
  """This is your integration week. Everything from Weeks 1-11 comes together in your project.

Before writing a single line of project code, do this:
  1. Read the project brief twice (highlight deliverables and marks allocation)
  2. List every feature required
  3. Match each feature to the concepts you know (which week did you learn this?)
  4. Build the simplest working version first — ugly but functional
  5. Then add polish

Code review strategy — check your own code for:
  ✓ Does every function have a clear, single purpose?
  ✓ Are all arrays accessed within bounds?
  ✓ Do all files get closed after opening?
  ✓ Does the program handle wrong input (e.g. letter when expecting a number)?
  ✓ Is the output readable — formatted and labelled?

Pair review: Swap code with a classmate. Read their code out loud. You'll spot each other's bugs faster than finding your own.""",
  "Evening students: use one focused 90-minute session for project work rather than scattered 15-minute attempts. Set a timer. At the 90-minute mark, stop and document what works and what's left. This prevents the Sunday-night panic. If stuck on a specific feature, WhatsApp your study group the exact error message — not just 'my code doesn't work'."),

s("programming","100",13,
  "Final Exam Preparation and Project Submission","exam_prep",
  """Exam preparation for a programming course is different from a theory course. You cannot memorise your way through it — you must be able to write code under time pressure.

One week before exam strategy:
  Day 1: Redo every lab exercise from Weeks 1-6 without looking at solutions
  Day 2: Redo labs from Weeks 7-11
  Day 3: Do past exam questions under timed conditions (45 minutes per question)
  Day 4: Focus on your two weakest topics only
  Day 5: Light review — read through your code notebook, rest early

In the exam:
  → Read all questions before starting
  → Start with the question you're most confident about
  → Write pseudocode first for complex logic questions
  → Partial marks exist — an incomplete working function scores better than nothing
  → Comments show the examiner you understand your intent even if syntax is wrong""",
  "Evening students — 3 days before exam: do one lab exercise per night (45 minutes max). Night before: review your code notebook and sleep by 10pm. Fatigue kills recall more than any lack of preparation. On exam day, eat before you go in — a hungry brain cannot debug."),
]

# ═══════════════════════════════════════════════════════════════════════════
#  PROGRAMMING — LEVEL 200  (C++ Intermediate)
# ═══════════════════════════════════════════════════════════════════════════
PROG_200 = [
s("programming","200",1,
  "OOP Review and Class Design Principles","lecture",
  """You enter Level 200 already knowing syntax. The shift now is from writing code that works to writing code that is organised. OOP is the framework for that organisation.

The 4 pillars in one real-world sentence:
  Encapsulation → a bank account hides its balance; you use deposit() and withdraw(), not direct access
  Inheritance   → a SavingsAccount IS-A BankAccount with extra rules
  Polymorphism  → processAccount(account) works whether it's savings or current
  Abstraction   → you drive a car without knowing how the engine works

This week: redesign your Level 100 Student struct as a full Student class.
  Private: name, id, gpa (hidden from outside)
  Public: constructor, getName(), getGpa(), setGpa(), display()

If you can explain WHY each variable is private and each method is public, you understand encapsulation — the hardest pillar to grasp initially.""",
  "On your commute, identify 3 real systems around you (payroll at work, till system at a shop, attendance register) and mentally list what their private data and public methods would be. This is OOP design thinking without a laptop."),

s("programming","200",2,
  "Classes and Objects — Constructors and Access Specifiers","lab",
  """This week is where theory becomes code. A class is the blueprint; an object is the building.

  BankAccount acc1("Kwame", 500.00);  → creating an object from the blueprint

Constructor strategy — always write 3 versions:
  Default constructor    → BankAccount()  (no arguments, sets safe defaults)
  Parameterized          → BankAccount(string name, float balance)
  Copy constructor       → BankAccount(const BankAccount& other)

Lab exercise approach:
  1. Write the class definition in a header file (.h)
  2. Write the method implementations in a .cpp file
  3. Test in main.cpp by creating 3 different objects
  4. Call every method on each object and verify output

Students who write the header first (interface before implementation) make fewer design errors than those who code directly in one file.""",
  "Split the class across header and implementation files even in lab — it takes 5 extra minutes to set up but trains the professional habit. Evening students who work with software systems: the class/object pattern is exactly how enterprise systems like ERP and HR software are structured internally."),

s("programming","200",3,
  "Inheritance — Base and Derived Classes","lecture",
  """Inheritance lets a new class absorb all the behaviour of an existing class and add its own. The keyword is IS-A: a Car IS-A Vehicle. A LecturerAccount IS-A UserAccount.

Real-world example from UPSA:
  class Person { name, id, getDetails() }
  class Student : public Person { gpa, level, getAcademicRecord() }
  class Lecturer : public Person { department, getCourses() }

Both Student and Lecturer inherit name, id, and getDetails() without rewriting them. Any change to Person automatically applies to both.

This week's challenge: Build a 3-level hierarchy.
  Shape → has area variable and getArea() (returns 0 by default)
  Circle : Shape → overrides getArea() with π × r²
  Rectangle : Shape → overrides getArea() with width × height

Test it: create one Circle and one Rectangle object. Call getArea() on both. If both return correct values, inheritance is working.""",
  "Trace the inheritance chain on paper before coding. Draw the parent class, then arrow down to child classes, listing what each adds. Students who plan the hierarchy before opening their IDE produce cleaner code and finish faster in lab."),

s("programming","200",4,
  "Polymorphism and Virtual Functions","lab",
  """Polymorphism means one function name, multiple behaviours. The magic is virtual functions — they let the program decide at runtime which version to call based on the actual object type.

  Shape* shapes[3];
  shapes[0] = new Circle(5);
  shapes[1] = new Rectangle(4, 6);
  shapes[2] = new Triangle(3, 8);
  for (int i = 0; i < 3; i++)
      cout << shapes[i]->getArea();   ← calls the RIGHT version automatically

Without virtual: always calls Shape::getArea() (wrong)
With virtual:    calls the correct child class version (right)

Lab strategy: Take your Week 3 Shape hierarchy and add the virtual keyword. Then store objects in an array of base class pointers (as above) and loop through calling getArea(). If each shape gives the correct area, polymorphism is working.

This pattern — one interface, many implementations — is the foundation of every plugin system, game engine, and payment gateway in existence.""",
  "If lab time is limited, focus on getting Circle and Rectangle working polymorphically. Triangle can be homework. The core insight (virtual + base pointer = correct child method) is more important than having all three shapes."),

s("programming","200",5,
  "Operator Overloading","lecture",
  """Operator overloading lets you define what +, -, ==, and << mean for your custom classes.

Real-world illustration:
  For strings: "Hello" + " World" = "Hello World"  (+ means concatenation)
  For numbers: 5 + 3 = 8  (+ means addition)
  For your Vector class: v1 + v2 adds x and y components

Why it matters: When you overload << for your class, you can do:
  cout << myStudent;  → prints all student details cleanly

Practice this week — overload 3 operators for a Vector2D class:
  operator+    → adds two vectors (x1+x2, y1+y2)
  operator==   → checks if two vectors are identical
  operator<<   → prints "Vector(x, y)"

Common mistake: forgetting to return *this in assignment-style operators. Draw out what each operator must return before writing the code.""",
  "Operator overloading is heavily tested in exams. Make sure you understand the syntax (return type, parameter, const placement) by writing each operator twice — once with your notes, once from memory. Evening students: 20 minutes of this daily beats a 3-hour cramming session."),

s("programming","200",6,
  "Dynamic Memory Allocation (new / delete)","lab",
  """Dynamic memory lets you allocate exactly as much memory as you need, exactly when you need it — not fixed at compile time.

Real-world parallel: Static arrays are like buying a fixed-size box. Dynamic arrays are like a bag that grows as you put things in. std::vector uses this under the hood.

  int* arr = new int[n];   → allocate n integers at runtime
  // ... use the array ...
  delete[] arr;            → ALWAYS free what you allocate

The golden rule: Every new must have a delete. Memory you allocate and never free is a memory leak — your program slowly eats RAM until it crashes.

Lab discipline this week:
  After every new → immediately write the matching delete below it (before writing the code in between)
  Run your program with valgrind if available, or manually check every allocation

Practice: Write a function that dynamically creates an array of students, fills it, prints it, then deletes it. Call this function 1000 times in a loop. If your RAM usage doesn't grow, you have no leaks.""",
  "Memory management is where evening students who work in IT support encounter real consequences — poorly written software that leaks memory slows down servers over time. Connect your learning to that. In lab: the allocate-use-delete pattern must become automatic this week."),

s("programming","200",7,
  "Templates — Generic Programming","lecture",
  """Templates let you write a function or class once and have it work for any data type. This is how the entire C++ Standard Library is built.

  template <typename T>
  T getMax(T a, T b) {
      return (a > b) ? a : b;
  }
  getMax(3, 5)       → returns 5 (int version)
  getMax(3.2, 5.7)   → returns 5.7 (float version)
  getMax("A", "Z")   → returns "Z" (string version)

One function. Every data type. No repetition.

This week's exercise: Write a template Stack class with push(), pop(), peek(), and isEmpty() operations. Test it with:
  Stack<int>    → push integers
  Stack<string> → push strings
  Stack<float>  → push floats

If all three work without changing the class, templates are working. This stack implementation is also your first data structure — a skill you'll use heavily in advanced courses.""",
  "The template concept is abstract — ground it with the stack exercise. Evening students: a stack is exactly how your browser's Back button works (pages are pushed as you visit, popped as you go back). Building this makes the concept concrete and memorable."),

s("programming","200",8,
  "Exception Handling (try / catch / throw)","lab",
  """Exception handling is the professional way to deal with errors — instead of crashing, your program catches the problem and responds gracefully.

Real-world example: Every banking app uses exception handling.
  try {
      withdraw(amount);
  } catch (InsufficientFundsException& e) {
      cout << "Cannot withdraw: " << e.what();
  } catch (InvalidAmountException& e) {
      cout << "Amount must be positive";
  }

Without this, the app would crash if you tried to withdraw more than your balance.

Lab practice — add exception handling to your BankAccount class:
  1. Throw InsufficientFundsException when balance < withdrawal amount
  2. Throw InvalidAmountException when amount <= 0
  3. Catch both in main() with meaningful messages
  4. Prove it works by deliberately triggering each exception

Students who test their error paths are better programmers than those who only test the happy path.""",
  "Exception handling is one of the most practical skills in this course — it's what separates student code from professional code. Evening students who work with software: you've seen error dialogs. This week you learn how to write them. Focus your lab time on triggering all three scenarios (happy path + both error paths)."),

s("programming","200",9,
  "STL Containers — vector, map, set","lecture",
  """The Standard Template Library (STL) gives you production-ready data structures so you don't have to build them yourself. Knowing these saves thousands of lines of code in your career.

The three you must master this week:
  vector<T>       → a dynamic array that grows automatically
  map<K,V>        → a dictionary — look up a value by key (like Python's dict)
  set<T>          → a collection of unique items, always sorted

Real-world applications:
  vector<Student> → your student registry, growable
  map<string,int> → word frequency counter ("hello" → 5 times)
  set<string>     → a list of unique enrolled courses (no duplicates)

Practice challenge: Build a simple phone book.
  map<string, string> phoneBook;
  → Add contacts (name → number)
  → Look up a number by name
  → Delete a contact
  → Check if a contact exists before looking them up

This program teaches the map interface in one practical session.""",
  "STL containers appear in almost every C++ exam at Level 200. On your commute, think of 3 real datasets around you and which container fits best (vector, map, or set). In lab, build the phone book — it's a 30-line program that covers the full map interface."),

s("programming","200",10,
  "File Handling — Advanced (Binary Files, File Streams)","lab",
  """You saved text files in Level 100. This week you learn binary files — faster, smaller, and more suitable for structured data like student records.

  Student s = {"Ama", 1001, 3.8};
  ofstream out("records.bin", ios::binary);
  out.write((char*)&s, sizeof(s));   → write the raw bytes of the struct

Binary vs text:
  Text file  → human-readable, larger, slower to parse
  Binary file → machine-readable, smaller, faster, exact copy of memory

Practice: Save 5 Student objects to a binary file. Close the program. Open and read them back. Verify all fields (name, id, gpa) are exactly what you saved.

Advanced extension: Add append mode — the program should add new students to the file without overwriting existing ones. This simulates how a real database file grows over time.""",
  "Binary file handling is the bridge between C++ programming and your Database Management course. Evening students who have handled spreadsheets or CSV exports at work — binary files are the next level of that. Lab target: get save-and-read working for 1 student record. All 5 is the full target."),

s("programming","200",11,
  "Data Structures — Linked Lists and Stacks","lab",
  """This week you build what the STL gives you for free — to understand how it works underneath.

A linked list is a chain: each node holds a value AND a pointer to the next node. There's no fixed size like an array. It can grow anywhere in memory.

  struct Node {
      int data;
      Node* next;
  };

Operations to implement:
  insertAtFront(value)  → add a new node at the beginning
  insertAtEnd(value)    → add at the end
  deleteNode(value)     → find and remove a node
  displayList()         → print all nodes

Real-world parallel: Your browser history is a linked list — pages are added to the front (insertAtFront) and deleted when you clear history.

Strategy: Draw every insertion and deletion on paper FIRST. Show the pointers changing. Then code what you drew. Students who draw before coding get linked lists right on the first attempt.""",
  "Draw before you code — this is non-negotiable for linked lists. The pointer manipulation is impossible to get right by trial and error. In lab: implement insertAtFront and displayList first (40 minutes). insertAtEnd and deleteNode are extensions. Evening students: pair up — one draws, one codes, then swap."),

s("programming","200",12,
  "Design Patterns — Singleton, Factory, Observer","lecture",
  """Design patterns are proven solutions to common programming problems. They are the shared language of professional programmers.

Three patterns to master this week:

  Singleton — ensures only ONE instance of a class exists
  Real use: your database connection. You never want two separate connections to the same database.

  Factory — a class that creates objects without specifying the exact class
  Real use: a NotificationFactory that creates Email, SMS, or Push notifications based on user preference

  Observer — objects subscribe to events and are notified automatically
  Real use: when a student submits an assignment, the Lecturer object and the Gradebook object both get notified

Study strategy: For each pattern, find ONE real system you use daily that uses it. Explaining a pattern through a real example you chose is how you prove understanding in an exam — not by reciting definitions.""",
  "Patterns appear in Level 300 coursework and in job interviews. Evening students who work in IT — you've used systems built with these patterns. The Singleton is the session manager on every web application. Identify these in your workplace systems this week."),

s("programming","200",13,
  "Final Exam Preparation — OOP Mastery Review","exam_prep",
  """Level 200 exams test your ability to design and implement OOP solutions, not just recall syntax.

Exam preparation strategy — one concept per day:
  Day 1: Write a full class hierarchy from memory (Animal → Dog → GoldenRetriever)
  Day 2: Implement virtual functions and test polymorphism
  Day 3: Write a program using STL (vector + map in one program)
  Day 4: Past exam questions — 45 minutes per question, timed
  Day 5: Weak spots only. Review your error notebook.

In the exam:
  → Class design questions: draw the UML diagram before writing code
  → Always add access specifiers (public/private)
  → Virtual functions in base class when polymorphism is needed
  → If asked to 'design a system', think: what classes exist? what do they inherit? what do they share?

Partial marks are significant at Level 200. A class with correct attributes and method signatures, even if the method bodies are incomplete, can score 60-70% of the marks.""",
  "Evening students: do one timed past-question per night for the 5 nights before the exam. 45 minutes. No notes. Mark yourself. Review what you got wrong the next morning for 10 minutes. This pattern is more effective than reading notes for 3 hours."),
]

# ═══════════════════════════════════════════════════════════════════════════
#  PROGRAMMING — LEVEL 300  (Visual Basic — Basics + Intermediate)
# ═══════════════════════════════════════════════════════════════════════════
PROG_300 = [
s("programming","300",1,
  "Introduction to Visual Basic and the IDE","lecture",
  """Visual Basic operates in a completely different paradigm from C++. C++ runs code line by line (procedural flow). VB waits for the user to do something, then runs code (event-driven flow).

The shift to understand immediately: you no longer write a main() that runs from top to bottom. You write event handlers that run WHEN something happens.

Button1_Click  → runs when user clicks Button1
TextBox1_TextChanged → runs when user types in a text box
Form1_Load     → runs when the form opens

IDE setup strategy:
  1. Open Visual Studio and create a new Windows Forms Application
  2. Add one button to the form
  3. Double-click it to auto-generate the click handler
  4. Add: MessageBox.Show("My first VB event!")
  5. Run it (F5). Click the button.

If the message box appears, you understand event-driven programming. The rest of this course builds on that moment.""",
  "Visual Studio is a large install — download it during the day on campus Wi-Fi if home internet is limited. The Community edition is free. Evening students: if lab access is limited this week, watch the IDE walkthrough video from your course materials on your phone. The first lab exercise (button + message box) takes 15 minutes once you know the steps."),

s("programming","300",2,
  "Controls, Properties, Variables and Data Types in VB","lab",
  """VB data types are similar to C++ but with key differences. VB is more forgiving but precision matters.

Core types:
  Integer   → whole numbers (-32768 to 32767)
  Long      → large whole numbers (use for IDs and counts)
  Double    → decimal numbers
  String    → text
  Boolean   → True or False
  Date      → date and time values

Controls are the visual building blocks: TextBox, Label, Button, ComboBox, ListBox, DataGridView.

Lab exercise — Student Information Form:
  Form with: TextBox (name), TextBox (ID), ComboBox (level: 100/200/300), Button (Display)
  On button click: build a string from the inputs and show it in a Label
  Add validation: if name is empty, MessageBox.Show("Please enter your name")

This exercise combines controls, properties, variables, data types, and basic validation in one realistic form — exactly the kind of mini-system you'll build in your project.""",
  "Evening students: this lab exercise is a miniature version of every data entry form you've used at work. Think of it as building the frontend of a staff registration system. If you've submitted forms online, you've used what you're now building. Focus on the validation — that's what separates useful forms from broken ones."),

s("programming","300",3,
  "Event-Driven Programming and Control Flow","lecture",
  """Event-driven programming is the core philosophy of VB. Your program doesn't control when things happen — the user does. Your job is to respond correctly to any sequence of events.

Common events to handle:
  _Click         → button or control clicked
  _TextChanged   → text box content changed
  _SelectedIndexChanged → dropdown selection changed
  _Load          → form opened
  _FormClosing   → user tries to close the form

Real-world scenario: An ATM machine is event-driven.
  User inserts card → Card_Inserted event fires
  User types PIN    → each keypress fires KeyPress events
  User clicks OK    → Button_Click fires, system checks PIN

Strategy this week: Map your Student Information Form to this model.
  What should happen when the user clears the form? → Button_Clear_Click
  What should happen when level changes? → ComboBox_SelectedIndexChanged
  Should the Display button be disabled until name is entered? → TextBox_TextChanged enables it

Programming every possible user interaction — not just the happy path — is what makes a system production-ready.""",
  "Think through your form's events on paper before the lab. List every possible thing a user could do and what should happen. Students who plan events before coding make fewer logic errors. Evening students: your commute is perfect for this — no laptop needed, just a notepad."),

s("programming","300",4,
  "Control Structures in Visual Basic","lab",
  """VB control structures (if/else, select case, loops) are logically identical to C++ but with cleaner syntax.

VB Select Case is cleaner than nested if/else for multiple conditions:
  Select Case grade
      Case "A" : MessageBox.Show("Distinction — excellent work!")
      Case "B" : MessageBox.Show("Credit — well done!")
      Case "C" : MessageBox.Show("Pass — you met the standard")
      Case Else : MessageBox.Show("Below pass — speak to your lecturer")
  End Select

For loops in VB:
  For i = 1 To 13
      ListBox1.Items.Add("Week " & i)
  Next i

Lab exercise — Grade Classifier GUI:
  User enters a score (0-100) in a TextBox
  On button click: classify the grade using Select Case
  Display result in a coloured Label (green for A/B, amber for C, red for fail)
  Add a Clear button that resets all fields

This is the same grade classifier from Level 100 — now with a professional GUI and colour feedback.""",
  "The grade classifier is your fastest path to mastering VB control structures because you already know the logic from C++. The only new skill is displaying results visually. Evening students: focus on getting the classification working first, then add colour as an enhancement if time allows."),

s("programming","300",5,
  "Procedures, Functions, and Modules","lecture",
  """VB has two types of reusable code blocks:
  Sub    → a procedure that does something but returns nothing
  Function → does something AND returns a value

  Sub ClearForm()           ← no return value
      txtName.Text = ""
      txtID.Text = ""
      lblResult.Text = ""
  End Sub

  Function CalculateGrade(score As Double) As String  ← returns a String
      If score >= 80 Then Return "A"
      If score >= 70 Then Return "B"
      If score >= 60 Then Return "C"
      Return "F"
  End Function

Modules let you share Subs and Functions across multiple forms — essential once your project grows beyond one window.

Strategy this week: Refactor everything in your grade classifier into Subs and Functions.
  ValidateInput()  → Sub that checks if TextBox is empty
  GetGrade()       → Function that returns grade string
  DisplayResult()  → Sub that updates label and colour
  ClearForm()      → Sub that resets everything

If every button click calls only one procedure (which calls others), your code is well-structured.""",
  "The refactoring exercise is the most important lab this week — it builds the code organisation habit. Evening students: well-structured VB code is faster to debug at 9pm when you're tired. Take the 20 minutes to refactor properly now and save an hour of confusion later."),

s("programming","300",6,
  "Arrays and Collections in VB","lab",
  """VB gives you both traditional arrays and the more powerful ArrayList and List(Of T) collections.

  Dim scores(4) As Double          → fixed array of 5 doubles
  Dim names As New List(Of String) → dynamic list, grows as needed
  names.Add("Ama")
  names.Add("Kofi")
  names.Remove("Ama")
  names.Count                      → number of items

Real-world application: A ListBox control is backed by a collection. Every time you call ListBox1.Items.Add(), you're adding to the control's internal collection.

Practice — Student List Manager:
  Form with: TextBox (enter name), Button (Add), ListBox (shows names), Button (Remove selected)
  Behind the buttons: use a List(Of String) to manage the data
  Display the count in a Label: "3 students registered"
  Add a Clear All button that empties both the list and the ListBox

This small form uses arrays, collections, ListBox, and event handling together — exactly the scale of a complete feature.""",
  "The Student List Manager is a standalone feature you could include in your final project. Evening students: build it fully this week and save it — it may become part of your project later. Focus on Add and Remove working correctly before attempting Clear All."),

s("programming","300",7,
  "Form Design and UI/UX Best Practices","lecture",
  """Your application works — but does it look professional? In Level 300, presentation matters. A well-designed form signals competence to lecturers and future employers.

Professional VB form design rules:
  Layout: Group related controls (use GroupBox). Align everything on a grid.
  Labels: Every input has a label. Left-aligned, consistent font.
  Feedback: Every action gives feedback — success message, error message, or loading indicator.
  Validation: Inputs validated BEFORE processing. Error shown inline, not in a popup if possible.
  Navigation: Tab order set correctly (Tab key moves logically through the form)

Colour strategy for ITM projects:
  Use a consistent 2-colour scheme (e.g. navy + gold — a professional combination)
  Red only for errors
  Green only for success
  Avoid mixing more than 3 colours

This week: Redesign your existing form with these rules.
  Set consistent fonts (Segoe UI 10pt is clean and professional)
  Add GroupBoxes to organise sections
  Set the form title and icon
  Check Tab order (Properties → TabIndex)""",
  "Evening students: a well-designed form is your first impression in the project presentation. 45 minutes on layout and visual consistency makes your project look significantly more professional. This is not optional polish — it signals attention to detail to your assessors."),

s("programming","300",8,
  "Database Connectivity with ADO.NET","lab",
  """This is the most important lab in the Level 300 VB course. Connecting your form to a database transforms a toy app into a real system.

ADO.NET connection steps:
  1. Create a SQLite or Access database with a Students table
  2. Add System.Data to your imports
  3. Build a connection string
  4. Write an SqlConnection, SqlCommand, and SqlDataReader

  Dim conn As New SQLiteConnection("Data Source=students.db")
  conn.Open()
  Dim cmd As New SQLiteCommand("SELECT * FROM students", conn)
  Dim reader As SQLiteDataReader = cmd.ExecuteReader()
  While reader.Read()
      ListBox1.Items.Add(reader("name").ToString())
  End While
  conn.Close()

Lab target:
  1. Read all students from database and show in a DataGridView
  2. Add a new student using a form and INSERT statement
  3. Delete selected student with DELETE statement

If you complete all 3, you have a fully functional CRUD application.""",
  "Evening students: this lab is the core skill of your final project and directly mirrors real business software. If your lab session is short, prioritise step 1 (read and display). Steps 2 and 3 build on it. Do not leave without at least seeing your database data appear in a DataGridView — that moment makes everything concrete."),

s("programming","300",9,
  "File Handling and Data Export in VB","lab",
  """VB file handling uses StreamReader and StreamWriter — cleaner than C++ file streams.

  ' Write to file
  Dim writer As New StreamWriter("report.txt")
  writer.WriteLine("Student Report — " & Date.Now.ToString())
  writer.WriteLine("Name: " & txtName.Text)
  writer.Close()

  ' Read from file
  Dim reader As New StreamReader("report.txt")
  Dim content As String = reader.ReadToEnd()
  reader.Close()
  TextBox1.Text = content

Practical use cases for your project:
  Export student list to CSV → Excel can open it
  Save application settings to a config file
  Generate a text report that can be printed

Practice: Add an Export button to your Student List Manager from Week 6.
  Clicking it writes all student names to a .csv file
  Format: ID, Name, Level (one student per line)
  Show a SaveFileDialog so the user can choose where to save it""",
  "File export (especially to CSV) is a feature your project assessors will appreciate because it shows real-world usefulness. Evening students who manage data at work — you've exported reports before. This week you learn to generate them programmatically."),

s("programming","300",10,
  "Error Handling and Debugging in VB","lecture",
  """Professional VB applications never crash — they catch errors and respond gracefully.

  Try
      Dim amount As Double = Convert.ToDouble(txtAmount.Text)
      ProcessPayment(amount)
  Catch ex As FormatException
      MessageBox.Show("Please enter a valid number", "Input Error", MessageBoxButtons.OK, MessageBoxIcon.Warning)
  Catch ex As Exception
      MessageBox.Show("Unexpected error: " & ex.Message, "Error")
  Finally
      ' Always runs — close connections, reset UI
  End Try

Debugging strategy in Visual Studio:
  1. Set breakpoints (F9) on suspicious lines
  2. Run in Debug mode (F5) — execution pauses at breakpoints
  3. Hover over variables to see their current values
  4. Step through code line by line (F10)

This week: Add Try-Catch to every database operation and every file operation in your existing code. An application that crashes on bad input fails in a presentation. An application that shows a friendly error message passes.""",
  "Error handling is your project's safety net. Evening students: add Try-Catch to database connections first — connection failures are the most common runtime error in project presentations. The 30 minutes you spend this week prevents the 30-second crash that can cost you marks on demo day."),

s("programming","300",11,
  "Reports and Printing in VB","lab",
  """Reports turn your data into professional printed output — a core feature of any business application.

Approach 1 — PrintDocument (built-in VB):
  Create a PrintDocument component
  Handle the PrintPage event to draw text and data
  Use e.Graphics.DrawString() to position text
  Call PrintDocument1.Print() to trigger printing

Approach 2 — Export to formatted text/PDF (simpler):
  Build an HTML string from your data
  Save as .html and open in the browser for printing
  Or use a free library like iTextSharp for direct PDF output

Your project report feature strategy:
  At minimum: export a formatted text report (student list, grade summary, or transaction log)
  Better: a DataGridView with a Print Preview button
  Best: a styled HTML report that opens in the browser

Pick the approach that matches your time. A simple working text report beats a complex broken PDF generator every time.""",
  "Evening students: the HTML report approach is the fastest to implement and gives the most professional result. Spend 45 minutes this week adding it to your project. It typically adds 10-15 marks to a project that otherwise works well but lacks a report feature."),

s("programming","300",12,
  "Intermediate Project Development and Integration","project",
  """This is your full integration week. All 11 weeks of skills come together.

Project integration checklist:
  ✓ Forms connected to database (CRUD working)
  ✓ Input validation on every form
  ✓ Error handling on all database and file operations
  ✓ At least one report or export feature
  ✓ Consistent form design (layout, colours, fonts)
  ✓ All buttons labelled clearly and all tabs/navigation working

Testing your project like a user:
  Give your project to someone who didn't write it
  Watch them use it without explaining anything
  Every time they hesitate or make an error, note it
  Fix the top 3 confusion points

Common last-minute project failures:
  → Database path hardcoded to your laptop (use relative paths or a file dialog)
  → Application crashes when TextBox is empty (add validation)
  → Form too small to see all controls on a different screen resolution (test at 1366x768)""",
  "Evening students: use your weekend for a focused 3-hour integration session rather than scattered weeknight work. Set the goal: by Sunday evening, all CRUD operations work. Monday and Tuesday evenings are for polish, validation, and testing. Wednesday is documentation. Submit by Thursday."),

s("programming","300",13,
  "Final Project Submission and Exam Preparation","exam_prep",
  """VB exams at Level 300 test your ability to design event-driven solutions and explain database integration decisions.

Exam preparation focus areas:
  Event-driven programming concepts (what fires when, why)
  ADO.NET connection lifecycle (open → query → read → close)
  Form design principles (which control for which purpose)
  Error handling (when to use Try-Catch, what to catch)
  Difference between Sub and Function, and when to use each

Practical exam strategy:
  Write a complete VB form from scratch under timed conditions (1 hour)
  Form: simple login screen that checks username/password against a database
  This tests: TextBox, Button, event handling, ADO.NET, conditional logic, MessageBox

For viva/demo presentations:
  Explain your design decisions, not just what the code does
  "I used ADO.NET with SQLite because it requires no server setup and the database file travels with the application"
  Examiners award marks for rationale, not just function""",
  "Evening students: project submission and exam are within the same week. Prioritise submission over exam revision until the project is done. A submitted project with minor bugs scores more than a perfect exam with no project. Once submitted: 3 focused exam revision sessions of 45 minutes each over the remaining days."),
]

# ═══════════════════════════════════════════════════════════════════════════
#  DATABASE MANAGEMENT — LEVEL 100
# ═══════════════════════════════════════════════════════════════════════════
DB_100 = [
s("database","100",1,
  "Introduction to Databases and Database Systems","lecture",
  """A database is an organised, persistent store of related data. Before you learn a single SQL command, understand WHY databases exist.

Real-world problem databases solve: UPSA stores 10,000 student records. If those records were in an Excel file, two administrators editing it simultaneously would destroy each other's changes. A database prevents that — and does much more.

What databases give you that files don't:
  Concurrent access → many users read and write at the same time
  Data integrity → rules that prevent wrong data (a student can't have a GPA of 6.0)
  Fast retrieval → find one student among millions in milliseconds
  Recovery → survive power failures without losing data

This week's strategy: compare every database concept to a physical filing cabinet you understand.
  Table → a labelled drawer in the cabinet
  Row → one folder (one student's complete record)
  Column → one item inside every folder (everyone's ID number)
  Primary Key → the unique reference number on each folder""",
  "Evening students: if you work in an office, you use databases daily — student portals, payroll systems, inventory software are all databases at the back. This week connects what you see on screen to what the course teaches. That connection makes the abstract concrete."),

s("database","100",2,
  "Data Models and Entity-Relationship Diagrams","lecture",
  """Before building a database, you design it. The ER diagram is your blueprint — drawn before writing a single line of SQL.

ER diagram components:
  Entity    → a real-world thing you store data about (Student, Course, Lecturer)
  Attribute → a property of that entity (Student has: ID, Name, Level, GPA)
  Relationship → how entities connect (Student ENROLS-IN Course)
  Cardinality → how many (one student enrols in MANY courses; each course has MANY students)

The UPSA student system ER diagram:
  Student (StudentID, Name, Level, Programme)
  Course (CourseCode, CourseName, Credits, LecturerID)
  Enrolment (StudentID, CourseCode, Semester, Grade)

Strategy: For every ER diagram question in an exam, follow this sequence:
  1. Identify all entities (nouns in the problem description)
  2. Identify attributes for each entity
  3. Identify relationships (verbs: enrolls, teaches, manages)
  4. Determine cardinality (one-to-one, one-to-many, many-to-many)
  5. Identify the primary key for each entity

Cardinality is where marks are most commonly lost. Practise determining it for 5 real-world relationships this week.""",
  "Draw ER diagrams by hand — not on a computer. The act of drawing forces understanding. Evening students: diagram a real system from your workplace (staff records, inventory, clients). This makes the exercise meaningful and the exam answer comes from a real example you know deeply."),

s("database","100",3,
  "Relational Model, Keys, and Table Design","lecture",
  """The relational model turns your ER diagram into actual tables. This week you learn the rules that make a table correct.

Key types — know all four:
  Primary Key → uniquely identifies each row (StudentID — no two students share it)
  Foreign Key → a column that references another table's primary key (EnrolmentTable.StudentID → StudentTable.StudentID)
  Candidate Key → any column that COULD be a primary key
  Composite Key → two columns together form the unique identifier (StudentID + CourseCode in Enrolment)

The foreign key rule is what makes data consistent across tables. You cannot enrol a student who doesn't exist in the Students table. The database enforces this automatically.

This week's practice: Take the UPSA ER diagram from Week 2 and convert it to a relational schema.
  Students(StudentID PK, Name, Level, Programme)
  Courses(CourseCode PK, CourseName, Credits, LecturerID FK)
  Enrolment(StudentID FK, CourseCode FK, Semester, Grade) — composite PK

Draw the schema with lines connecting foreign keys to their primary keys. This visual makes relationships immediately clear.""",
  "The relational schema exercise is your most directly exam-tested skill this semester. Evening students: do this conversion exercise for 3 different scenarios (school system, hospital, library). Speed and accuracy on this in an exam comes from repetition, not memory."),

s("database","100",4,
  "SQL Fundamentals — SELECT, FROM, WHERE","lab",
  """SQL is the language of databases. This week you start speaking it. SELECT retrieves data. FROM tells SQL which table. WHERE filters which rows.

  SELECT name, gpa
  FROM students
  WHERE level = '200' AND gpa > 3.0;

Read it like English: "Show me the name and GPA of Level 200 students with a GPA above 3.0."

Practice with intention — not just running queries, but predicting output first:
  Write the query → predict what it will return → run it → compare
  If your prediction was wrong, find out why before moving on

5 queries to write this week (on a students table with 20 test records):
  1. All Level 100 students
  2. Students whose name starts with 'A'  (LIKE 'A%')
  3. Students with GPA between 2.0 and 3.5  (BETWEEN)
  4. All students sorted by GPA descending  (ORDER BY)
  5. Top 5 students by GPA  (LIMIT 5 with ORDER BY)

Every query you write this week builds the muscle memory that makes exam queries fast.""",
  "Evening students: SQL is the most immediately employable skill in this entire course. Employers use it daily. Spend at least 20 minutes practising queries outside of lab. SQLiteOnline.com works from any browser, no installation needed — use it on your phone during a break."),

s("database","100",5,
  "SQL Data Manipulation — INSERT, UPDATE, DELETE","lab",
  """SELECT reads data. INSERT, UPDATE, and DELETE change it. Together these 4 commands are called CRUD (Create, Read, Update, Delete) — the foundation of every database application.

  -- Add a new student
  INSERT INTO students (id, name, level, gpa)
  VALUES (1001, 'Ama Serwaa', '100', 0.0);

  -- Update her GPA after first semester
  UPDATE students SET gpa = 2.8 WHERE id = 1001;

  -- Remove a withdrawn student
  DELETE FROM students WHERE id = 1001;

Warning drills — practise these dangerous mistakes BEFORE you make them:
  UPDATE students SET gpa = 4.0;          ← NO WHERE clause — sets EVERYONE's GPA to 4.0!
  DELETE FROM students;                   ← deletes EVERY student record!

Golden rule: ALWAYS write the WHERE clause before executing UPDATE or DELETE. Test your WHERE with a SELECT first to confirm you're targeting the right rows.

Lab exercise: Build all 4 CRUD operations on your student table. Insert 5 students, update 2, delete 1, then SELECT to verify.""",
  "The WHERE clause rule is the most important safety habit in SQL. Evening students who work with databases: one accidental UPDATE without WHERE on a production system can be catastrophic. This week's lab is where that habit starts. Always SELECT first, then UPDATE/DELETE."),

s("database","100",6,
  "Aggregate Functions and GROUP BY","lab",
  """Aggregate functions summarise your data. Instead of seeing every row, you see counts, totals, averages, and extremes.

  COUNT(*)        → how many rows
  SUM(column)     → total of all values
  AVG(column)     → average value
  MAX(column)     → largest value
  MIN(column)     → smallest value

Real-world query: "How many students are in each level, and what is their average GPA?"
  SELECT level, COUNT(*) AS total, AVG(gpa) AS avg_gpa
  FROM students
  GROUP BY level;

Result:
  Level 100 | 45 students | avg GPA 2.8
  Level 200 | 38 students | avg GPA 3.1
  Level 300 | 29 students | avg GPA 3.3

HAVING filters GROUP BY results (like WHERE, but for groups):
  HAVING AVG(gpa) > 3.0  → only show levels where average GPA exceeds 3.0

Practice: Write 5 aggregate queries on your student data. For each, predict the result before running it.""",
  "Aggregate functions are heavily tested in exams. Evening students: these are the exact queries businesses run on sales data, payroll, and inventory every day. If your workplace has a database system, try to see what reports it generates — you'll recognise the GROUP BY logic behind them."),

s("database","100",7,
  "Joins — Combining Tables","lab",
  """Joins are the most powerful SQL concept. They let you combine data from multiple tables in a single query — essential because real databases always have multiple related tables.

The three joins to master:
  INNER JOIN → rows that exist in BOTH tables (students who have enrolled in at least one course)
  LEFT JOIN  → all rows from left table, matched rows from right (all students, even those not enrolled)
  RIGHT JOIN → all rows from right table, matched rows from left

  -- Students and their enrolled courses:
  SELECT s.name, c.course_name, e.grade
  FROM students s
  INNER JOIN enrolment e ON s.id = e.student_id
  INNER JOIN courses c ON e.course_id = c.id
  WHERE s.level = '200';

Visualisation strategy: Draw the two tables as overlapping circles (Venn diagram).
  INNER JOIN → the overlap only
  LEFT JOIN  → entire left circle + overlap
  RIGHT JOIN → entire right circle + overlap

Lab exercise: Join students, courses, and enrolment tables. Answer these questions using SQL:
  1. What courses is student ID 1001 enrolled in?
  2. Which students are enrolled in the Database Management course?
  3. Which students have not enrolled in any course yet? (LEFT JOIN + WHERE ... IS NULL)""",
  "Joins are the #1 most-tested SQL topic in Level 100 exams. Practice drawing the Venn diagram first, then writing the query. Evening students: Question 3 (finding un-enrolled students) is a common real-world HR/admin task — 'which staff members haven't completed their training?'"),

s("database","100",8,
  "Subqueries and Nested SELECT","lecture",
  """A subquery is a SELECT statement inside another SELECT. It answers questions that require two steps.

Question: "Which students have a GPA above the department average?"
Step 1: Calculate the average → SELECT AVG(gpa) FROM students
Step 2: Find students above it → WHERE gpa > (step 1 result)

Combined as a subquery:
  SELECT name, gpa
  FROM students
  WHERE gpa > (SELECT AVG(gpa) FROM students);

The inner query runs first, produces a value, and the outer query uses it. Read it from the inside out.

Types of subqueries:
  Scalar subquery  → returns one value (like the AVG example above)
  IN subquery      → returns a list: WHERE id IN (SELECT student_id FROM honour_roll)
  EXISTS subquery  → checks if rows exist: WHERE EXISTS (SELECT 1 FROM ...)

Practice: Write 3 subqueries for your student database.
  1. Students with GPA above average (scalar)
  2. Students enrolled in 'Database Management' course (IN)
  3. Students who have at least one grade recorded (EXISTS)""",
  "Subqueries appear in both exams and practical tests. Evening students: the pattern of 'find records that meet a condition based on another table' is exactly what business reports do (e.g., 'employees whose salary exceeds department average'). Mastering subqueries makes you genuinely useful in a data role."),

s("database","100",9,
  "Views and Indexes","lecture",
  """Views and indexes are your database optimisation tools — views simplify complex queries; indexes make queries faster.

A view is a saved query that looks like a table:
  CREATE VIEW level200_students AS
  SELECT name, id, gpa FROM students WHERE level = '200';

  -- Now you can query it like a real table:
  SELECT * FROM level200_students WHERE gpa > 3.0;

Benefits: hides complexity, controls what data users see, simplifies application code.

An index tells the database engine to build a fast lookup structure on a column:
  CREATE INDEX idx_student_level ON students(level);

Without index: database scans every row to find Level 200 students (slow with 10,000 records)
With index: database jumps directly to Level 200 records (fast)

When to use an index: on columns you frequently filter by (WHERE level = ...) or join on.
When NOT to: on columns that change very frequently (inserts/updates are slower with indexes).

Practice: Create a view for each level's students and a report view that joins students and courses.""",
  "Views are the basis of database security — you can grant users access to a view without giving them access to the underlying tables. Evening students who work with business databases: most of what you see in reports is querying views, not raw tables. This week makes that visible."),

s("database","100",10,
  "Normalisation — 1NF, 2NF, 3NF","lecture",
  """Normalisation is the process of structuring a database to reduce redundancy and prevent inconsistency. Most database exam questions at Level 100 are about normalisation.

The problem without normalisation:
  If you store a lecturer's name in every course row, and the lecturer changes their name,
  you must update every single row. Miss one → data inconsistency.

The 3 normal forms:
  1NF → each cell holds one value only. No repeating groups. (Split "Course1, Course2" into separate rows)
  2NF → no partial dependency. Every non-key attribute depends on the WHOLE primary key.
  3NF → no transitive dependency. Non-key attributes don't depend on other non-key attributes.

Exam strategy for normalisation questions:
  Step 1: Check 1NF — any multi-value cells? Any repeating columns (Course1, Course2, Course3)?
  Step 2: Identify the primary key. Is it composite?
  Step 3: Check 2NF — does every column depend on the FULL key, or just part of it?
  Step 4: Check 3NF — does any non-key column determine another non-key column?

Practice: Normalise this un-normalised table through to 3NF:
  StudentCourse(StudentID, StudentName, Level, CourseCode, CourseName, Credits, LecturerName, Grade)""",
  "Normalisation is worth significant marks in every Level 100 database exam. The example table in the practice exercise contains all three violations. Work through it step by step, creating new tables at each step. Evening students: do this exercise twice — once with notes, once without. That's your exam preparation for this topic."),

s("database","100",11,
  "Transactions and ACID Properties","lecture",
  """A transaction is a group of SQL operations that must ALL succeed or ALL fail together. No partial success allowed.

Real-world scenario: Transferring GHS 200 from Account A to Account B.
  Step 1: Deduct 200 from Account A
  Step 2: Add 200 to Account B

If step 1 succeeds and step 2 fails (power cut), Account A lost GHS 200 with nowhere to go. A transaction prevents this — if step 2 fails, step 1 is reversed (rolled back).

  BEGIN TRANSACTION;
      UPDATE accounts SET balance = balance - 200 WHERE id = 'A';
      UPDATE accounts SET balance = balance + 200 WHERE id = 'B';
  COMMIT;   -- save both changes together

ACID properties:
  Atomicity    → all or nothing (our bank transfer)
  Consistency  → data always valid (balance never negative if rules say so)
  Isolation    → concurrent transactions don't interfere
  Durability   → committed data survives crashes

Exam strategy: For ACID questions, always answer with a concrete banking or e-commerce example. Examiners give credit for correct examples, not just definitions.""",
  "ACID is a classic exam topic. Evening students: if you work in finance, retail, or logistics, your employer's systems depend on ACID properties for every transaction. Connecting this week's theory to real monetary transactions makes it memorable and exam-ready."),

s("database","100",12,
  "Database Design Project — Building a Mini System","project",
  """This week you design and build a small working database system that applies everything from the semester.

Recommended project: UPSA Course Registration System
  Tables: Students, Courses, Lecturers, Enrolment, Semesters
  SQL coverage:
    CREATE TABLE with proper keys and constraints
    INSERT data for at least 10 students, 5 courses, 3 lecturers
    SELECT queries using joins, aggregates, and subqueries
    UPDATE and DELETE with correct WHERE clauses
    At least one VIEW
    Normalised to 3NF

Project approach:
  Day 1: ER diagram on paper → relational schema
  Day 2: CREATE TABLE statements → insert test data
  Day 3: Write all required queries → test and fix
  Day 4: Add view → normalisation documentation
  Day 5: Write project report → final review

Document your design decisions: why you chose each primary key, why relationships are structured as they are, how normalisation was applied.""",
  "Evening students: use a 2-hour focused session per day this week rather than sporadic attempts. The project has 5 natural stages — one per session. By Friday, you have a complete, documented system. Evening students with SQL experience at work: this is your opportunity to apply that experience properly in an academic context."),

s("database","100",13,
  "Final Exam Preparation","exam_prep",
  """Level 100 database exams are typically 60% SQL queries and 40% theory (ER diagrams, normalisation, ACID).

SQL revision strategy:
  Write every type of query from memory:
    SELECT with WHERE, ORDER BY, LIMIT
    SELECT with GROUP BY, HAVING, aggregate functions
    INNER JOIN across 3 tables
    Subquery (scalar, IN, EXISTS)
    INSERT, UPDATE (with WHERE), DELETE (with WHERE)

Theory revision strategy:
  ER diagram: practise 3 different scenarios (hospital, library, online shop)
  Normalisation: do 2 full normalisation exercises (unnormalised → 3NF)
  ACID: know one real example per property
  Keys: be able to identify PK, FK, composite key in any table

Exam technique:
  For SQL questions: write the query, trace through it mentally, check the WHERE
  For ER questions: identify entities first, then relationships, then cardinality last
  For normalisation: work through each normal form in order — never skip""",
  "Evening students: 3 nights before exam — one SQL practice session per night (45 minutes, write queries without notes). Night before: ER diagram practice (30 minutes) + ACID examples review (15 minutes). Day of exam: review your own written notes only, not the textbook."),
]

# ═══════════════════════════════════════════════════════════════════════════
#  DATABASE MANAGEMENT — LEVEL 200
# ═══════════════════════════════════════════════════════════════════════════
DB_200 = [
s("database","200",1,
  "Advanced SQL — Stored Procedures and Functions","lecture",
  """Stored procedures are SQL programs stored in the database and executed by name. They reduce network traffic, enforce business rules, and can be called from any application.

  CREATE PROCEDURE EnrolStudent(
      @studentID INT, @courseCode VARCHAR(10), @semester INT
  )
  AS
  BEGIN
      -- Check student exists
      IF NOT EXISTS (SELECT 1 FROM Students WHERE id = @studentID)
          RAISERROR('Student not found', 16, 1);
      -- Insert enrolment
      INSERT INTO Enrolment(student_id, course_code, semester)
      VALUES (@studentID, @courseCode, @semester);
  END;

  -- Call it:
  EXEC EnrolStudent 1001, 'ITM301', 2;

Strategy this week: Identify 3 repetitive SQL operations in your Level 100 project (enrol student, calculate GPA, generate report) and convert them to stored procedures. This forces you to think about parameters, return values, and error conditions.""",
  "Evening students: stored procedures are how enterprise databases expose functionality to applications. Every time you log into a business system and it processes your data, a stored procedure is likely running. This week connects what you've always used to what you're now building."),

s("database","200",2,
  "Triggers — Automated Database Actions","lab",
  """A trigger is code that runs automatically when a specified event (INSERT, UPDATE, DELETE) happens on a table.

Real-world use: When a student's GPA drops below 1.5, automatically create an academic_alert record.

  CREATE TRIGGER CheckGPA
  AFTER UPDATE ON Students
  FOR EACH ROW
  BEGIN
      IF NEW.gpa < 1.5 AND OLD.gpa >= 1.5 THEN
          INSERT INTO AcademicAlerts(student_id, alert_date, reason)
          VALUES (NEW.id, CURDATE(), 'GPA dropped below 1.5');
      END IF;
  END;

Lab practice: Build 3 triggers on your student database:
  1. AFTER INSERT on Enrolment → log the enrolment in an audit table
  2. AFTER UPDATE on Students WHERE gpa changes → create an alert if GPA < 1.5
  3. BEFORE DELETE on Students → prevent deletion if the student has active enrolments

Test each trigger by performing the triggering action and verifying the side effect occurred.""",
  "Triggers are widely misunderstood and therefore heavily tested. Evening students: triggers are how accounting systems enforce double-entry rules automatically. Every financial software you've used enforces constraints through trigger-like mechanisms. Get your 3 triggers working and tested this week — partial implementation scores less than 3 simple working ones."),

s("database","200",3,
  "Cursors — Row-by-Row Processing","lecture",
  """Cursors let you process query results one row at a time — essential when set-based SQL cannot express the required logic.

  DECLARE student_cursor CURSOR FOR
      SELECT id, name, gpa FROM Students WHERE level = '200';

  OPEN student_cursor;
  FETCH NEXT FROM student_cursor INTO @id, @name, @gpa;

  WHILE @@FETCH_STATUS = 0
  BEGIN
      -- Process one student at a time
      IF @gpa > 3.5
          PRINT @name + ' qualifies for Dean''s List';
      FETCH NEXT FROM student_cursor INTO @id, @name, @gpa;
  END;

  CLOSE student_cursor;
  DEALLOCATE student_cursor;

Warning: Cursors are significantly slower than set-based SQL. Only use them when you genuinely need row-by-row processing. Every cursor should be followed by the question: 'could I do this with a single SELECT?'

Practice: Write a cursor that generates a class performance summary — processing each student and categorising them (Distinction/Credit/Pass/Fail).""",
  "Cursors appear in exams more than in real-world use (because set-based SQL is usually better). Evening students: learn the syntax and the open/fetch/close lifecycle — that's what exam questions target. The real-world lesson is knowing when NOT to use cursors."),

s("database","200",4,
  "Advanced Normalisation — BCNF and Beyond","lecture",
  """BCNF (Boyce-Codd Normal Form) tightens 3NF to handle edge cases where a table can still have anomalies even in 3NF.

A relation is in BCNF if: for every functional dependency X → Y, X is a superkey.

Example violation of 3NF that satisfies 3NF but violates BCNF:
  CourseOffering(Student, Course, Teacher)
  Dependency: Teacher → Course (each teacher teaches only one course)
  This creates anomalies even though it's in 3NF

BCNF fix: split into Teacher(Teacher, Course) + Enrolment(Student, Teacher)

Exam strategy for normalisation questions beyond 3NF:
  1. Identify ALL functional dependencies first
  2. Check each one: is the left side a superkey?
  3. If not → BCNF violation → decompose the table
  4. Verify the decomposition is lossless (you can rejoin without losing data)

Practice: Find 2 real-world scenarios that violate BCNF and decompose them.""",
  "BCNF questions are exam differentiators — students who score A on normalisation understand functional dependencies deeply. Evening students: spend 30 minutes writing functional dependencies for a real database you work with (payroll, inventory). Identifying dependencies in a familiar context teaches the concept faster than abstract examples."),

s("database","200",5,
  "Database Security and User Management","lecture",
  """Database security controls who can access which data and what they can do with it. This week you learn the SQL commands and principles that protect databases in production.

  -- Create a new database user
  CREATE USER 'ama_admin'@'localhost' IDENTIFIED BY 'SecurePass2024';

  -- Grant specific privileges
  GRANT SELECT, INSERT, UPDATE ON university.students TO 'ama_admin'@'localhost';
  GRANT SELECT ON university.courses TO 'ama_admin'@'localhost';

  -- Revoke when no longer needed
  REVOKE INSERT ON university.students FROM 'ama_admin'@'localhost';

Security principle — Least Privilege:
  Never grant more access than the minimum needed.
  A report-only user gets SELECT only.
  A data entry clerk gets SELECT + INSERT.
  Only the DBA gets all privileges.

Roles and views as security tools:
  Create a view that shows only non-sensitive columns, grant users access to the view instead of the table.
  Student portal view: name, level, courses (not: personal address, fees balance)

Practice: Design a 3-role permission scheme for the UPSA student system (student role, staff role, admin role). Write the GRANT statements for each.""",
  "Database security is increasingly relevant in Ghana's growing tech ecosystem. Evening students who work in IT: data breaches often happen because of excessive database privileges. This week's material is directly applicable to your professional role. Build the 3-role permission scheme for a system similar to your workplace."),

s("database","200",6,
  "Backup, Recovery, and Database Maintenance","lecture",
  """A database without a backup strategy is a disaster waiting to happen. This week covers the professional practices that keep databases running and recoverable.

Backup types:
  Full backup      → complete copy of entire database (weekly)
  Differential     → changes since last full backup (daily)
  Transaction log  → every change since last backup (hourly or continuous)

Recovery scenarios:
  Scenario 1: Accidental table deletion → restore from full backup + replay transaction log
  Scenario 2: Hardware failure → restore to another server from most recent full + differential
  Scenario 3: Corruption → point-in-time recovery using transaction log

MySQL backup command:
  mysqldump -u root -p university > backup_20240315.sql

Recovery:
  mysql -u root -p university < backup_20240315.sql

Practice exercise:
  1. Create your student database backup using mysqldump
  2. Deliberately drop a table
  3. Restore it from your backup
  4. Verify all data is intact

If you have never practiced a restore, you don't actually have a backup strategy.""",
  "Evening students who work in IT support or system administration: backup and recovery is a core responsibility. Practice the full backup-drop-restore cycle in lab this week. The 20 minutes you spend proves you can actually recover data — not just talk about it. That skill belongs on your CV."),

s("database","200",7,
  "Query Optimisation and Execution Plans","lecture",
  """A slow database query can bring an entire application to its knees. This week you learn to read, interpret, and improve query performance.

EXPLAIN command — your diagnostic tool:
  EXPLAIN SELECT s.name, c.course_name
  FROM Students s JOIN Enrolment e ON s.id = e.student_id
  JOIN Courses c ON e.course_id = c.id
  WHERE s.level = '300';

EXPLAIN shows: which indexes are used, how many rows are scanned, join order.
If you see "ALL" in the type column → full table scan → likely needs an index.

Optimisation strategies:
  Add indexes on columns used in WHERE and JOIN conditions
  Avoid SELECT * — specify only the columns you need
  Avoid functions on indexed columns in WHERE: WHERE YEAR(dob) = 1998 prevents index use
  Rewrite correlated subqueries as JOINs where possible

Practice: Take your 5 slowest queries from Level 100 (joins + subqueries). Run EXPLAIN on each. Add indexes where indicated. Compare execution times before and after.""",
  "Query optimisation is a senior database skill that separates good DBA candidates from average ones. Evening students: if your workplace database runs slowly, this week teaches you why. Run EXPLAIN on a common query at work (if permitted) and identify what indexes could help."),

s("database","200",8,
  "Distributed Databases and Replication","lecture",
  """A distributed database stores data across multiple physical locations but appears as one logical database to the user.

Real-world example: A Ghanaian bank with branches in Accra, Kumasi, and Tamale. Each branch operates locally even if the central server is unreachable. Data synchronises when connectivity restores.

Key concepts:
  Replication   → copies of data on multiple servers (one fails, others continue)
  Fragmentation → different parts of the data live on different servers
  Horizontal    → different rows on different servers (Accra customers on Server A, Kumasi on Server B)
  Vertical      → different columns on different servers (names on one, balances on another)
  CAP Theorem   → a distributed system can guarantee at most 2 of 3: Consistency, Availability, Partition Tolerance

Exam strategy for distributed database questions: always anchor your answer with the bank branch scenario. Examiners credit concrete examples. Define the concept in one sentence, then illustrate with the bank example, then state the trade-off.""",
  "Distributed databases are the backbone of mobile money systems (MTN, Vodafone Cash) — systems you use daily in Ghana. Evening students: the bank branch scenario is directly familiar. Use it in every answer this week."),

s("database","200",9,
  "NoSQL — Introduction and When to Use It","lecture",
  """NoSQL databases store data without rigid table schemas. They trade the consistency guarantees of relational databases for flexibility and scale.

Types and their uses:
  Document stores (MongoDB)   → JSON-like documents, good for varied/nested data (product catalogues, user profiles)
  Key-Value stores (Redis)    → lightning-fast lookups by key (session data, caching)
  Column-family (Cassandra)   → massive writes distributed across servers (IoT sensor data, logs)
  Graph databases (Neo4j)     → relationships are first-class (social networks, fraud detection)

When NOT to use NoSQL:
  When data is highly relational and transactional (banking, payroll)
  When you need ACID guarantees across multiple entities
  When your team knows SQL and the data fits a schema

Decision framework: "Does this problem require relationships, transactions, and consistency? → SQL. Does it require flexibility, scale, and simple retrieval? → NoSQL."

Practice: For each of these systems, argue SQL or NoSQL with reasons:
  UPSA student registration | WhatsApp message storage | ATM transaction log | E-commerce product catalogue""",
  "NoSQL is increasingly tested at Level 200 because cloud-native applications use it extensively. Evening students in tech roles: identify which NoSQL type your company's systems use. Document stores are most common in web applications; Redis is almost certainly running behind any fast web service you use."),

s("database","200",10,
  "Database Administration — Performance Monitoring","lab",
  """A Database Administrator (DBA) keeps the database healthy, fast, and available. This week introduces the monitoring skills that differentiate a developer from a DBA.

Key DBA monitoring tasks:
  Slow query log → identify queries taking > 1 second
  Connection count → alert when too many connections accumulate
  Table size → identify tables growing unexpectedly fast
  Index usage → find indexes that are never used (they slow writes for no benefit)

MySQL monitoring commands:
  SHOW PROCESSLIST;           → active queries right now
  SHOW STATUS LIKE 'Slow%';  → count of slow queries since startup
  SHOW TABLE STATUS;          → size, rows, and engine for all tables
  EXPLAIN FORMAT=JSON ...;   → detailed execution plan

Lab exercise: Take your student database, insert 10,000 fake student records using a loop or script. Run your most complex join query. Check SHOW PROCESSLIST during execution. Add an index. Run the query again. Record the time difference.

The difference between 4 seconds and 0.02 seconds, caused by one CREATE INDEX command, is the most memorable lesson in this course.""",
  "Evening students in IT roles: this lab teaches a skill valued in every data-related job. Inserting 10,000 records exposes problems invisible at small scale. If your workplace database runs slowly, this week gives you the vocabulary and tools to investigate. Document your findings — it could inform a useful conversation with your employer."),

s("database","200",11,
  "Data Warehousing Concepts","lecture",
  """A data warehouse is a separate database optimised for analysis, not transactions. Transactional databases (OLTP) are optimised for fast individual operations. Warehouses (OLAP) are optimised for complex queries across large historical datasets.

  OLTP database: Process a sale in < 50ms. Highly normalised.
  OLAP warehouse: "What were total sales by region by month for the past 3 years?" Denormalised for speed.

Core data warehouse concepts:
  ETL (Extract, Transform, Load) → pull data from operational systems, clean it, load into warehouse
  Star Schema → fact table at centre, dimension tables around it
  Fact table → transactional events (Sales, Enrolments, Payments)
  Dimension tables → descriptive context (Student, Course, Date, Location)

UPSA example star schema:
  Fact: EnrolmentFact(student_key, course_key, date_key, grade, credits_attempted)
  Dimensions: DimStudent, DimCourse, DimDate, DimLecturer

Practice: Design a star schema for an UPSA academic performance warehouse. Identify the fact table and at least 3 dimension tables. Specify the grain (what does one row in the fact table represent?).""",
  "Data warehousing is the foundation of business intelligence and analytics — one of the fastest-growing career areas in Ghana's tech sector. Evening students: every management dashboard your employer uses is querying a data warehouse or similar analytical store. This week explains the architecture behind those reports."),

s("database","200",12,
  "Database Project — Advanced System Development","project",
  """Your Level 200 project should demonstrate mastery of the advanced features, not just basic CRUD.

Required features for a strong Level 200 project:
  ✓ At least 2 stored procedures (e.g. EnrolStudent, CalculateSemesterGPA)
  ✓ At least 1 trigger (audit log or business rule enforcement)
  ✓ User roles with appropriate GRANT statements
  ✓ At least one view used in a report query
  ✓ Evidence of query optimisation (EXPLAIN output showing index use)
  ✓ Backup procedure documented

Project differentiation strategy:
  Average project → CRUD working, basic queries
  Good project → stored procedures + trigger + roles
  Excellent project → all of the above + optimisation evidence + backup strategy documented in report

The project report should explain WHY each design decision was made. One paragraph per stored procedure explaining its purpose and why it was stored in the database rather than application code.""",
  "Evening students: your final project is worth significant marks. Book one full weekend for project work. Saturday: stored procedures and trigger. Sunday: user roles, view, backup. During the week: testing and documentation. This schedule leaves Monday-Wednesday for refinement."),

s("database","200",13,
  "Exam Preparation — Advanced SQL and Database Theory","exam_prep",
  """Level 200 exams are weighted toward procedures, triggers, optimisation, and distributed concepts.

SQL revision — write from memory:
  A stored procedure with input parameters and error handling
  A trigger that enforces a business rule
  A cursor that processes rows
  A GRANT statement for a specific role
  An EXPLAIN-informed CREATE INDEX statement

Theory revision — one real example per concept:
  BCNF → your normalisation exercise from Week 4
  Backup types → the bank example with full + differential + log
  Distributed databases → bank branches with replication
  OLTP vs OLAP → bank transactions vs annual report generation
  NoSQL decision → product catalogue (MongoDB) vs payroll (PostgreSQL)

Exam technique at Level 200:
  SQL questions: write the code first, annotate with comments explaining each clause
  Design questions: diagram first (table names, arrows for relationships), then write SQL
  Theory questions: define in one sentence, example in two sentences, trade-off in one sentence""",
  "Evening students: the night before exam — review your stored procedure and trigger code (30 minutes). Review your normalisation exercise (15 minutes). Sleep. On exam morning, eat and arrive 15 minutes early. Rushing in causes the first 20 minutes of the exam to be wasted on anxiety rather than answers."),
]

# ═══════════════════════════════════════════════════════════════════════════
#  DATABASE MANAGEMENT — LEVEL 300
# ═══════════════════════════════════════════════════════════════════════════
DB_300 = [
s("database","300",1,
  "Advanced Database Architecture and System Design","lecture",
  """At Level 300, you design systems, not just queries. This week shifts your focus from writing SQL to architecting complete database solutions.

Architecture decisions you'll make this week:
  Centralised vs distributed → one server or many?
  Relational vs document → structured transactions or flexible content?
  On-premise vs cloud → own the hardware or rent it?
  OLTP vs OLAP vs HTAP → pure transactions, pure analytics, or hybrid?

The decision framework — always answer these before choosing architecture:
  1. What is the transaction volume? (queries per second)
  2. How large is the dataset? (GB, TB, PB)
  3. What consistency guarantees are needed? (financial = strict ACID)
  4. What is the read/write ratio? (mostly reads → different design than mostly writes)
  5. What is the budget? (open source, cloud, or enterprise licence)

Practice: Evaluate MTN Ghana's mobile money system. Estimate transaction volume, data size, consistency requirements, and read/write ratio. Recommend an architecture with justification. This exercise mirrors real DBA consultancy work.""",
  "Evening students in senior IT roles: this week's content is the strategic layer of your current or future career. The decision framework is directly applicable to any database project you're involved in professionally. Bring a real architecture problem from your workplace and apply the framework to it."),

s("database","300",2,
  "Big Data Concepts and Processing Frameworks","lecture",
  """Big data is not just large data — it's data that exceeds traditional database capacity for storage, processing, or real-time requirements.

The 5 Vs of Big Data:
  Volume     → terabytes to petabytes (MTN's call records, ECOWAS trade data)
  Velocity   → real-time streaming (fraud detection must happen in milliseconds)
  Variety    → structured, semi-structured, unstructured (tables + JSON + video)
  Veracity   → data quality and trustworthiness
  Value      → the insights extracted must justify the cost

Processing frameworks:
  Hadoop MapReduce → batch processing of very large datasets (historical analysis)
  Apache Spark     → in-memory processing, 100x faster than Hadoop for iterative tasks
  Apache Kafka     → real-time event streaming (MTN transaction stream)

Ghana context: The National Health Insurance Authority (NHIA) processes millions of claims across all regions. Their system is a real big data problem — regional variety, high volume during peak periods, and the cost of incorrect data is a patient getting wrong treatment.

This week: Map the NHIA claim processing scenario to the 5 Vs. Identify which processing framework fits each stage.""",
  "Evening students: big data frameworks appear in every forward-looking IT organisation in Ghana. Understanding the 5 Vs and being able to apply them to a Ghanaian context (NHIA, GRA, Electoral Commission) makes your exam answers and interview answers stand out."),

s("database","300",3,
  "Data Mining and Analytics","lecture",
  """Data mining extracts patterns and knowledge from large datasets. It answers questions you didn't know to ask.

Core data mining techniques:
  Classification → predict a category (will this loan default? Yes/No)
  Clustering    → group similar records (identify student performance segments)
  Association   → find items that appear together (students who fail DB also tend to fail Networking)
  Regression    → predict a numeric value (predict final GPA from mid-sem results)

UPSA application:
  Cluster students by engagement level (lab attendance, query frequency)
  Association: which topic combinations in the knowledge base appear in the same student session?
  Regression: predict a student's exam score from their chatbot query patterns

The CRISP-DM process (your mining methodology):
  Business Understanding → Data Understanding → Data Preparation → Modelling → Evaluation → Deployment

Practice: Define a data mining problem for UPSA. Specify: the question, the data needed, the technique, and what the output looks like. Write a 1-page mining project proposal.""",
  "Data analytics is one of the highest-demand skills in Ghana's job market. Evening students: if your organisation has data (and every organisation does), there is a mining opportunity in it. Your 1-page proposal should be about a REAL problem in your workplace — this makes the assignment both practical and personally useful."),

s("database","300",4,
  "OLAP and Advanced Data Warehousing","lab",
  """OLAP (Online Analytical Processing) enables multi-dimensional analysis of large datasets. This week you go beyond designing star schemas to actually querying them.

OLAP operations:
  Roll-up    → aggregate to higher level (daily → weekly → monthly → yearly)
  Drill-down → from summary to detail (Ghana total → region → district)
  Slice      → one dimension fixed (only Semester 1 data)
  Dice       → multiple dimensions fixed (Semester 1, Level 200, Database course)
  Pivot      → rotate axes (rows become columns)

SQL for OLAP:
  -- Total enrolments by level and semester (cube)
  SELECT level, semester, COUNT(*) as total
  FROM EnrolmentFact ef
  JOIN DimStudent s ON ef.student_key = s.key
  GROUP BY ROLLUP(level, semester);

Lab exercise: Using your Level 200 warehouse design, write OLAP queries that:
  1. Show total enrolments per course per semester (ROLLUP)
  2. Drill down from total enrolments to level-by-level breakdown
  3. Slice for Semester 1 only across all years
  4. Create a pivot showing each level's GPA by semester""",
  "OLAP queries are the SQL of business intelligence tools. Evening students who use Excel pivot tables: OLAP is the database-level equivalent of what pivot tables do visually. The GROUP BY ROLLUP syntax is what powers those reports."),

s("database","300",5,
  "Database Tuning and Performance Engineering","lab",
  """Database tuning at Level 300 goes beyond adding indexes. You tune at the query, schema, configuration, and hardware level.

Tuning hierarchy (apply in this order):
  1. Schema design → normalise/denormalise appropriately for the workload
  2. Indexes → right indexes, right columns, no redundant indexes
  3. Query rewriting → eliminate full scans, reduce subqueries, use query hints
  4. Configuration → buffer pool size, connection pool, cache settings
  5. Hardware → SSD vs HDD for I/O-bound workloads

Query rewriting example:
  -- Slow (correlated subquery):
  SELECT name FROM Students s WHERE gpa > (SELECT AVG(gpa) FROM Students WHERE level = s.level)

  -- Fast (join to pre-computed averages):
  SELECT s.name FROM Students s
  JOIN (SELECT level, AVG(gpa) avg FROM Students GROUP BY level) avg_table
  ON s.level = avg_table.level AND s.gpa > avg_table.avg

Lab: Insert 100,000 student records. Run 10 complex queries. Profile with EXPLAIN. Apply all 4 schema/query/index improvements. Measure and document the performance improvement percentage for each.""",
  "Performance tuning evidence in your project significantly elevates your grade. Evening students in DBA or senior developer roles: the skills this week are directly billable. A database tuning engagement at a Ghanaian enterprise can take days — you're building that capability now."),

s("database","300",6,
  "Cloud Databases and Database-as-a-Service","lecture",
  """Cloud databases eliminate infrastructure management. You focus on data, not servers. This week covers the major platforms and when to choose each.

Major cloud database services:
  AWS RDS      → managed relational (MySQL, PostgreSQL, Oracle)
  Google Cloud SQL → fully managed, auto-backup, scaling
  Azure SQL Database → enterprise SQL Server in the cloud
  Firebase Firestore → real-time NoSQL, popular for mobile apps
  MongoDB Atlas    → managed MongoDB with global distribution

Migration strategy — on-premise to cloud:
  1. Assess current database size and usage patterns
  2. Choose cloud provider and service
  3. Set up target database
  4. Migrate schema → migrate data → test → cut over
  5. Decommission on-premise (only after 30-day parallel run)

Ghanaian context: Government agencies moving from physical servers to GovCloud. Health facilities connecting to the national DHIMS2 health database. Understanding cloud database migration is directly relevant to Ghana's digital transformation agenda.

Practice: Design a migration plan for moving the UPSA student database from on-premise MySQL to AWS RDS. Specify steps, risks, rollback plan, and estimated downtime.""",
  "Evening students in IT management: cloud database migration projects are active in Ghana's public and private sector. Your migration plan this week is a portfolio piece. Research GhanaCloud and GovCloud as local alternatives to international providers — this local context is valued in both exams and job interviews."),

s("database","300",7,
  "Advanced Database Security and Compliance","lecture",
  """At Level 300, security covers not just access control but encryption, auditing, and regulatory compliance.

Security layers:
  Transport encryption → TLS/SSL for all connections (data in transit)
  Storage encryption   → AES-256 for data at rest (encrypted disk)
  Row-level security   → users only see rows they're authorised for
  Column-level masking → phone numbers shown as +233 XXX XXX 678 in reports
  Audit logging        → every SELECT, INSERT, UPDATE, DELETE recorded with user and timestamp

Ghana Data Protection Act (Act 843) compliance requirements:
  Personal data must be collected with consent
  Data must be accurate and not kept longer than necessary
  Security measures must prevent unauthorised access
  Data subjects have the right to access their own data

Practical audit trigger:
  CREATE TRIGGER AuditStudentAccess
  AFTER SELECT ON Students
  FOR EACH ROW
      INSERT INTO AuditLog(user, table_name, action, record_id, timestamp)
      VALUES (CURRENT_USER(), 'Students', 'SELECT', NEW.id, NOW());

Practice: Redesign the UPSA database security model to comply with Act 843. Specify encryption, audit logging, and a data retention policy.""",
  "Evening students: Ghana's Data Protection Commission is actively enforcing Act 843. Any organisation handling personal data (which is every organisation) must comply. Your security model this week has direct legal and professional relevance. Understanding compliance is increasingly a prerequisite for senior IT roles in Ghana."),

s("database","300",8,
  "Replication, Clustering, and High Availability","lecture",
  """High availability means the database keeps running even when components fail. This week covers the architectures that achieve it.

Replication types:
  Master-slave (primary-replica) → writes go to master, reads distributed to replicas
  Master-master → any node can accept writes, synchronised bi-directionally
  Multi-region → replicas in different geographic locations (disaster recovery)

Clustering:
  MySQL Cluster → multiple nodes, no single point of failure, data sharded across nodes
  Galera Cluster → synchronous multi-master replication, all nodes identical

Failover scenario:
  Without HA: master server fails → application down until manually restored (hours)
  With HA:   master server fails → replica automatically promoted to master (seconds)

RTO and RPO — the two numbers every DBA must know:
  RTO (Recovery Time Objective)  → maximum acceptable downtime (bank: 30 seconds)
  RPO (Recovery Point Objective) → maximum acceptable data loss (bank: 0 transactions)

Practice: Design a high-availability database architecture for a Ghanaian commercial bank. Specify primary/replica setup, failover mechanism, RTO, RPO, and geographic distribution.""",
  "Evening students in systems administration: RTO and RPO are the metrics your management cares about. The bank architecture exercise is a realistic scenario you may face professionally. Present your design as a diagram with failover sequence labeled — this is exam and interview format."),

s("database","300",9,
  "XML, JSON, and Semi-Structured Data","lab",
  """Modern databases must handle semi-structured data alongside relational tables. This week covers native JSON/XML support in relational databases.

MySQL JSON support:
  CREATE TABLE products (
      id INT PRIMARY KEY,
      name VARCHAR(100),
      attributes JSON   ← stores any structure per product
  );

  INSERT INTO products VALUES (1, 'Laptop', '{"ram": "16GB", "storage": "512GB SSD", "os": "Windows 11"}');

  -- Query inside JSON:
  SELECT name, attributes->>'$.ram' AS ram FROM products WHERE attributes->>'$.storage' LIKE '%SSD%';

When to use JSON columns: data with highly variable attributes (products, event logs, API responses) where adding a new attribute should not require an ALTER TABLE.

Lab exercise: Build a product catalogue with JSON attributes. Insert 10 products with different attribute sets. Write queries that:
  1. Find all products with more than 16GB RAM
  2. Update the price inside a JSON attribute
  3. Extract all unique keys used across all products""",
  "JSON databases (or JSON columns in relational databases) are how modern web APIs store their data. Evening students in web development or integration roles: the JSON column pattern explains why your REST API can return different fields for different records. This lab directly connects to API development practices."),

s("database","300",10,
  "Advanced Stored Procedures, Functions, and Database Programming","lab",
  """Level 300 database programming means building complete, tested, production-quality procedures — not just syntactically correct ones.

Production-quality procedure checklist:
  ✓ Input validation (reject invalid parameters before any DML)
  ✓ Transaction wrapping (all DML in BEGIN...COMMIT/ROLLBACK)
  ✓ Specific error handling (different messages for different failures)
  ✓ Output parameters or result sets (caller knows what happened)
  ✓ Logging (every significant action recorded in an audit table)

Example — production-quality EnrolStudent:
  PROCEDURE EnrolStudent(IN p_student_id INT, IN p_course_code VARCHAR(10), OUT p_status VARCHAR(100))
  BEGIN
      DECLARE EXIT HANDLER FOR SQLEXCEPTION
      BEGIN
          ROLLBACK;
          SET p_status = 'ERROR: Database exception during enrolment';
      END;

      START TRANSACTION;
          -- Validate student exists
          IF NOT EXISTS (SELECT 1 FROM Students WHERE id = p_student_id) THEN
              SET p_status = 'ERROR: Student not found'; ROLLBACK; LEAVE proc_label;
          END IF;
          -- Check not already enrolled
          -- ... (additional validation)
          INSERT INTO Enrolment ...;
          INSERT INTO AuditLog ...;
          SET p_status = 'SUCCESS';
      COMMIT;
  END;

Lab: Refactor your Level 200 stored procedures to production standard using this checklist.""",
  "Production-quality procedures are the difference between student code and professional code. Evening students who work with enterprise databases: look at existing procedures in your workplace database. Do they follow this checklist? Identifying gaps in production systems is a senior-level skill."),

s("database","300",11,
  "Database Project Management and Documentation","lecture",
  """A database project has a lifecycle — from requirements to decommission. This week covers managing that lifecycle professionally.

Database project phases:
  1. Requirements analysis → what data, what volume, what queries, what SLA
  2. Logical design → ER diagram, normalisation
  3. Physical design → table creation, indexes, partitioning
  4. Implementation → migration, stored procedures, security
  5. Testing → performance testing, security testing, data validation
  6. Deployment → production cutover, backup strategy, monitoring
  7. Maintenance → ongoing tuning, capacity planning, incident response

Documentation a professional DBA maintains:
  Data dictionary → every table, column, data type, purpose, sample value
  ER diagram → current state, version-controlled
  Backup and recovery runbook → step-by-step procedures
  Change log → every schema change with date, author, reason, rollback procedure
  Performance baseline → normal query times, documented for comparison

Practice: Create a complete data dictionary for your Level 300 project database. Include every table, every column, and the business reason for its existence.""",
  "Evening students: the data dictionary is the most undervalued and most needed deliverable in every database project. In many Ghanaian organisations, the database was built years ago with no documentation. Being the person who documents the database is immediately valuable and positions you as a senior contributor."),

s("database","300",12,
  "Capstone Database Project","project",
  """Your Level 300 capstone is a complete, production-standard database system with full documentation.

Capstone deliverables:
  1. ER diagram and justified design decisions
  2. Normalised schema to 3NF or BCNF (documented)
  3. At least 3 production-quality stored procedures
  4. At least 2 triggers with business rule enforcement
  5. Role-based security model with GRANT statements
  6. Performance analysis (EXPLAIN output + index justification)
  7. Backup and recovery plan
  8. Data dictionary
  9. A data warehouse component (star schema + 2 OLAP queries)
  10. Full project report with design rationale throughout

Differentiation strategy: Most students deliver a working system. Top students deliver a working system WITH documented rationale. Every design decision should have one sentence explaining why: "The Enrolment table uses a composite primary key because each student-course pair is unique, and a surrogate key would allow duplicate enrolments."

Present your project as if explaining it to a future DBA who must maintain it after you're gone.""",
  "Evening students: use one full weekend per week for the last 3 weeks. Weekend 1 (this week): complete the database + procedures + triggers. Weekend 2 (Week 13): security model + performance + data warehouse. Weeknights: documentation. This schedule makes submission day calm instead of chaotic."),

s("database","300",13,
  "Final Exam Preparation — Advanced Database Systems","exam_prep",
  """Level 300 exams assess architectural thinking and professional judgement, not just syntax recall.

Theory revision — answer with context:
  Big data: 5 Vs with a Ghana-specific example (NHIA, GRA, electoral data)
  Cloud migration: steps + risks + Ghana cloud providers
  High availability: RTO/RPO for a bank vs a school
  Data mining: CRISP-DM applied to a real problem
  Security + compliance: Act 843 requirements

SQL revision — write production-quality code:
  A stored procedure with transaction, error handling, and audit logging
  A trigger that enforces a business rule
  An OLAP query with ROLLUP
  A JSON column query

Presentation preparation:
  Prepare 3-sentence explanations for: your architecture choice, your security model, your performance optimisation
  Practise delivering your project demo — every click should have a one-sentence commentary
  Know your schema deeply — examiners test whether you can answer 'why' questions about your own database

The Level 300 examiner is evaluating whether you think like a database professional. Every answer should reflect that perspective.""",
  "Evening students: the Level 300 exam rewards real-world connection. Every answer you give that references a Ghanaian organisation, a professional scenario, or a workplace decision is stronger than a purely academic answer. Your evening work experience is an advantage — use it deliberately in every exam answer."),
]

# ═══════════════════════════════════════════════════════════════════════════
#  NETWORKING — LEVEL 100
# ═══════════════════════════════════════════════════════════════════════════
NET_100 = [
s("networking","100",1,
  "Introduction to Computer Networks","lecture",
  """Every time you send a WhatsApp message or load a web page, a network is working. This week you start understanding how.

What a network is at its most basic: devices that can communicate. A network can be 2 computers connected by a cable, or a billion devices connected globally (the internet).

Why networks matter — every IT role you will hold involves networks:
  Software developers need networks to deploy applications
  Database administrators need networks to manage remote servers
  System administrators spend most of their time managing networks

Start building your network vocabulary this week — these terms will appear in every course:
  Node       → any device on a network (computer, phone, printer, router)
  Protocol   → agreed rules for communication (how to say hello, send data, say goodbye)
  Bandwidth  → maximum data rate (MTN 4G = ~20 Mbps theoretical)
  Latency    → time for data to travel from A to B (Accra to London = ~100ms)
  Packet     → a chunk of data — all network communication is split into packets

Real-world grounding: When you load a webpage, your browser sends packets to a server in another country. The server sends packets back. Your network reassembles them into the page you see. Everything in this course explains how that works.""",
  "Evening students: if you work in any IT support role, networking concepts are used daily — every time you troubleshoot a connectivity issue, extend a Wi-Fi network, or configure a printer. This course makes your instinctive troubleshooting systematic."),

s("networking","100",2,
  "Network Topologies and Types","lecture",
  """A topology is the physical or logical arrangement of devices on a network. Choosing the wrong topology for an environment is a common IT mistake.

Physical topologies:
  Bus       → all devices on one cable (simple but one break kills the whole network)
  Star      → all devices connect to a central switch (most common today — one device fails, others continue)
  Ring      → devices in a circle (data travels in one direction — rare today)
  Mesh      → every device connects to every other (expensive but very fault-tolerant — used in military networks)
  Hybrid    → combination (UPSA campus likely uses star within buildings, connected in a hybrid to the internet)

Network types by scale:
  PAN  → Personal (Bluetooth headphones to phone — < 10 metres)
  LAN  → Local (your home router, office network — building or campus)
  MAN  → Metropolitan (a city-wide network — some ISPs use this)
  WAN  → Wide Area (the internet, MTN's national network)

Exam strategy: For topology questions, always justify your choice. "I recommend Star topology because a single device failure does not affect others, and it is easy to add or remove devices." Two reasons beats one word answer.""",
  "Evening students: draw the topology of your workplace network. Is it a star? (Most offices are.) How many switches? Where's the router? This exercise connects textbook diagrams to real infrastructure you interact with daily."),

s("networking","100",3,
  "The OSI Model — 7 Layers","lecture",
  """The OSI model is the most important conceptual framework in networking. Every networking question eventually comes back to it.

The 7 layers (memorise top-down AND bottom-up):
  7. Application  → what the user sees (HTTP, FTP, DNS, SMTP)
  6. Presentation → encryption, compression, data format (SSL/TLS, JPEG, MP3)
  5. Session      → start, manage, end communication sessions
  4. Transport    → reliable delivery (TCP) or fast delivery (UDP), port numbers
  3. Network      → routing between networks, IP addresses
  2. Data Link    → error-free delivery on a single link, MAC addresses
  1. Physical     → the actual bits on wire/fibre/air, cables, signals

Memory trick: "All People Seem To Need Data Processing" (Application → Physical, top to bottom)

Exam strategy: For every protocol you encounter, know its layer:
  HTTP → Layer 7 | IP → Layer 3 | Ethernet → Layer 2 | Cable → Layer 1

The WhatsApp example mapped to OSI:
  L7: The message content you type
  L6: Encryption (end-to-end)
  L4: TCP connection to WhatsApp servers
  L3: Your IP → WhatsApp server IP
  L2: Your phone's MAC → router's MAC
  L1: Wi-Fi radio waves to your router""",
  "The OSI model is tested in every networking exam at every level. Evening students: the WhatsApp example makes it memorable. Trace a message you sent today through all 7 layers — the exercise takes 5 minutes and makes the model concrete for the exam."),

s("networking","100",4,
  "TCP/IP Model and Protocol Suite","lecture",
  """TCP/IP is the actual model the internet uses. OSI is the reference framework; TCP/IP is the implementation.

TCP/IP has 4 layers (maps to OSI's 7):
  Application  → OSI Layers 5-7 (HTTP, FTP, DNS, SMTP, DHCP)
  Transport    → OSI Layer 4 (TCP, UDP)
  Internet     → OSI Layer 3 (IP, ICMP, ARP)
  Network Access → OSI Layers 1-2 (Ethernet, Wi-Fi)

TCP vs UDP — know the difference cold:
  TCP → Transmission Control Protocol
        Reliable, ordered, error-checked
        Used for: web browsing, email, file transfer
        Analogy: registered post — you get a receipt, guaranteed delivery

  UDP → User Datagram Protocol
        Fast, no guarantee, no order
        Used for: video streaming, online gaming, DNS lookups
        Analogy: throwing a message in a bottle — fast but not guaranteed

Exam question type: "Why does YouTube use UDP instead of TCP?"
Answer: A 1-second video delay is acceptable. Re-transmitting a dropped packet would cause stuttering. Speed over reliability is the right trade-off for streaming.

Practice: For 10 common applications, decide TCP or UDP and justify: web browser, WhatsApp call, WhatsApp message, online game, file download, live radio stream, email, ATM transaction.""",
  "Evening students: the TCP vs UDP question appears in almost every networking exam. The 10-application exercise is your exam preparation. Do it on paper tonight — 15 minutes. By the time the exam arrives, this will feel obvious."),

s("networking","100",5,
  "IP Addressing and Subnetting","lab",
  """IP addressing is the most practical skill in this course — and the most failed exam topic. The key is practice, not memorisation.

IPv4 structure:
  192.168.1.100 → four 8-bit octets = 32 bits total
  Network part → which network (like a street name)
  Host part    → which device (like a house number)

Subnet mask tells you the split:
  255.255.255.0 = /24 → first 24 bits = network, last 8 bits = host
  Hosts available: 2^8 - 2 = 254 (minus network address and broadcast)

Private IP ranges (used inside your office/home — not routable on internet):
  10.0.0.0/8       → large organisations
  172.16.0.0/12    → medium organisations
  192.168.0.0/16   → home and small office (your router uses this)

Subnetting drill (do 10 of these):
  Network: 192.168.10.0/24 — divide into 4 equal subnets
  New mask: /26 (2 extra bits = 4 subnets)
  Subnet 1: 192.168.10.0/26 (hosts: .1 to .62)
  Subnet 2: 192.168.10.64/26 (hosts: .65 to .126)
  Subnet 3: 192.168.10.128/26 (hosts: .129 to .190)
  Subnet 4: 192.168.10.192/26 (hosts: .193 to .254)

Subnetting is a calculation skill — you get it through repetition, not reading.""",
  "Evening students: subnetting is worth significant exam marks and is a daily skill for any network administrator. Use a subnetting app on your phone during commute — Subnet Calc or CIDR Calc. 10 practice problems per day for one week makes this automatic."),

s("networking","100",6,
  "Network Devices — Routers, Switches, and Hubs","lecture",
  """Every device on a network has a specific role. Confusing them costs marks in exams and causes problems in real networks.

Hub:
  Broadcasts to ALL ports when it receives data
  Every device sees every message (even if not for them)
  Very little intelligence — Layer 1 device
  Almost obsolete today

Switch:
  Learns which MAC address is on which port (MAC address table)
  Sends data ONLY to the correct port
  Layer 2 device — operates on MAC addresses
  Used in every LAN today

Router:
  Connects DIFFERENT networks together
  Makes routing decisions based on IP addresses
  Layer 3 device — your gateway to the internet
  Your home device (the box from your ISP) is a router+switch+wireless access point combined

Real-world: At UPSA, each computer lab likely has a switch (connecting computers inside the lab). The switch connects to a router. The router connects to the internet via the ISP.

Exam question: "Why is a switch more efficient than a hub in a busy office?"
Answer: A switch builds a MAC address table and sends data only to the destination device, eliminating collision and reducing unnecessary traffic. A hub broadcasts to all devices, wasting bandwidth.""",
  "Evening students: if you've ever connected a network at work, you've used a switch. The MAC address table is what makes the switch intelligent. Understanding this explains why your network slows down when you connect too many devices to a hub (if one still exists) versus a switch."),

s("networking","100",7,
  "LAN and WAN Technologies","lecture",
  """LAN and WAN are not just scale — they use different technologies, speeds, and ownership models.

LAN (Local Area Network):
  Technologies: Ethernet (wired), Wi-Fi 802.11 (wireless)
  Speed: 100 Mbps to 10 Gbps within a building
  Ownership: you own and manage it
  Typical range: single building or campus

WAN (Wide Area Network):
  Technologies: leased lines, MPLS, VPN over internet, fibre optic long-distance
  Speed: varies widely (1 Mbps to 100 Gbps depending on cost)
  Ownership: leased from a service provider (MTN, Vodafone, AT)
  Connects: different cities, countries, continents

Ghana context: MTN and Vodafone Ghana operate WAN infrastructure across the country. An organisation with offices in Accra and Kumasi uses a WAN (typically a leased MPLS line or VPN) to connect them. Each office internally uses a LAN.

Practice: Draw a diagram of a Ghanaian bank with 3 branches (Accra, Kumasi, Takoradi). Show what technology is inside each branch (LAN) and between branches (WAN). Label the devices at each layer.""",
  "Evening students: the bank branch diagram is the physical infrastructure behind every multi-branch organisation you've worked for. Drawing it makes the LAN/WAN distinction concrete. If your organisation has multiple offices, draw their actual network topology this week."),

s("networking","100",8,
  "Network Protocols — HTTP, FTP, DNS, SMTP","lab",
  """Protocols are the rules that make communication possible. This week you learn the 4 protocols behind the internet services you use every day.

HTTP/HTTPS → HyperText Transfer Protocol
  Used for: every web page
  How it works: browser sends GET request → server sends back HTML
  HTTPS = HTTP + TLS encryption (the padlock in your browser)
  Port: 80 (HTTP), 443 (HTTPS)

FTP → File Transfer Protocol
  Used for: uploading files to a web server, downloading large files
  Port: 20 (data), 21 (control)

DNS → Domain Name System
  Translates domain names to IP addresses
  upsa.edu.gh → 197.255.x.x (the actual IP)
  Without DNS: you'd type IP addresses instead of names
  Port: 53

SMTP/POP3/IMAP → Email protocols
  SMTP: sends email (port 25/587)
  POP3: downloads email, deletes from server (port 110)
  IMAP: reads email on server, syncs across devices (port 143)

Lab exercise: Use tools to observe these protocols live:
  Browser DevTools (F12 → Network tab) → watch HTTP requests as a page loads
  nslookup upsa.edu.gh → see the DNS lookup result
  ping upsa.edu.gh → test basic IP connectivity""",
  "Evening students: the browser DevTools exercise is one of the most revealing lab activities in this course. Every web request you've ever made is visible in that Network tab. Spend 15 minutes exploring a website through DevTools — you'll understand HTTP headers, status codes, and caching in one session."),

s("networking","100",9,
  "Network Security Basics","lecture",
  """This week introduces the attacks that networks face and the basic defences against them.

Common attacks:
  Phishing        → fake emails/sites that steal credentials (most common attack in Ghana)
  Man-in-the-middle → attacker intercepts traffic between two parties
  DoS/DDoS        → flood a server with requests until it can't respond
  Packet sniffing → capturing unencrypted network traffic

Basic defences:
  Firewall        → blocks unauthorised traffic based on rules (port, IP, protocol)
  Encryption      → HTTPS, VPN — makes captured packets unreadable
  Strong authentication → passwords + 2FA
  Patch management → keeping software updated closes known vulnerabilities
  Network segmentation → attackers who breach one segment can't reach others

Real-world Ghana context: Mobile money fraud is a social engineering attack — not a technical network attack but a human-layer compromise. HTTPS prevents your browser session being intercepted on public Wi-Fi. VPNs protect workers accessing company systems from home.

Practice: Map the defences to specific threats. For each attack type above, name the primary defence and explain in one sentence why it works.""",
  "Evening students: security affects you personally and professionally. The phishing defence (check sender address, look for HTTPS, never click unexpected links) is immediately applicable. The firewall rules concept explains why some websites are blocked on your work network."),

s("networking","100",10,
  "Wireless Networking — Wi-Fi Standards and Security","lecture",
  """Wi-Fi is so ubiquitous it's easy to take for granted. This week you understand what's actually happening in wireless networking.

Wi-Fi standards:
  802.11b → 11 Mbps, 2.4 GHz (old)
  802.11g → 54 Mbps, 2.4 GHz (still common)
  802.11n → 600 Mbps, 2.4 & 5 GHz (home routers)
  802.11ac → 1.3 Gbps, 5 GHz (modern — called Wi-Fi 5)
  802.11ax → > 9 Gbps, Wi-Fi 6 (current high-end)

Wireless security protocols (critical to know):
  WEP  → broken. Never use. Cracked in minutes.
  WPA  → better but outdated. Some vulnerabilities.
  WPA2 → current standard. Use this.
  WPA3 → latest, strongest. Use on new hardware.

Common wireless issues and their causes:
  Slow speed → interference, distance, too many devices, wrong channel
  Drops → interference from neighbours on same channel, physical obstacles
  Cannot connect → wrong password, MAC filtering, wrong band (2.4 vs 5 GHz)

Lab: Use inSSIDer or Wi-Fi Analyser to scan wireless networks in your lab area. Identify channel overlap and signal strength. Recommend channel and placement changes.""",
  "Evening students: if you set up Wi-Fi at home or in a small office, this week's knowledge directly applies. Changing your router from channel 6 to channel 1 or 11 (to avoid neighbours' overlap) can significantly improve speed. Using WPA2 (not WEP or open) is an immediate security improvement you can make tonight."),

s("networking","100",11,
  "Network Troubleshooting Tools and Methodology","lab",
  """Systematic troubleshooting is the difference between a professional and someone who just reboots the router and hopes.

The network troubleshooting ladder — test from bottom up (OSI Layer 1 → 7):
  L1: Is the cable plugged in? Is the link light on? (ping 127.0.0.1 to test local stack)
  L2: Is the NIC working? Is the switch port active?
  L3: Do you have an IP address? (ipconfig/ifconfig) Can you ping your default gateway?
  L4: Is the service running? Is the port open? (telnet host port)
  L7: Is the application responding? Does DNS resolve the hostname? (nslookup)

Essential tools:
  ping         → test if a host is reachable and measure latency
  traceroute   → trace the path packets take across the network
  nslookup     → diagnose DNS issues
  netstat      → show active connections and listening ports
  ipconfig     → show your IP address, subnet mask, default gateway

Lab exercise:
  1. ping 8.8.8.8 (Google's DNS) — tests internet connectivity
  2. ping upsa.edu.gh — tests DNS resolution + connectivity
  3. traceroute upsa.edu.gh — see the hops between you and UPSA
  4. nslookup google.com — observe DNS in action
  5. netstat -an — see all active connections""",
  "Evening students: these tools are what you use in IT support to diagnose network problems. The 5 commands in the lab exercise cover 80% of network troubleshooting scenarios you'll face professionally. Practice them until you can run them and interpret results without notes."),

s("networking","100",12,
  "Network Design and Planning Project","project",
  """This week you apply everything to design a real network — the most practical assessment of the semester.

Recommended project: Network Design for a Small Business (e.g. a 3-floor office in Accra)

Ground floor: Reception (2 PCs, 1 printer), Server Room (1 server)
First floor: 10 staff PCs, 2 meeting rooms (projectors)
Second floor: Management (5 PCs, 1 NAS storage)

Your design must include:
  Network topology diagram (Lucidchart or draw.io, or hand-drawn)
  IP addressing scheme (subnet each floor)
  Device list (how many switches, one router, wireless access points)
  Security measures (firewall rules, WPA2, VLAN separation of guest from staff)
  Cost estimate (approximate prices for Accra market)
  Justification for each major decision

Grading differentiation:
  Basic: topology diagram + IP scheme
  Good: all of above + security measures + device list
  Excellent: full design + cost estimate + justify every decision with course concepts""",
  "Evening students who work in IT: this is your strongest project. Your real-world experience of office networks makes the design more realistic and the justification more compelling. Reference actual equipment you've installed. A design grounded in real experience scores higher than a purely textbook one."),

s("networking","100",13,
  "Final Exam Preparation","exam_prep",
  """Networking exams at Level 100 are typically 40% diagram questions, 30% subnetting calculations, and 30% protocol/theory questions.

Diagram preparation:
  Practise drawing network topologies in under 5 minutes
  Know exactly which device connects what (hub/switch/router placement)
  Label all devices with their layer (Layer 1, 2, or 3)

Subnetting preparation:
  Do 10 subnetting calculations without a calculator
  Know CIDR notation /24, /25, /26, /27, /28, /29, /30 and what each gives you
  Know the formula: hosts = 2^(32-prefix) - 2

Protocol theory:
  Every protocol: name, purpose, OSI layer, port number, TCP or UDP
  HTTP(S), FTP, DNS, SMTP, POP3, IMAP, DHCP, SNMP

OSI model:
  Name all 7 layers in both directions in under 30 seconds
  Map any given protocol or technology to its layer immediately

Exam technique:
  Subnetting: show your working — partial credit for correct method
  Diagram: label everything — unlabelled devices lose marks
  Theory: use the format "Protocol — Purpose — Layer — Port"
  Time allocation: 40% for diagrams, 35% for calculations, 25% for theory""",
  "Evening students: subnetting is the most time-pressured part of the exam. If you haven't practised 10+ calculations without a calculator, do it this week — 5 per night, two nights. The OSI layer recall should be automatic — test yourself on your commute. Diagrams are marks given if you draw them completely and label everything."),
]

# ═══════════════════════════════════════════════════════════════════════════
#  NETWORKING — LEVEL 200
# ═══════════════════════════════════════════════════════════════════════════
NET_200 = [
s("networking","200",1,
  "Advanced TCP/IP and Protocol Analysis","lab",
  """At Level 200, you don't just know protocols — you analyse them. This week you use Wireshark to see actual protocol traffic.

Wireshark — your packet analysis tool:
  Captures every packet on your network interface
  Filters by protocol: filter 'http' or 'dns' or 'tcp.port == 443'
  Shows headers at every layer (Ethernet frame → IP packet → TCP segment → HTTP request)

Lab exercise:
  1. Start a Wireshark capture
  2. Open a web page (http only, not https, so you can see the content)
  3. Stop capture and filter for 'http'
  4. Find the GET request — observe: source/destination IP, port, request headers
  5. Find the server response — observe: status code, content type, size

What to look for:
  The TCP 3-way handshake (SYN → SYN-ACK → ACK) before HTTP starts
  The DNS query before the TCP connection starts
  How many TCP connections open for one web page

This lab makes the entire TCP/IP stack visible. What you study theoretically becomes a packet you can click on and read.""",
  "Evening students: Wireshark is used in professional network analysis and security roles. Seeing the actual packet flow of a website you visit makes TCP/IP permanent knowledge — not just exam knowledge. This lab is one of the most valuable in this entire degree."),

s("networking","200",2,
  "Routing Protocols — RIP and OSPF","lecture",
  """Routers exchange information about networks through routing protocols. Without routing protocols, you'd have to manually configure every router's routing table — impossible at internet scale.

RIP (Routing Information Protocol):
  Distance vector protocol — decisions based on hop count (number of routers)
  Maximum 15 hops (anything beyond = unreachable)
  Updates every 30 seconds regardless of changes (wasteful)
  Simple, good for small networks
  Metric: hop count

OSPF (Open Shortest Path First):
  Link-state protocol — each router has a complete map of the network
  Uses Dijkstra's shortest path algorithm
  Updates only when topology changes (efficient)
  No hop count limit — scales to large networks
  Metric: cost (based on bandwidth — faster links preferred)

When to choose which:
  Small office (< 15 routers, simple topology) → RIP is adequate
  Medium to large network → OSPF
  Multi-vendor enterprise → OSPF (vendor-neutral)

Lab exercise: Configure RIP on 3 routers (using Cisco Packet Tracer). Verify routing tables. Then add a 4th router. Observe how routing tables update automatically.""",
  "Evening students: OSPF is what runs the backbone of Ghana's major ISPs. MTN and Vodafone Ghana's national networks use link-state routing. Understanding OSPF explains how your packet finds its way from Tamale to Accra in milliseconds."),

s("networking","200",3,
  "Switching — VLANs and Spanning Tree Protocol","lab",
  """VLANs (Virtual LANs) let you logically separate a network without physical separation. One physical switch can host multiple isolated networks.

Real-world UPSA example:
  One building, one switch, but separate networks:
  VLAN 10 → Student devices (internet access, no access to admin servers)
  VLAN 20 → Staff devices (internet + internal systems)
  VLAN 30 → Administration servers (restricted access)
  VLAN 99 → Management (switch/router configuration only)

Benefits: security (students can't reach staff systems), performance (reduced broadcast domain), flexibility (move staff to a different desk without rewiring).

Spanning Tree Protocol (STP) prevents loops in switched networks:
  Loop scenario: two switches connected by two cables — broadcasts loop forever, crashing the network
  STP solution: blocks one path, activates it if the primary path fails

Lab: Configure VLANs on a switch in Packet Tracer.
  Create VLANs 10, 20, 30
  Assign ports to VLANs
  Test: PC in VLAN 10 should NOT ping PC in VLAN 20
  Configure a trunk port between two switches (carries all VLANs)""",
  "Evening students: VLANs are configured in virtually every corporate network. If you work in IT support, you've likely encountered VLAN issues (device on wrong VLAN, can't reach a server). This lab makes VLAN troubleshooting intuitive."),

s("networking","200",4,
  "Network Address Translation (NAT)","lecture",
  """NAT solves the IPv4 address shortage. Your home network has one public IP from your ISP but many private devices. NAT translates between them.

How NAT works:
  Your laptop: 192.168.1.5 (private)
  Your router: 197.255.14.22 (public IP from ISP)
  You request google.com:

  1. Laptop sends packet: src=192.168.1.5:45231 → dst=142.250.200.100:80
  2. Router translates: src=197.255.14.22:12001 → dst=142.250.200.100:80 (replaces private with public)
  3. Router records the mapping in NAT table
  4. Response arrives at router's public IP
  5. Router translates back using NAT table → forwards to your laptop

Types:
  Static NAT    → one public IP ↔ one private IP (for servers that must be reachable externally)
  Dynamic NAT   → pool of public IPs shared among private IPs
  PAT (Port Address Translation) → many private IPs share ONE public IP using different ports (your home router uses this)

Ghana context: Every home and office in Ghana using Vodafone or MTN broadband uses PAT. You share a public IP with other subscribers on the same street.""",
  "Evening students: NAT is why you cannot directly reach your home computer from outside your network without port forwarding. Understanding NAT explains many remote access problems you've encountered in IT support. The PAT explanation also explains why VoIP calls sometimes fail on heavily-loaded NAT routers."),

s("networking","200",5,
  "DHCP and DNS Configuration","lab",
  """DHCP and DNS are the services that make networks usable. Without them, every device would need manual IP configuration and you'd browse by typing IP addresses.

DHCP (Dynamic Host Configuration Protocol) — automatically gives devices their network settings:
  IP address, subnet mask, default gateway, DNS server
  Lease time: how long the device keeps the address before renewal

DHCP process (DORA):
  D → Discover: device broadcasts "I need an IP"
  O → Offer: DHCP server responds "Here's 192.168.1.50"
  R → Request: device says "I'll take that one"
  A → Acknowledge: server confirms the lease

DNS (Domain Name System) — the internet's phone book:
  Resolver: your device asks DNS server for google.com
  Recursive resolver: your ISP's DNS server finds the answer
  Root server → TLD server (.com) → authoritative server (google.com) → IP

Lab: Configure a DHCP server in Packet Tracer.
  Set address pool: 192.168.1.100 - 192.168.1.200
  Set gateway: 192.168.1.1, DNS: 8.8.8.8, lease time: 24 hours
  Connect 3 PCs — verify each gets a unique IP automatically
  Test DNS resolution: ping google.com from a PC""",
  "Evening students: every network problem you've solved by typing 'ipconfig /release' and 'ipconfig /renew' was a DHCP problem. This lab explains exactly what those commands do. Understanding DHCP makes you significantly faster at network troubleshooting."),

s("networking","200",6,
  "Firewalls and Access Control Lists (ACLs)","lecture",
  """Firewalls filter traffic based on rules — allowing or denying packets based on source, destination, port, and protocol.

ACL types on Cisco routers:
  Standard ACL   → filter by source IP only (numbered 1-99)
  Extended ACL   → filter by source IP, destination IP, protocol, port (numbered 100-199)

Extended ACL example — allow web traffic from the student VLAN, deny everything else:
  permit tcp 192.168.10.0 0.0.0.255 any eq 80     ← allow HTTP from student VLAN to anywhere
  permit tcp 192.168.10.0 0.0.0.255 any eq 443    ← allow HTTPS
  deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255  ← block students from staff VLAN
  permit ip any any                               ← allow all other traffic

ACL placement rule:
  Standard ACLs → place close to destination (they only filter by source)
  Extended ACLs → place close to source (they're specific enough to block early)

Practice: Write ACL rules for this scenario:
  Allow HTTP and HTTPS from any source to web servers at 10.0.0.100
  Allow SSH from the admin subnet (10.0.1.0/24) to the server only
  Deny all other traffic to the server""",
  "Evening students in IT roles: firewall rules and ACLs are what you're working with when you configure network security. The extended ACL syntax is Cisco-specific but the logic (source, destination, protocol, port, allow/deny) is universal. Practice the ACL writing exercise until it feels automatic."),

s("networking","200",7,
  "VPN and Network Tunnelling","lecture",
  """A VPN (Virtual Private Network) creates an encrypted tunnel over a public network, making remote users appear to be on the local network.

Why VPNs matter:
  Remote work: staff working from home access the office network securely
  Branch connectivity: connect offices across the country over the internet (cheaper than dedicated WAN)
  Privacy: hide your traffic from your ISP (personal VPN services like NordVPN)

VPN types:
  Site-to-site VPN → connects two office networks over the internet (IPsec tunnel between routers)
  Remote access VPN → individual user connects to the office network (SSL VPN, OpenVPN)
  MPLS VPN → carrier-managed, private, high-performance WAN (enterprise use)

IPsec (Internet Protocol Security) — the most common VPN protocol:
  Provides: encryption (confidentiality), integrity verification, authentication
  Modes: Tunnel mode (full IP packet encrypted — used for site-to-site) vs Transport mode

Ghana context: During COVID-19, Ghanaian organisations moved to remote work. VPNs were the technology that made it possible to access internal systems from home. MTN and Vodafone Ghana both offer managed VPN services.

Practice: Configure a site-to-site VPN in Packet Tracer between two branch offices. Verify that the two internal networks can communicate through the encrypted tunnel.""",
  "Evening students who worked remotely: the VPN you connected through is what you're now configuring. Understanding how it works makes you more effective at troubleshooting VPN connectivity issues and explaining requirements to vendors."),

s("networking","200",8,
  "Network Monitoring and Management — SNMP","lab",
  """You cannot manage what you cannot see. Network monitoring tools give visibility into performance, failures, and security events.

SNMP (Simple Network Management Protocol):
  Manager (your monitoring system) polls Agents (routers, switches, servers)
  Agents respond with MIB data (Management Information Base — a structured database of device stats)
  Traps: agents proactively send alerts when something changes (link down, high CPU)

Key metrics to monitor:
  Bandwidth utilisation (alert if > 80%)
  Packet loss (anything > 0.1% is a problem)
  Latency (alert if > 100ms on LAN)
  Interface errors (CRC errors indicate a bad cable or NIC)
  Device CPU and memory (router CPU > 90% = performance crisis)

Tools used in industry:
  Zabbix (open source, widely used in Ghana's public sector)
  PRTG Network Monitor (SME-friendly, popular with Ghanaian ISPs)
  Nagios (open source, highly configurable)
  Cisco Prime (Cisco-specific)

Lab: Install Zabbix on a virtual machine. Add your lab's router as a monitored device via SNMP. Create a trigger that alerts when interface utilisation exceeds 70%.""",
  "Evening students in network operations roles: this lab teaches the daily tools of your profession. Zabbix or similar platforms are what NOC (Network Operations Centre) teams use to maintain visibility. Setting up SNMP monitoring is a directly billable skill in Ghanaian IT services companies."),

s("networking","200",9,
  "IPv6 — The Future of IP Addressing","lecture",
  """IPv4 addresses are exhausted. IPv6 is the solution — 128-bit addresses provide 340 undecillion addresses (enough for every grain of sand on Earth to have a trillion addresses).

IPv6 address format:
  2001:0db8:85a3:0000:0000:8a2e:0370:7334
  8 groups of 4 hex digits, separated by colons
  Can abbreviate: 2001:db8:85a3::8a2e:370:7334 (:: replaces consecutive zeros)

Key differences from IPv4:
  No NAT needed → every device can have a globally unique address
  Built-in IPsec → security is mandatory, not optional
  No broadcast → uses multicast instead (more efficient)
  Stateless autoconfiguration → devices configure themselves without DHCP

Transition mechanisms (we're in a dual-stack period):
  Dual-stack → devices have both IPv4 and IPv6 simultaneously
  6to4 tunnelling → IPv6 traffic wrapped in IPv4 packets
  NAT64 → IPv6-only devices communicate with IPv4-only resources

Ghana context: All major Ghanaian ISPs support IPv6 on their backbone. MTN Ghana has IPv6-enabled infrastructure. Your smartphone already uses IPv6 on mobile networks.

Practice: Configure IPv6 addresses in Packet Tracer. Test connectivity using ping6. Compare the autoconfiguration process to DHCP in IPv4.""",
  "Evening students: IPv6 migration projects are active in Ghana's ISPs and government networks. Understanding IPv6 addressing and dual-stack configuration is an increasingly valuable skill. Identify whether your workplace uses IPv6 — it likely does on the WAN side even if not internally."),

s("networking","200",10,
  "Wireless Network Security — WPA2, 802.1X, and RADIUS","lab",
  """Level 200 wireless security goes beyond WPA2 passwords — you configure enterprise-grade authentication.

WPA2-Personal vs WPA2-Enterprise:
  Personal (PSK) → one password for all users. If one person leaves, change the password for everyone.
  Enterprise → each user has their own credentials. Remove one user without affecting others.

802.1X + RADIUS architecture:
  Supplicant → the device trying to connect (laptop, phone)
  Authenticator → the access point — forwards credentials to RADIUS
  Authentication Server → RADIUS server (checks credentials against Active Directory or LDAP)

How it works:
  1. Device connects to Wi-Fi and provides username/password
  2. Access point forwards credentials to RADIUS server
  3. RADIUS checks against user database
  4. RADIUS says Accept or Reject
  5. Access point allows or blocks the connection

Real-world: UPSA's staff Wi-Fi likely uses 802.1X. Your staff login is checked against the university's Active Directory.

Lab: Configure a RADIUS server in Packet Tracer. Set up an access point for WPA2-Enterprise. Test authentication with a valid and invalid user account.""",
  "Evening students: if you manage a corporate Wi-Fi network, this lab teaches the architecture behind 'bring your own device' security. 802.1X with RADIUS is the standard for any organisation where employees use individual accounts — and it's what you recommend when a client asks 'how do we control who accesses our network?'"),

s("networking","200",11,
  "Network Design — Enterprise Architecture","lecture",
  """Enterprise network design follows the 3-tier hierarchical model used by Cisco and the industry worldwide.

3-tier hierarchy:
  Core layer → high-speed backbone connecting distribution switches (Layer 3, fastest switches, redundant paths)
  Distribution layer → policy enforcement, routing between VLANs, connects core to access (Layer 3 switches)
  Access layer → connects end devices (PCs, phones, printers) to the network (Layer 2 switches, PoE for IP phones)

Why 3 tiers?
  Each layer has a defined role → easier to troubleshoot
  Problems stay within their tier → a faulty access switch doesn't affect the core
  Scalable → add capacity at the appropriate tier

UPSA campus network likely follows this model:
  Core: central building, connecting all faculties
  Distribution: one switch per building/block
  Access: one switch per lab/floor

Design principles:
  Redundancy at every tier above access (dual links, dual devices)
  VLANs to segment traffic types (data, voice, management, guest)
  QoS to prioritise voice traffic over data

Practice: Design a 3-tier network for a new 5-building university campus. Specify devices at each tier, VLANs, and redundant links.""",
  "Evening students: this design framework is used in every significant network infrastructure project in Ghana. Knowing it positions you to contribute meaningfully to network design conversations at your organisation or with clients."),

s("networking","200",12,
  "Lab Practical — End-to-End Network Configuration","project",
  """This practical week builds a complete small enterprise network from scratch in Packet Tracer — the kind of network that appears in practical exams.

Network requirements:
  2 routers (configured with OSPF between them)
  3 switches (one per department — IT, HR, Finance)
  VLANs: 10 (IT), 20 (HR), 30 (Finance)
  DHCP server providing addresses to each VLAN
  ACL: Finance VLAN cannot access IT servers
  Wi-Fi access point in HR office (WPA2)
  Internet connectivity via one router

Build sequence:
  1. Physical connections — cables, labelled topology diagram
  2. Basic device configuration — hostnames, passwords, IP addresses
  3. VLANs and trunking — on all switches
  4. Routing — OSPF between routers
  5. DHCP — server configuration and verification
  6. ACL — test deny rule works
  7. Wi-Fi — configure and test client connection
  8. Full verification — ping from each VLAN, trace routes

Work through this in order. Do not skip steps. Document every configuration command you apply.""",
  "Evening students: this practical is the closest thing in this course to a real network deployment. Every step mirrors what you'd do in a live environment. Save your Packet Tracer file — the completed topology can be adapted as a template for real small-office deployments."),

s("networking","200",13,
  "Exam Preparation — Advanced Networking","exam_prep",
  """Level 200 exams balance practical configuration knowledge with design and troubleshooting scenarios.

Configuration revision (write from memory):
  OSPF configuration commands on a Cisco router
  VLAN creation, port assignment, and trunk configuration
  Extended ACL for a given policy
  DHCP server configuration
  Basic NAT/PAT configuration

Design revision:
  3-tier hierarchy → when to use each layer, which devices
  VLAN design → how many VLANs, naming, subnets
  Redundancy → where and why

Troubleshooting methodology revision:
  OSI bottom-up approach
  show commands: show ip route, show interfaces, show vlan, show ip nat translations
  Wireshark capture interpretation (TCP handshake, DNS, HTTP)

Exam technique for practical/configuration questions:
  Write commands in the correct sequence (global config → interface/VLAN → verify)
  Show verify commands (show ip ospf neighbor, show vlan brief)
  Explain what each command does in a comment

For scenario questions:
  Identify the requirement → match to a protocol or technology → justify the choice""",
  "Evening students: the configuration revision is done best on Packet Tracer, not paper. Spend two evenings configuring the Level 200 practical from Week 12 from scratch, without your notes. If you can build it from memory, the exam configuration questions are answerable. Theory questions benefit from Ghana-context examples in every answer."),
]

# ═══════════════════════════════════════════════════════════════════════════
#  NETWORKING — LEVEL 300
# ═══════════════════════════════════════════════════════════════════════════
NET_300 = [
s("networking","300",1,
  "Enterprise Network Design and Architecture","lecture",
  """Level 300 networking is strategic. You design, evaluate, and justify complete network solutions — not just configure individual devices.

The enterprise design process:
  1. Requirements gathering → users, applications, performance, compliance, budget
  2. Site assessment → existing infrastructure, physical constraints, growth plans
  3. High-level design → topology, technology choices, redundancy strategy
  4. Low-level design → IP scheme, VLAN design, device selection, routing protocol
  5. Implementation plan → staging, rollout sequence, rollback plan
  6. Validation → testing against requirements

Requirements categories:
  Functional   → what the network must do (connect 500 users, support VoIP)
  Performance  → measurable targets (< 10ms latency, 99.9% uptime)
  Security     → compliance requirements (PCI-DSS for payment systems, Act 843)
  Scalability  → expected growth over 3-5 years
  Budget       → CAPEX (equipment) and OPEX (maintenance, ISP fees)

Ghana context: The National Communications Authority (NCA) has published broadband targets for Ghana. Designing networks for Ghanaian enterprises means accounting for power reliability (generator backup), ISP redundancy (two different providers), and indoor wireless coverage for open-plan offices.

Practice: Write a requirements document for an UPSA network upgrade project. Use all 5 requirement categories.""",
  "Evening students in IT management: requirements gathering is often more valuable than technical configuration skills at the senior level. Practice asking the right questions this week — the requirements document exercise is directly applicable to your next client meeting or internal project."),

s("networking","300",2,
  "BGP — Border Gateway Protocol","lecture",
  """BGP is the routing protocol of the internet. Every AS (Autonomous System) — each ISP, each major organisation — uses BGP to exchange routing information globally.

Key BGP concepts:
  AS (Autonomous System) → a network under single administrative control (MTN Ghana = one AS)
  AS Number → unique 16 or 32-bit identifier (e.g. AS37204 for MTN Ghana)
  EBGP → BGP between different ASes (MTN ↔ Vodafone peering)
  IBGP → BGP within the same AS

BGP is a path vector protocol — it advertises the complete AS path:
  Prefix 196.0.0.0/16 reached via AS37204 → AS1234 → AS7018

BGP path selection (simplified):
  1. Highest LOCAL_PREF (within your AS — prefer this exit)
  2. Shortest AS_PATH (fewer hops = better)
  3. Lowest MED (suggested preference from neighbour)
  4. EBGP over IBGP
  5. Lowest router ID (tiebreaker)

Real Ghana context: When MTN Ghana and Vodafone Ghana exchange routes (peering at the Ghana Internet Exchange Point — GIX), they use EBGP. Your packet from an MTN SIM to a Vodafone destination crosses this peering point.

Practice: Map the AS path from Ghana to a US website. Use BGPview.io to trace actual routes.""",
  "Evening students in senior network roles: BGP is the technology behind ISP peering and multi-homing (connecting to two ISPs for redundancy). Understanding BGP positions you to participate in internet infrastructure discussions at your organisation or with ISP partners."),

s("networking","300",3,
  "Software Defined Networking (SDN)","lecture",
  """SDN separates the network control plane from the data plane, enabling programmatic control of network behaviour.

Traditional network:
  Intelligence IN the device (each router decides independently)
  Configuration: log into each device separately
  Change one policy: update every device individually

SDN:
  Intelligence in a central controller
  Data plane: dumb switches that just forward based on flow tables
  Controller pushes rules to all switches simultaneously
  Change one policy: update the controller once

SDN architecture:
  Application layer → network applications (load balancer, firewall, monitoring)
  Control layer    → SDN controller (OpenDaylight, ONOS, Cisco ACI)
  Data/Infrastructure layer → network devices (OpenFlow-enabled switches)

Real-world impact: Google's internal network (B4) is fully SDN. They reduce network costs by 70% by dynamically routing traffic based on real-time demand rather than static configurations.

Ghana relevance: Safaricom (which includes Ghana operations) uses SDN in their core network for traffic engineering. Huawei's network equipment, widely deployed in Ghana's telcos, supports SDN/NFV.

Practice: Deploy a simple SDN environment using Mininet (runs on Linux). Create a topology with 4 switches and an OpenFlow controller. Observe how flow rules are pushed to switches.""",
  "Evening students: SDN is the future of large-scale network management. Hands-on Mininet experience is a CV differentiator in Ghana's telco and ISP sector. This week's practical setup takes about 2 hours — invest the time."),

s("networking","300",4,
  "Network Virtualisation — NFV and Overlay Networks","lecture",
  """Network Function Virtualisation (NFV) replaces physical network appliances with software running on commodity servers.

Traditional: physical firewall + physical load balancer + physical IDS = 3 appliances, expensive, fixed capacity
NFV: firewall app + load balancer app + IDS app = 3 VMs on one server, flexible, scalable

ETSI NFV architecture:
  VNF (Virtual Network Function) → the software appliance (virtual firewall, virtual router)
  NFVI (Infrastructure) → the servers, storage, and network that host VNFs
  MANO (Management and Orchestration) → provisions, scales, and manages VNFs

Overlay networks (VXLAN):
  VXLAN encapsulates Layer 2 frames in UDP packets
  Allows Layer 2 domains to span physical network boundaries
  Each VXLAN segment identified by 24-bit VNI (16 million segments vs 4096 VLANs)
  Used by: VMware NSX, OpenStack Neutron, AWS VPC

Ghana telco application: MTN Ghana's core network uses NFV for their IMS (IP Multimedia Subsystem) — the infrastructure behind 4G voice calls.

Practice: Set up a simple VXLAN overlay in a virtualised lab environment. Verify that two VMs on different physical hosts can communicate through the overlay.""",
  "Evening students in telco or cloud roles: NFV and VXLAN are the technologies being deployed in Ghana's next-generation network upgrades. Understanding these architectures is increasingly required for senior network engineering roles in Ghana."),

s("networking","300",5,
  "Cloud Networking — AWS VPC, Azure VNet","lab",
  """Cloud networking extends enterprise networks into public cloud infrastructure. At Level 300, you design and configure cloud network topology.

AWS VPC (Virtual Private Cloud):
  Your private network inside AWS
  Subnets: public (internet-accessible) and private (internal only)
  Internet Gateway: connects public subnet to internet
  NAT Gateway: allows private subnet to reach internet (outbound only)
  Security Groups: stateful firewall per resource
  Route Tables: control traffic flow within VPC

Typical 3-tier web app architecture in AWS:
  Public subnet: Load Balancer (internet-facing)
  Private subnet 1: Web/App servers (no direct internet access)
  Private subnet 2: Database (no internet access, only from app servers)

Security Group rules:
  Load Balancer SG: allow inbound 80/443 from anywhere
  App Server SG: allow inbound 8080 from Load Balancer SG only
  DB SG: allow inbound 3306 from App Server SG only

Lab: Using the AWS free tier, create a VPC with:
  1 public subnet and 1 private subnet
  Internet Gateway for public subnet
  NAT Gateway for private subnet
  EC2 instance in public subnet (web server)
  RDS instance in private subnet (database)
  Security Groups following least-privilege""",
  "Evening students: AWS free tier allows you to build this architecture at no cost. This lab is directly portfolio-worthy and increasingly asked about in Ghanaian IT interviews. Companies building on AWS (there are many in Ghana) look for candidates who have done this."),

s("networking","300",6,
  "Advanced Network Security — IDS, IPS, and SIEM","lecture",
  """At Level 300, security is not reactive — it is systematic and intelligence-driven.

IDS vs IPS:
  IDS (Intrusion Detection System) → monitors and ALERTS (passive — watch only)
  IPS (Intrusion Prevention System) → monitors and BLOCKS in real-time (active — inline)

IDS/IPS detection methods:
  Signature-based → match traffic against known attack patterns (fast, misses new attacks)
  Anomaly-based   → detect deviations from baseline (catches new attacks, more false positives)
  Heuristic       → behaviour analysis over time (sophisticated, resource-intensive)

SIEM (Security Information and Event Management):
  Aggregates logs from all network devices, servers, and security tools
  Correlates events across sources (a failed login from IP X + port scan from IP X = alert)
  Provides timeline for incident response
  Tools: Splunk, IBM QRadar, open source ELK Stack

Incident response process:
  1. Preparation → policies, tools, team roles
  2. Detection → SIEM alert, IDS notification
  3. Containment → isolate affected segment
  4. Eradication → remove malware, patch vulnerability
  5. Recovery → restore service, verify clean
  6. Lessons learned → document and improve

Practice: Set up a basic ELK Stack (Elasticsearch, Logstash, Kibana) on a VM. Forward firewall logs into it. Create a dashboard showing top source IPs and blocked ports.""",
  "Evening students in IT security roles: the ELK Stack setup this week is a portfolio piece and a practical skill. Many Ghanaian organisations lack proper log management — offering to set up basic SIEM monitoring is a value-adding project for your employer."),

s("networking","300",7,
  "Network Forensics and Traffic Analysis","lab",
  """Network forensics answers the question: what happened, when, from where, and to where? It's the investigation skill of the network world.

Forensic analysis tools:
  Wireshark    → deep packet inspection and protocol analysis
  tcpdump      → command-line packet capture (server environments)
  NetworkMiner → passively extracts files and credentials from pcap files
  Zeek (Bro)   → network security monitor that generates high-level logs

A forensics investigation workflow:
  1. Capture: collect pcap files from affected network segment (with legal authorisation)
  2. Preserve: hash the pcap file (MD5/SHA256) to prove it hasn't been tampered with
  3. Analyse: timeline the events, identify anomalous traffic
  4. Report: document findings with timestamps and evidence

Lab exercise — analyse a provided pcap file:
  Open the file in Wireshark
  Apply filter: ip.addr == [suspicious IP]
  Identify: what protocol, what data was accessed, what timestamps
  Follow TCP stream of the suspicious connection
  Write a 1-page incident report from your findings

This exercise simulates a real security incident investigation.""",
  "Evening students in IT security or audit roles: network forensics is a regulatory requirement in some sectors (financial services, healthcare) when security incidents occur. The pcap analysis skill and the incident report format are directly applicable. Keep your Wireshark and tcpdump skills current."),

s("networking","300",8,
  "Quality of Service (QoS) and Traffic Engineering","lecture",
  """QoS ensures that critical traffic gets priority when the network is congested. Without QoS, a large file download can degrade a VoIP call on the same link.

Traffic classification → QoS can only prioritise traffic it can identify:
  By DSCP (Differentiated Services Code Point) markings in IP header
  By protocol and port (VoIP = UDP port 5060/5004, video = TCP 443)
  By application (requires deep packet inspection)

QoS mechanisms:
  Classification → identify and mark traffic
  Policing       → drop or remark traffic that exceeds its rate
  Shaping        → buffer excess traffic and send smoothly
  Queuing        → PQ (Priority Queuing) gives VoIP absolute priority
                   CBWFQ (Class-Based WFQ) gives guaranteed bandwidth per class

Real-world: Ghana's commercial banks use QoS to prioritise SWIFT financial messages over staff browsing. Teleconference platforms (Zoom, Teams) need low-latency, low-jitter treatment.

QoS policy for a typical Ghanaian enterprise:
  Priority queue: VoIP (UDP 5060, RTP)
  High priority: financial transactions, VPN tunnels
  Normal: web browsing, email
  Low priority: software updates, backups

Practice: Configure QoS in Packet Tracer to prioritise VoIP traffic. Simulate congestion. Verify VoIP quality (latency, jitter) is maintained while other traffic is affected.""",
  "Evening students: QoS configuration is directly relevant to any enterprise network with mixed traffic types. If your organisation uses VoIP or video conferencing alongside regular data traffic, QoS tuning is a concrete improvement project you could propose."),

s("networking","300",9,
  "MPLS and Service Provider Networks","lecture",
  """MPLS (Multiprotocol Label Switching) is how service providers build fast, private WAN services for enterprises.

How MPLS works:
  At ingress router: a label is attached to each packet based on destination
  Core routers: forward based on label only (faster than IP lookup)
  At egress router: label removed, normal IP forwarding resumes

Labels enable VPN services:
  Different customers use the same SP network but traffic is completely isolated
  Customer A's packet and Customer B's packet have different labels → never mix

MPLS services:
  L3 VPN → customer networks appear to be directly connected (SP handles routing)
  L2 VPN (VPLS) → simulate a LAN across a wide geographic area
  Traffic Engineering → route critical traffic on specific paths (not just shortest path)

Ghana context: Enterprise WAN connectivity from MTN Business, Vodafone Business, and Surfline uses MPLS. A company with offices in Accra, Kumasi, and Takoradi can have what feels like a single LAN connecting all three — this is MPLS L3 VPN.

Practice: Configure a basic MPLS lab in GNS3. Demonstrate that two customer sites can communicate through an MPLS service provider backbone with traffic isolation from other customers.""",
  "Evening students in enterprise networking: if your organisation uses a managed WAN service from an ISP, it is almost certainly MPLS-based. Understanding MPLS helps you have informed conversations with your service provider about SLAs, traffic engineering, and troubleshooting WAN performance issues."),

s("networking","300",10,
  "Network Automation — Python and Ansible","lab",
  """Network automation replaces manual CLI configuration with code. A task that takes an engineer 2 hours to configure on 20 devices takes an automation script 2 minutes.

Python for network automation (Netmiko library):
  from netmiko import ConnectHandler

  device = {
      'device_type': 'cisco_ios',
      'host': '192.168.1.1',
      'username': 'admin',
      'password': 'password',
  }

  connection = ConnectHandler(**device)
  output = connection.send_command('show ip interface brief')
  print(output)
  connection.disconnect()

Ansible for network automation:
  Agentless → no software installed on network devices
  YAML playbooks → human-readable automation scripts
  Idempotent → safe to run multiple times (only makes changes if needed)

Automation use cases:
  Configuration backup → automated nightly backup of all device configs
  Bulk configuration → apply a VLAN change to 50 switches at once
  Compliance checking → verify all devices meet security standards
  Incident response → automatically block a suspicious IP on all firewalls

Lab: Write a Python script using Netmiko that connects to 3 routers (in GNS3 or Packet Tracer), collects 'show running-config', and saves each to a timestamped file.""",
  "Evening students: network automation is one of the highest-value skills in the current Ghanaian IT market. Engineers who can automate configuration tasks command higher salaries and are far more productive. The Python/Netmiko skill built in this lab is immediately deployable in any organisation with network infrastructure."),

s("networking","300",11,
  "Disaster Recovery and Business Continuity","lecture",
  """Every organisation depends on its network. When the network fails, business stops. Disaster Recovery (DR) and Business Continuity Planning (BCP) ensure the network can survive and recover from failures.

Key terms:
  RTO (Recovery Time Objective) → maximum time to restore service (1 hour, 4 hours, 24 hours)
  RPO (Recovery Point Objective) → maximum data loss in time (0 minutes for banking, 24 hours for archive)
  MTTR (Mean Time To Repair) → average time to fix a failure
  MTBF (Mean Time Between Failures) → average time between failures (reliability measure)

Network DR strategies:
  Hot standby → duplicate infrastructure running in parallel, instant failover (most expensive)
  Warm standby → duplicate equipment, not fully loaded, minutes to activate
  Cold standby → spare equipment in storage, hours to days to activate (cheapest)

Ghana-specific threats to plan for:
  Power outages (most common) → UPS, generator, dual PSU on critical equipment
  Fibre cuts on main routes → dual ISP, different physical routes
  Flooding (harmattan/rainy season) → equipment location above floor, waterproof cabinets
  Equipment theft → physical security, cable locks, alarmed racks

DR plan exercise: Write a DR plan for UPSA's network. Specify: risk identification, RTO for each system, recovery procedure for top 3 failure scenarios, and test frequency.""",
  "Evening students: business continuity planning is increasingly required by Ghana's regulatory environment (Bank of Ghana, NIC, NCA). Having written DR plans strengthens your professional portfolio. The UPSA DR plan exercise can be adapted to your organisation's context — a real deliverable from your studies."),

s("networking","300",12,
  "Capstone Network Project","project",
  """Your Level 300 capstone integrates enterprise design, security, automation, and documentation into a single comprehensive deliverable.

Project: Complete Enterprise Network Design for a Ghanaian Organisation

Deliverables:
  1. Requirements document (stakeholder interview simulated)
  2. High-level and low-level design
  3. Complete Packet Tracer / GNS3 implementation
  4. OSPF or BGP routing configuration (with justification)
  5. VLAN design with security segmentation
  6. QoS policy for VoIP and critical traffic
  7. IDS/IPS placement and rule design
  8. Automation script for configuration backup
  9. DR plan with RTO/RPO for each system
  10. Full project report with design rationale

Project differentiation:
  Average: working topology + basic routing + VLANs
  Good: all above + QoS + security + documentation
  Excellent: all above + automation + DR plan + Ghana-context justification

Throughout your report, justify every design decision using: requirements traceability, cost justification, and industry best practice. A decision without justification is worth half marks.""",
  "Evening students: the capstone project is your professional showcase. One strong, well-documented network design project is more valuable in a job interview than 10 undocumented school exercises. Treat this as a portfolio piece. Use your workplace as the reference organisation for context and realism."),

s("networking","300",13,
  "Final Exam Preparation — Advanced Networking","exam_prep",
  """Level 300 exams test your ability to design, justify, and troubleshoot complex enterprise scenarios.

Design question strategy:
  Requirement → Technology → Implementation → Justification → Trade-offs
  Example: "Design a network for a 3-branch Ghanaian bank"
  → Requirements (availability, security, compliance)
  → Technology (MPLS WAN, OSPF, VLANs, 802.1X, IDS/IPS)
  → Implementation (3-tier hierarchy, HSRP for redundancy)
  → Justification (PCI-DSS compliance requires segmentation)
  → Trade-offs (MPLS cost vs VPN over internet cost)

Protocol comparison questions:
  SDN vs traditional: control plane separation, programmability, cost
  MPLS vs VPN: performance, cost, SLA guarantees
  BGP vs OSPF: when each is appropriate, why

Security questions:
  Always address: detection (IDS), prevention (IPS/firewall), response (SIEM/incident process)
  Ghana's Data Protection Act → data that crosses the network must be encrypted (Act 843 implication)

Automation questions:
  Describe a network automation workflow → discovery → script → test → schedule → monitor

The Level 300 examiner wants to see that you think at the scale and complexity of a professional network engineer. Every answer should reflect enterprise-level thinking, not home network thinking.""",
  "Evening students: your work experience is your biggest advantage in a Level 300 exam. Every answer that references a real Ghanaian organisation, a real technology you've worked with, or a real failure you've helped resolve is stronger than a purely theoretical answer. Write with that confidence."),
]

# ═══════════════════════════════════════════════════════════════════════════
#  COMBINED
# ═══════════════════════════════════════════════════════════════════════════
ALL_ENTRIES = (
    PROG_100 + PROG_200 + PROG_300 +
    DB_100   + DB_200   + DB_300   +
    NET_100  + NET_200  + NET_300
)

# ═══════════════════════════════════════════════════════════════════════════
#  SEED RUNNER
# ═══════════════════════════════════════════════════════════════════════════
def seed():
    app = create_app()
    with app.app_context():
        added = skipped = 0
        for e in ALL_ENTRIES:
            exists = WeeklyStrategy.query.filter_by(
                course=e["course"], level=e["level"], week=e["week"]
            ).first()
            if exists:
                skipped += 1
                continue
            db.session.add(WeeklyStrategy(
                course=e["course"],
                level=e["level"],
                week=e["week"],
                topic=e["topic"],
                activity=e["activity"],
                strategy=e["strategy"],
                evening_tip=e["evening_tip"],
            ))
            added += 1
        db.session.commit()
        print(f"✅ Strategies seeded — {added} added, {skipped} already existed.")
        print(f"   Total entries: {len(ALL_ENTRIES)}")
        print(f"   Courses: Programming (L100 C++, L200 C++, L300 VB) | Database | Networking")
        print(f"   Each course × 3 levels × 13 weeks = 117 entries")

if __name__ == "__main__":
    seed()
