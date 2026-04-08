#!/usr/bin/env python3
"""
seed_cpp.py — Seeds the UPSA ITM chatbot with a complete C++ Programming
knowledge base for Level 100 (Fundamentals), Level 200 (Intermediate),
and Level 300 (Advanced).

Run from project root with venv active:
    python seed_cpp.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app
from server.extensions import db
from server.models.models import KnowledgeBase

# ═══════════════════════════════════════════════════════════════════════════
# ALL KNOWLEDGE BASE ENTRIES
# ═══════════════════════════════════════════════════════════════════════════
CPP_DATA = [

# ───────────────────────────────────────────────────────────────────────────
#  LEVEL 100 — FUNDAMENTALS
# ───────────────────────────────────────────────────────────────────────────

{
"intent": "cpp_what_is_cpp",
"keywords": ["what is c++", "about c++", "c++ language", "history c++", "who created c++", "define c++", "introduction c++"],
"response": """
📘 **What is C++?**

C++ is a powerful, general-purpose programming language created by **Bjarne Stroustrup** in 1979 at Bell Labs. It was designed as an extension of the C language, adding support for **Object-Oriented Programming (OOP)**.

---

🌍 **Real-Life Analogy:**
Think of C as a basic hand toolkit — a hammer, nails, and a screwdriver. C++ is the same toolkit but now includes power tools: a drill, electric saw, and nail gun. You can still use the basics, but you now have far greater capability and speed.

---

**Why C++ matters:**
- Powers **operating systems** (parts of Windows and Linux)
- Drives **game engines** (Unreal Engine is written in C++)
- Runs **embedded systems** in cars, ATMs, and medical devices
- Used in **high-frequency trading** systems where every microsecond counts
- Extremely fast — closer to hardware than most languages

**Key Characteristics:**
| Feature | Description |
|---------|-------------|
| Compiled | Converted to machine code before running — very fast |
| Statically typed | You must declare data types upfront |
| Multi-paradigm | Supports procedural, OOP, and generic programming |
| Manual memory | You control how memory is used and freed |

💡 **Fun Fact:** WhatsApp's server backend, Adobe Photoshop, Google Chrome, and the Mars Rover software are all built with C++.
""",
"level": "100", "semester": "1"
},

{
"intent": "cpp_first_program",
"keywords": ["hello world", "first program", "write c++ program", "basic program", "simple c++ code", "how to start c++", "setup c++", "compile c++"],
"response": """
💻 **Your First C++ Program — Hello, World!**

Every C++ journey starts with this classic program. Here is the full code:

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
```

---

🔍 **Line-by-Line Breakdown:**

| Line | What it does |
|------|-------------|
| `#include <iostream>` | Imports the input/output library — like loading a printer driver |
| `using namespace std;` | Lets you write `cout` instead of `std::cout` every time |
| `int main()` | The entry point — every C++ program starts here |
| `cout << "Hello, World!"` | Sends text to the screen (`cout` = character output) |
| `endl` | Moves cursor to the next line (like pressing Enter) |
| `return 0;` | Signals the program finished successfully |

---

🌍 **Real-Life Analogy:**
`main()` is like the **main entrance of UPSA** — every visitor (instruction) must pass through it first. No matter how large the building (program), all activity begins at one front door.

---

⚙️ **To Compile and Run:**
```bash
g++ hello.cpp -o hello
./hello
```
**Output:** `Hello, World!`

---

💡 **Try it yourself:** Change `"Hello, World!"` to `"Hello, UPSA ITM!"` and recompile to see your custom output.
""",
"level": "100", "semester": "1"
},

{
"intent": "cpp_variables_datatypes",
"keywords": ["variables", "data types", "int", "float", "double", "char", "bool", "string", "declare variable", "variable types", "data type"],
"response": """
📦 **Variables and Data Types in C++**

A **variable** is a named location in memory used to store a value that can change during the program.

---

🌍 **Real-Life Analogy:**
A variable is like a **labelled box in a storage room**. You write a name on the box (the variable name), put something inside (the value), and you can always open the box to check or change its contents.

---

**Declaring a Variable:**
```cpp
datatype variableName = value;
```

**Common Data Types:**

| Type | Size | Example | Real-Life Use |
|------|------|---------|--------------|
| `int` | 4 bytes | `int age = 20;` | Student ID, age, count |
| `float` | 4 bytes | `float gpa = 3.5f;` | Decimal — less precise |
| `double` | 8 bytes | `double salary = 4500.75;` | Decimal — more precise |
| `char` | 1 byte | `char grade = 'A';` | Single character |
| `bool` | 1 byte | `bool passed = true;` | Yes/No, True/False |
| `string` | varies | `string name = "Ama";` | Any text (needs `#include <string>`) |

---

**Practical Example — Student Record:**
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string studentName = "Kofi Mensah";
    int    studentID   = 20240001;
    double gpa         = 3.75;
    bool   isEnrolled  = true;

    cout << "Name     : " << studentName << endl;
    cout << "ID       : " << studentID   << endl;
    cout << "GPA      : " << gpa         << endl;
    cout << "Enrolled : " << (isEnrolled ? "Yes" : "No") << endl;

    return 0;
}
```

---

⚠️ **Common Mistakes to Avoid:**
- Using `=` to compare (use `==` for comparison, `=` for assignment)
- Forgetting to initialise a variable — it will hold garbage memory values
- Using `float` for financial calculations — always use `double` for precision
""",
"level": "100", "semester": "1"
},

{
"intent": "cpp_input_output",
"keywords": ["cin", "cout", "input", "output", "user input", "read input", "print output", "display", "getline", "keyboard input"],
"response": """
⌨️ **Input and Output in C++**

C++ uses `cout` to display information and `cin` to receive input from the user.

---

🌍 **Real-Life Analogy:**
- `cout` is like a **loudspeaker** — it sends information outward to the user
- `cin` is like a **microphone** — it picks up what the user types in

---

**Displaying Output with `cout`:**
```cpp
cout << "Welcome to UPSA ITM!" << endl;
cout << "Your score is: " << 85 << endl;
cout << "Name: " << "Ama" << "  Age: " << 20 << endl;
```

**Receiving Input with `cin`:**
```cpp
int age;
cout << "Enter your age: ";
cin  >> age;
cout << "You are " << age << " years old." << endl;
```

**Reading Full Names with `getline` (handles spaces):**
```cpp
string fullName;
cout << "Enter your full name: ";
cin.ignore();           // clears the input buffer
getline(cin, fullName);
cout << "Hello, " << fullName << "!" << endl;
```

---

**Full Example — Student Information Form:**
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    int    studentID;
    double gpa;

    cout << "=== UPSA Student Registration ===" << endl;
    cout << "Enter full name  : "; cin.ignore(); getline(cin, name);
    cout << "Enter student ID : "; cin >> studentID;
    cout << "Enter GPA        : "; cin >> gpa;

    cout << "\\n--- Registered Record ---" << endl;
    cout << "Name       : " << name      << endl;
    cout << "Student ID : " << studentID << endl;
    cout << "GPA        : " << gpa       << endl;

    return 0;
}
```

---

