# haxxor
Haxxor is a programming language I'm making for fun. Eventually it'll be Turing Complete... -ish.

## Running haxxor code
I haven't developed it to the point where an executable release would be useful, but you can play around with it by downloading the source code and installing with whatever Python-Executable program you want. Just keep in mind that by the time you've downloaded and set up, it may be out of date.

Once installed, run it like this:
```
haxxor /path/to/script.hx false
```

You can, of course, run it from the source code directly. Assuming you're in the code directory:

```
python3 interpret.py /path/to/script.hx false
```
 (You may be wondering what the `false` is for... don't worry, it'll be useful soon. Just use it for now and all will be well.)

## Writing haxxor code
You can read the documentation in [specs.md](info/specs.md). If you have any questions and a thorough reading of the docs doesn't help, [submit an issue](../../issues).

There's a custom file type for developing in PyCharm which you can download [here](info/filetype.jar).