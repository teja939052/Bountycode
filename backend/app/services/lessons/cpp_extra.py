CPP_EXTRA_LESSONS = [
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
                "content": "C++ string is a class in <string>. It supports concatenation with +, length(), and indexing.",
                "code": "#include <string>\nstring name = \"Ada\";\nstring msg = \"Hello \" + name;\ncout << msg << endl;\ncout << name.length() << endl;",
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
                "instruction": "Concatenate two strings and print the result.",
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
                "id": "ci1",
                "type": "explain",
                "title": "Basic inheritance",
                "content": "A derived class inherits members from a base class using : public BaseClass.",
                "code": "class Animal {\npublic:\n  void eat() { cout << \"Eating\" << endl; }\n};\nclass Dog : public Animal {\n  void bark() { cout << \"Barking\" << endl; }\n};",
                "explanation": "Dog inherits eat() from Animal."
            },
            {
                "id": "ci2",
                "type": "explain",
                "title": "Method overriding",
                "content": "A derived class can redefine a base class method with the same signature.",
                "code": "class Animal {\npublic:\n  virtual void speak() { cout << \"Sound\" << endl; }\n};\nclass Dog : public Animal {\npublic:\n  void speak() override { cout << \"Woof\" << endl; }\n};",
                "explanation": "virtual enables polymorphism; override ensures correct override."
            },
            {
                "id": "ci3",
                "type": "exercise",
                "title": "Override speak",
                "instruction": "Create class Cat inheriting Animal with speak() printing \"Meow\".",
                "starterCode": "class Animal {\npublic:\n  virtual void speak() { cout << \"Animal sound\" << endl; }\n};\nclass Cat : public Animal {\n  // override speak\n};",
                "solution": "class Animal {\npublic:\n  virtual void speak() { cout << \"Animal sound\" << endl; }\n};\nclass Cat : public Animal {\npublic:\n  void speak() override { cout << \"Meow\" << endl; }\n};",
                "tests": [{"input": None, "expected": None, "check": "cat_meows"}],
                "explanation": "Cat::speak() overrides Animal::speak() to print Meow.",
                "hints": ["void speak() override { cout << \"Meow\" << endl; }"]
            },
            {
                "id": "ci5",
                "type": "quiz",
                "title": "Inheritance keyword",
                "question": "C++ keyword for inheritance?",
                "options": [": extends", ": public", "inherits", "subclass"],
                "correctIndex": 1,
                "explanation": "Use : public BaseClass for public inheritance."
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
                "code": "class Animal {\npublic:\n  virtual void speak() { cout << \"Animal\" << endl; }\n};\nclass Dog : public Animal {\npublic:\n  void speak() override { cout << \"Woof\" << endl; }\n};",
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
                "instruction": "Create base class Shape with virtual draw(), and class Circle overriding draw() to print \"Drawing circle\".",
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