💡 **Rule of Thumb:** Always use `cin.ignore()` after `cin >>` before calling `getline()` — otherwise the leftover newline character from pressing Enter gets swallowed into your string.
""",
"level": "100", "semester": "1"
},

{
"intent": "cpp_operators",
"keywords": ["operators", "arithmetic", "comparison operators", "logical operators", "assignment operator", "modulus", "increment", "decrement", "relational"],
"response": """
🔢 **Operators in C++**

Operators perform operations on variables and values. Think of them as the **verbs** of programming — they tell the computer what action to take.

---

**1️⃣ Arithmetic Operators**

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Addition | `10 + 3` | `13` |
| `-` | Subtraction | `10 - 3` | `7` |
| `*` | Multiplication | `10 * 3` | `30` |
| `/` | Division | `10 / 3` | `3` ⚠️ integer division! |
| `%` | Modulus (remainder) | `10 % 3` | `1` |

🌍 **Modulus in real life:** Checking if today is a work day — `day % 7` gives the day of the week. Checking even/odd — `num % 2 == 0` means even.

---

**2️⃣ Comparison (Relational) Operators**

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `grade == 'A'` |
| `!=` | Not equal to | `result != "Fail"` |
| `>` | Greater than | `score > 50` |
| `<` | Less than | `age < 18` |
| `>=` | Greater or equal | `marks >= 40` |
| `<=` | Less or equal | `temperature <= 100` |

---

**3️⃣ Logical Operators**

| Operator | Meaning | Example |
|----------|---------|---------|
| `&&` | AND — both must be true | `age >= 18 && hasID == true` |
| `||` | OR — at least one true | `isMember || hasCoupon` |
| `!` | NOT — reverses the truth | `!isLate` |

🌍 **Real-Life:** A bank ATM grants access only if `cardIsValid && pinIsCorrect`. Both conditions must be true — that is `&&`.

---

**4️⃣ Increment and Decrement**
```cpp
int x = 5;
x++;   // x = 6  (add 1 after using)
++x;   // x = 7  (add 1 before using)
x--;   // x = 6  (subtract 1 after using)
```

---

**Practical Example — Grade Evaluator:**
```cpp
int score = 75;
bool passed = (score >= 50);
cout << (passed ? "Congratulations, you passed!" : "Please resit the exam.") << endl;
```
""",
"level": "100", "semester": "1"
},

{
"intent": "cpp_if_else",
"keywords": ["if else", "if statement", "conditional", "else if", "decision making", "branching", "conditions", "switch statement"],
"response": """
🔀 **Decision Making — If / Else Statements in C++**

`if/else` lets your program choose different paths based on conditions — just like humans make decisions every day.

---

🌍 **Real-Life Analogy:**
A UPSA security guard at the gate:
- **If** you have a valid student ID → let you in freely
- **Else If** you have a visitor's pass → escort you to the office
- **Else** → you cannot enter

---

**Basic Syntax:**
```cpp
if (condition) {
    // runs when condition is TRUE
} else if (anotherCondition) {
    // runs when second condition is TRUE
} else {
    // runs when ALL conditions are FALSE
}
```

---

**Example — UPSA Grade Classification:**
```cpp
#include <iostream>
using namespace std;

int main() {
    int score;
    cout << "Enter your exam score (0-100): ";
    cin  >> score;

    if (score >= 80) {
        cout << "Grade: A — Excellent! Keep it up! 🏆" << endl;
    } else if (score >= 70) {
        cout << "Grade: B — Very Good 👍" << endl;
    } else if (score >= 60) {
        cout << "Grade: C — Good, aim higher!" << endl;
    } else if (score >= 50) {
        cout << "Grade: D — You passed, but work harder." << endl;
    } else {
        cout << "Grade: F — Please see your lecturer. ❌" << endl;
    }

    return 0;
}
```

---

**Switch Statement — for fixed menu options:**
```cpp
int day = 3;
switch (day) {
    case 1: cout << "Monday";   break;
    case 2: cout << "Tuesday";  break;
    case 3: cout << "Wednesday"; break;
    default: cout << "Other day"; break;
}
```

🌍 **Switch is like a lift (elevator)** — you press a floor button (case) and go directly there. No need to check every floor on the way.

---

**Shorthand — Ternary Operator:**
```cpp
string result = (score >= 50) ? "Pass" : "Fail";
cout << result << endl;
```
""",
"level": "100", "semester": "1"
},

{
"intent": "cpp_loops",
"keywords": ["loops", "for loop", "while loop", "do while", "iteration", "repeat", "loop in c++", "looping"],
"response": """
🔁 **Loops in C++**

Loops let you repeat a block of code multiple times without rewriting it. They are one of the most powerful tools in programming.

---

🌍 **Real-Life Analogy:**
Imagine a lecturer calling out attendance for 200 students. Instead of writing "call next student" 200 times, you say: *"Repeat: call next student, until all 200 are checked."* That is a loop.

---

**1️⃣ For Loop — when you know exactly how many times to repeat:**
```cpp
for (int i = 1; i <= 5; i++) {
    cout << "Student number: " << i << endl;
}
```
**Output:**
```
Student number: 1
Student number: 2
...
Student number: 5
```

---

**2️⃣ While Loop — repeat while a condition is true:**
```cpp
int attempts = 0;
while (attempts < 3) {
    cout << "Enter your PIN: ";
    // check PIN logic here
    attempts++;
}
```
🌍 **Like an ATM** — it keeps asking for your PIN until you succeed or run out of attempts.

---

**3️⃣ Do-While Loop — runs at least once, then checks:**
```cpp
int choice;
do {
    cout << "1. Register  2. Login  3. Exit" << endl;
    cout << "Enter choice: ";
    cin >> choice;
} while (choice != 3);
```
🌍 **Like a restaurant menu** — you always see the menu at least once before deciding to leave.

---

**Practical Example — Sum of Student Scores:**
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, score, total = 0;
    cout << "How many students? ";
    cin  >> n;

    for (int i = 1; i <= n; i++) {
        cout << "Enter score for student " << i << ": ";
        cin  >> score;
        total += score;
    }

    cout << "Total score : " << total << endl;
    cout << "Average     : " << (double)total / n << endl;

    return 0;
}
```

---

⚠️ **Watch out for infinite loops:**
```cpp
// DANGER — this never stops!
while (true) {
    cout << "This runs forever..." << endl;
}
```
Always make sure your loop condition will eventually become false.
""",
"level": "100", "semester": "1"
},

{
"intent": "cpp_functions",
"keywords": ["functions", "function c++", "void function", "return function", "parameters", "arguments", "call function", "define function", "function declaration"],
"response": """
🧩 **Functions in C++**

A **function** is a reusable block of code that performs a specific task. Instead of writing the same code repeatedly, you define it once and call it whenever needed.

---

🌍 **Real-Life Analogy:**
A function is like a **department at UPSA**. The Admissions Office does one job — process applications. You don't need to know exactly how they do it; you just send them a student's details (input) and receive back an admission status (output). 

---

**Basic Syntax:**
```cpp
returnType functionName(parameters) {
    // function body
    return value; // if not void
}
```

**Example — Greeting Function:**
```cpp
#include <iostream>
#include <string>
using namespace std;

// Function definition
void greetStudent(string name) {
    cout << "Welcome to UPSA, " << name << "!" << endl;
}

