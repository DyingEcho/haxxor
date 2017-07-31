# Specifications for the `haxxor` language
## The basics
### Displaying text
Displaying text on the screen is done like this:
```
disp myString
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