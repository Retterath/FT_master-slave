## Python
_ means the name is to be treated like private
__ "dunder" means the name is class-specific. Access them from the class itself

<b>Tkinter</b> 
We should not use fixed height/width. That excludes the use of: grid_propagate(), pack_propagate(), width, height

the main program is being passed to each object as the "controller" parameter

Switching Pages
Don't destroy widgets as this can lead to memory leak SOURCE: https://stackoverflow.com/questions/14408521/perl-tk-memory-leak-when-using-destroy-command
## VS CODE
<p> In your settings.json, set "python.languageServer": "Pylance". 
This extension works better (in my opinion) than the one
microsoft uses. https://github.com/microsoft/vscode-python/issues/3977 <p>

#args: pass as much crap as you want (passing through values)
#kwargs: key-word-arguments (passing through dictionaries)
If you want to call method without creating object use @staticmethod