int main() {
    greetStudent("Ama");    // Call 1
    greetStudent("Kofi");   // Call 2
    greetStudent("Efua");   // Call 3
    return 0;
}
```

---

**Function that returns a value — Calculate GPA:**
```cpp
double calculateGPA(double totalPoints, int courses) {
    return totalPoints / courses;
}

int main() {
    double gpa = calculateGPA(15.0, 4);
    cout << "Your GPA is: " << gpa << endl;
    return 0;
}
```

---

**Function with multiple parameters:**
```cpp
int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int main() {
    cout << "3 + 4 = " << add(3, 4)      << endl;
    cout << "3 x 4 = " << multiply(3, 4) << endl;
    return 0;
}
```

---

**Types of Functions:**

| Type | Returns | Example |
|------|---------|---------|
| `void` | Nothing | `void printMenu()` |
| Value-returning | A result | `int getAge()` |
| With parameters | Takes input | `double area(double r)` |

---

💡 **Rule:** Each function should do **one thing well**. If a function does too many things, split it up — this is called the **Single Responsibility Principle**.
""",
"level": "100", "semester": "1"
},

{
"intent": "cpp_arrays",
"keywords": ["arrays", "array c++", "array declaration", "array index", "array loop", "list of values", "multiple values", "array size"],
"response": """
📊 **Arrays in C++**

An **array** stores multiple values of the **same data type** under a single variable name. Instead of creating 30 variables for 30 students, you create one array.

---

🌍 **Real-Life Analogy:**
An array is like a **row of seats in a lecture hall** — each seat has a number (index), and you can refer to any seat directly: "Seat 0, Seat 1, Seat 2..."

---

**Declaring an Array:**
```cpp
datatype arrayName[size];
datatype arrayName[size] = {value1, value2, value3};
```

**Example:**
```cpp
int scores[5] = {85, 72, 90, 68, 77};

// Access individual elements
cout << scores[0] << endl;   // 85 — first element
cout << scores[4] << endl;   // 77 — last element
```

⚠️ **Important:** Array indices start at **0**, not 1!

---

**Looping Through an Array:**
```cpp
#include <iostream>
using namespace std;

int main() {
    int scores[5] = {85, 72, 90, 68, 77};
    int total = 0;

    for (int i = 0; i < 5; i++) {
        cout << "Student " << (i+1) << " score: " << scores[i] << endl;
        total += scores[i];
    }

    cout << "Class Average: " << (double)total / 5 << endl;
    return 0;
}
```

---

**Finding the Highest Score:**
```cpp
int scores[5] = {85, 72, 90, 68, 77};
int highest = scores[0];

for (int i = 1; i < 5; i++) {
    if (scores[i] > highest) {
        highest = scores[i];
    }
}
cout << "Highest score: " << highest << endl;
```

---

**2D Array (Table/Grid) — like a seating chart:**
```cpp
int marks[3][2] = {
    {85, 90},   // Student 1: Maths, Science
    {70, 75},   // Student 2
    {95, 88}    // Student 3
};

cout << marks[0][1] << endl;  // Student 1, Science = 90
```

---

⚠️ **Common Mistake:** Going out of bounds — accessing `scores[5]` in a 5-element array crashes the program. The valid range is `scores[0]` to `scores[4]`.
""",
"level": "100", "semester": "1"
},

{
"intent": "cpp_strings",
"keywords": ["strings", "string c++", "string methods", "string length", "string functions", "text", "characters", "string operations", "substring"],
"response": """
🔤 **Strings in C++**

A **string** is a sequence of characters used to represent text. In C++, you can use the `string` class from the `<string>` library.

---

🌍 **Real-Life Analogy:**
A string is like a **necklace of beads** — each bead is a character, and the whole necklace together forms a word or sentence. You can add beads, count them, or pick any specific bead by its position.

---

**Declaring Strings:**
```cpp
#include <string>
string greeting = "Hello, UPSA!";
string name     = "Ama Owusu";
```

---

**Common String Operations:**

```cpp
string s = "Hello, World!";

// Length of string
cout << s.length() << endl;          // 13

// Access a character
cout << s[0] << endl;                // H

// Concatenation (joining strings)
string first = "Kofi";
string last  = "Boateng";
string full  = first + " " + last;
cout << full << endl;                // Kofi Boateng

// Substring
cout << s.substr(7, 5) << endl;      // World

// Find a word
cout << s.find("World") << endl;     // 7 (position)

// Convert to uppercase (needs <algorithm>)
transform(s.begin(), s.end(), s.begin(), ::toupper);
cout << s << endl;                   // HELLO, WORLD!

// Compare strings
string a = "apple", b = "apple";
if (a == b) cout << "Same string!" << endl;
```

---

**Practical Example — Name Formatter:**
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string firstName, lastName;
    cout << "Enter first name: "; cin >> firstName;
    cout << "Enter last name : "; cin >> lastName;

    string fullName = firstName + " " + lastName;
    cout << "Full name   : " << fullName           << endl;
    cout << "Characters  : " << fullName.length()  << endl;
    cout << "First letter: " << fullName[0]        << endl;

    return 0;
}
```

---

**Useful String Methods Summary:**

| Method | What it does |
|--------|-------------|
| `.length()` | Returns number of characters |
| `.substr(pos, len)` | Extracts part of the string |
| `.find("text")` | Returns position of text |
| `.replace(pos, len, "new")` | Replaces part of string |
| `.empty()` | Returns true if string is empty |
| `.erase(pos, len)` | Removes characters |
""",
"level": "100", "semester": "1"
},

# ───────────────────────────────────────────────────────────────────────────
#  LEVEL 200 — INTERMEDIATE
# ───────────────────────────────────────────────────────────────────────────

{
"intent": "cpp_pointers",
"keywords": ["pointers", "pointer c++", "memory address", "pointer declaration", "dereference", "null pointer", "pointer arithmetic", "address of"],
"response": """
🔍 **Pointers in C++**

A **pointer** is a variable that stores the **memory address** of another variable — instead of storing the value itself, it stores where the value lives in memory.

---

🌍 **Real-Life Analogy:**
Imagine a **house** (the variable) and its **street address** (the pointer). You don't need to carry the house with you — you just keep the address and can find the house whenever you need it. A pointer is the street address of a variable.

---

**Declaring and Using Pointers:**
```cpp
int age   = 21;
int* ptr  = &age;      // ptr stores the address of 'age'

cout << age   << endl;  // 21          — the value
cout << &age  << endl;  // 0x7fff...   — the memory address
cout << ptr   << endl;  // 0x7fff...   — same address (stored in ptr)
cout << *ptr  << endl;  // 21          — dereference: get value at address
```

**Key Symbols:**
| Symbol | Meaning |
|--------|---------|
| `&` | "Address of" — gives the memory address |
| `*` | "Dereference" — gets value at an address |

---

**Modifying a Variable through a Pointer:**
```cpp
int score = 75;
int* p    = &score;

*p = 90;   // changes score to 90 through the pointer
cout << score << endl;  // 90
```

---

**Null Pointer — pointer that points to nothing:**
```cpp
int* ptr = nullptr;   // safe, points to nothing

if (ptr == nullptr) {
    cout << "Pointer is not pointing to anything." << endl;
}
```

---

