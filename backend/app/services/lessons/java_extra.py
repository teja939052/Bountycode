JAVA_EXTRA_LESSONS = [
    {
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
