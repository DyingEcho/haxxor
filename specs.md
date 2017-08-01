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
disp $myVar
```
where `$myVar` is a string you want printed.

### Variables
Strings are assigned like this:
```
assn str myVar "myString"
```
where `myVar` is the variable name (will be `$myVar`) and `"myString"` is what it contains.

### Waiting
You can wait for a certain amount of time like this:
```
wait 7
```
where 7 is the number of milliseconds you want to wait for.