**Pointers and Arrays:**
Arrays and pointers are closely related — an array name is essentially a pointer to its first element.
```cpp
int numbers[3] = {10, 20, 30};
int* p = numbers;        // points to numbers[0]

cout << *p     << endl;  // 10
cout << *(p+1) << endl;  // 20
cout << *(p+2) << endl;  // 30
```

---

**Passing by Pointer to a Function:**
```cpp
void doubleValue(int* x) {
    *x = *x * 2;
}

int main() {
    int num = 5;
    doubleValue(&num);
    cout << num << endl;  // 10
}
```

🌍 **Real-Life:** When a doctor updates your medical record, they don't take a copy of your file — they directly edit the original. Passing by pointer = editing the original.
""",
"level": "200", "semester": "1"
},

{
"intent": "cpp_references",
"keywords": ["references", "reference c++", "pass by reference", "reference variable", "& reference", "call by reference"],
"response": """
🔗 **References in C++**

A **reference** is an alias — another name for an existing variable. It refers to the same memory location.

---

🌍 **Real-Life Analogy:**
You are known as "Kofi" at home, "Mr. Mensah" at work, and "Coach" on the football pitch — but you are the **same person**. All three names refer to you. References work the same way.

---

**Declaring a Reference:**
```cpp
int age = 21;
int& ref = age;   // ref is another name for age

ref = 25;         // changes age too!
cout << age << endl;   // 25
cout << ref << endl;   // 25 — same memory location
```

---

**References vs Pointers:**

| Feature | Pointer | Reference |
|---------|---------|-----------|
| Can be null | Yes | No |
| Can be reassigned | Yes | No (fixed at declaration) |
| Syntax to access value | `*ptr` | `ref` (directly) |
| Safer to use | Less | More |

---

**Pass by Reference — Function modifying original values:**
```cpp
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    int x = 10, y = 20;
    swap(x, y);
    cout << x << " " << y << endl;  // 20 10
}
```

Without `&`, the function would only swap **copies** — the original x and y would stay the same.

---

**Const Reference — read-only access:**
```cpp
void printName(const string& name) {
    cout << "Name: " << name << endl;
    // name = "other";  // ERROR — cannot modify const reference
}
```

Using `const&` avoids copying large data (like strings or arrays) while still preventing accidental modification.
""",
"level": "200", "semester": "1"
},

{
"intent": "cpp_oop_classes_objects",
"keywords": ["classes", "objects", "oop", "object oriented", "class c++", "object c++", "class definition", "attributes", "methods", "instance"],
"response": """
🏗️ **Classes and Objects in C++ (OOP)**

**Object-Oriented Programming (OOP)** models real-world entities as objects. A **class** is the blueprint; an **object** is the actual thing built from that blueprint.

---

🌍 **Real-Life Analogy:**
A **class** is like the **architectural plan** for a building. The **object** is the actual building constructed from that plan. You can build many buildings (objects) from one plan (class).

---

**Defining a Class:**
```cpp
class Student {
public:
    // Attributes (data)
    string name;
    int    studentID;
    double gpa;

    // Method (behaviour)
    void displayInfo() {
        cout << "Name : " << name      << endl;
        cout << "ID   : " << studentID << endl;
        cout << "GPA  : " << gpa       << endl;
    }

    bool hasHonours() {
        return gpa >= 3.5;
    }
};
```

---

**Creating and Using Objects:**
```cpp
int main() {
    // Create two Student objects
    Student s1, s2;

    s1.name      = "Ama Owusu";
    s1.studentID = 20240001;
    s1.gpa       = 3.8;

    s2.name      = "Kofi Boateng";
    s2.studentID = 20240002;
    s2.gpa       = 2.9;

    s1.displayInfo();
    cout << (s1.hasHonours() ? "Honours student!" : "Regular student") << endl;

    s2.displayInfo();

    return 0;
}
```

---

**Access Modifiers:**

| Modifier | Meaning |
|----------|---------|
| `public` | Accessible from anywhere |
| `private` | Only accessible within the class |
| `protected` | Accessible within class and subclasses |

---

**Private data with Getters and Setters:**
```cpp
class BankAccount {
private:
    double balance;   // hidden from outside

public:
    void setBalance(double amount) {
        if (amount >= 0) balance = amount;
    }

    double getBalance() {
        return balance;
    }
};
```

🌍 **Like an ATM:** You can check your balance and deposit (public interface), but you cannot directly reach into the bank's vault (private data). The bank controls access.
""",
"level": "200", "semester": "1"
},

{
"intent": "cpp_constructors_destructors",
"keywords": ["constructor", "destructor", "constructor c++", "default constructor", "parameterised constructor", "object initialisation", "~class"],
"response": """
🏗️ **Constructors and Destructors in C++**

A **constructor** automatically initialises an object when it is created. A **destructor** automatically cleans up when the object is destroyed.

---

🌍 **Real-Life Analogy:**
- **Constructor** = The moment you move into a new flat — you set up electricity, furniture, and internet. It runs automatically on arrival.
- **Destructor** = The moment you move out — you clean up, return keys, and cancel subscriptions. It runs automatically on departure.

---

**Default Constructor:**
```cpp
class Student {
public:
    string name;
    int    id;

    // Default constructor — no parameters
    Student() {
        name = "Unknown";
        id   = 0;
        cout << "Student object created." << endl;
    }

    // Destructor
    ~Student() {
        cout << "Student object destroyed." << endl;
    }
};

int main() {
    Student s;   // Constructor runs here automatically
    cout << s.name << endl;
}              // Destructor runs here automatically
```

---

**Parameterised Constructor:**
```cpp
class Student {
public:
    string name;
    double gpa;

    Student(string n, double g) {
        name = n;
        gpa  = g;
    }

    void display() {
        cout << name << " — GPA: " << gpa << endl;
    }
};

int main() {
    Student s1("Ama Owusu", 3.9);
    Student s2("Kofi Mensah", 3.2);
    s1.display();
    s2.display();
}
```

---

**Constructor Initialiser List (preferred style):**
```cpp
Student(string n, double g) : name(n), gpa(g) {}
```

---

**Copy Constructor:**
```cpp
Student s1("Ama", 3.9);
Student s2 = s1;   // Copies all values from s1 into s2
```

---

💡 **Rule:** Always initialise all your class attributes in the constructor — never leave them with garbage values.
""",
"level": "200", "semester": "1"
},

{
"intent": "cpp_inheritance",
"keywords": ["inheritance", "inherit c++", "base class", "derived class", "parent class", "child class", "extends", "super class", "subclass", "is-a relationship"],
"response": """
👨‍👩‍👧 **Inheritance in C++**

**Inheritance** allows a class (child) to acquire the properties and behaviours of another class (parent), promoting **code reuse**.

---

🌍 **Real-Life Analogy:**
A **Person** has a name, age, and can speak. A **Student** is a Person who also has a student ID and can study. A **Lecturer** is a Person who can teach. They all **inherit** the basic human traits, but each adds their own specialised behaviour.

---

**Base Class (Parent):**
```cpp
class Person {
public:
    string name;
    int    age;

    void introduce() {
        cout << "Hi, I am " << name << ", aged " << age << "." << endl;
    }
};
```

