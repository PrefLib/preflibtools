# -*- coding: utf-8 -*-
"""
Copyright Simon Rey
reysimon@orange.fr

This file is part of PrefLib-Tools.
"""
from preflibtools.sub_package_2.my_class_2 import MyClass2


class MyClass1:
    """A whatever-you-are-doing.

    Parameters
    ----------
    a : float
        The `a` of the system. Must be non-negative.
    b : float
        The `b` of the system.

    Attributes
    ----------
    my_string : str
        A nice string.

    Raises
    ------
    ValueError
        If `a` is negative.

    Notes
    -----
    Document the :meth:`__init__` method in the docstring of the class itself,
    because the docstring of the :meth:`__init__` method does not appear in the
    documentation.

    * Refer to a class this way: :class:`MyClass2` (except as a type indication, cf. :meth:`update_b_from_class_2`).
    * Refer to a method this way: :meth:`addition`.
    * Refer to a method in another class: :meth:`MyClass2.addition`.
    * Refer to an attribute this way: :attr:`my_string`.
    * Refer to a property this way: :attr:`a_square`.
    * Refer to a parameter or variable this way: `a`.

    Examples
    --------
    >>> my_object = MyClass1(a=5, b=3)
    """

    #: This is a nice constant.
    A_NICE_CONSTANT = 42
    #:
    A_VERY_NICE_CONSTANT = 51

    def __init__(self, a: float, b: float):
        if a < 0:
            raise ValueError('Expected non-negative a, got: ', a)
        self.a = a
        self.b = b
        self.my_string = 'a = %s and b = %s' % (a, b)

    def __repr__(self) -> str:
        return 'MyClass1(a=%r, b=%r)' % (self.a, self.b)

    def __str__(self) -> str:
        return '(a, b) = %s, %s' % (self.a, self.b)

    def divide_a_by_c_and_add_d(self, c: float, d: float) -> float:
        """Divide `a` by something and add something else.

        Parameters
        ----------
        c : Number
            A non-zero number. You can say many things about this parameter
            in several indented lines, like this.
        d : Number
            A beautiful number.

        Returns
        -------
        Number
            The result of `a / c + d`.

        Raises
        ------
        ZeroDivisionError
            If `c` = 0.

        Notes
        -----
        This function gives an example of documentation with typical features.

        Examples
        --------
        We can write some text to explain the following example:

            >>> my_object = MyClass1(a=5, b=3)
            >>> my_object.divide_a_by_c_and_add_d(c=2, d=10)
            12.5

        And we can explain a second example here:

            >>> my_object = MyClass1(a=5, b=3)
            >>> my_object.divide_a_by_c_and_add_d(c=2, d=20)
            22.5
        """
        return self.a / c + d

    def addition(self) -> float:
        """Add `a` and `b`.

        Returns
        -------
        Number
            The sum of `a` and `b`.

        Examples
        --------
            >>> my_object = MyClass1(a=5, b=3)
            >>> my_object.addition()
            8
        """
        return MyClass2(self.a, self.b).addition()

    @property
    def a_square(self) -> float:
        """The square of `a`."""
        return self.a ** 2

    def update_b_from_class_2(self, object_of_class_2):
        """Update `b` from a :class:`MyClass2` object.

        Parameters
        ----------
        object_of_class_2 : MyClass2
            An object from the other class. The purpose of this function is essentially to show how to document when
            an argument is an object of another class.

            N.B.: for the type of an argument, you can enter only the name of the class, e.g. ``MyClass2``.
            However, in the rest of the documentation, you must use the full syntax, like ``:class:`MyClass2```.

        Examples
        --------
            >>> my_object = MyClass1(a=5, b=3)
            >>> my_object.update_b_from_class_2(MyClass2(42, 51))
            >>> my_object.b
            51
        """
        self.b = object_of_class_2.b

    # noinspection PyProtectedMember
    def _secret_function(self) -> float:
        """Difference between `a` and `b`.

        Returns
        -------
        Number
            The result of `a` - `b`.

        Notes
        -----
        Since the name of this function starts with _, it does not appear in
        the Sphinx documentation (by default).

        Examples
        --------
            >>> my_object = MyClass1(a=5, b=3)
            >>> my_object._secret_function()
            2
        """
        return self.a - self.b
