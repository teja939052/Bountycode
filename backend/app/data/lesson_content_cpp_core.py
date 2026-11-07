"""Authored C++ placement-fundamentals lesson profiles."""
from __future__ import annotations

from typing import Any, Dict

from app.data.lesson_content_authored_builder import build_authored_lesson


_CPP_CORE: Dict[str, Dict[str, Any]] = {
    "if / else if / else": {
        "concept": "if, else if and else selection",
        "purpose": "choose one execution path based on ordered Boolean conditions",
        "how": "C++ evaluates the if condition first, then checks else if conditions in order. The first true branch executes and the remaining branches are skipped. The optional final else handles every case not matched earlier. Conditions must be convertible to bool.",
        "why": "Selection is used for grading bands, menu commands, validation and business rules. Put the most restrictive threshold first so a broad condition does not capture values intended for a later branch.",
        "pitfall": "Use == for comparison and = for assignment. A semicolon immediately after if(condition) creates an empty body and can make the following block run unconditionally. Use braces consistently, even for one statement.",
        "code": "#include <iostream>\nusing namespace std;\nint main() {\n    int score = 82;\n    if (score >= 90) cout << \"A\";\n    else if (score >= 75) cout << \"B\";\n    else cout << \"Practice\";\n}",
        "expected": "The program prints B for score 82.",
        "exercise": "Write a grade classifier for scores 0–100: A for 90+, B for 75–89, C for 60–74 and Needs Practice below 60. Reject values outside the range.",
        "expected2": "Boundary checks 90, 75, 60, 59, -1 and 101 produce the correct band or an invalid-score message.",
        "quiz": [
            ("Which branch runs in one if / else if / else chain?", ["Every true branch", "Only the first matching branch", "All branches after else", "No branch"], 1, "The chain stops after the first true condition, so at most one branch executes."),
            ("Why should score >= 90 be checked before score >= 75?", ["The compiler requires it", "A score of 95 also satisfies score >= 75", "It uses less memory", "It changes the type"], 1, "The broader condition would match high scores first if it appeared before the more specific threshold."),
            ("What does a semicolon directly after if(condition) do?", ["Starts a block", "Terminates the if body as an empty statement", "Declares a variable", "Adds an else automatically"], 1, "The semicolon is an empty statement, so the intended following block is no longer controlled by the if."),
        ],
    },
    "for Loop": {
        "concept": "counted for loops",
        "purpose": "repeat a block while a counter follows a defined progression",
        "how": "A traditional for loop has an initialisation, condition and update expression: for (int i = 0; i < n; ++i). Initialisation runs once, the condition is checked before each iteration, and the update runs after the body. The loop stops when the condition becomes false.",
        "why": "Counted loops are suitable when the number of repetitions is known, such as processing array indexes, generating multiplication tables and accumulating totals.",
        "pitfall": "The condition i < n excludes n, so check whether the task uses zero-based indexes or one-based values. An incorrect update can skip values or create an infinite loop. Avoid reading an array beyond its valid indexes.",
        "code": "#include <iostream>\nusing namespace std;\nint main() {\n    int total = 0;\n    for (int i = 1; i <= 5; ++i) total += i;\n    cout << total;\n}",
        "expected": "15",
        "exercise": "Read an integer n and print its multiplication table from 1 through 10 using a for loop.",
        "expected2": "For n=4, the program prints 4 x 1 = 4 through 4 x 10 = 40.",
        "quiz": [
            ("How many times does for(int i=0; i<5; ++i) run?", ["4", "5", "6", "Infinite"], 1, "The values are 0, 1, 2, 3 and 4, so the body executes five times."),
            ("When does the update expression run?", ["Before initialisation", "After each completed body iteration", "Only after the loop ends", "Before every condition check"], 1, "The update expression runs after the body and before the next condition check."),
            ("What is a common off-by-one error?", ["Using int", "Using <= when the upper bound should be excluded", "Using braces", "Using cout"], 1, "The loop condition must match whether the upper boundary is inclusive or exclusive."),
        ],
    },
    "Function Basics": {
        "concept": "C++ function declarations, definitions and calls",
        "purpose": "organise reusable operations with typed inputs and return values",
        "how": "A function declaration tells the compiler its name, return type and parameter types. A definition provides the body. Calling the function supplies arguments, executes the body and returns a value when the return type is not void. A function prototype is commonly placed before main when the definition appears later.",
        "why": "Functions divide a program into small responsibilities, reduce duplication and make logic easier to test. A well-named function can describe a calculation without exposing every implementation detail to its caller.",
        "pitfall": "The declaration and definition must agree on return and parameter types. A non-void function must return a value on every reachable path. Do not confuse printing a value with returning it to the caller.",
        "code": "#include <iostream>\nusing namespace std;\nint calculateTotal(int price, int quantity);\nint main() { cout << calculateTotal(25, 3); }\nint calculateTotal(int price, int quantity) { return price * quantity; }",
        "expected": "75",
        "exercise": "Write an isEven(int number) function that returns true for even numbers and false for odd numbers. Call it with 8 and 7.",
        "expected2": "The calls return true and false respectively; print the results from main.",
        "quiz": [
            ("What does a function prototype provide?", ["The function's implementation", "The function signature to the compiler", "A runtime input", "A class object"], 1, "A prototype declares the function's return type, name and parameter types before its definition is encountered."),
            ("What should a non-void function do?", ["Always print", "Return a value of its declared type on every path", "Declare a global variable", "Call itself"], 1, "A non-void function must provide a return value that matches its declared return type."),
            ("What is the difference between cout and return?", ["They are identical", "cout displays output; return passes a value to the caller", "return prints to console", "cout ends the function"], 1, "Returning makes a value available to the caller; cout only writes output."),
        ],
    },
    "Pass by Value vs Reference": {
        "concept": "passing arguments by value and by reference",
        "purpose": "choose whether a function receives a copy or can work with the caller's original object",
        "how": "Pass by value creates a separate parameter value, so changes to that parameter do not change the caller's variable. Pass by reference uses a reference parameter such as int& value, allowing the function to modify the original object. Use const T& to avoid copying large objects without allowing modification.",
        "why": "This distinction affects correctness and performance. Small primitive values are commonly passed by value; larger objects are often passed by const reference for read-only access, or by non-const reference when mutation is part of the function's contract.",
        "pitfall": "A reference must bind to a valid object and cannot be reseated to refer to another object. Do not use a non-const reference when the function should not modify its input. Be explicit about ownership and lifetime when returning references.",
        "code": "#include <iostream>\nusing namespace std;\nvoid changeCopy(int x) { x = 99; }\nvoid changeOriginal(int& x) { x = 99; }\nint main() { int a = 5, b = 5; changeCopy(a); changeOriginal(b); cout << a << \" \" << b; }",
        "expected": "5 99",
        "exercise": "Write one function that attempts to swap two integers by value and another that swaps them by reference. Call both and compare the caller's variables.",
        "expected2": "The by-value function leaves caller values unchanged; the reference version swaps them.",
        "quiz": [
            ("What happens to a caller variable passed by value?", ["It is always modified", "The function receives a separate copy", "It becomes a pointer", "It is deleted"], 1, "The parameter is a separate object initialised from the argument, so assigning to it does not update the caller's variable."),
            ("Which syntax declares an integer reference parameter?", ["int* value", "int& value", "const int value*", "int value&*"], 1, "The ampersand after the type declares a reference parameter."),
            ("Why pass a large read-only object as const T&?", ["To force a copy", "To avoid copying while preventing modification through the parameter", "To allocate it on the heap", "To make it global"], 1, "A const reference avoids a potentially expensive copy and communicates read-only intent."),
        ],
    },
    "C-style Arrays": {
        "concept": "fixed-size C++ arrays",
        "purpose": "store a fixed number of elements of the same type in contiguous memory",
        "how": "An array declaration such as int marks[5] reserves five integer elements. Indexes start at zero and the final valid index is size minus one. A range-based for loop can visit every element, while std::size can report the element count for built-in arrays in modern C++.",
        "why": "Arrays are a foundation for understanding contiguous storage, indexing and algorithmic complexity. They appear in placement problems involving sums, searching, rotations and frequency counts.",
        "pitfall": "Built-in arrays do not check bounds. Accessing marks[5] in a five-element array is undefined behaviour. Uninitialised local arrays contain indeterminate values; initialise them before reading.",
        "code": "#include <iostream>\nusing namespace std;\nint main() {\n    int marks[5] = {70, 80, 90, 60, 85};\n    int total = 0;\n    for (int mark : marks) total += mark;\n    cout << marks[0] << \" \" << total;\n}",
        "expected": "70 385",
        "exercise": "Read five integers into an array, then calculate the minimum, maximum and average.",
        "expected2": "For 4, 8, 2, 10, 6 the minimum is 2, maximum is 10 and average is 6.",
        "quiz": [
            ("What is the first valid index of a C++ array?", ["1", "0", "-1", "The array length"], 1, "C++ arrays use zero-based indexing."),
            ("What is the last valid index of int values[5]?", ["5", "4", "6", "0"], 1, "Five elements have indexes zero through four."),
            ("What can happen when a built-in array is accessed out of bounds?", ["It always returns zero", "Undefined behaviour", "The compiler resizes it", "A safe exception is always thrown"], 1, "Built-in array indexing does not perform automatic bounds checking."),
        ],
    },
    "std::vector Basics": {
        "concept": "std::vector",
        "purpose": "store a dynamically sized sequence with contiguous elements",
        "how": "std::vector<T> is a standard-library container that manages its own storage. push_back appends an element, size returns the number of elements, and operator[] accesses an element without bounds checking. at(index) performs a bounds-checked access. Include <vector>.",
        "why": "Vectors are the default sequence container for many C++ placement problems because they grow dynamically and work with standard algorithms. They avoid manual new[] and delete[] for ordinary dynamic arrays.",
        "pitfall": "A vector's size is the number of elements, not its capacity. Reallocation can invalidate pointers, references and iterators to its elements. Use at() when a checked access is useful, and avoid indexing an empty vector.",
        "code": "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    vector<int> values = {3, 1, 4};\n    values.push_back(2);\n    cout << values.size() << \" \" << values.at(2);\n}",
        "expected": "4 4",
        "exercise": "Read n marks into a vector, append one additional mark, then print the count and average.",
        "expected2": "The vector contains n+1 elements and the average includes the appended mark.",
        "quiz": [
            ("Which method appends an element to a vector?", ["add", "push_back", "insert_end_only", "append"], 1, "push_back appends a new element to the end of a std::vector."),
            ("What is the difference between size and capacity?", ["They are identical", "size counts elements; capacity reports allocated storage before reallocation", "capacity counts elements only", "size is bytes"], 1, "size is the current element count, while capacity is how many elements can fit before reallocation is needed."),
            ("Which vector method performs bounds-checked access?", ["operator[]", "at()", "front() only", "data()"], 1, "at() checks the index and throws std::out_of_range when it is outside the vector."),
        ],
    },
    "Classes & Objects": {
        "concept": "classes and objects in C++",
        "purpose": "combine data and operations into user-defined types",
        "how": "A class declares members and access sections such as public and private. An object is an instance of a class. Member functions operate on the object's state, and private members restrict direct access from outside the class.",
        "why": "Classes model concepts such as bank accounts, students and products. Encapsulation protects invariants by allowing state changes through methods that validate the requested operation.",
        "pitfall": "Class members are private by default, while struct members are public by default. Do not expose mutable state unnecessarily. A member function should preserve the class's invariants after every operation.",
        "code": "#include <iostream>\n#include <string>\nusing namespace std;\nclass Student {\npublic:\n    string name;\n    int marks;\n    void display() const { cout << name << \": \" << marks; }\n};\nint main() { Student s; s.name = \"Asha\"; s.marks = 88; s.display(); }",
        "expected": "Asha: 88",
        "exercise": "Create a BankAccount class with private balance, a deposit method that rejects non-positive amounts, and a getBalance method.",
        "expected2": "A valid deposit increases the balance; zero or negative deposits leave it unchanged.",
        "quiz": [
            ("What is an object?", ["A class definition", "An instance of a class", "A header file", "A namespace"], 1, "An object is a concrete instance created from a class definition."),
            ("What is the default access level for class members in C++?", ["public", "private", "protected", "global"], 1, "Members of a class are private by default."),
            ("Why encapsulate a balance field as private?", ["To make it slower", "To control updates and preserve valid state", "To prevent all methods", "To convert it to a pointer"], 1, "Private state can only be changed through the class interface, where validation rules can be enforced."),
        ],
    },
    "Constructors & Destructors": {
        "concept": "constructors and destructors",
        "purpose": "initialise objects and release resources when their lifetime ends",
        "how": "A constructor has the same name as the class and no return type. It runs when an object is created and can initialise members through a member-initialiser list. A destructor is named with a tilde and runs when the object is destroyed, making it useful for releasing owned resources.",
        "why": "Correct construction ensures objects begin in a valid state. Destruction and RAII help tie resource lifetime to object lifetime, reducing leaks and making cleanup reliable when control leaves a scope.",
        "pitfall": "A constructor is not a normal function returning the object. Prefer member-initialiser lists, especially for const and reference members. Avoid owning raw resources without a clear destructor and copy/move policy; standard containers and smart pointers are safer.",
        "code": "#include <iostream>\n#include <string>\nusing namespace std;\nclass User {\n    string name;\npublic:\n    User(string value) : name(value) { cout << \"Created \" << name << endl; }\n    ~User() { cout << \"Destroyed \" << name << endl; }\n};\nint main() { User user(\"Asha\"); }",
        "expected": "Created Asha followed by Destroyed Asha.",
        "exercise": "Create a Logger class that prints a message when constructed and another when destroyed. Instantiate it inside a nested scope and observe when destruction occurs.",
        "expected2": "The destructor message appears immediately after execution leaves the nested scope, before the program continues.",
        "quiz": [
            ("Does a constructor have a return type?", ["Yes, void", "No", "Only int", "It returns a pointer"], 1, "Constructors have no declared return type."),
            ("When is a local object's destructor normally called?", ["Before construction", "When its lifetime ends at scope exit", "Only when main returns", "Only after delete"], 1, "Automatic objects are destroyed when their scope ends, in reverse order of construction."),
            ("What is the purpose of a member-initialiser list?", ["To initialise members before the constructor body", "To print member names", "To allocate every object on the heap", "To call main"], 0, "The member-initialiser list initialises data members directly and is required for const and reference members."),
        ],
    },
    "Inheritance": {
        "concept": "inheritance in C++",
        "purpose": "derive a specialised class from a base class and reuse its interface and implementation",
        "how": "A derived class declares its base after a colon, such as class Dog : public Animal. Public inheritance models an is-a relationship. The derived class inherits accessible members and can add or override behaviour. Access specifiers affect how inherited members are exposed.",
        "why": "Inheritance can model related types that share a stable interface, such as different notification channels or shapes. It supports runtime polymorphism when base classes provide virtual functions.",
        "pitfall": "Do not use inheritance solely to reuse unrelated code; composition may be better. A base class intended for polymorphic deletion should have a virtual destructor. Avoid slicing when copying a derived object into a base object by value.",
        "code": "#include <iostream>\nusing namespace std;\nclass Animal {\npublic:\n    virtual void speak() const { cout << \"Sound\"; }\n    virtual ~Animal() = default;\n};\nclass Dog : public Animal {\npublic:\n    void speak() const override { cout << \"Woof\"; }\n};\nint main() { Dog dog; dog.speak(); }",
        "expected": "Woof",
        "exercise": "Create a base class Shape with a virtual area method and derive Rectangle with width and height. Override area to return width times height.",
        "expected2": "A Rectangle with width 4 and height 5 returns area 20 through a Shape pointer or reference.",
        "quiz": [
            ("How does a C++ class declare public inheritance?", ["class Dog extends Animal", "class Dog : public Animal", "class Dog(Animal)", "inherit Dog Animal"], 1, "C++ places a colon and access specifier between the derived class and its base class."),
            ("Why should a polymorphic base class often have a virtual destructor?", ["To make construction faster", "To ensure derived cleanup runs when deleting through a base pointer", "To prevent inheritance", "To overload operators"], 1, "A virtual destructor ensures the derived destructor is called when an object is deleted through a base-class pointer."),
            ("What is object slicing?", ["Copying only the base part of a derived object into a base object by value", "Sorting class members", "Deleting a virtual method", "Moving an array"], 0, "Copying a derived object into a base object by value discards the derived portion."),
        ],
    },
    "Smart Pointers: unique_ptr": {
        "concept": "std::unique_ptr smart pointers",
        "purpose": "manage exclusive dynamic-object ownership automatically",
        "how": "std::unique_ptr owns one dynamically allocated object and deletes it automatically when the unique_ptr is destroyed. std::make_unique<T>(...) is the preferred way to create one. Ownership can be moved with std::move, but unique_ptr cannot be copied.",
        "why": "Unique ownership is the default choice for dynamically allocated resources when one owner is responsible for their lifetime. It expresses ownership in the type system and prevents many memory leaks.",
        "pitfall": "Do not call delete on the raw pointer owned by a unique_ptr. Do not copy a unique_ptr; move it to transfer ownership. Prefer stack objects and standard containers when dynamic ownership is not actually required.",
        "code": "#include <iostream>\n#include <memory>\nusing namespace std;\nint main() {\n    auto value = make_unique<int>(42);\n    cout << *value << endl;\n    auto owner = move(value);\n    cout << (value == nullptr) << \" \" << *owner;\n}",
        "expected": "42 followed by 1 42.",
        "exercise": "Create a unique_ptr to a Student object, move it into a second unique_ptr, and verify that the original owner is empty while the new owner can access the student.",
        "expected2": "After the move, the source unique_ptr is nullptr and the destination owns the object.",
        "quiz": [
            ("Can std::unique_ptr be copied?", ["Yes", "No, ownership is exclusive", "Only for integers", "Only when raw pointers are used"], 1, "unique_ptr is move-only so that there is one clear owner."),
            ("Which helper is preferred to create a unique_ptr?", ["new_unique", "std::make_unique", "std::malloc_unique", "std::shared"], 1, "make_unique constructs the object and returns an owning unique_ptr."),
            ("What does std::move enable for unique_ptr?", ["A deep copy", "Transfer of ownership", "Automatic sharing", "Deletion of the target"], 1, "std::move allows the unique_ptr ownership to be transferred to another unique_ptr."),
        ],
    },
    "STL: map & unordered_map": {
        "concept": "ordered and unordered associative maps in the C++ STL",
        "purpose": "associate keys with values and retrieve values efficiently by key",
        "how": "std::map stores unique keys in sorted order and typically provides O(log n) lookup, insertion and deletion. std::unordered_map uses hashing and offers average O(1) operations, but does not maintain key order. Both provide find, insert, erase and operator[] access.",
        "why": "Maps are useful for frequency counting, indexing records by identifier and memoization. Choose map when sorted traversal or ordered range queries matter; choose unordered_map for average constant-time lookup when ordering is unnecessary.",
        "pitfall": "operator[] inserts a default value when the key is missing. Use find or contains when you only want to test presence. Hash-map worst-case operations can be slower than average, and custom key types need a suitable hash function.",
        "code": "#include <iostream>\n#include <unordered_map>\nusing namespace std;\nint main() {\n    unordered_map<string, int> counts;\n    counts[\"python\"]++;\n    counts[\"sql\"] += 2;\n    cout << counts.at(\"sql\") << \" \" << counts.contains(\"python\");\n}",
        "expected": "2 1",
        "exercise": "Read a sequence of words and use unordered_map to count each word's frequency. Print the count for a requested word without inserting it when absent.",
        "expected2": "Repeated words increase their counts; querying a missing word reports not found and does not add a new map entry.",
        "quiz": [
            ("Which container maintains keys in sorted order?", ["unordered_map", "map", "vector", "stack"], 1, "std::map stores keys according to its ordering comparator."),
            ("What is the average lookup complexity of unordered_map?", ["O(n squared)", "O(1)", "O(log n) always", "O(n log n)"], 1, "Hash-based lookup is average constant time, although worst-case behaviour can be linear."),
            ("What can operator[] do for a missing key?", ["Always throw", "Insert a default-initialised mapped value", "Sort the map", "Delete another key"], 1, "operator[] inserts a new key with a default-initialised mapped value when the key is absent."),
        ],
    },
}


def get_cpp_core_lesson(lesson_title: str) -> Dict[str, Any] | None:
    title = str(lesson_title or "").strip().lower()
    matches = [
        (len(key), profile)
        for key, profile in _CPP_CORE.items()
        if key.lower() in title
    ]
    if not matches:
        return None
    profile = max(matches, key=lambda item: item[0])[1]
    return build_authored_lesson(profile, "C++")
