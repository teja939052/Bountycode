"""Authored Java placement-fundamentals lesson profiles."""
from __future__ import annotations

from typing import Any, Dict

from app.data.lesson_content_authored_builder import build_authored_lesson


_JAVA_CORE: Dict[str, Dict[str, Any]] = {
    "if / else if / else": {
        "concept": "if, else if and else selection",
        "purpose": "choose one execution path based on ordered Boolean conditions",
        "how": "Java evaluates the if condition, then checks else if conditions in order. The first true branch runs and the remaining branches are skipped. A final else handles all unmatched cases. Unlike some languages, Java conditions must be Boolean expressions.",
        "why": "Selection is used for grading bands, menu choices, eligibility rules and validation. Put the highest threshold first so a broad condition does not capture values intended for a more specific branch.",
        "pitfall": "Use == for primitive equality, but use equals() for String value comparison. A semicolon directly after an if header creates an empty statement and can detach the intended block. Use braces consistently.",
        "code": "public class Main {\n    public static void main(String[] args) {\n        int score = 82;\n        if (score >= 90) System.out.println(\"A\");\n        else if (score >= 75) System.out.println(\"B\");\n        else System.out.println(\"Practice\");\n    }\n}",
        "expected": "B",
        "exercise": "Write a grade classifier for scores 0–100: A for 90+, B for 75–89, C for 60–74 and Needs Practice below 60. Reject values outside the range.",
        "expected2": "Boundary checks 90, 75, 60, 59, -1 and 101 produce the correct band or an invalid-score message.",
        "quiz": [
            ("Which branch runs in one if / else if / else chain?", ["Every true branch", "Only the first matching branch", "All branches", "No branch"], 1, "The chain stops at the first true condition, so at most one branch executes."),
            ("Which method compares String contents?", ["== only", "equals()", "compareAddress()", "same()"], 1, "String.equals compares character content; == compares whether references identify the same object."),
            ("What does a semicolon directly after if(condition) create?", ["A new class", "An empty statement body", "An else branch", "A loop"], 1, "The semicolon is an empty statement and can cause the following statement to run outside the condition."),
        ],
    },
    "for Loop": {
        "concept": "counted for loops",
        "purpose": "repeat a block while a counter follows a defined progression",
        "how": "A traditional Java for loop has initialisation, condition and update sections: for (int i = 0; i < n; i++). Initialisation runs once, the condition is checked before each iteration, and the update runs after the body.",
        "why": "Counted loops are useful when the repetition count is known, such as processing array indexes, generating tables and calculating totals.",
        "pitfall": "The condition i < n excludes n, so choose the correct boundary. An incorrect update can create an infinite loop or skip values. Keep the loop variable's scope narrow by declaring it in the for header when possible.",
        "code": "public class Main {\n    public static void main(String[] args) {\n        int total = 0;\n        for (int i = 1; i <= 5; i++) total += i;\n        System.out.println(total);\n    }\n}",
        "expected": "15",
        "exercise": "Read an integer n with Scanner and print its multiplication table from 1 through 10.",
        "expected2": "For n=4, the program prints 4 x 1 = 4 through 4 x 10 = 40.",
        "quiz": [
            ("How many times does for(int i=0; i<5; i++) run?", ["4", "5", "6", "Infinite"], 1, "The loop visits 0, 1, 2, 3 and 4, so it executes five times."),
            ("When does the update expression run?", ["Before initialisation", "After each body iteration", "Only at program end", "Before the first condition"], 1, "The update executes after the loop body and before the next condition check."),
            ("What does i <= 5 include compared with i < 5?", ["No difference", "It includes the value 5", "It excludes zero", "It reverses the loop"], 1, "The <= operator includes the upper boundary, which changes the number of iterations."),
        ],
    },
    "Method Basics": {
        "concept": "Java method declarations and calls",
        "purpose": "organise reusable operations with explicit parameter and return types",
        "how": "A method declaration includes an access modifier, optional static modifier, return type, name and parameter list. A method call supplies arguments. A non-void method must return a value compatible with its declared return type; void methods do not return a result.",
        "why": "Methods divide a large program into small responsibilities, reduce duplication and make behaviour easier to test. Static methods belong to the class, while instance methods operate on a particular object.",
        "pitfall": "A method's return type is part of its signature declaration, and every reachable path in a non-void method must return. Printing a value is not the same as returning it to the caller.",
        "code": "public class Main {\n    static int calculateTotal(int price, int quantity) {\n        return price * quantity;\n    }\n    public static void main(String[] args) {\n        System.out.println(calculateTotal(25, 3));\n    }\n}",
        "expected": "75",
        "exercise": "Write a static boolean isEven(int number) method and call it with 8 and 7 from main.",
        "expected2": "The method returns true for 8 and false for 7; main prints both results.",
        "quiz": [
            ("Which keyword indicates that a method returns no value?", ["null", "void", "static", "final"], 1, "void is the declared return type for a method that does not return a value."),
            ("Where can a static method be called from?", ["Only an object instance", "Through the class without creating an instance", "Only from a constructor", "Only from another package"], 1, "A static method belongs to the class and can be called using the class name."),
            ("What must a non-void method provide?", ["A print statement", "A compatible return value on every reachable path", "A constructor", "A global variable"], 1, "The method must return a value compatible with its declared return type."),
        ],
    },
    "Pass by Value (Everything)": {
        "concept": "Java pass-by-value semantics",
        "purpose": "understand exactly what a method receives when primitive and reference variables are passed",
        "how": "Java is always pass-by-value. For primitives, the value is copied. For objects, the value copied is the reference, so the method can mutate the same object through that copied reference, but reassigning the parameter does not change the caller's reference variable.",
        "why": "This distinction explains why a method can update an object's fields but cannot swap two caller variables by reassigning its parameters. It is a frequent interview question and prevents incorrect assumptions about pass-by-reference.",
        "pitfall": "Do not say Java passes objects by reference. It passes a copy of the reference value. Mutating the referenced object and reassigning the local parameter are different operations.",
        "code": "class Box { int value = 5; }\npublic class Main {\n    static void change(Box box) { box.value = 99; box = new Box(); }\n    public static void main(String[] args) {\n        Box original = new Box();\n        change(original);\n        System.out.println(original.value);\n    }\n}",
        "expected": "99",
        "exercise": "Write one method that changes an object's field and another that reassigns its parameter to a new object. Demonstrate what the caller observes after each method.",
        "expected2": "The caller sees mutations to the original object's field but does not see the method's local parameter reassignment.",
        "quiz": [
            ("Does Java pass method arguments by reference?", ["Yes, always", "No, Java is always pass-by-value", "Only for objects", "Only for arrays"], 1, "Java passes a copy of each argument value; for objects, that value is a reference."),
            ("Can a method mutate an object through a copied reference?", ["No", "Yes, it refers to the same object", "Only if the class is static", "Only with primitive fields"], 1, "The copied reference still points to the same object, so the method can mutate that object's state."),
            ("Does reassigning a reference parameter change the caller's variable?", ["Yes", "No, the parameter is a local copy", "Only for arrays", "Only for strings"], 1, "Reassigning the local parameter changes only the copied reference, not the caller's reference variable."),
        ],
    },
    "Arrays Basics": {
        "concept": "Java arrays",
        "purpose": "store a fixed-size sequence of elements of one declared type",
        "how": "An array is created with a component type and fixed length, for example int[] marks = new int[5]. Indexes start at zero, length reports the number of elements, and Java initialises array elements to default values. Enhanced for loops visit each element without exposing its index.",
        "why": "Arrays are foundational for placement problems involving sums, searching, sorting, rotations and matrices. Their fixed size makes the memory layout and indexing model predictable.",
        "pitfall": "Accessing an invalid index throws ArrayIndexOutOfBoundsException. The last valid index is length - 1. Arrays are objects, so an array variable stores a reference; assigning it to another variable does not clone the array.",
        "code": "public class Main {\n    public static void main(String[] args) {\n        int[] marks = {70, 80, 90, 60, 85};\n        int total = 0;\n        for (int mark : marks) total += mark;\n        System.out.println(marks[0] + \" \" + total);\n    }\n}",
        "expected": "70 385",
        "exercise": "Read five integers into an array, then calculate the minimum, maximum and average.",
        "expected2": "For 4, 8, 2, 10, 6 the minimum is 2, maximum is 10 and average is 6.",
        "quiz": [
            ("What is the first valid array index?", ["1", "0", "-1", "The array length"], 1, "Java arrays use zero-based indexing."),
            ("What does marks.length return?", ["The last index", "The number of elements", "The sum", "The array type"], 1, "length is a field on arrays that reports the number of elements."),
            ("What happens when an invalid index is accessed?", ["The array grows", "ArrayIndexOutOfBoundsException is thrown", "It always returns zero", "The index wraps around"], 1, "Java performs runtime bounds checks and throws an exception for an invalid array index."),
        ],
    },
    "ArrayList": {
        "concept": "ArrayList collections",
        "purpose": "store a resizable sequence of object references",
        "how": "ArrayList<E> is a resizable array implementation in the Java Collections Framework. add appends an element, get reads by index, set replaces an element, remove deletes one, and size reports the current element count. Use wrapper types such as Integer rather than primitive int as the generic type.",
        "why": "ArrayList is useful when the number of elements changes during program execution. It offers fast indexed access and is a common choice for lists of students, products, tasks and search results.",
        "pitfall": "Use size(), not length, for ArrayList. Removing by an int can select the index overload rather than remove an Integer value. ArrayList is not automatically thread-safe, and inserting at the beginning shifts later elements.",
        "code": "import java.util.ArrayList;\npublic class Main {\n    public static void main(String[] args) {\n        ArrayList<Integer> marks = new ArrayList<>();\n        marks.add(80); marks.add(90); marks.add(70);\n        marks.set(1, 95);\n        System.out.println(marks.size() + \" \" + marks.get(1));\n    }\n}",
        "expected": "3 95",
        "exercise": "Create an ArrayList of student marks, add four values, update one mark, remove one entry, and calculate the average of the remaining values.",
        "expected2": "The list size decreases after removal and the average uses only the remaining marks.",
        "quiz": [
            ("Which method returns the number of elements in an ArrayList?", ["length", "size()", "count()", "capacity()"], 1, "ArrayList uses size() to report the current number of stored elements."),
            ("Which generic type stores integer values?", ["ArrayList<int>", "ArrayList<Integer>", "Array<Integer>", "int<ArrayList>"], 1, "Java generics use reference types, so Integer is the wrapper type for int."),
            ("What does set(index, value) do?", ["Adds at the end", "Replaces the element at an index", "Removes the list", "Sorts the list"], 1, "set replaces the element at the specified index and returns the previous value."),
        ],
    },
    "String & StringBuilder": {
        "concept": "String and StringBuilder",
        "purpose": "represent text and build text efficiently when many changes are required",
        "how": "String objects are immutable: operations such as concatenation create new String values. StringBuilder is mutable and supports append, insert, delete and reverse without creating a new String for every change. Convert the final builder to a String with toString().",
        "why": "Use String for values that should not change and StringBuilder for repeated concatenation, such as constructing reports or processing many tokens in a loop.",
        "pitfall": "Repeated String concatenation in a large loop can create many temporary objects. StringBuilder is not thread-safe; use StringBuffer only when its synchronization is specifically needed. Compare String contents with equals(), not ==.",
        "code": "public class Main {\n    public static void main(String[] args) {\n        StringBuilder text = new StringBuilder();\n        text.append(\"Bounty\").append(\"code\");\n        text.insert(6, \" Learning\");\n        System.out.println(text.toString());\n    }\n}",
        "expected": "Bounty Learningcode",
        "exercise": "Use StringBuilder to join five skill names with a comma and a space. Avoid adding an extra separator after the final skill.",
        "expected2": "The result is one string containing all five skills separated by exactly ', '.",
        "quiz": [
            ("Are Java String objects mutable?", ["Yes", "No, they are immutable", "Only in loops", "Only when empty"], 1, "String operations create new values rather than changing an existing String object."),
            ("Which class is designed for repeated mutable text building?", ["String", "StringBuilder", "Character", "Scanner"], 1, "StringBuilder provides mutable text operations without creating a new String for every append."),
            ("Which method compares String contents?", ["==", "equals()", "same()", "compareReference()"], 1, "equals compares the character content of two String objects."),
        ],
    },
    "Classes & Objects": {
        "concept": "Java classes and objects",
        "purpose": "model related state and behaviour using user-defined reference types",
        "how": "A class declares fields, constructors and methods. An object is created with new and stores its own instance state. Access modifiers such as private and public control which code can read or change members.",
        "why": "Classes model concepts such as accounts, students and orders. Encapsulation keeps data and the operations that maintain its validity together, which makes larger programs easier to reason about.",
        "pitfall": "A class definition does not create an object. Instance members require an instance, while static members belong to the class. Keep fields private when callers should use validated methods to change state.",
        "code": "class Student {\n    private String name;\n    private int marks;\n    Student(String name, int marks) { this.name = name; this.marks = marks; }\n    public void display() { System.out.println(name + \": \" + marks); }\n}\npublic class Main {\n    public static void main(String[] args) { new Student(\"Asha\", 88).display(); }\n}",
        "expected": "Asha: 88",
        "exercise": "Create a BankAccount class with a private balance, a deposit method that rejects non-positive amounts, and a getter for the balance.",
        "expected2": "A valid deposit increases the balance; zero or negative deposits leave the balance unchanged.",
        "quiz": [
            ("What does new Student(...) do?", ["Defines the class", "Creates an object", "Imports a package", "Declares a method"], 1, "new creates an instance and invokes a constructor."),
            ("What is encapsulation?", ["Making every field public", "Controlling access to state through a class interface", "Removing all methods", "Creating only static variables"], 1, "Encapsulation protects internal state and exposes controlled operations."),
            ("What does private mean for a field?", ["Accessible from every class", "Accessible within its declaring class", "Accessible only from main", "It becomes static"], 1, "A private member is directly accessible only within the class that declares it."),
        ],
    },
    "Constructors": {
        "concept": "Java constructors",
        "purpose": "initialise new objects with valid starting state",
        "how": "A constructor has the same name as its class and no return type. It runs when new creates an object. Constructors can be overloaded to support different initialisation options, and this(...) can delegate to another constructor in the same class.",
        "why": "Constructors ensure objects begin in a predictable state. Requiring essential values at creation time prevents partially initialised objects and reduces repeated setup logic.",
        "pitfall": "A constructor is not a method returning void; it has no return type at all. If you declare any constructor, Java does not automatically provide the no-argument default constructor. Constructor delegation with this(...) must be the first statement.",
        "code": "class Product {\n    String name;\n    double price;\n    Product(String name, double price) {\n        this.name = name;\n        this.price = price;\n    }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Product item = new Product(\"Book\", 250);\n        System.out.println(item.name + \" \" + item.price);\n    }\n}",
        "expected": "Book 250.0",
        "exercise": "Create a Student class with a constructor that accepts name, roll number and marks. Create two students with different data and display both.",
        "expected2": "Each object displays its own values without overwriting the other object's state.",
        "quiz": [
            ("Does a Java constructor declare a return type?", ["Yes, void", "No", "Only int", "Only the class name"], 1, "A constructor has no return type, not even void."),
            ("When does a constructor run?", ["When the class is imported", "When an object is created with new", "Every time a field is read", "Only when main ends"], 1, "The constructor runs during object creation to initialise the new instance."),
            ("What happens if a class declares a constructor?", ["A default no-argument constructor is still always added", "The compiler does not add the default no-argument constructor", "The class cannot be instantiated", "All fields become static"], 1, "The implicit default constructor is supplied only when no constructor is declared."),
        ],
    },
    "Inheritance": {
        "concept": "Java class inheritance",
        "purpose": "derive a specialised class from a base class and reuse accessible behaviour",
        "how": "A Java class uses extends to inherit from one superclass. The subclass inherits accessible members, can add new fields and methods, and can override eligible instance methods. Java supports single class inheritance but allows a class to implement multiple interfaces.",
        "why": "Inheritance models an is-a relationship, such as SavingsAccount being a specialised Account. It allows shared behaviour to live in a base class while specialised classes add or customise behaviour.",
        "pitfall": "Constructors are not inherited. A subclass constructor invokes a superclass constructor with super(...), and that call must be first. Prefer composition when the relationship is not genuinely is-a.",
        "code": "class Animal {\n    void speak() { System.out.println(\"Sound\"); }\n}\nclass Dog extends Animal {\n    @Override void speak() { System.out.println(\"Woof\"); }\n}\npublic class Main {\n    public static void main(String[] args) { new Dog().speak(); }\n}",
        "expected": "Woof",
        "exercise": "Create an Employee superclass with a name and a display method. Create a Developer subclass with a programmingLanguage field and override display to include both.",
        "expected2": "A Developer object displays its inherited name and its own programming language.",
        "quiz": [
            ("Which keyword declares Java class inheritance?", ["implements", "extends", "inherits", "super"], 1, "A class names its superclass with the extends keyword."),
            ("Are constructors inherited by subclasses?", ["Yes", "No", "Only public constructors", "Only default constructors"], 1, "Constructors are not inherited; a subclass constructor can invoke a superclass constructor."),
            ("Where must an explicit super(...) constructor call appear?", ["At the end", "As the first statement in the constructor", "Inside every method", "After return"], 1, "A superclass constructor invocation must be the first statement in a constructor."),
        ],
    },
    "Polymorphism Deep": {
        "concept": "runtime polymorphism and method overriding",
        "purpose": "write code against a common superclass or interface while executing the actual object's implementation",
        "how": "A superclass reference can refer to a subclass object. When an overridden instance method is called, Java uses dynamic dispatch to choose the implementation based on the runtime object type. The @Override annotation asks the compiler to verify the override.",
        "why": "Polymorphism lets a program process different payment methods, notifications or shapes through one common interface without a long chain of instanceof checks.",
        "pitfall": "Fields and static methods are not dynamically dispatched like overridden instance methods. The declared reference type controls which members are accessible at compile time, while the runtime object selects the overridden instance method implementation.",
        "code": "class Shape { double area() { return 0; } }\nclass Rectangle extends Shape {\n    double width = 4, height = 5;\n    @Override double area() { return width * height; }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Shape shape = new Rectangle();\n        System.out.println(shape.area());\n    }\n}",
        "expected": "20.0",
        "exercise": "Create a Notification interface with send(). Implement EmailNotification and SmsNotification, store both in a List<Notification>, and call send on each.",
        "expected2": "The same loop calls each object's own implementation without checking its concrete class.",
        "quiz": [
            ("What determines which overridden instance method runs?", ["The variable name", "The runtime object type", "The file name", "The package name"], 1, "Dynamic dispatch selects the overridden method using the actual object type at runtime."),
            ("What does @Override provide?", ["Automatic inheritance", "Compile-time checking that a method really overrides", "A new object", "Thread safety"], 1, "The annotation helps catch misspelled signatures or methods that do not override a superclass method."),
            ("Are static methods dynamically dispatched?", ["Yes, like all instance methods", "No, static methods are hidden and resolved using the reference/class context", "Only in interfaces", "Only for final classes"], 1, "Static methods are resolved at compile time rather than dynamically dispatched as overridden instance methods."),
        ],
    },
    "HashMap Deep": {
        "concept": "HashMap and key-value lookup",
        "purpose": "associate keys with values and retrieve values efficiently by key",
        "how": "HashMap<K,V> stores key-value entries using hashing. put inserts or replaces a value, get retrieves a value or returns null when absent, containsKey checks presence, and remove deletes an entry. Keys should have stable equals and hashCode behaviour while stored.",
        "why": "HashMap is useful for frequency counting, ID-to-record lookup, caching and grouping data. Average lookup and insertion are constant time when hashes are well distributed.",
        "pitfall": "If two objects are equal according to equals(), they must return the same hashCode(). Mutating fields used in a key's hash or equality while it is stored can make the entry difficult to find. HashMap does not guarantee iteration order.",
        "code": "import java.util.HashMap;\npublic class Main {\n    public static void main(String[] args) {\n        HashMap<String, Integer> counts = new HashMap<>();\n        counts.put(\"python\", 2);\n        counts.put(\"sql\", 3);\n        System.out.println(counts.get(\"sql\"));\n        System.out.println(counts.containsKey(\"python\"));\n    }\n}",
        "expected": "3 followed by true.",
        "exercise": "Count word frequencies from a list of words using HashMap.merge or getOrDefault. Print the count for a requested word safely.",
        "expected2": "Repeated words increase their count; a missing word returns zero without causing a NullPointerException.",
        "quiz": [
            ("Which method checks whether a key exists in a HashMap?", ["containsValue", "containsKey", "has", "includes"], 1, "containsKey checks for the presence of a key independently of its mapped value."),
            ("What is the average lookup complexity of HashMap?", ["O(n squared)", "O(1)", "O(log n) always", "O(n log n)"], 1, "HashMap provides average constant-time lookup when hash distribution is suitable."),
            ("What contract must equals and hashCode follow?", ["Equal objects must have equal hash codes", "Different objects must always have different hashes", "hashCode must return the object's address", "equals must compare only references"], 0, "The Java contract requires equal objects to return the same hash code."),
        ],
    },
}


def get_java_core_lesson(lesson_title: str) -> Dict[str, Any] | None:
    title = str(lesson_title or "").strip().lower()
    matches = [
        (len(key), profile)
        for key, profile in _JAVA_CORE.items()
        if key.lower() in title
    ]
    if not matches:
        return None
    profile = max(matches, key=lambda item: item[0])[1]
    return build_authored_lesson(profile, "Java")