**Derived Class (Child) — inherits Person:**
```cpp
class Student : public Person {
public:
    int    studentID;
    double gpa;

    void study() {
        cout << name << " is studying hard!" << endl;
    }

    void displayRecord() {
        introduce();   // inherited from Person
        cout << "ID : " << studentID << endl;
        cout << "GPA: " << gpa       << endl;
    }
};

class Lecturer : public Person {
public:
    string department;

    void teach() {
        cout << name << " is teaching " << department << "." << endl;
    }
};
```

---

**Using Inherited Classes:**
```cpp
int main() {
    Student s;
    s.name      = "Ama Owusu";
    s.age       = 20;
    s.studentID = 20240001;
    s.gpa       = 3.8;
    s.displayRecord();
    s.study();

    Lecturer l;
    l.name       = "Dr. Mensah";
    l.age        = 45;
    l.department = "ITM";
    l.teach();
}
```

---

**Types of Inheritance:**

| Type | Syntax | Example |
|------|--------|---------|
| Single | `class B : public A` | Student inherits Person |
| Multilevel | `C inherits B inherits A` | PostGrad inherits Student |
| Multiple | `class C : public A, public B` | TeachingAssistant inherits both |

---

⚠️ **Key Rule:** Use inheritance for **"is-a"** relationships — a Student IS-A Person. Do not use it for "has-a" relationships (a Car HAS-A Engine — use composition instead).
""",
"level": "200", "semester": "1"
},

{
"intent": "cpp_polymorphism",
"keywords": ["polymorphism", "virtual function", "override", "runtime polymorphism", "function overriding", "virtual", "dynamic binding", "overloading"],
"response": """
🎭 **Polymorphism in C++**

**Polymorphism** means "many forms" — one function or method behaves differently depending on the object that calls it.

---

🌍 **Real-Life Analogy:**
A **person** can "communicate" in different ways — a student submits an assignment, a lecturer gives a lecture, an admin files a report. The action is "communicate" but the behaviour differs based on who is doing it.

---

**Two Types of Polymorphism:**

**1️⃣ Compile-Time (Function Overloading):**
Same function name, different parameters:
```cpp
class Calculator {
public:
    int    add(int a, int b)       { return a + b; }
    double add(double a, double b) { return a + b; }
    int    add(int a, int b, int c){ return a + b + c; }
};

int main() {
    Calculator c;
    cout << c.add(3, 4)       << endl;  // 7
    cout << c.add(3.5, 2.1)   << endl;  // 5.6
    cout << c.add(1, 2, 3)    << endl;  // 6
}
```

---

**2️⃣ Runtime Polymorphism (Virtual Functions):**
```cpp
class Shape {
public:
    virtual void draw() {
        cout << "Drawing a shape." << endl;
    }
};

class Circle : public Shape {
public:
    void draw() override {
        cout << "Drawing a Circle ⭕" << endl;
    }
};

class Rectangle : public Shape {
public:
    void draw() override {
        cout << "Drawing a Rectangle ▭" << endl;
    }
};

int main() {
    Shape* s1 = new Circle();
    Shape* s2 = new Rectangle();

    s1->draw();   // Drawing a Circle ⭕
    s2->draw();   // Drawing a Rectangle ▭

    delete s1; delete s2;
}
```

The **same pointer type** (`Shape*`) calls **different functions** depending on the actual object — that is runtime polymorphism.

---

**Abstract Classes (Pure Virtual):**
```cpp
class Animal {
public:
    virtual void makeSound() = 0;   // Pure virtual — must be overridden
};

class Dog : public Animal {
public:
    void makeSound() override { cout << "Woof!" << endl; }
};
```

`Animal` cannot be instantiated directly — it is a blueprint only.

---

💡 **Key Takeaway:** Polymorphism lets you write **generic, flexible code** that works with many different types — reducing duplication and improving maintainability.
""",
"level": "200", "semester": "1"
},

{
"intent": "cpp_file_handling",
"keywords": ["file handling", "file c++", "read file", "write file", "fstream", "ofstream", "ifstream", "open file", "save to file", "file operations"],
"response": """
📁 **File Handling in C++**

File handling allows your program to **read from** and **write to** files on disk — enabling data to persist after the program closes.

---

🌍 **Real-Life Analogy:**
Without file handling, your program's data disappears when you close it — like writing on a whiteboard. File handling is like writing in a **permanent notebook** — the data stays even after you leave.

---

**Required Header:**
```cpp
#include <fstream>
```

**Three Stream Types:**

| Class | Purpose |
|-------|---------|
| `ofstream` | Output — writing to a file |
| `ifstream` | Input — reading from a file |
| `fstream` | Both reading and writing |

---

**Writing to a File:**
```cpp
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ofstream outFile("students.txt");

    if (!outFile) {
        cout << "Error opening file!" << endl;
        return 1;
    }

    outFile << "Ama Owusu, 20240001, 3.9" << endl;
    outFile << "Kofi Mensah, 20240002, 3.2" << endl;

    outFile.close();
    cout << "Data saved to students.txt" << endl;
    return 0;
}
```

---

**Reading from a File:**
```cpp
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ifstream inFile("students.txt");
    string   line;

    if (!inFile) {
        cout << "File not found!" << endl;
        return 1;
    }

    cout << "=== Student Records ===" << endl;
    while (getline(inFile, line)) {
        cout << line << endl;
    }

    inFile.close();
    return 0;
}
```

---

**Appending to an existing file (not overwriting):**
```cpp
ofstream outFile("students.txt", ios::app);
outFile << "Efua Asante, 20240003, 3.5" << endl;
outFile.close();
```

---

**Full Student Record System:**
```cpp
void saveStudent(string name, int id, double gpa) {
    ofstream f("records.txt", ios::app);
    f << name << "," << id << "," << gpa << endl;
    f.close();
}
```

---

💡 **Always close your files** with `.close()` after use — leaving files open wastes system resources and can cause data corruption.
""",
"level": "200", "semester": "1"
},

{
"intent": "cpp_dynamic_memory",
"keywords": ["dynamic memory", "heap", "new", "delete", "malloc", "memory allocation", "dynamic array", "memory leak", "stack heap"],
"response": """
🧠 **Dynamic Memory Allocation in C++**

Dynamic memory lets you allocate memory **at runtime** — when you don't know in advance how much memory you'll need.

---

🌍 **Real-Life Analogy:**
**Stack memory** is like the **seats already set up in a lecture hall** — fixed, pre-arranged.
**Heap memory** is like **bringing in extra chairs** when more students arrive than expected — flexible, on-demand.

---

**Stack vs Heap:**

| Feature | Stack | Heap |
|---------|-------|------|
| Allocation | Automatic | Manual (`new`) |
| Deallocation | Automatic | Manual (`delete`) |
| Size | Limited | Large |
| Speed | Faster | Slower |

---

**Allocating a Single Variable:**
```cpp
int* p = new int;     // allocate one int on the heap
*p = 42;
cout << *p << endl;   // 42
delete p;             // MUST free when done
p = nullptr;          // good practice
```

---

**Allocating an Array Dynamically:**
```cpp
int n;
cout << "How many students? ";
cin  >> n;

int* scores = new int[n];   // array size decided at runtime!

for (int i = 0; i < n; i++) {
    cout << "Score " << (i+1) << ": ";
    cin  >> scores[i];
}

// Display
for (int i = 0; i < n; i++) {
    cout << scores[i] << " ";
}

delete[] scores;    // use delete[] for arrays
scores = nullptr;
```

