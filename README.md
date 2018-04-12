# Functional Python Programming - Second Edition
This is the code repository for [Functional Python Programming - Second Edition](https://www.packtpub.com/application-development/functional-python-programming-second-edition?utm_source=github&utm_medium=repository&utm_campaign=9781788627061), published by [Packt](https://www.packtpub.com/?utm_source=github). It contains all the supporting project files necessary to work through the book from start to finish.
## About the Book
If you’re a Python developer who wants to discover how to take the power of functional programming (FP) and bring it into your own programs, then this book is essential for you, even if you know next to nothing about the paradigm.

Starting with a general overview of functional concepts, you’ll explore common functional features such as first-class and higher-order functions, pure functions, and more. You’ll see how these are accomplished in Python 3.6 to give you the core foundations you’ll build upon. After that, you’ll discover common functional optimizations for Python to help your apps reach even higher speeds.

You’ll learn FP concepts such as lazy evaluation using Python’s generator functions and expressions. Moving forward, you’ll learn to design and implement decorators to create composite functions. You'll also explore data preparation techniques and data exploration in depth, and see how the Python standard library fits the functional programming model. Finally, to top off your journey into the world of functional Python, you’ll at look at the PyMonad project and some larger examples to put everything into perspective.

## Instructions and Navigation
All of the code is organized into folders. Each folder starts with a number followed by the application name. For example, Chapter02.



The code will look like the following:
```
s = 0 
for n in range(1, 10): 
    if n % 3 == 0 or n % 5 == 0: 
        s += n 
print(s) 
```

This book presumes some familiarity with Python 3 and general concepts of application development. We won’t look deeply at subtle or complex features of Python; we’ll avoid much consideration of the internals of the language.

We’ll presume some familiarity with functional programming. Since Python is not a functional programming language, we can’t dig deeply into functional concepts. We’ll pick and choose the aspects of functional programming that fit well with Python and leverage just those that seem useful.

Some of the examples use exploratory data analysis (EDA) as a problem domain to show the value of functional programming. Some familiarity with basic probability and statistics will help with this. There are only a few examples that move into more serious data science.

You’ll need to have Python 3.6 installed and running. For more information on Python, visit http://www.python.org/. The examples all make extensive use of type hints, which means that the latest version of mypy must be installed as well.

Check out https://pypi.python.org/pypi/mypy for the latest version of mypy.

Examples in Chapter 9, More Itertools Techniques, use PIL and Beautiful Soup 4. The Pillow fork of the original PIL library works nicely; refer to https://pypi.python.org/pypi/Pillow/2.7.0 and https://pypi.python.org/pypi/beautifulsoup4/4.6.0.

Examples in Chapter 14, The PyMonad Library, use PyMonad; check out https://pypi.python.org/pypi/PyMonad/1.3.

All of these packages should be installed using the following:

$ pip install pillow beautifulsoup4 PyMonad

To confirm that all the doctests pass run the following:

$ python3 test_all.py

Tests must be run from the top-level directory using the following:

$ python3 -m doctest Chapter_3/*.py

There is no response when the tests pass.

If you want details, you can run the following:

$ python3 -m doctest -v Chapter_4/*.py

This will produce a lot of detail, but at the end is a count of tests passed.

## Related Products
* [Functional Python Programming](https://www.packtpub.com/application-development/functional-python-programming?utm_source=github&utm_medium=repository&utm_campaign=9781784396992)

* [Learn Python Programming - Fundamentals of Python - Second Edition](https://www.packtpub.com/application-development/learn-python-programming-fundamentals-python?utm_source=github&utm_medium=repository&utm_campaign=9781788996662)

* [Neural Network Programming with Python](https://www.packtpub.com/big-data-and-business-intelligence/neural-network-programming-python?utm_source=github&utm_medium=repository&utm_campaign=9781784398217)

### Suggestions and Feedback
[Click here](https://docs.google.com/forms/d/e/1FAIpQLSe5qwunkGf6PUvzPirPDtuy1Du5Rlzew23UBp2S-P3wB-GcwQ/viewform) if you have any feedback or suggestions.
