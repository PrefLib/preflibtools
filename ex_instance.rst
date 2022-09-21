
We use different Python classes to deal with the different types of data that are hosted on
`PrefLib.org website <https://www.preflib.org/>`_. All these classes inherit from `PrefLibInstance`, the abstract
class that implements all the basic functionalities common to all the others. Let us first discuss the class
`PrefLibInstance`, the other classes will be introduced later.

The most important functionality, is the ability to read and parse PrefLib data. We provide several ways to do so, as
illustrated below.

.. code-block:: python

    from preflibtools.instance import PrefLibInstance

    # The instance can be populated either by reading a file, or from an URL.
    instance = PrefLibInstance()
    instance.parse_file("00001-00000001.soi")
    instance.parse_url("https://www.preflib.org/static/data/irish/00001-00000001.soi")

`PrefLibInstance` also stores most of the metadata about the data file.

.. code-block:: python

    # Path to the original file, and the name of the file
    instance.file_path
    instance.file_name
    # The type of the instance and its modification type
    instance.data_type
    instance.modification_type
    # Some potentially related files
    instance.relates_to
    instance.related_files
    # The title of the data file and its description (mainly empty, on purpose)
    instance.title
    instance.description
    # Some historical landmark about the data file
    instance.publication_date
    instance.modification_date
    # The number of alternatives and their names
    instance.num_alternatives
    for alt, alt_name in instance.alternatives_name.items():
        alternative = alt
        name = alt_name
    # The number of voters
    instance.num_voters

Finally, `PrefLibInstance` also provide the basic functions to write the instance.

.. code-block:: python

    instance.write(path_to_the_file)

As said before, `PrefLibInstance` is an abstract class, so all the actual stuff only happens in what comes next.