"""C++ track â€” beginner to intermediate lessons."""

CPP_LESSONS = [
    {
        "id": "cpp-hello",
        "title": "Hello, World!",
        "track": "cpp",
        "description": "Write your first C++ program.",
        "difficulty": "beginner",
        "xpReward": 50,
        "steps": [
            {
                "id": "cpp1",
                "type": "explain",
                "title": "Your first C++ program",
                "content": "C++ programs start in main(). Use #include <iostream> for input/output.",
                "code": '#include <iostream>\nusing namespace std;\nint main() {\n  cout << "Hello, World!" << endl;\n  return 0;\n}',
                "output": "Hello, World!",
                "explanation": "#include <iostream> brings in input/output. cout << prints text. endl ends the line."
            },
            {
                "id": "cpp2",
                "type": "explain",
                "title": "Semicolons and braces",
                "content": "C++ uses semicolons to end statements and curly braces {} for blocks.",
                "code": "int x = 5;\nif (x > 0) {\n  cout << \"positive\" << endl;\n}",
                "output": "positive",
                "explanation": "Every statement ends with ;. Blocks use { }."
            },
            {
                "id": "cpp3",
                "type": "exercise",
                "title": "Print your name",
                "instruction": "Write a C++ program that prints your name.",
                "starterCode": '#include <iostream>\nusing namespace std;\nint main() {\n  \n  return 0;\n}',
                "solution": '#include <iostream>\nusing namespace std;\nint main() {\n  cout << "Ada Lovelace" << endl;\n  return 0;\n}',
                "tests": [{"input": None, "expected": None, "check": "contains_cout_and_quotes"}],
                "explanation": "Use cout << \"Your Name\" << endl; inside main.",
            },
            {
                "id": "cpp4",
                "type": "quiz",
                "title": "Entry point",
                "question": "What is the entry point of a C++ program?",
                "options": ["main()", "start()", "run()", "init()"],
                "correctIndex": 0,
                "explanation": "The main() function is where C++ program execution begins."
            }
        ]
    },
    {
        "id": "cpp-variables",
        "title": "Variables & Types",
        "track": "cpp",
        "description": "Store data with typed variables.",
        "difficulty": "beginner",
        "prerequisites": ["cpp-hello"],
        "xpReward": 60,
        "steps": [
            {
                "id": "cp1",
                "type": "explain",
                "title": "Declaring variables",
                "content": "C++ is statically typed. Declare the type before the name.",
                "code": 'string name = "Ada";\nint score = 0;\ndouble pi = 3.14159;\nbool isCoding = true;\ncout << name << " " << score << endl;',
                "output": "Ada 0",
                "explanation": "string = text, int = whole number, double = decimal, bool = true/false."
            },
            {
                "id": "cp2",
                "type": "exercise",
                "title": "Create variables",
                "instruction": "Create int age = 25; and string name = \"Ada\"; then print both.",
                "starterCode": "",
                "solution": "int age = 25;\nstring name = \"Ada\";\ncout << name << \" \" << age << endl;",
                "tests": [{"input": None, "expected": None, "check": "declares_age_and_name_and_prints"}],
                "explanation": "Declare int age = 25; and string name = \"Ada\"; then print both."
            },
            {
                "id": "cp3",
                "type": "quiz",
                "title": "Which is not a primitive?",
                "question": "Which of these is NOT a C++ primitive type?",
                "options": ["int", "string", "double", "bool"],
                "correctIndex": 1,
                "explanation": "string is a class (object), not a primitive. int, double, bool are primitives."
            }
        ]
    },
    {
        "id": "cpp-conditionals",
        "title": "If / Else",
        "track": "cpp",
        "description": "Make decisions with if, else if, else.",
        "difficulty": "beginner",
        "prerequisites": ["cpp-variables"],
        "xpReward": 70,
        "steps": [
            {
                "id": "cc1",
                "type": "explain",
                "title": "The if statement",
                "content": "Run code only when a condition is true.",
                "code": "int age = 20;\nif (age >= 18) {\n  cout << \"You can vote\" << endl;\n}",
                "output": "You can vote",
                "explanation": "If age >= 18 is true, the block runs."
            },
            {
                "id": "cc2",
                "type": "explain",
                "title": "if / else",
                "content": "Use else for the opposite case.",
                "code": "int age = 16;\nif (age >= 18) {\n  cout << \"You can vote\" << endl;\n} else {\n  cout << \"Too young\" << endl;\n}",
                "output": "Too young",
                "explanation": "Since 16 < 18, the else block runs."
            },
            {
                "id": "cc3",
                "type": "exercise",
                "title": "Grade checker",
                "instruction": "Create int score = 75. Print Pass if score >= 60, else print Fail.",
                "starterCode": "int score = 75;",
                "solution": "int score = 75;\nif (score >= 60) {\n    cout << \"Pass\" << endl;\n} else {\n    cout << \"Fail\" << endl;\n}",
                "tests": [{"input": None, "expected": None, "check": "prints_pass_for_75"}],
                "explanation": "if (score >= 60) { cout << \"Pass\" << endl; } else { cout << \"Fail\" << endl; }."
            },
            {
                "id": "cc4",
                "type": "quiz",
                "title": "Else execution",
                "question": "When does the else block run?",
                "options": ["Always", "When the if condition is false", "Never", "Only with else if"],
                "correctIndex": 1,
                "explanation": "The else block runs when the preceding if/else if conditions are all false."
            }
        ]
    },
    {
        "id": "cpp-loops",
        "title": "Loops",
        "track": "cpp",
        "description": "Repeat code with for and while loops.",
        "difficulty": "beginner",
        "prerequisites": ["cpp-conditionals"],
        "xpReward": 80,
        "steps": [
            {
                "id": "cl1",
                "type": "explain",
                "title": "for loop",
                "content": "Repeat code a set number of times with a for loop.",
                "code": "for (int i = 0; i < 3; i++) {\n  cout << i << endl;\n}",
                "output": "0\n1\n2",
                "explanation": "i starts at 0, runs while i < 3, increments i by 1 each time."
            },
            {
                "id": "cl2",
                "type": "explain",
                "title": "for-each loop",
                "content": "Loop over items in an array.",
                "code": "string fruits[] = {\"apple\", \"banana\", \"cherry\"};\nfor (string fruit : fruits) {\n  cout << fruit << endl;\n}",
                "output": "apple\nbanana\ncherry",
                "explanation": "fruit takes each value from the array in turn."
            },
            {
                "id": "cl3",
                "type": "exercise",
                "title": "Print 1 to 5",
                "instruction": "Use a for loop to print numbers 1 through 5.",
                "starterCode": "",
                "solution": "for (int i = 1; i <= 5; i++) {\n  cout << i << endl;\n}",
                "tests": [{"input": None, "expected": None, "check": "prints_1_to_5"}],
                "explanation": "i starts at 1, runs while i <= 5, increments by 1."
            }
        ]
    },
    {
        "id": "cpp-arrays",
        "title": "Arrays",
        "track": "cpp",
        "description": "Store collections of items with arrays.",
        "difficulty": "beginner",
        "prerequisites": ["cpp-loops"],
        "xpReward": 80,
        "steps": [
            {
                "id": "ca1",
                "type": "explain",
                "title": "Creating an array",
                "content": "An array holds multiple items of the same type in order.",
                "code": "string fruits[] = {\"apple\", \"banana\", \"cherry\"};\ncout << fruits[0] << endl;\ncout << fruits[1] << endl;",
                "output": "apple\nbanana",
                "explanation": "Arrays are zero-indexed. fruits[0] is the first element."
            },
            {
                "id": "ca2",
                "type": "exercise",
                "title": "Print array elements",
                "instruction": "Create int[] nums = {10, 20, 30}; and print each element using a for-each loop.",
                "starterCode": "",
                "solution": "int nums[] = {10, 20, 30};\nfor (int n : nums) {\n  cout << n << endl;\n}",
                "tests": [{"input": None, "expected": None, "check": "prints_array_elements"}],
                "explanation": "for-each loop: for (int n : nums) { cout << n << endl; }."
            }
        ]
    },
    {
        "id": "cpp-functions",
        "title": "Functions",
        "track": "cpp",
        "description": "Write reusable functions.",
        "difficulty": "beginner",
        "prerequisites": ["cpp-variables"],
        "xpReward": 80,
        "steps": [
            {
                "id": "cf1",
                "type": "explain",
                "title": "Defining a function",
                "content": "Use return type and name to create a reusable function.",
                "code": "void greet(string name) {\n  cout << \"Hello, \" + name << endl;\n}\nint main() {\n  greet(\"Ada\");\n  greet(\"Bob\");\n  return 0;\n}",
                "output": "Hello, Ada\nHello, Bob",
                "explanation": "void greet(string name) defines the function. Calling greet(\"Ada\") runs it with name = \"Ada\"."
            },
            {
                "id": "cf2",
                "type": "explain",
                "title": "Return values",
                "content": "Use return to send a value back from a function.",
                "code": "int add(int a, int b) {\n    return a + b;\n  }\n  int main() {\n    int result = add(3, 4);\n    cout << result << endl;\n    return 0;\n  }",
                "output": "7",
                "explanation": "return sends a + b back to the caller."
            },
            {
                "id": "cf3",
                "type": "exercise",
                "title": "Double it",
                "instruction": "Write a function double(int n) that returns n * 2. Then print double(7).",
                "starterCode": "",
                "solution": "int double(int n) {\n    return n * 2;\n  }\n  int main() {\n    cout << double(7) << endl;\n    return 0;\n  }",
                "tests": [{"input": None, "expected": None, "check": "defines_double_and_prints_14"}],
                "explanation": "int double(int n) { return n * 2; } then cout << double(7) prints 14."
            }
        ]
    },
    {
        "id": "cpp-pointers",
        "title": "Pointers",
        "track": "cpp",
        "description": "Pointers and references.",
        "difficulty": "intermediate",
        "prerequisites": ["cpp-variables"],
        "xpReward": 90,
        "steps": [
            {
                "id": "cp1",
                "type": "explain",
                "title": "What is a pointer?",
                "content": "A pointer is a variable that stores the memory address of another variable.",
                "code": "int x = 42;\nint* ptr = &x;\ncout << *ptr << endl;  // 42",
                "output": "42",
                "explanation": "&x gets the address of x. *ptr dereferences the pointer to get the value at that address."
            },
            {
                "id": "cp2",
                "type": "explain",
                "title": "Pointer arithmetic",
                "content": "Pointer arithmetic moves by the size of the pointed-to type.",
                "code": "int arr[] = {10, 20, 30};\nint* p = arr;\ncout << *p << endl;\np++;\ncout << *p << endl;",
                "output": "10\n20",
                "explanation": "p++ moves the pointer to the next int (4 bytes on most systems)."
            },
            {
                "id": "cp3",
                "type": "exercise",
                "title": "Swap using pointers",
                "instruction": "Write a function swap(int* a, int* b) that swaps the values of two integers using pointers.",
                "starterCode": "",
                "solution": "void swap(int* a, int* b) {\n    int temp = *a;\n    *a = *b;\n    *b = temp;\n}",
                "tests": [{"input": None, "expected": None, "check": "implements_swap"}],
                "explanation": "Use pointers to access and swap the values of the variables passed in."
            }
        ]
    },
    {
        "id": "cpp-strings",
        "title": "Strings",
        "track": "cpp",
        "description": "C++ string class, concatenation, length, common operations.",
        "difficulty": "beginner",
        "prerequisites": ["cpp-variables"],
        "xpReward": 60,
        "steps": [
            {
                "id": "cs1",
                "type": "explain",
                "title": "String class",
                "content": "C++ string is an object in <string>. It supports concatenation with +, length(), and indexing.",
                "code": '#include <string>\nstring name = "Ada";\nstring msg = "Hello " + name;\ncout << msg << endl;\ncout << name.length() << endl;',
                "output": "Hello Ada\n3",
                "explanation": "string supports + for concatenation and .length() for length."
            },
            {
                "id": "cs2",
                "type": "explain",
                "title": "String access",
                "content": "Use [] to access individual characters. Strings are zero-indexed.",
                "code": "string s = \"hello\";\ncout << s[0] << endl;  // h\ncout << s[4] << endl;  // o",
                "output": "h\no",
                "explanation": "s[0] is the first character, s[s.length()-1] is the last."
            },
            {
                "id": "cs3",
                "type": "exercise",
                "title": "String concatenation",
                "instruction": "Concatenate two strings and print.",
                "starterCode": "string a = \"Hello\";\nstring b = \"World\";\n// concatenate and print",
                "solution": "string a = \"Hello\";\nstring b = \"World\";\ncout << a + \" \" + b << endl;",
                "tests": [{"input": None, "expected": None, "check": "prints_Hello_World"}],
                "explanation": "Use + operator to concatenate strings.",
                "hints": ['cout << a + " " + b << endl;']
            },
            {
                "id": "cs4",
                "type": "quiz",
                "title": "String header",
                "question": "Which header is needed for string?",
                "options": ["<string>", "<iostream>", "<vector>", "<algorithm>"],
                "correctIndex": 0,
                "explanation": "Use #include <string> for the string class."
            }
        ]
    },
    {
        "id": "cpp-references",
        "title": "References",
        "track": "cpp",
        "description": "Reference variables as aliases for existing variables.",
        "difficulty": "beginner",
        "prerequisites": ["cpp-variables"],
        "xpReward": 70,
        "steps": [
            {
                "id": "cr1",
                "type": "explain",
                "title": "Reference basics",
                "content": "A reference is an alias for an existing variable. Use & to declare.",
                "code": "int x = 42;\nint& ref = x;\nref = 100;\ncout << x << endl;  // 100",
                "output": "100",
                "explanation": "ref is an alias for x. Changing ref changes x."
            },
            {
                "id": "cr2",
                "type": "explain",
                "title": "Reference vs pointer",
                "content": "References must be initialized and cannot be null. Pointers can be null and reassigned.",
                "explanation": "References are safer but less flexible than pointers."
            },
            {
                "id": "cr3",
                "type": "exercise",
                "title": "Modify via reference",
                "instruction": "Write a function void increment(int& x) that adds 1 to x.",
                "starterCode": "",
                "solution": "void increment(int& x) {\n    x++;\n}",
                "tests": [{"input": None, "expected": None, "check": "defines_increment"}],
                "explanation": "Use int& parameter to modify the original variable.",
                "hints": ["void increment(int& x) { x++; }"]
            },
            {
                "id": "cr4",
                "type": "quiz",
                "title": "Reference behavior",
                "question": "Can a reference be null?",
                "options": ["Yes", "No", "Only with nullptr", "Only in C++17"],
                "correctIndex": 1,
                "explanation": "References must always refer to a valid object; they cannot be null."
            }
        ]
    },
    {
        "id": "cpp-structs",
        "title": "Structures & Classes",
        "track": "cpp",
        "description": "Structs and classes with members and methods.",
        "difficulty": "beginner",
        "prerequisites": ["cpp-variables"],
        "xpReward": 80,
        "steps": [
            {
                "id": "cs1",
                "type": "explain",
                "title": "Struct basics",
                "content": "A struct groups related variables together under one name.",
                "code": "struct Person {\n  string name;\n  int age;\n};\nPerson p = {\"Ada\", 28};\ncout << p.name << \" \" << p.age << endl;",
                "output": "Ada 28",
                "explanation": "Access members with dot notation: p.name, p.age."
            },
            {
                "id": "cs2",
                "type": "explain",
                "title": "Class vs struct",
                "content": "Classes and structs are nearly identical. Classes default to private members; structs default to public.",
                "explanation": "Use struct for data-only, class for objects with behavior."
            },
            {
                "id": "cs3",
                "type": "exercise",
                "title": "Create a struct",
                "instruction": "Create a struct Point with int x and int y, then create one and print its fields.",
                "starterCode": "",
                "solution": "struct Point {\n  int x;\n  int y;\n};\nint main() {\n  Point p = {3, 4};\n  cout << p.x << \" \" << p.y << endl;\n  return 0;\n}",
                "tests": [{"input": None, "expected": None, "check": "prints_3_4"}],
                "explanation": "Define struct with fields, create instance, access fields with dot.",
                "hints": ["struct Point { int x; int y; };"]
            },
            {
                "id": "cs4",
                "type": "quiz",
                "title": "Struct vs class",
                "question": "Default member access in struct is?",
                "options": ["private", "public", "protected", "internal"],
                "correctIndex": 1,
                "explanation": "Struct members are public by default; class members are private."
            }
        ]
    },
    {
        "id": "cpp-inheritance",
        "title": "Inheritance",
        "track": "cpp",
        "description": "Derive classes from base classes.",
        "difficulty": "intermediate",
        "prerequisites": ["cpp-structs"],
        "xpReward": 80,
        "steps": [
            {
                "id": "ji1",
                "type": "explain",
                "title": "Extends keyword",
                "content": "Use extends to inherit from a parent class.",
                "code": "class Animal {\npublic:\n  void eat() { cout << \"Eating\" << endl; }\n};\nclass Dog : public Animal {\n  void bark() { cout << \"Barking\" << endl; }\n};",
                "explanation": "Dog inherits eat() from Animal."
            },
            {
                "id": "ji2",
                "type": "explain",
                "title": "Method overriding",
                "content": "A derived class can redefine a base class method with the same signature.",
                "code": "class Animal {\npublic:\n  virtual void makeSound() { cout << \"Sound\" << endl; }\n};\nclass Dog : public Animal {\npublic:\n  void speak() override { cout << \"Woof\" << endl; }\n};",
                "explanation": "Dog overrides makeSound() to bark."
            },
            {
                "id": "ji3",
                "type": "explain",
                "title": "super keyword",
                "content": "super refers to parent class. Use super.method() to call parent method.",
                "explanation": "Access parent class members from child."
            },
            {
                "id": "ji4",
                "type": "exercise",
                "title": "Override method",
                "instruction": "Override makeSound() in Dog class to print 'Bark'.",
                "starterCode": "class Animal {\n  void makeSound() { cout << \"Animal sound\" << endl; }\n}\nclass Dog extends Animal {\n  // override makeSound\n  \n}",
                "solution": "class Animal {\n  void makeSound() { cout << \"Animal sound\" << endl; }\n}\nclass Dog : public Animal {\n  void makeSound() override { cout << \"Woof\" << endl; }\n};",
                "tests": [{"input": None, "expected": None, "check": "dog_barks"}],
                "explanation": "Dog.makeSound() overrides Animal.makeSound() to print Woof.",
                "hints": ["@Override void makeSound() { cout << \"Woof\" << endl; }"]
            },
            {
                "id": "ji5",
                "type": "quiz",
                "title": "Inheritance keyword",
                "question": "Java keyword for inheritance?",
                "options": ["extends", "implements", "inherits", "subclass"],
                "correctIndex": 0,
                "explanation": "extends keyword is used for inheritance in Java."
            }
        ]
    },
    {
        "id": "cpp-polymorphism",
        "title": "Polymorphism",
        "track": "cpp",
        "description": "Virtual functions and dynamic dispatch.",
        "difficulty": "intermediate",
        "prerequisites": ["cpp-inheritance"],
        "xpReward": 80,
        "steps": [
            {
                "id": "pp1",
                "type": "explain",
                "title": "Virtual functions",
                "content": "virtual keyword enables dynamic dispatch. The actual object type determines which method runs.",
                "code": "class Animal {\npublic:\n  virtual void speak() { cout << \"Sound\" << endl; }\n};\nclass Dog : public Animal {\npublic:\n  void speak() override { cout << \"Woof\" << endl; }\n};",
                "explanation": "Base pointer to Derived object calls Derived::speak()."
            },
            {
                "id": "pp2",
                "type": "explain",
                "title": "Polymorphic behavior",
                "content": "A base pointer can point to derived objects and call overridden methods.",
                "code": "Animal* a = new Dog();\na->speak();  // prints Woof",
                "explanation": "Even through a base pointer, the derived method runs."
            },
            {
                "id": "pp3",
                "type": "exercise",
                "title": "Polymorphic call",
                "instruction": "Create class Shape with virtual draw(), and class Circle overriding draw() to print \"Drawing circle\".",
                "starterCode": "class Shape {\npublic:\n  virtual void draw() { cout << \"Shape\" << endl; }\n};\nclass Circle : public Shape {\n  // override draw\n};",
                "solution": "class Shape {\npublic:\n  virtual void draw() { cout << \"Shape\" << endl; }\n};\nclass Circle : public Shape {\npublic:\n  void draw() override { cout << \"Drawing circle\" << endl; }\n};",
                "tests": [{"input": None, "expected": None, "check": "circle_draws"}],
                "explanation": "Circle::draw() overrides Shape::draw().",
                "hints": ["void draw() override { cout << \"Drawing circle\" << endl; }"]
            },
            {
                "id": "pp5",
                "type": "quiz",
                "title": "Virtual keyword",
                "question": "virtual keyword enables?",
                "options": ["Static dispatch", "Dynamic dispatch", "Multiple inheritance", "Operator overloading"],
                "correctIndex": 1,
                "explanation": "virtual enables dynamic dispatch (runtime polymorphism)."
            }
        ]
    },
    {
        "id": "cpp-oop-summary",
        "title": "OOP Summary",
        "track": "cpp",
        "description": "Review of classes, inheritance, polymorphism, encapsulation.",
        "difficulty": "intermediate",
        "prerequisites": ["cpp-polymorphism"],
        "xpReward": 90,
        "steps": [
            {
                "id": "os1",
                "type": "explain",
                "title": "OOP recap",
                "content": "Classes bundle data and behavior. Inheritance enables reuse. Polymorphism enables flexibility. Encapsulation hides internals.",
                "explanation": "These four pillars form the foundation of object-oriented programming."
            },
            {
                "id": "os2",
                "type": "explain",
                "title": "Access modifiers",
                "content": "public = accessible everywhere. private = accessible only within class. protected = accessible within class and derived classes.",
                "explanation": "Use private for data, public for interface."
            },
            {
                "id": "os3",
                "type": "exercise",
                "title": "Complete OOP example",
                "instruction": "Create class Animal with private name, public constructor, and virtual speak(). Create Dog inheriting Animal overriding speak().",
                "starterCode": "",
                "solution": "class Animal {\nprivate:\n  string name;\npublic:\n  Animal(string n) : name(n) {}\n  virtual void speak() { cout << name << \" makes sound\" << endl; }\n};\nclass Dog : public Animal {\npublic:\n  Dog(string n) : Animal(n) {}\n  void speak() override { cout << name << \" barks\" << endl; }\n};",
                "tests": [{"input": None, "expected": None, "check": "defines_animal_and_dog"}],
                "explanation": "Animal has private name, public constructor, virtual speak. Dog inherits and overrides speak.",
                "hints": ["Use : public Animal for inheritance"]
            },
            {
                "id": "os5",
                "type": "quiz",
                "title": "OOP benefit",
                "question": "Main benefit of OOP?",
                "options": ["Code reuse", "Faster execution", "Less memory", "Simpler syntax"],
                "correctIndex": 0,
                "explanation": "OOP promotes code reuse through inheritance and composition."
            }
        ]
    }
]
