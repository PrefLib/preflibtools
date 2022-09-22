""" This module describes the main class to deal with PrefLib instances..
"""
import os.path

from .sampling import *

from copy import deepcopy
from os import path

import urllib.request
import re


class PrefLibInstance(object):
    """ This class provide a general template to implement specific classes representing PrefLib instances. It should
        mainly be used as an abstract class.

        :ivar file_path: The path to the file the instance is taken from.
        :ivar file_name: The name of the file the instance is taken from.
        :ivar data_type: The data type of the instance. Whenever a function only applies to certain types of data
            (strict and complete orders for instance), we do so by checking this value.
        :ivar modification_type: The modification type of the file: original if it represents original data; induced
            or imbued it is derived from some other data; synthetic if it is synthetically generated.
        :ivar relates_to: The data file this instance relates to, typically the original data file for induced
            preferences.
        :ivar related_files: The data files that are to the instance.
        :ivar title: The title of the instance.
        :ivar description: A description of the instance.
        :ivar publication_date: Date at which the corresponding file has been added to PrefLib.com.
        :ivar modification_date: Last date the  file has been modified on PrefLib.com.
        :ivar num_alternatives: The number of alternatives in the instance.
        :ivar alternatives_name: A dictionary mapping alternative (int) to their name (str).
        :ivar num_voters: The number of voters in the instance.
    """

    def __init__(self):
        self.file_path = ""
        self.file_name = ""
        self.data_type = ""
        self.modification_type = ""
        self.relates_to = ""
        self.related_files = ""
        self.title = ""
        self.description = ""
        self.publication_date = ""
        self.modification_date = ""
        self.num_alternatives = 0
        self.alternatives_name = {}
        self.num_voters = 0
        self.alt_name_pattern = re.compile(r'# ALTERNATIVE NAME (\d+): (.*)')

    def type_validator(self, data_type):
        """ Returns a boolean indicating whether the data_type given as argument is a valid one for the python class.

            :param data_type: A strong representing a data type.
            :type data_type: str
            :return: True if the data type is valid for the class and False otherwise.
            :rtype: bool
        """
        pass

    def parse(self, lines, autocorrect=False):
        pass

    def parse_lines(self, lines, autocorrect=False):
        """ Parses the lines provided as argument. The parser to be used is deducted from the instance's inner value of
            data_type.

            :param lines: A list of string, each string being one line of the instance to parse.
            :type lines: list
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """

        if self.type_validator(self.data_type):
            self.parse(lines, autocorrect=autocorrect)
        else:
            raise TypeError("File extension " + str(self.data_type) + " is not valid for this type of PrefLib " +
                            "instance. This file cannot be parsed.")

    def parse_file(self, filepath, autocorrect=False):
        """ Parses the file whose path is provided as argument and populates the PreflibInstance object accordingly.
            The parser to be used is deduced from the file extension.

            :param filepath: The path to the file to be parsed.
            :type filepath: str
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """

        # Populating basic properties of the instance
        self.file_path = filepath
        self.file_name = path.split(filepath)[1]
        self.data_type = path.splitext(filepath)[1][1:]

        # Read the file
        file = open(filepath, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        self.parse_lines(lines, autocorrect=autocorrect)

    def parse_str(self, string, data_type, file_name="", autocorrect=False):
        """ Parses the string provided as argument and populates the PreflibInstance object accordingly.
            The parser to be used is deduced from the file extension passed as argument.

            :param string: The string to parse.
            :type string: str
            :param data_type: The data type represented by the string.
            :type data_type: str
            :param file_name: The value to store in the file_name member of the instance. Default is the empty string.
            :type file_name: str
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """

        self.file_path = "parsed_from_string"
        self.file_name = file_name
        self.data_type = data_type

        self.parse_lines(string.splitlines(), autocorrect=autocorrect)

    def parse_url(self, url, autocorrect=False):
        """ Parses the file located at the provided URL and populates the PreflibInstance object accordingly.
            The parser to be used (whether the file describes a graph or an order for instance) is deduced based
            on the file extension.

            :param url: The target URL.
            :type url: str
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """

        data = urllib.request.urlopen(url)
        lines = [line.decode("utf-8").strip() for line in data]
        data.close()

        self.file_path = url
        self.file_name = url.split('/')[-1].split('.')[0]
        self.data_type = url.split('.')[-1]

        self.parse_lines(lines, autocorrect=autocorrect)

    def parse_metadata(self, line, autocorrect=False):
        """ A helper function that parses metadata.

            :param line: The line to parse.
            :type line: str
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """
        if line.startswith("# FILE NAME"):
            self.file_name = line[12:].strip()
        elif line.startswith("# TITLE"):
            self.title = line[8:].strip()
        elif line.startswith("# DESCRIPTION"):
            self.description = line[14:].strip()
        elif line.startswith("# DATA TYPE"):
            self.data_type = line[12:].strip()
        elif line.startswith("# MODIFICATION TYPE"):
            self.modification_type = line[20:].strip()
        elif line.startswith("# RELATES TO"):
            self.relates_to = line[13:].strip()
        elif line.startswith("# RELATED FILES"):
            self.related_files = line[16:].strip()
        elif line.startswith("# PUBLICATION DATE"):
            self.publication_date = line[19:].strip()
        elif line.startswith("# MODIFICATION DATE"):
            self.modification_date = line[20:].strip()
        elif line.startswith("# NUMBER ALTERNATIVES"):
            self.num_alternatives = int(line[22:].strip())
        elif line.startswith("# NUMBER VOTERS"):
            self.num_voters = int(line[16:].strip())
        elif line.startswith("# ALTERNATIVE NAME"):
            match = re.match(self.alt_name_pattern, line)
            if match:
                alt = int(match.group(1))
                alt_name = match.group(2)
                if autocorrect and alt_name in self.alternatives_name.values():
                    tmp = 1
                    while alt_name + "__" + str(tmp) in self.alternatives_name.values():
                        tmp += 1
                    self.alternatives_name[alt] = alt_name + "__" + str(tmp)
                else:
                    self.alternatives_name[alt] = alt_name

    def write(self, filepath):
        pass

    def write_metadata(self, file):
        """ A helper function that writes the metadata in the file.

            :param file: The file to write into as a file object.

        """
        file.write("# FILE NAME: {}\n# TITLE: {}\n# DESCRIPTION: {}\n# DATA TYPE: {}\n# MODIFICATION TYPE: {}\n".format(
            self.file_name, self.title, self.description, self.data_type, self.modification_type))
        file.write("# RELATES TO: {}\n# RELATED FILES: {}\n# PUBLICATION DATE: {}\n# MODIFICATION DATE: {}\n".format(
            self.relates_to, self.related_files, self.publication_date, self.modification_date))

    def __str__(self):
        return "PrefLib-Instance: {} <{},{}>".format(self.file_name, self.num_voters, self.num_alternatives)


class OrdinalInstance(PrefLibInstance):
    """ This is the class representing a PrefLib instance of ordinal preferences. It basically contains the data and
        information written within a PrefLib file.

        :param file_path: The path to the file the instance is taken from. If a path is provided as a parameter,
            the file is immediately parsed and the instance populated accordingly.
        :type file_path: str, optional

        :ivar num_unique_orders: The number of unique orders in the instance.
        :ivar multiplicity: A dictionary mapping each order to the number of voters who submitted that order.
        :ivar orders: The list of all the distinct orders in the instance.
    """

    def __init__(self, file_path=""):
        PrefLibInstance.__init__(self)
        self.file_path = file_path
        self.num_unique_orders = 0
        self.multiplicity = {}
        self.orders = []

        # If a filePath is given as argument, we parse it immediately
        if len(file_path) > 0:
            self.parse_file(file_path)

    def type_validator(self, data_type):
        return data_type in ['soc', 'soi', 'toc', 'toi']

    def parse(self, lines, autocorrect=False):
        """ Parses the strings provided as argument, assuming that the latter describes an order.

            :param lines: A list of string, each string being one line of the instance to parse.
            :type lines: list
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """

        # The first few lines contain the metadata
        i = 0
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('#'):
                if line.startswith("# NUMBER UNIQUE ORDERS"):
                    self.num_unique_orders = int(line[23:].strip())
                else:
                    self.parse_metadata(line, autocorrect=autocorrect)
            else:
                break

        # The rest of the lines are about the preferences
        order_pattern = re.compile(r'{[\d,]+?}|[\d,]+')
        for line in lines[i:]:
            # The first element indicates the multiplicity of the order
            multiplicity, order_str = line.strip().split(":")
            multiplicity = int(multiplicity)
            order = []
            for group in re.findall(order_pattern, order_str):
                if group.startswith('{'):
                    group = group[1:-1]
                    order.append(tuple(int(alt.strip()) for alt in group.split(',') if len(alt) > 0))
                else:
                    for alt in group.split(','):
                        if len(alt) > 0:
                            order.append((int(alt.strip()),))
            order = tuple(order)
            if autocorrect and order in self.multiplicity:
                self.multiplicity[tuple(order)] += multiplicity
            else:
                self.orders.append(order)
                self.multiplicity[tuple(order)] = multiplicity

        if autocorrect:
            self.num_alternatives = len(self.alternatives_name)
            self.num_unique_orders = len(self.orders)
            self.num_voters = sum(self.multiplicity.values())

    def parse_old(self, lines, autocorrect=False):
        """ Parses the strings provided as argument, assuming that the latter describes an order, in the old PrefLib
            format.

            :param lines: A list of string, each string being one line of the instance to parse.
            :type lines: list
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """

        # The first line gives us the number of alternatives, then comes the names of the alternatives
        self.num_alternatives = int(lines[0])
        for i in range(1, self.num_alternatives + 1):
            alt_name = lines[i].split(",")[1].strip()
            if autocorrect and alt_name in self.alternatives_name.values():
                tmp = 1
                while alt_name + "__" + str(tmp) in self.alternatives_name.values():
                    tmp += 1
                self.alternatives_name[i] = alt_name + "__" + str(tmp)
            else:
                self.alternatives_name[i] = alt_name

        # We've reached the description of the preferences. We start by some numbers...
        self.num_voters = int(lines[self.num_alternatives + 1].split(",")[0])
        self.num_unique_orders = int(lines[self.num_alternatives + 1].split(",")[2])

        # ... and finally comes the preferences
        for line in lines[self.num_alternatives + 2:]:
            # The first element indicates the multiplicity of the order
            elements = line.strip().split(",")
            multiplicity = int(elements[0])

            # Then we deal with the rest
            in_braces = False
            order = []
            indif_class = []
            for w in elements[1:]:
                # If there is something in w
                if w != "{}" and len(w) > 0:
                    # If we are entering a series of ties (grouped by {})
                    if w.startswith("{"):
                        # If w also ends with a }, we remove it
                        if w.endswith("}"):
                            w = w[:-1]
                        in_braces = True
                        indif_class.append(int(w[1:]))  # The first element of w is {, so we go beyond that
                    # If we finished reading a series of ties (grouped by {})
                    elif w.endswith("}"):
                        in_braces = False
                        indif_class.append(int(w[:-1]))  # The first element of w is }, so we go beyond that
                        order.append(tuple(indif_class))
                        indif_class = []
                    # Otherwise, we are just reading numbers
                    else:
                        # If we are facing ties, we add in the indifference class
                        if in_braces:
                            if int(w) not in indif_class:
                                indif_class.append(int(w))
                        # Otherwise, we add the strict preference.
                        else:
                            if (int(w),) not in order:
                                order.append((int(w),))
            order = tuple(order)
            if autocorrect and order in self.multiplicity:
                self.multiplicity[tuple(order)] += multiplicity
            else:
                self.orders.append(order)
                self.multiplicity[tuple(order)] = multiplicity

    def write(self, filepath):
        """ Writes the instance into a file whose destination has been given as argument. If no file extension is
        provided the data type of the instance is used.

            :param filepath: The destination where to write the instance.
            :type filepath: str
        """
        if len(path.splitext(filepath)[1]) == 0:
            filepath += "." + str(self.data_type)
        file = open(filepath, "w", encoding="utf-8")
        # Writing metadata in the file header
        self.write_metadata(file)
        file.write("# NUMBER ALTERNATIVES: {}\n# NUMBER VOTERS: {}\n# NUMBER UNIQUE ORDERS: {}\n".format(
            self.num_alternatives, self.num_voters, self.num_unique_orders
        ))
        for alt, name in self.alternatives_name.items():
            file.write("# ALTERNATIVE NAME {}: {}\n".format(alt, name))
        # Writing the actual ballots with their multiplicity
        orders = deepcopy(self.orders)
        orders.sort(key=lambda o: (-self.multiplicity[o], -len(o)))
        for order in orders:
            order_str = ""
            for indif_class in order:
                if len(indif_class) == 1:
                    order_str += str(indif_class[0]) + ","
                else:
                    order_str += "{" + ",".join((str(alt) for alt in indif_class)) + "},"
            file.write("{}: {}\n".format(self.multiplicity[order], order_str[:-1]))
        file.close()

    def vote_map(self):
        """ Returns the instance described as a vote map, i.e., a dictionary whose keys are orders, mapping
            to the number of voters with the given order as their preferences. This format can be useful for some
            applications. It also ensures interoperability with the old preflibtools (vote maps were the main object).

            :return: A vote map representing the preferences in the instance.
            :rtype: dict of (tuples, int)
        """
        vote_map = {}
        for order in self.orders:
            vote_map[order] = self.multiplicity[order]
        return vote_map

    def full_profile(self):
        """ Returns a list containing all the orders appearing in the preferences, with each order appearing as
            many times as their multiplicity.

            :return: A list of preferences (lists of alternatives).
            :rtype: list
        """
        res = []
        for order in self.orders:
            res += [order] * self.multiplicity[order]
        return res

    def flatten_strict(self):
        """ Strict orders are represented as orders with indifference classes of size 1. This is somewhat heavy when
            working with strict preferences. This function flattens strict preferences by removing the indifference
            class.

            :return: A list of tuples of preference order and multiplicity.
            :rtype: list
        """
        res = []
        for order in self.orders:
            if len(order) != self.num_alternatives:
                print("WARNING: You are flattening a non-strict order.")
            res.append((tuple(indif_class[0] for indif_class in order), self.multiplicity[order]))
        return res

    def infer_type(self):
        """ Loops through the orders of the instance to infer whether the preferences strict and/or complete,.

            :return: The data type of the instance.
            :rtype: str 
        """
        strict = True
        complete = True
        for order in self.orders:
            if max(len(indif_class) for indif_class in order) != 1:
                strict = False
            if len([alt for indif_class in order for alt in indif_class]) != self.num_alternatives:
                complete = False
            if not strict and not complete:
                return "toi"
        if strict and complete:
            return "soc"
        if strict and not complete:
            return "soi"
        if not strict and complete:
            return "toc"

    def recompute_cardinality_param(self):
        """ Recomputes the basic cardinality parameters based on the order list in the instance. Numbers that are
            recomputed are the number of voters and the number of unique orders.
        """
        num_voters = 0
        for order in self.orders:
            num_voters += self.multiplicity[order]
        self.num_voters = num_voters
        self.num_unique_orders = len(set(self.orders))

    def append_order_list(self, orders):
        """ Appends a vote map to the instance. That function incorporates the new orders into the instance and
            updates the set of alternatives if needed.

            :param orders: A list of tuples of tuples, each tuple representing a preference order. 
            :type orders: list
        """
        alternatives = set(alt for order in orders for indif_class in order for alt in indif_class)
        for alt in alternatives:
            if alt not in self.alternatives_name:
                self.alternatives_name[alt] = "Alternative " + str(alt)
        self.num_alternatives = len(self.alternatives_name)

        self.num_voters += len(orders)

        for order in orders:
            if order in self.multiplicity:
                self.multiplicity[order] += 1
            else:
                self.orders.append(deepcopy(order))
                self.multiplicity[order] = 1
                self.num_unique_orders += 1

        self.data_type = self.infer_type()

    def append_vote_map(self, vote_map):
        """ Appends a vote map to the instance. That function incorporates the new orders into the instance and
            updates the set of alternatives if needed.
            
            :param vote_map: A vote map representing preferences. A vote map is a dictionary whose keys represent
                orders (tuples of tuples of int) that are mapped to the number of voters with the given order as 
                their preferences. We re-map the orders to tuple of tuples to be sure we are dealing with the correct
                type.
            :type vote_map: dict of (tuple, int)
        """
        for ballot, multiplicity in vote_map.items():
            order = tuple(tuple(indif_class) for indif_class in ballot)
            if order not in self.orders:
                self.orders.append(order)
                self.multiplicity[order] = multiplicity
            else:
                self.multiplicity[order] += multiplicity
            self.num_voters += multiplicity

            for indif_class in ballot:
                for alt in indif_class:
                    if alt not in self.alternatives_name:
                        self.alternatives_name[alt] = "Alternative " + str(alt)

        self.num_alternatives = len(self.alternatives_name)
        self.num_unique_orders = len(self.multiplicity)

        self.data_type = self.infer_type()

    def populate_IC(self, num_voters, num_alternatives):
        """ Populates the instance with a random profile of strict preferences taken from the impartial culture
            distribution. Uses :math:`preflibtools.instances.sampling.urnModel` for sampling.

            :param num_voters: Number of orders to sample.
            :type num_voters: int
            :param num_alternatives: Number of alternatives for the sampled orders.
            :type num_alternatives: int
        """
        self.append_vote_map(generate_IC(num_voters, list(range(num_alternatives))))

    def populate_IC_anon(self, num_voters, num_alternatives):
        """ Populates the instance with a random profile of strict preferences taken from the impartial anonymous
            culture distribution. Uses :class:`preflibtools.instances.sampling` for sampling.

            :param num_voters: Number of orders to sample.
            :type num_voters: int
            :param num_alternatives: Number of alternatives for the sampled orders.
            :type num_alternatives: int
        """
        self.append_vote_map(generate_IC_anon(num_voters, list(range(num_alternatives))))

    def populate_urn(self, num_voters, num_alternatives, replace):
        """ Populates the instance with a random profile of strict preferences taken from the urn distribution.
            Uses :class:`preflibtools.instances.sampling` for sampling.

            :param num_voters: Number of orders to sample.
            :type num_voters: int
            :param num_alternatives: Number of alternatives for the sampled orders.
            :type num_alternatives: int
            :param replace: The number of replacements for the urn model.
            :type replace: int
        """
        self.append_vote_map(generate_urn(num_voters, list(range(num_alternatives)), replace))

    def populate_mallows(self, num_voters, num_alternatives, mixture, dispersions, references):
        """ Populates the instance with a random profile of strict preferences taken from a mixture of Mallows'
            models. Uses :class:`preflibtools.instances.sampling` for sampling.

            :param num_voters: Number of orders to sample.
            :type num_voters: int
            :param num_alternatives: Number of alternatives for the sampled orders.
            :type num_alternatives: int
            :param mixture: A list of the weights of each element of the mixture.
            :type mixture: list of positive numbers
            :param dispersions: A list of the dispersion coefficient of each element of the mixture.
            :type dispersions: list of float
            :param references: A list of the reference orders for each element of the mixture.
            :type references: list of tuples of tuples of int
        """
        self.append_vote_map(generate_mallows(num_voters, num_alternatives, mixture, dispersions, references))

    def populate_mallows_mix(self, num_voters, num_alternatives, num_references):
        """ Populates the instance with a random profile of strict preferences taken from a mixture of Mallows'
            models for which reference points and dispersion coefficients are independently and identically 
            distributed. Uses :class:`preflibtools.instances.sampling` for sampling.

            :param num_voters: Number of orders to sample.
            :type num_voters: int
            :param num_alternatives: Number of alternatives for the sampled orders.
            :type num_alternatives: int
            :param num_references: Number of element
            :type num_references: int
        """
        self.append_vote_map(generate_mallows_mix(num_voters, list(range(num_alternatives)), num_references))

    def __str__(self):
        return "Ordinal-Instance: {} <{},{}>".format(self.file_name, self.num_voters, self.num_alternatives)

class ComparisonInstance(PrefLibInstance):
    """ To be implemented.

    """

    def __init__(self):
        PrefLibInstance.__init__(self)


class CategoricalInstance(PrefLibInstance):
    """ This is the class representing a PrefLib instance of categorical preferences. It basically contains the data and
        information written within a PrefLib file.
    """

    def __init__(self, file_path=""):
        PrefLibInstance.__init__(self)
        self.file_path = file_path
        self.num_unique_preferences = 0
        self.multiplicity = {}
        self.num_categories = 0
        self.categories_name = {}
        self.preferences = []

        # If a filePath is given as argument, we parse it immediately
        if len(file_path) > 0:
            self.parse_file(file_path)

    def type_validator(self, data_type):
        return data_type == "cat"

    def parse(self, lines, autocorrect=False):
        """ Parses the strings provided as argument, assuming that the latter describes categorical preferences.

            :param lines: A list of string, each string being one line of the instance to parse.
            :type lines: list
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """

        # The first few lines contain the metadata
        i = 0
        cat_name_pattern = re.compile(r'# CATEGORY NAME (\d+): (.*)')
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('#'):
                if line.startswith("# NUMBER UNIQUE PREFERENCES"):
                    self.num_unique_preferences = int(line[28:].strip())
                if line.startswith("# NUMBER CATEGORIES"):
                    self.num_categories = int(line[20:].strip())
                elif line.startswith("# CATEGORY NAME"):
                    match = re.match(cat_name_pattern, line)
                    if match:
                        cat = int(match.group(1))
                        cat_name = match.group(2)
                        if autocorrect and cat_name in self.categories_name.values():
                            tmp = 1
                            while cat_name + "__" + str(tmp) in self.categories_name.values():
                                tmp += 1
                            self.categories_name[cat] = cat_name + "__" + str(tmp)
                        else:
                            self.categories_name[cat] = cat_name
                else:
                    self.parse_metadata(line, autocorrect=autocorrect)
            else:
                break

        # The rest of the lines are about the preferences
        pref_pattern = re.compile(r'{[\d,]+?}|[\d,]+|{}')
        for line in lines[i:]:
            # The first element indicates the multiplicity of the order
            multiplicity, pref_str = line.strip().split(":")
            multiplicity = int(multiplicity)
            pref = []
            for group in re.findall(pref_pattern, pref_str):
                if group == '{}':
                    pref.append(tuple())
                elif group.startswith('{'):
                    group = group[1:-1]
                    pref.append(tuple(int(alt.strip()) for alt in group.split(',') if len(alt) > 0))
                else:
                    for alt in group.split(','):
                        if len(alt) > 0:
                            pref.append((int(alt.strip()),))
            pref = tuple(pref)
            if autocorrect and pref in self.multiplicity:
                self.multiplicity[tuple(pref)] += multiplicity
            else:
                self.preferences.append(pref)
                self.multiplicity[tuple(pref)] = multiplicity

        if autocorrect:
            self.num_alternatives = len(self.alternatives_name)
            self.num_unique_preferences = len(self.preferences)
            self.num_voters = sum(self.multiplicity.values())

    def write(self, filepath):
        """ Writes the instance into a file whose destination has been given as argument. If no file extension is
        provided the data type of the instance is used.

            :param filepath: The destination where to write the instance.
            :type filepath: str
        """
        if len(path.splitext(filepath)[1]) == 0:
            filepath += "." + str(self.data_type)
        file = open(filepath, "w", encoding="utf-8")
        # Writing metadata in the file header
        self.write_metadata(file)
        file.write("# NUMBER ALTERNATIVES: {}\n# NUMBER VOTERS: {}\n# NUMBER UNIQUE PREFERENCES: {}\n".format(
            self.num_alternatives, self.num_voters, self.num_unique_preferences
        ))
        file.write("# NUMBER CATEGORIES: {}\n".format(self.num_categories))
        for cat, name in self.categories_name.items():
            file.write("# CATEGORY NAME {}: {}\n".format(cat, name))
        for alt, name in self.alternatives_name.items():
            file.write("# ALTERNATIVE NAME {}: {}\n".format(alt, name))
        # Writing the actual ballots with their multiplicity
        preferences = deepcopy(self.preferences)
        preferences.sort(key=lambda o: (-self.multiplicity[o], -len(o)))
        for pref in preferences:
            pref_str = ""
            for category in pref:
                if len(category) == 0:
                    pref_str += '{},'
                elif len(category) == 1:
                    pref_str += str(category[0]) + ","
                else:
                    pref_str += "{" + ",".join((str(alt) for alt in category)) + "},"
            file.write("{}: {}\n".format(self.multiplicity[pref], pref_str[:-1]))
        file.close()

    def __str__(self):
        return "Categorical-Instance: {} <{},{}>".format(self.file_name, self.num_voters, self.num_alternatives)


class WeightedDiGraph(object):
    """ This class is used to represent weighted directed graphs.

        :ivar dict: The dictionary representing the graph mapping each node to its neighbourhood (set of nodes
            to which it is connected). A node can be of any hashable type.
        :ivar weight: The dictionary mapping every node to its weight.
    """

    def __init__(self):
        self.node_mapping = dict()
        self.weights = dict()

    def neighbours(self, node):
        """ Returns all the neighbours of a given node.

            :param node: The node whose neighbours we want to know.

            :return: The set of the neighbours of the node.
            :rtype: set
        """
        return self.node_mapping[node]

    def outgoing_edges(self, node):
        """ Returns all the edges leaving a given node.

            :param node: The node whose edges we want to get.

            :return: The set of the tuples (node, neighbour, edgeWeight) representing (weighted) edges.
            :rtype: set of tuples
        """
        return {(node, n, self.weights[(node, n)]) for n in self.node_mapping[node]}

    def add_node(self, node):
        """ Adds a node to the graph if the node does not already exist.

            :param node: The node to add.
        """
        if node not in self.node_mapping:
            self.node_mapping[node] = set()

    def add_edge(self, node1, node2, weight):
        """ Adds an edge to the graph. If the nodes do not exist in the graph, those are also added.

            :param node1: The departure node of the edge.
            :param node2: The arrival node of the edge.
            :param weight: The weight of the edge.
        """
        self.add_node(node1)
        self.add_node(node2)
        self.node_mapping[node1].add(node2)
        self.weights[(node1, node2)] = weight

    def edges(self):
        """ Returns the set of all the edges of the graph.

            :return: A set of tuples (node, neighbour, weight) representing (weighted) edges.
            :rtype: set of tuples
        """
        return {(n1, n2, self.weights[(n1, n2)]) for n1 in self.node_mapping for n2 in self.node_mapping[n1]}

    def nodes(self):
        """ Returns the set of all the nodes of the graph.

            :return: The set of all the nodes of the graph.
            :rtype: set
        """
        return self.node_mapping.keys()

    def __str__(self):
        """ Returns the string used when printing the graph """
        return "Graph with {} vertices and {} edges :\n".format(len(self.node_mapping), len(self.edges()))


class MatchingInstance(PrefLibInstance, WeightedDiGraph):
    """ This is the class representing a PrefLib instance for matching preferences. It basically contains the data and
        information written within a PrefLib file.

    """

    def __init__(self, file_path = ""):
        PrefLibInstance.__init__(self)
        WeightedDiGraph.__init__(self)
        self.num_edges = 0
        self.file_path = file_path

        # If a filePath is given as argument, we parse it immediately
        if len(file_path) > 0:
            self.parse_file(file_path)

    def type_validator(self, data_type):
        return data_type == "wmd"

    def parse(self, lines, autocorrect=False):
        """ Parses the strings, assuming that the latter describes a graph.

            :param lines: A list of string, each string being one line of the instance to parse.
            :type lines: list
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """
        # The first few lines contain the metadata
        i = 0
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('#'):
                if line.startswith("# NUMBER EDGES"):
                    self.num_edges = int(line[15:].strip())
                else:
                    self.parse_metadata(line, autocorrect=autocorrect)
            else:
                break
        self.num_voters = self.num_alternatives

        for line in lines[i:]:
            (vertex1, vertex2, weight) = line.strip().split(",")
            self.add_edge(int(vertex1), int(vertex2), float(weight))
        self.num_edges = sum(len(edge_set) for edge_set in self.node_mapping.values())

    def parse_old(self, lines, autocorrect=False):
        """ Parses the strings, assuming that the latter describes a graph.

            :param lines: A list of string, each string being one line of the instance to parse.
            :type lines: list
            :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
            :type autocorrect: bool
        """

        self.num_alternatives = int(lines[0].strip().split(",")[0])
        self.num_voters = int(lines[0].strip().split(",")[1])
        for i in range(1, self.num_alternatives + 1):
            alt_name = lines[i].split(",")[1].strip()
            if autocorrect and alt_name in self.alternatives_name.values():
                tmp = 1
                while alt_name + "__" + str(tmp) in self.alternatives_name.values():
                    tmp += 1
                self.alternatives_name[i] = alt_name + "__" + str(tmp)
            else:
                self.alternatives_name[i] = alt_name

        # Skip the lines that describe the data
        graph_first_line = self.num_alternatives + 1
        for line in lines[graph_first_line:]:
            (vertex1, vertex2, weight) = line.strip().split(",")
            weight = float(weight)
            vertex1 = int(vertex1)
            vertex2 = int(vertex2)
            self.add_edge(vertex1, vertex2, weight)
        self.num_edges = sum(len(edge_set) for edge_set in self.node_mapping.values())

    def write(self, filepath):
        """ Writes the instance into a file whose destination has been given as argument, assuming the instance
            represents a graph. If no file extension is provided the data type of the instance is used.

            :param filepath: The destination where to write the instance.
            :type filepath: str
        """

        if len(path.splitext(filepath)[1]) == 0:
            filepath += "." + str(self.data_type)
        file = open(filepath, "w", encoding="utf-8")
        # Writing metadata in the file header
        self.write_metadata(file)
        file.write("# NUMBER ALTERNATIVES: {}\n# NUMBER EDGES: {}\n".format(
            self.num_alternatives, self.num_edges,
        ))
        for alt, name in self.alternatives_name.items():
            file.write("# ALTERNATIVE NAME {}: {}\n".format(alt, name))

        # Writing the actual graph
        nodes = sorted(list(self.nodes()))
        for n in nodes:
            out_edges = sorted(list(self.outgoing_edges(n)), key=lambda x: x[1])
            for (vertex1, vertex2, weight) in out_edges:
                file.write("{},{},{}\n".format(vertex1, vertex2, weight))
        file.close()

    def __str__(self):
        return "Matching-Instance: {} <{},{}>".format(self.file_name, self.num_voters, self.num_alternatives)


def get_parsed_instance(file_path):
    """ Infers from the extension of the file given as input the correct instance to use. Parses the file and return
        the instance.

        :param file_path: The path to the file to be parsed.
        :type file_path: str

        :return: The instance with the file already parsed.
        :rtype: :class:`preflibtools.instances.preflibinstance.PrefLibInstance`
    """
    extension = os.path.splitext(file_path)[1][1:]
    if extension in ["soc", "soi", "toc", "toi"]:
        return OrdinalInstance(file_path)
    elif extension == "cat":
        return CategoricalInstance(file_path)
    elif extension == "wmd":
        return MatchingInstance(file_path)
