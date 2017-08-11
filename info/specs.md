# Specifications for the `haxxor` language
## The basics
### Displaying text
Displaying text on the screen is done like this:
```
disp "myString"
```
where `myString` is the text you want printed.

You can also use
```
disp $myStr
disp #myInt
```

### Variables
#### Strings
Strings are assigned like this:
```
assn str myVar "myString"
```

where `myVar` is the variable name (will be `$myVar`) and `"myString"` is what it contains.

#### Integers
Integers are assigned like this:
```
assn int myVar 42
```
where `myVar` is the variable name (will be `#myVar`) and it contains 42.

#### Deleting
You can also delete variables to save memory.

Do it like this:
```
assn del myVar
```
where `$myVar` is the variable you want to delete.

### Waiting
You can wait for a certain amount of time like this:
```
wait 7
```
where 7 is the number of milliseconds you want to wait for.

### Input
Get a string of user input like this:
```
assn in myVar "What is your name?"
```
where `myVar` is the variable name (will be `$myVar`) and `What is your name?` is the prompt.

### If/Else
#### If
An `if` statement allows you to check if a clause is true, and if so, execute a statement.
You can do it like this:
```
if 7 == 7 |> goto sevenIsSeven 
```

In this example, the interpreter will go to the tag sevenIsSeven because `7==7` evaluates to True.
#### Else
An `else` statement will execute its clause if the `if` statement before it evaluated to False.
```
if 7 == 7 |> goto sevenIsSeven 
else |> disp "Logic is on break today."
```
#### Operators
You can use different operators to compare values.
`==` is for equality.
`>` is for greater than.
`<` is for less than.
`<=` is for less than or equal to.
`>=` is for greater than or equal to.
`!=` is for inequality.

## String Operations
### Concatenation
Concatenate strings like this:
 ```
 strop add $a $b
 ```
where `$b` is the string you want to add to the end of `$a`.



strop add $nameis $name
assn del name
disp $nameis

## Gotos and Tags
### Tags
Tags can be added like this:
```
tag myTag
```
where `myTag` is the name of the tag.

### Gotos
You can jump to a tag like this:
```
goto myTag
```
where `myTag` is the tag you want to go to.

## File Operations
### Opening
You can open a file for reading, writing or appending like so:
```
flop open path/to/myFile.txt
flop open $myFilePath
```
You can only open one file at a time.

### Reading
You can store the content of a file like so:
```
flop read $myVar
```

### Appending
You can append a line to a file like so:
```
flop append "myText"
flop append $myStr
```

### Overwriting
You can overwrite a file like this:
```
flop owrite "myText"
flop owrite $myStr
```

### Closing
Finally, it's important to close files once you're finished working on them.
```
flop close
```