---

**Memory Leak — what happens when you forget `delete`:**
```cpp
// BAD — memory leak!
void badFunction() {
    int* p = new int(100);
    // forgot delete p — memory is never freed!
}
```

Every `new` must have a matching `delete`. Forgetting to `delete` causes your program to slowly consume more and more RAM — called a **memory leak**.

---

💡 **Modern C++ alternative:** Use `smart pointers` (`unique_ptr`, `shared_ptr`) from `<memory>` — they delete automatically and prevent memory leaks.
```cpp
#include <memory>
auto p = make_unique<int>(42);
// No need to call delete — handled automatically!
```
""",
"level": "200", "semester": "1"
},

# ───────────────────────────────────────────────────────────────────────────
#  LEVEL 300 — ADVANCED
# ───────────────────────────────────────────────────────────────────────────

{
"intent": "cpp_templates",
"keywords": ["templates", "template c++", "generic programming", "function template", "class template", "typename", "template parameter"],
"response": """
🧬 **Templates in C++ — Generic Programming**

**Templates** allow you to write functions and classes that work with **any data type** — write once, use with int, double, string, or any custom type.

---

🌍 **Real-Life Analogy:**
A **template** is like a **form** at UPSA — the same form works for registering any student, regardless of their name, ID, or programme. You fill in the blanks with whatever type of data you need.

---

**Function Template:**
```cpp
#include <iostream>
using namespace std;

// Works for ANY type T
template <typename T>
T findMax(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    cout << findMax(10, 20)       << endl;   // 20    (int)
    cout << findMax(3.14, 2.72)   << endl;   // 3.14  (double)
    cout << findMax('z', 'a')     << endl;   // z     (char)
}
```

The compiler **generates a separate version** of the function for each type used — at compile time.

---

**Class Template — Generic Stack:**
```cpp
template <typename T>
class Stack {
private:
    T    data[100];
    int  top = -1;

public:
    void push(T value) {
        data[++top] = value;
    }

    T pop() {
        return data[top--];
    }

    bool isEmpty() {
        return top == -1;
    }
};

int main() {
    Stack<int>    intStack;
    Stack<string> strStack;

    intStack.push(10);
    intStack.push(20);
    cout << intStack.pop() << endl;   // 20

    strStack.push("UPSA");
    strStack.push("ITM");
    cout << strStack.pop() << endl;   // ITM
}
```

---

**Multiple Template Parameters:**
```cpp
template <typename K, typename V>
class Pair {
public:
    K key;
    V value;
    Pair(K k, V v) : key(k), value(v) {}
    void display() {
        cout << key << " : " << value << endl;
    }
};

int main() {
    Pair<string, int> p("StudentID", 20240001);
    p.display();   // StudentID : 20240001
}
```

---

💡 **Why Templates?** The C++ Standard Template Library (STL) — `vector`, `map`, `set`, `queue` — is entirely built on templates. Mastering templates unlocks the full power of the STL.
""",
"level": "300", "semester": "1"
},

{
"intent": "cpp_stl",
"keywords": ["stl", "standard template library", "vector", "map", "set", "queue", "stack stl", "list", "algorithm", "iterator", "containers"],
"response": """
📚 **The Standard Template Library (STL) in C++**

The **STL** is a collection of ready-made, highly optimised data structures and algorithms built into C++. You don't need to implement them from scratch.

---

🌍 **Real-Life Analogy:**
The STL is like the **tools already in a professional workshop** — you don't forge your own hammer; you pick the right tool from the shelf and get to work.

---

**1️⃣ Vector — dynamic array (most used container):**
```cpp
#include <vector>
#include <iostream>
using namespace std;

int main() {
    vector<int> scores;

    scores.push_back(85);
    scores.push_back(92);
    scores.push_back(78);

    cout << "Size   : " << scores.size()  << endl;  // 3
    cout << "First  : " << scores[0]      << endl;  // 85
    cout << "Last   : " << scores.back()  << endl;  // 78

    scores.pop_back();  // removes 78

    for (int s : scores) {    // range-based for loop
        cout << s << " ";
    }
}
```

---

**2️⃣ Map — key-value pairs (like a dictionary):**
```cpp
#include <map>
map<string, int> studentGrades;

studentGrades["Ama"]  = 90;
studentGrades["Kofi"] = 75;
studentGrades["Efua"] = 88;

cout << studentGrades["Ama"] << endl;   // 90

// Iterate
for (auto& pair : studentGrades) {
    cout << pair.first << " : " << pair.second << endl;
}
```

---

**3️⃣ Set — unique sorted values:**
```cpp
#include <set>
set<int> uniqueIDs = {101, 203, 101, 305, 203};
// Duplicates are removed automatically
// Contains: {101, 203, 305}

for (int id : uniqueIDs) cout << id << " ";
```

---

**4️⃣ Queue — First In First Out (FIFO):**
```cpp
#include <queue>
queue<string> waitingList;
waitingList.push("Ama");
waitingList.push("Kofi");
waitingList.push("Efua");

cout << waitingList.front() << endl;   // Ama (first in)
waitingList.pop();                      // removes Ama
cout << waitingList.front() << endl;   // Kofi
```
🌍 **Like a bank queue** — first person in is first served.

---

**5️⃣ STL Algorithms:**
```cpp
#include <algorithm>
#include <vector>
vector<int> v = {5, 3, 8, 1, 9, 2};

sort(v.begin(), v.end());               // {1, 2, 3, 5, 8, 9}
int mx = *max_element(v.begin(), v.end()); // 9
int mn = *min_element(v.begin(), v.end()); // 1
reverse(v.begin(), v.end());            // {9, 8, 5, 3, 2, 1}
```

---

**STL Container Cheat Sheet:**

| Container | Use When |
|-----------|----------|
| `vector` | You need a dynamic array |
| `list` | Frequent insertions/deletions in middle |
| `map` | Key-value lookup |
| `set` | Unique sorted elements |
| `queue` | FIFO processing |
| `stack` | LIFO processing |
| `priority_queue` | Always access highest priority item |
""",
"level": "300", "semester": "1"
},

{
"intent": "cpp_exception_handling",
"keywords": ["exception handling", "try catch", "throw exception", "exception c++", "runtime error", "error handling", "try block", "catch block"],
"response": """
🛡️ **Exception Handling in C++**

**Exception handling** lets your program deal with **runtime errors gracefully** — instead of crashing, it catches the problem and responds appropriately.

---

🌍 **Real-Life Analogy:**
You attempt to make an ATM withdrawal:
- **Try:** Request GHS 500
- **Exception thrown:** Insufficient funds
- **Catch:** Display "Insufficient balance, please enter a lower amount"
- **Finally (execution continues):** Return the card

Without exception handling, the ATM would just crash!

---

**Basic Syntax:**
```cpp
try {
    // code that might cause an error
    throw exceptionValue;
} catch (exceptionType e) {
    // handle the error
}
```

---

