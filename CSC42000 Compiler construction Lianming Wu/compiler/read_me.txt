Project written in: Python 3.6
PLATFORM : Pycharm
CSC 42000 compiler construction
Student: Lianming Wu


To use the compiler:
	Edit the input_file text, and run the compiler.py file
	You can edit the file name in the read_file to take in different input
	cd into the compiler folder
	type python compiler.py input_file to get the output, or just uncomment and edit the string in the compiler.py file
	


***Use notepad to open the input files and simple_stack***

What this 'compiler' is capble of doing:
	* Acts as a little interpreter and gives you the result of your program immediately (Result showing in the symble_table and memory_table)
	* Able to do add,subtract,multiply,division, int_div, modulo
	* Able to declare variables and assign variable values,  a := b is ok too
	* Able to do a simple repeat until loop with ( =, <>, <,>,<=,>=) conditions
	* Able to check for duplicate declaration, syntax error (not matching), assignment with wrong type error
	* Able to add comments using { } anywhere
	* Able to do pass mutiple BEGIN and END blocks without scopes 
	* Able to generate a simple_stack that basically represents the actions of the program


Stack_Machine Language:
a: .word INTEGER // declare variable a as an integer
MOV a ,b  // Make a and b's value the same
ADD a ,b  // returns a+b
SUB a ,b  // returns a-b
MUL a ,b  // returns a*b
DIV a ,b  // returns int(a/b)
MOD a ,b  // returns a%b
F_DIV a, b // returns a/b
PUSH a // push the variable a
PUSHI 9 // push int 9 into the stack
POP // pop the top of the stack
JG // jump if greater
JGE // jump greater or equal
JG // jump greater
Simlarly JL JLE
JE // jump equal
JNE // jump not equal