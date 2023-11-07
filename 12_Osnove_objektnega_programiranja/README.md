




Speaking of dir(), you can use this function to inspect the methods and attributes that are available in a particular object:

>>> dir(str)
['__add__', '__class__', ..., 'title', 'translate', 'upper', 'zfill']

>>> dir(tuple)
['__add__', '__class__', ..., 'count', 'index']
When you call dir() with the name of a Python object as an argument, the function attempts to return a list of valid attributes for that specific object. This is a convenient way to get an idea of what a given object can do.