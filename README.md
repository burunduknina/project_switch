switch-support
===============================================================

switch-support is a module to work with Python code with additions of switch-case blocks


Functions:
--------

* exec: Overrode built-in function with support switch-case statement.

* support_switch: Decorator to execute docstring of a functions instead of code. Support switch-case statement.

Installation
------------

To use switch_support.py copy 'switch' folder to your project and import 
necessary functions.

Examples usage:
------------------------
- Example of exec():

```python
from switch.switch_support import exec
a, b, c = 2, 4, 5
d = None

exec("""switch a*a:
    case b:
        print("Foo")
        d = 1
        break
    case c:
        print("Bar")
        d = 2
        break 
assert d == 1
""")
```
- Example of support_switch():

```python
from switch.switch_support import support_switch
@support_switch
def my_function_with_switch(a: int, b: int, c: int):
    """
    switch a:
         case b:
              return True
         case c:
              return False
		sw
    """

assert my_function_with_switch(2*2, 4, 5)
```