**Example — Division by Zero:**
```cpp
#include <iostream>
#include <stdexcept>
using namespace std;

double divide(double a, double b) {
    if (b == 0) {
        throw runtime_error("Error: Division by zero is not allowed!");
    }
    return a / b;
}

int main() {
    try {
        cout << divide(10, 2)  << endl;   // 5
        cout << divide(10, 0)  << endl;   // throws!
    } catch (runtime_error& e) {
        cout << "Caught: " << e.what() << endl;
    }

    cout << "Program continues normally." << endl;
    return 0;
}
```

---

**Multiple Catch Blocks:**
```cpp
try {
    int choice;
    cin >> choice;
    if (choice == 1) throw "String error";
    if (choice == 2) throw 404;
    if (choice == 3) throw 3.14;
}
catch (const char* msg)  { cout << "String: " << msg << endl; }
catch (int code)          { cout << "Code: "   << code << endl; }
catch (double val)        { cout << "Value: "  << val  << endl; }
catch (...)               { cout << "Unknown error!" << endl; }
```

---

**Custom Exception Class:**
```cpp
class InsufficientFundsException : public exception {
private:
    double amount;
public:
    InsufficientFundsException(double a) : amount(a) {}
    const char* what() const noexcept override {
        return "Insufficient funds for this transaction.";
    }
    double getAmount() { return amount; }
};

void withdraw(double balance, double amount) {
    if (amount > balance) throw InsufficientFundsException(amount);
    cout << "Withdrawal successful." << endl;
}

int main() {
    try {
        withdraw(100.0, 500.0);
    } catch (InsufficientFundsException& e) {
        cout << e.what() << endl;
    }
}
```

---

💡 **Best Practices:**
- Catch by **reference** (`catch (exception& e)`) not by value
- Never use exceptions for normal control flow — only for actual errors
- Always clean up resources in `catch` blocks or use RAII
""",
"level": "300", "semester": "1"
},

{
"intent": "cpp_smart_pointers",
"keywords": ["smart pointers", "unique_ptr", "shared_ptr", "weak_ptr", "memory management", "raii", "automatic memory", "smart pointer c++"],
"response": """
🧠 **Smart Pointers in C++ — Modern Memory Management**

**Smart pointers** automatically manage memory — they `delete` themselves when no longer needed, preventing memory leaks without manual cleanup.

---

🌍 **Real-Life Analogy:**
A **raw pointer** is like borrowing a car with no return policy — it's your job to remember to return it. A **smart pointer** is like a rental car with GPS tracking and auto-return — it goes back automatically when your rental period ends.

---

**Three Types of Smart Pointers:**

| Type | Ownership | Use Case |
|------|-----------|---------|
| `unique_ptr` | Exclusive — only one owner | When one object owns a resource |
| `shared_ptr` | Shared — multiple owners | When multiple objects share a resource |
| `weak_ptr` | Non-owning observer | To break circular references |

---

**1️⃣ unique_ptr — exclusive ownership:**
```cpp
#include <memory>
#include <iostream>
using namespace std;

class Student {
public:
    string name;
    Student(string n) : name(n) {
        cout << name << " created." << endl;
    }
    ~Student() {
        cout << name << " destroyed." << endl;
    }
};

int main() {
    unique_ptr<Student> s = make_unique<Student>("Ama");
    cout << s->name << endl;

    // No need to call delete — automatic!
}  // "Ama destroyed." prints here automatically
```

Cannot copy a `unique_ptr`, only **move** it:
```cpp
unique_ptr<Student> s2 = move(s);   // s is now empty, s2 owns it
```

---

**2️⃣ shared_ptr — shared ownership:**
```cpp
shared_ptr<Student> s1 = make_shared<Student>("Kofi");
shared_ptr<Student> s2 = s1;   // Both own the same Student

cout << s1.use_count() << endl;   // 2 — two owners
// Deleted only when BOTH s1 and s2 go out of scope
```

---

**3️⃣ weak_ptr — observe without owning:**
```cpp
shared_ptr<Student> s = make_shared<Student>("Efua");
weak_ptr<Student>   w = s;   // does not increase count

cout << s.use_count() << endl;   // still 1

if (auto locked = w.lock()) {   // safe access
    cout << locked->name << endl;
}
```

---

💡 **Golden Rule for Modern C++:**
- Prefer `make_unique<T>()` over `new T`
- Prefer `make_shared<T>()` when sharing
- **Never use raw `new`/`delete`** unless you have a specific reason
""",
"level": "300", "semester": "1"
},

{
"intent": "cpp_multithreading",
"keywords": ["multithreading", "threads", "thread c++", "parallel", "concurrency", "mutex", "thread safety", "async", "concurrent programming"],
"response": """
⚡ **Multithreading in C++**

**Multithreading** allows a program to run multiple tasks **simultaneously** — like your computer playing music while you browse the internet at the same time.

---

🌍 **Real-Life Analogy:**
A **single-threaded** program is like one cashier serving an entire supermarket queue alone. **Multithreading** is like opening 4 checkout lanes at once — customers are served in parallel, much faster.

---

**Required Header:**
```cpp
#include <thread>
#include <mutex>
```

---

**Creating and Running Threads:**
```cpp
#include <iostream>
#include <thread>
using namespace std;

void downloadFile(string filename) {
    cout << "Downloading: " << filename << endl;
    // simulate work
    this_thread::sleep_for(chrono::seconds(2));
    cout << filename << " downloaded!" << endl;
}

int main() {
    // Start two threads simultaneously
    thread t1(downloadFile, "report.pdf");
    thread t2(downloadFile, "lecture.mp4");

    // Wait for both to finish before continuing
    t1.join();
    t2.join();

    cout << "All downloads complete." << endl;
    return 0;
}
```

---

**Race Condition — the danger of shared data:**
```cpp
int counter = 0;

void increment() {
    for (int i = 0; i < 1000; i++) {
        counter++;   // UNSAFE — two threads modifying at once!
    }
}
```
Without protection, two threads reading and writing `counter` simultaneously gives unpredictable results.

---

**Mutex — locking to prevent race conditions:**
```cpp
#include <mutex>
int   counter = 0;
mutex mtx;

void safeIncrement() {
    for (int i = 0; i < 1000; i++) {
        lock_guard<mutex> lock(mtx);   // auto-unlocks when scope ends
        counter++;
    }
}

int main() {
    thread t1(safeIncrement);
    thread t2(safeIncrement);
    t1.join();
    t2.join();
    cout << "Counter: " << counter << endl;  // always 2000
}
```

---

**Async and Future — get a return value from a thread:**
```cpp
#include <future>

int calculateSum(int a, int b) {
    return a + b;
}

int main() {
    future<int> result = async(launch::async, calculateSum, 100, 200);
    cout << "Sum: " << result.get() << endl;  // 300
}
```

---

💡 **Key Terms:**
| Term | Meaning |
|------|---------|
| Thread | Independent unit of execution |
| Mutex | Lock that prevents simultaneous access |
| Race Condition | Bug from unsynchronised shared data |
| Deadlock | Two threads each waiting for the other's lock |
| `join()` | Wait for thread to complete |
""",
"level": "300", "semester": "1"
},

{
"intent": "cpp_design_patterns",
"keywords": ["design patterns", "singleton", "factory pattern", "observer pattern", "strategy pattern", "software design", "pattern c++", "creational patterns"],
"response": """
🏛️ **Design Patterns in C++**

