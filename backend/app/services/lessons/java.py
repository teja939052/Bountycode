"""Java track â€” beginner to intermediate lessons."""

JAVA_LESSONS = [
    {
        "id": "java-hello",
        "title": "Hello, World!",
        "track": "java",
        "description": "Write your first Java program.",
        "difficulty": "beginner",
        "xpReward": 50,
        "steps": [
            {
                "id": "j1",
                "type": "explain",
                "title": "Java program structure",
                "content": "Java programs start in main(). Use #include <iostream> for input/output.",
                "code": 'public class Main {\n  public static void main(String[] args) {\n    System.out.println("Hello, World!");\n  }\n}',
                "output": "Hello, World!",
                "explanation": "class Main defines the program. main() is the entry point. System.out.println prints text."
            },
            {
                "id": "j2",
                "type": "explain",
                "title": "Semicolons and braces",
                "content": "Java uses semicolons to end statements and curly braces {} for blocks.",
                "code": "int x = 5;\nif (x > 0) {\n  cout << \"positive\" << endl;\n}",
                "output": "positive",
                "explanation": "Every statement ends with ;. Blocks use { }. Java is case-sensitive.",
            },
            {
                "id": "j3",
                "type": "exercise",
                "title": "Print your name",
                "instruction": "Write a Java program that prints your name.",
                "starterCode": "public class Main {\n  public static void main(String[] args) {\n    \n  }\n}",
                "solution": "public class Main {\n  public static void main(String[] args) {\n    System.out.println(\"Ada Lovelace\");\n  }\n}",
                "tests": [{"input": None, "expected": None, "check": "contains_system_out_println"}],
                "explanation": "Use System.out.println(\"Your Name\"); inside main.",
            },
            {
                "id": "j4",
                "type": "quiz",
                "title": "Entry point",
                "question": "What is the entry point of a Java program?",
                "options": ["main()", "start()", "run()", "init()"],
                "correctIndex": 0,
                "explanation": "The main() method is where Java program execution begins.",
            },
        ],
    },
    {
        "id": "java-variables",
        "title": "Variables & Types",
        "track": "java",
        "description": "Store data with typed variables.",
        "difficulty": "beginner",
        "prerequisites": ["java-hello"],
        "xpReward": 60,
        "steps": [
            {
                "id": "jv1",
                "type": "explain",
                "title": "Declaring variables",
                "content": "Java is statically typed. Declare the type before the name.",
                "code": 'String name = "Ada";\nint score = 0;\ndouble pi = 3.14159;\nboolean isCoding = true;\nSystem.out.println(name + " " + score);',
                "output": "Ada 0",
                "explanation": "String = text, int = whole number, double = decimal, boolean = true/false.",
            },
            {
                "id": "jv2",
                "type": "exercise",
                "title": "Create variables",
                "instruction": "Create int age = 25; and String name = \"Ada\"; then print both.",
                "starterCode": "",
                "solution": "int age = 25;\nString name = \"Ada\";\nSystem.out.println(name + \" \" + age);",
                "tests": [{"input": None, "expected": None, "check": "declares_age_and_name_and_prints"}],
                "explanation": "Declare int age = 25; and String name = \"Ada\"; then print both.",
            },
            {
                "id": "jv3",
                "type": "quiz",
                "title": "Which is not a primitive?",
                "question": "Which of these is NOT a Java primitive type?",
                "options": ["int", "String", "double", "boolean"],
                "correctIndex": 1,
                "explanation": "String is a class (object), not a primitive. int, double, boolean are primitives.",
            },
        ],
    },
    {
        "id": "java-conditionals",
        "title": "If / Else",
        "track": "java",
        "description": "Make decisions with if, else if, else.",
        "difficulty": "beginner",
        "prerequisites": ["java-variables"],
        "xpReward": 70,
        "steps": [
            {
                "id": "jc1",
                "type": "explain",
                "title": "The if statement",
                "content": "Run code only when a condition is true.",
                "code": "int age = 20;\nif (age >= 18) {\n  System.out.println(\"You can vote\");\n}",
                "output": "You can vote",
                "explanation": "If age >= 18 is true, the block runs.",
            },
            {
                "id": "jc2",
                "type": "explain",
                "title": "if / else",
                "content": "Use else for the opposite case.",
                "code": "int age = 16;\nif (age >= 18) {\n  System.out.println(\"You can vote\");\n} else {\n  System.out.println(\"Too young\");\n}",
                "output": "Too young",
                "explanation": "Since 16 < 18, the else block runs.",
            },
            {
                "id": "jc3",
                "type": "exercise",
                "title": "Grade checker",
                "instruction": "Create int score = 75. Print Pass if score >= 60, else print Fail.",
                "starterCode": "int score = 75;",
                "solution": "int score = 75;\nif (score >= 60) {\n    System.out.println(\"Pass\");\n} else {\n    System.out.println(\"Fail\");\n}",
                "tests": [{"input": None, "expected": None, "check": "prints_pass_for_75"}],
                "explanation": "if (score >= 60) { System.out.println(\"Pass\"); } else { System.out.println(\"Fail\"); }.",
            },
            {
                "id": "jc4",
                "type": "quiz",
                "title": "Else execution",
                "question": "When does the else block run?",
                "options": ["Always", "When the if condition is false", "Never", "Only with else if"],
                "correctIndex": 1,
                "explanation": "The else block runs when the preceding if/else if conditions are all false.",
            },
        ],
    },
    {
        "id": "java-loops",
        "title": "Loops",
        "track": "java",
        "description": "Repeat code with for and while loops.",
        "difficulty": "beginner",
        "prerequisites": ["java-conditionals"],
        "xpReward": 80,
        "steps": [
            {
                "id": "jl1",
                "type": "explain",
                "title": "for loop",
                "content": "Repeat code a set number of times with a for loop.",
                "code": "for (int i = 0; i < 3; i++) {\n  cout << i << endl;\n}",
                "output": "0\n1\n2",
                "explanation": "i starts at 0, runs while i < 3, increments i by 1 each time.",
            },
            {
                "id": "jl2",
                "type": "explain",
                "title": "for-each loop",
                "content": "Loop over items in an array.",
                "code": "String[] fruits = {\"apple\", \"banana\", \"cherry\"};\nfor (String fruit : fruits) {\n  cout << fruit << endl;\n}",
                "output": "apple\nbanana\ncherry",
                "explanation": "fruit takes each value from the array in turn.",
            },
            {
                "id": "jl3",
                "type": "exercise",
                "title": "Print 1 to 5",
                "instruction": "Use a for loop to print numbers 1 through 5.",
                "starterCode": "",
                "solution": "for (int i = 1; i <= 5; i++) {\n  cout << i << endl;\n}",
                "tests": [{"input": None, "expected": None, "check": "prints_1_to_5"}],
                "explanation": "i starts at 1, runs while i <= 5, increments by 1.",
            },
        ],
    },
    {
        "id": "java-arrays",
        "title": "Arrays",
        "track": "java",
        "description": "Store collections of items with arrays.",
        "difficulty": "beginner",
        "prerequisites": ["java-loops"],
        "xpReward": 80,
        "steps": [
            {
                "id": "ca1",
                "type": "explain",
                "title": "Creating an array",
                "content": "An array holds multiple items of the same type in order.",
                "code": "String[] fruits = {\"apple\", \"banana\", \"cherry\"};\ncout << fruits[0] << endl;\ncout << fruits[1] << endl;",
                "output": "apple\nbanana",
                "explanation": "Arrays are zero-indexed. fruits[0] is the first element.",
            },
            {
                "id": "ca2",
                "type": "exercise",
                "title": "Print array elements",
                "instruction": "Create int[] nums = {10, 20, 30}; and print each element using a for-each loop.",
                "starterCode": "",
                "solution": "int nums[] = {10, 20, 30};\nfor (int n : nums) {\n  cout << n << endl;\n}",
                "tests": [{"input": None, "expected": None, "check": "prints_array_elements"}],
                "explanation": "for-each loop: for (int n : nums) { cout << n << endl; }.",
            },
        ],
    },
    {
        "id": "java-functions",
        "title": "Methods",
        "track": "java",
        "description": "Write reusable methods.",
        "difficulty": "beginner",
        "prerequisites": ["java-variables"],
        "xpReward": 80,
        "steps": [
            {
                "id": "cf1",
                "type": "explain",
                "title": "Defining a function",
                "content": "Use public static to create a reusable method inside a class.",
                "code": "public class Main {\n  public static void greet(String name) {\n    cout << \"Hello, \" + name << endl;\n  }\n  public static void main(String[] args) {\n    greet(\"Ada\");\n    greet(\"Bob\");\n  }\n}",
                "output": "Hello, Ada\nHello, Bob",
                "explanation": "public static void greet(String name) defines the method. Calling greet(\"Ada\") runs it with name = \"Ada\".",
            },
            {
                "id": "cf2",
                "type": "explain",
                "title": "Return values",
                "content": "Use return to send a value back from a function.",
                "code": "public static int add(int a, int b) {\n    return a + b;\n  }\n  public static void main(String[] args) {\n    int result = add(3, 4);\n    cout << result << endl;\n  }",
                "output": "7",
                "explanation": "return sends a + b back to the caller.",
            },
            {
                "id": "cf3",
                "type": "exercise",
                "title": "Double it",
                "instruction": "Write a function double(int n) that returns n * 2. Then print double(7).",
                "starterCode": "",
                "solution": "int double(int n) {\n    return n * 2;\n  }\n  int main() {\n    cout << double(7) << endl;\n    return 0;\n  }",
                "tests": [{"input": None, "expected": None, "check": "defines_double_and_prints_14"}],
                "explanation": "int double(int n) { return n * 2; } then cout << double(7) prints 14.",
            },
        ],
    },
    {
        "id": "java-arrays2",
        "title": "Arrays",
        "track": "java",
        "description": "Store collections of items with arrays.",
        "difficulty": "beginner",
        "prerequisites": ["java-loops"],
        "xpReward": 80,
        "steps": [
            {
                "id": "ca1",
                "type": "explain",
                "title": "Creating an array",
                "content": "An array holds multiple items of the same type in order.",
                "code": "String[] fruits = {\"apple\", \"banana\", \"cherry\"};\ncout << fruits[0] << endl;\ncout << fruits[1] << endl;",
                "output": "apple\nbanana",
                "explanation": "Arrays are zero-indexed. fruits[0] is the first element.",
            },
            {
                "id": "ca2",
                "type": "exercise",
                "title": "Print array elements",
                "instruction": "Create int[] nums = {10, 20, 30}; and print each element using a for-each loop.",
                "starterCode": "",
                "solution": "int nums[] = {10, 20, 30};\nfor (int n : nums) {\n  cout << n << endl;\n}",
                "tests": [{"input": None, "expected": None, "check": "prints_array_elements"}],
                "explanation": "for-each loop: for (int n : nums) { cout << n << endl; }.",
            },
        ],
    },        {
            "id": "java-string",
            "title": "Strings",
            "track": "java",
            "description": "String class, immutability, common String methods.",
            "difficulty": "beginner",
            "prerequisites": ["java-arrays2"],
            "xpReward": 60,
            "steps": [
                {
                    "id": "js1",
                    "type": "explain",
                    "title": "String class",
                    "content": "String is an object in Java. String literals are stored in string pool.",
                    "code": "String s = \"hello\";\nSystem.out.println(s.length());",
                    "output": "5",
                    "explanation": "String is an object with methods like length()."
                },
                {
                    "id": "js2",
                    "type": "explain",
                    "title": "String immutability",
                    "content": "Strings are immutable in Java. Modifying creates a new String object.",
                    "code": "String s = \"hello\";\ns.concat(\" world\");\nSystem.out.println(s); // still \"hello\"",
                    "output": "hello",
                    "explanation": "concat returns a new String; original unchanged."
                },
                {
                    "id": "js3",
                    "type": "exercise",
                    "title": "String concatenation",
                    "instruction": "Concatenate two strings and print.",
                    "starterCode": "String a = \"Hello\";\nString b = \"World\";\n// concatenate and print",
                    "solution": "String a = \"Hello\";\nString b = \"World\";\nSystem.out.println(a + \" \" + b);",
                    "tests": [{"input": None, "expected": None, "check": "prints_Hello_World"}],
                    "explanation": "Use + operator to concatenate strings.",
                    "hints": ['System.out.println(a + " " + b)']
                },
                {
                    "id": "js4",
                    "type": "quiz",
                    "title": "String immutability",
                    "question": "Are Java Strings immutable?",
                    "options": ["Yes", "No", "Only sometimes", "Only in Java 8+"],
                    "correctIndex": 0,
                    "explanation": "Yes, Strings are immutable in Java."
                }
            ]
        },
        {
            "id": "java-oop-basics",
            "title": "Classes & Objects",
            "track": "java",
            "description": "Define classes, create objects, use constructors.",
            "difficulty": "beginner",
            "prerequisites": ["java-string"],
            "xpReward": 70,
            "steps": [
                {
                    "id": "jc1",
                    "type": "explain",
                    "title": "Class and object",
                    "content": "Class is a blueprint. Object is an instance of the class.",
                    "code": "class Car {\n  String model;\n  Car(String m) { model = m; }\n}\nCar c = new Car(\"Tesla\");",
                    "explanation": "Car is the class, c is an object/instance."
                },
                {
                    "id": "jc2",
                    "type": "explain",
                    "title": "Constructor",
                    "content": "Constructor initializes object state. Same name as class, no return type.",
                    "code": "class Car {\n  String model;\n  Car(String m) {\n    model = m;\n  }\n}",
                    "explanation": "Constructor sets initial values."
                },
                {
                    "id": "jc3",
                    "type": "exercise",
                    "title": "Create class with constructor",
                    "instruction": "Create class Student with String name field and constructor setting it.",
                    "starterCode": "class Student {\n  String name;\n  Student(String n) {\n    // set name\n  }\n}",
                    "solution": "class Student {\n  String name;\n  Student(String n) {\n    name = n;\n  }\n}",
                    "tests": [{"input": None, "expected": None, "check": "student_has_constructor"}],
                    "explanation": "Constructor assigns parameter to field.",
                    "hints": ["name = n;"]
                },
                {
                    "id": "jc4",
                    "type": "quiz",
                    "title": "Constructor name",
                    "question": "Constructor name must match?",
                    "options": ["Class name", "Method name", "Package name", "File name"],
                    "correctIndex": 0,
                    "explanation": "Constructor must have same name as class."
                }
            ]
        },
        {
            "id": "java-inheritance",
            "title": "Inheritance & Polymorphism",
            "track": "java",
            "description": "Extend classes, override methods, use super().",
            "difficulty": "intermediate",
            "prerequisites": ["java-oop-basics"],
            "xpReward": 80,
            "steps": [
                {
                    "id": "ji1",
                    "type": "explain",
                    "title": "Extends keyword",
                    "content": "Use extends to inherit from a parent class.",
                    "code": "class Animal {\n  void eat() { System.out.println(\"Eating\"); }\n}\nclass Dog extends Animal {\n  void bark() { System.out.println(\"Barking\"); }\n}",
                    "explanation": "Dog inherits eat() from Animal."
                },
                {
                    "id": "ji2",
                    "type": "explain",
                    "title": "Method overriding",
                    "content": "@Override lets child class provide its own implementation.",
                    "code": "class Animal {\n  void makeSound() { System.out.println(\"Sound\"); }\n}\nclass Dog extends Animal {\n  @Override\n  void makeSound() { System.out.println(\"Woof\"); }\n}",
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
                    "starterCode": "class Animal {\n  void makeSound() { System.out.println(\"Animal sound\"); }\n}\nclass Dog extends Animal {\n  // override makeSound\n  \n}",
                    "solution": "class Animal {\n  void makeSound() { System.out.println(\"Animal sound\"); }\n}\nclass Dog extends Animal {\n  @Override\n  void makeSound() { System.out.println(\"Bark\"); }\n}",
                    "tests": [{"input": None, "expected": None, "check": "dog_barks"}],
                    "explanation": "Dog.makeSound() prints 'Bark' not 'Animal sound'.",
                    "hints": ["@Override void makeSound() { System.out.println(\"Bark\"); }"]
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
            "id": "java-exception",
            "title": "Exception Handling",
            "track": "java",
            "description": "try-catch-finally, try-with-resources, custom exceptions.",
            "difficulty": "intermediate",
            "prerequisites": ["java-oop-basics"],
            "xpReward": 80,
            "steps": [
                {
                    "id": "je1",
                    "type": "explain",
                    "title": "try-catch",
                    "content": "Use try-catch to handle exceptions gracefully.",
                    "code": "try {\n  int x = 10 / 0;\n} catch (ArithmeticException e) {\n  System.out.println(\"Cannot divide by zero\");\n}",
                    "explanation": "catch block handles the exception."
                },
                {
                    "id": "je2",
                    "type": "explain",
                    "title": "finally block",
                    "content": "finally block runs whether exception occurs or not. Used for cleanup.",
                    "code": "try {\n  // code\n} catch (Exception e) {\n  // handle\n} finally {\n  // cleanup code\n}",
                    "explanation": "finally always executes."
                },
                {
                    "id": "je3",
                    "type": "explain",
                    "title": "Checked vs Unchecked",
                    "content": "Checked exceptions (IOException) must be handled. Unchecked (NullPointerException) are runtime.",
                    "explanation": "Compiler forces handling of checked exceptions."
                },
                {
                    "id": "je4",
                    "type": "exercise",
                    "title": "Handle division by zero",
                    "instruction": "Wrap division in try-catch for ArithmeticException.",
                    "starterCode": "int a = 10;\nint b = 0;\n// wrap division in try-catch\nint result = a / b;",
                    "solution": "int a = 10;\nint b = 0;\ntry {\n  int result = a / b;\n} catch (ArithmeticException e) {\n  System.out.println(\"Cannot divide by zero\");\n}",
                    "tests": [{"input": None, "expected": None, "check": "student_wrapped_division"}],
                    "explanation": "Wrap division in try-catch ArithmeticException.",
                    "hints": ["try { int result = a / b; } catch (ArithmeticException e) {...}"]
                },
                {
                    "id": "je5",
                    "type": "quiz",
                    "title": "ArithmeticException",
                    "question": "Dividing by zero throws?",
                    "options": ["ArithmeticException", "NullPointerException", "ArrayIndexOutOfBoundsException", "IOException"],
                    "correctIndex": 0,
                    "explanation": "Division by zero throws ArithmeticException."
                }
            ]
        },
        {
            "id": "java-collections",
            "title": "Collections Framework",
            "track": "java",
            "description": "ArrayList, HashMap, HashSet basics.",
            "difficulty": "intermediate",
            "prerequisites": ["java-oop-basics"],
            "xpReward": 80,
            "steps": [
                {
                    "id": "jcol1",
                    "type": "explain",
                    "title": "ArrayList",
                    "content": "ArrayList is resizable array. Import java.util.ArrayList.",
                    "code": "import java.util.ArrayList;\nArrayList<String> list = new ArrayList<>();\nlist.add(\"Apple\");\nlist.add(\"Banana\");\nSystem.out.println(list.get(0));  // Apple",
                    "explanation": "ArrayList grows dynamically."
                },
                {
                    "id": "jc2",
                    "type": "explain",
                    "title": "HashMap",
                    "content": "HashMap stores key-value pairs. Import java.util.HashMap.",
                    "code": "import java.util.HashMap;\nHashMap<String, Integer> map = new HashMap<>();\nmap.put(\"Alice\", 25);\nSystem.out.println(map.get(\"Alice\"));  // 25",
                    "explanation": "Key-value storage with O(1) average lookup."
                },
                {
                    "id": "jc3",
                    "type": "explain",
                    "title": "HashSet",
                    "content": "HashSet stores unique elements only.",
                    "explanation": "Duplicates are not allowed."
                },
                {
                    "id": "jc4",
                    "type": "exercise",
                    "title": "Use ArrayList",
                    "instruction": "Create ArrayList<String>, add \"Apple\" and \"Banana\", print first element.",
                    "starterCode": "import java.util.ArrayList;\nArrayList<String> list = new ArrayList<>();\n// add \"Apple\" and \"Banana\"\n// print list.get(0)",
                    "solution": "import java.util.ArrayList;\nArrayList<String> list = new ArrayList<>();\nlist.add(\"Apple\");\nlist.add(\"Banana\");\nSystem.out.println(list.get(0));",
                    "tests": [{"input": None, "expected": None, "check": "prints_Apple"}],
                    "explanation": "list.add() adds, list.get(0) retrieves first.",
                    "hints": ['list.add("Apple"); list.add("Banana"); System.out.println(list.get(0));']
                },
                {
                    "id": "jc5",
                    "type": "quiz",
                    "title": "HashMap allows duplicates?",
                    "question": "HashMap allows duplicate keys?",
                    "options": ["Yes", "No", "Only null", "Only strings"],
                    "correctIndex": 1,
                    "explanation": "HashMap keys must be unique; values can duplicate."
                }
            ]
        }
]