**Design patterns** are proven, reusable solutions to commonly occurring software design problems. They are not code — they are **blueprints** for solving design challenges.

---

🌍 **Real-Life Analogy:**
A design pattern is like a **building architect's standard solution** — when a client says "I need a fire exit," the architect already knows the standard design. They don't invent it from scratch each time.

---

**Three Categories:**

| Category | Purpose | Examples |
|----------|---------|---------|
| Creational | How objects are created | Singleton, Factory, Builder |
| Structural | How objects are composed | Adapter, Decorator, Facade |
| Behavioural | How objects communicate | Observer, Strategy, Command |

---

**1️⃣ Singleton — only one instance ever exists:**
```cpp
class DatabaseConnection {
private:
    static DatabaseConnection* instance;
    DatabaseConnection() {
        cout << "Database connected." << endl;
    }

public:
    static DatabaseConnection* getInstance() {
        if (!instance) {
            instance = new DatabaseConnection();
        }
        return instance;
    }

    void query(string sql) {
        cout << "Running: " << sql << endl;
    }
};

DatabaseConnection* DatabaseConnection::instance = nullptr;

int main() {
    auto* db1 = DatabaseConnection::getInstance();
    auto* db2 = DatabaseConnection::getInstance();
    // db1 and db2 point to the SAME object — only one connection
    db1->query("SELECT * FROM students");
}
```
🌍 **Like a university's single printing office** — no matter which department requests a print, they all go through one central office.

---

**2️⃣ Observer — notify many objects of a change:**
```cpp
class EventObserver {
public:
    virtual void update(string event) = 0;
};

class EmailNotifier : public EventObserver {
public:
    void update(string event) override {
        cout << "Email sent: " << event << endl;
    }
};

class SMSNotifier : public EventObserver {
public:
    void update(string event) override {
        cout << "SMS sent: " << event << endl;
    }
};
```
🌍 **Like UPSA's announcement system** — one announcement goes to all students via email, SMS, and the noticeboard simultaneously.

---

**3️⃣ Factory — create objects without specifying the exact class:**
```cpp
class Shape { public: virtual void draw() = 0; };
class Circle    : public Shape { public: void draw() { cout << "Circle ⭕";    }};
class Square    : public Shape { public: void draw() { cout << "Square ▪";    }};

Shape* createShape(string type) {
    if (type == "circle")   return new Circle();
    if (type == "square")   return new Square();
    return nullptr;
}

int main() {
    Shape* s = createShape("circle");
    s->draw();
    delete s;
}
```

---

💡 **Why Learn Design Patterns?**
They make your code easier to **extend**, **maintain**, and **understand** — and they are the language software engineers use to discuss architecture at a professional level.
""",
"level": "300", "semester": "1"
},

{
"intent": "cpp_data_structures",
"keywords": ["data structures", "linked list", "binary tree", "stack", "queue data structure", "hash table", "graph", "tree traversal", "node"],
"response": """
🌳 **Data Structures in C++**

A **data structure** is a way of organising and storing data so it can be accessed and modified efficiently. Choosing the right data structure can make the difference between a program that runs in milliseconds and one that takes hours.

---

**1️⃣ Linked List — chain of nodes:**

🌍 **Like a train** — each carriage (node) connects to the next. You can add/remove carriages anywhere in the chain.

```cpp
struct Node {
    int   data;
    Node* next;
    Node(int d) : data(d), next(nullptr) {}
};

class LinkedList {
public:
    Node* head = nullptr;

    void insertFront(int data) {
        Node* newNode  = new Node(data);
        newNode->next  = head;
        head           = newNode;
    }

    void display() {
        Node* cur = head;
        while (cur) {
            cout << cur->data << " → ";
            cur = cur->next;
        }
        cout << "NULL" << endl;
    }
};

int main() {
    LinkedList list;
    list.insertFront(30);
    list.insertFront(20);
    list.insertFront(10);
    list.display();   // 10 → 20 → 30 → NULL
}
```

---

**2️⃣ Binary Search Tree (BST):**

🌍 **Like a library filing system** — smaller values go left, larger go right. Finding any book takes at most O(log n) time.

```cpp
struct TreeNode {
    int       value;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v) : value(v), left(nullptr), right(nullptr) {}
};

TreeNode* insert(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    if (val < root->value) root->left  = insert(root->left,  val);
    else                   root->right = insert(root->right, val);
    return root;
}

void inOrder(TreeNode* root) {
    if (!root) return;
    inOrder(root->left);
    cout << root->value << " ";
    inOrder(root->right);
}

int main() {
    TreeNode* root = nullptr;
    root = insert(root, 50);
    root = insert(root, 30);
    root = insert(root, 70);
    root = insert(root, 20);
    inOrder(root);   // 20 30 50 70 (sorted!)
}
```

---

**Complexity Cheat Sheet:**

| Structure | Access | Search | Insert | Delete |
|-----------|--------|--------|--------|--------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |
| Hash Table | O(1) | O(1) | O(1) | O(1) |

---

💡 **Choosing the right structure:**
- Need fast access by index → **Array / Vector**
- Frequent insert/delete anywhere → **Linked List**
- Fast search with sorted data → **BST / Set**
- Fast key-value lookup → **Hash Table / Map**
""",
"level": "300", "semester": "1"
},

]

# ═══════════════════════════════════════════════════════════════════════════
# SEED FUNCTION
# ═══════════════════════════════════════════════════════════════════════════
def seed():
    app = create_app()
    with app.app_context():
        added = 0
        skipped = 0

        for entry in CPP_DATA:
            exists = KnowledgeBase.query.filter_by(intent_name=entry["intent"]).first()
            if exists:
                skipped += 1
                continue

            kb = KnowledgeBase(
                intent_name   = entry["intent"],
                keywords      = ",".join(entry["keywords"]),
                response_text = entry["response"].strip(),
                level         = entry["level"],
            )
            db.session.add(kb)
            added += 1

        db.session.commit()

        print(f"""
╔══════════════════════════════════════════════════════════════╗
║         UPSA ITM — C++ Knowledge Base Seeded               ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ Added   : {added:<3}  entries                               ║
║  ⏭️  Skipped : {skipped:<3}  (already exist)                      ║
╠══════════════════════════════════════════════════════════════╣
║  Level 100 Topics (Fundamentals):                           ║
║    • What is C++          • First Program                   ║
║    • Variables & Types    • Input / Output                  ║
║    • Operators            • If / Else                       ║
║    • Loops                • Functions                       ║
║    • Arrays               • Strings                         ║
╠══════════════════════════════════════════════════════════════╣
║  Level 200 Topics (Intermediate):                           ║
║    • Pointers             • References                      ║
║    • Classes & Objects    • Constructors                    ║
║    • Inheritance          • Polymorphism                    ║
║    • File Handling        • Dynamic Memory                  ║
╠══════════════════════════════════════════════════════════════╣
║  Level 300 Topics (Advanced):                               ║
║    • Templates            • STL                             ║
║    • Exception Handling   • Smart Pointers                  ║
║    • Multithreading       • Design Patterns                 ║
║    • Data Structures                                        ║
╚══════════════════════════════════════════════════════════════╝
""")

if __name__ == "__main__":
    seed()
