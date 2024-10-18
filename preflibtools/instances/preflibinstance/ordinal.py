import re
from collections.abc import Iterable
from copy import deepcopy
from os import path

from preflibtools.instances.preflibinstance.instance import PrefLibInstance
from preflibtools.instances.sampling import (
    generate_IC_anon,
    generate_urn,
    generate_mallows,
    generate_mallows_mix,
    generate_IC,
)


class OrdinalInstance(PrefLibInstance):
    """This is the class representing a PrefLib instance of ordinal preferences. It basically contains the data and
    information written within a PrefLib file.

    :param file_path: The path to the file the instance is taken from. If a path is provided as a parameter,
        the file is immediately parsed and the instance populated accordingly.
    :type file_path: str, optional

    :ivar num_unique_orders: The number of unique orders in the instance.
    :ivar multiplicity: A dictionary mapping each order to the number of voters who submitted that order.
    :ivar orders: The list of all the distinct orders in the instance.
    :ivar preferences: A pointer to the orders attribute so that it can be accessed both ways.
    """

    def __init__(self, file_path=""):
        PrefLibInstance.__init__(self)
        self.file_path = file_path
        self.num_unique_orders = 0
        self.multiplicity = {}
        self.orders = []
        self.preferences = self.orders
        self.data_type = "toi"

        # If a filePath is given as argument, we parse it immediately
        if len(file_path) > 0:
            self.parse_file(file_path)

    def type_validator(self, data_type):
        return data_type in ["soc", "soi", "toc", "toi"]

    def parse(self, lines, autocorrect=False, header_only=False):
        """Parses the strings provided as argument, assuming that the latter describes an order.

        :param lines: A list of string, each string being one line of the instance to parse.
        :type lines: list
        :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
        :type autocorrect: bool
        :param header_only: A boolean indicating whether we should stop after having read the header. Default is False.
        :type header_only: bool
        """

        # The first few lines contain the metadata
        i = 0
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith("#"):
                if line.startswith("# NUMBER UNIQUE ORDERS"):
                    self.num_unique_orders = int(line[23:].strip())
                else:
                    self.parse_metadata(line, autocorrect=autocorrect)
            else:
                break

        if header_only:
            return

        # The rest of the lines are about the preferences
        order_pattern = re.compile(r"\{[\d,]+?\}|[\d,]+")
        for line in lines[i:]:
            line = "".join(line.split())
            if len(line) > 0:
                # The first element indicates the multiplicity of the order
                multiplicity, order_str = line.strip().split(":")
                multiplicity = int(multiplicity.strip())
                order = []
                for group in re.findall(order_pattern, order_str):
                    if group.startswith("{"):
                        group = group[1:-1]
                        order.append(
                            tuple(
                                int(alt.strip())
                                for alt in group.split(",")
                                if len(alt) > 0
                            )
                        )
                    else:
                        for alt in group.split(","):
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
        """Parses the strings provided as argument, assuming that the latter describes an order, in the old PrefLib
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
        for line in lines[self.num_alternatives + 2 :]:
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
                        indif_class.append(
                            int(w[1:])
                        )  # The first element of w is {, so we go beyond that
                    # If we finished reading a series of ties (grouped by {})
                    elif w.endswith("}"):
                        in_braces = False
                        indif_class.append(
                            int(w[:-1])
                        )  # The first element of w is }, so we go beyond that
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
        """Writes the instance into a file whose destination has been given as argument. If no file extension is
        provided the data type of the instance is used.

        Also sets `self.file_name` correctly (according to `filepath`), if `self.file_name` is empty.

        :param filepath: The destination where to write the instance.
        :type filepath: str
        """
        if len(path.splitext(filepath)[1]) == 0:
            filepath += "." + str(self.data_type)
        # set self.filename if it is undefined
        if not self.file_name:
            self.set_file_name(filepath)
        with open(filepath, "w", encoding="utf-8") as file:
            # Writing metadata in the file header
            self.write_metadata(file)
            file.write(
                "# NUMBER ALTERNATIVES: {}\n# NUMBER VOTERS: {}\n# NUMBER UNIQUE ORDERS: {}\n".format(
                    self.num_alternatives, self.num_voters, self.num_unique_orders
                )
            )
            for alt, name in self.alternatives_name.items():
                file.write("# ALTERNATIVE NAME {}: {}\n".format(alt, name))
            # Writing the actual ballots with their multiplicity
            orders = deepcopy(self.orders)
            orders.sort(key=lambda o: (-self.multiplicity[o], -len(o)))
            for order in orders:
                order_str = ""
                for indif_class in order:
                    if len(indif_class) == 1:
                        order_str += str(indif_class[0]) + ", "
                    else:
                        order_str += (
                            "{" + ", ".join((str(alt) for alt in indif_class)) + "}, "
                        )
                file.write(
                    "{}: {}\n".format(self.multiplicity[order], order_str.strip(", "))
                )

    def vote_map(self):
        """Returns the instance described as a vote map, i.e., a dictionary whose keys are orders, mapping
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
        """Returns a list containing all the orders appearing in the preferences, with each order appearing as
        many times as their multiplicity.

        :return: A list of preferences (lists of alternatives).
        :rtype: list
        """
        res = []
        for order in self.orders:
            res += [order] * self.multiplicity[order]
        return res

    def flatten_strict(self):
        """Strict orders are represented as orders with indifference classes of size 1. This is somewhat heavy when
        working with strict preferences. This function flattens strict preferences by removing the indifference
        class.

        :return: A list of tuples of preference order and multiplicity.
        :rtype: list
        """
        res = []
        for order in self.orders:
            if len(order) != self.num_alternatives:
                print("WARNING: You are flattening a non-strict order.")
            res.append(
                (
                    tuple(indif_class[0] for indif_class in order),
                    self.multiplicity[order],
                )
            )
        return res

    def infer_type(self):
        """Loops through the orders of the instance to infer whether the preferences strict and/or complete,.

        :return: The data type of the instance.
        :rtype: str
        """
        strict = True
        complete = True
        for order in self.orders:
            if max(len(indif_class) for indif_class in order) != 1:
                strict = False
            if (
                len([alt for indif_class in order for alt in indif_class])
                != self.num_alternatives
            ):
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
        """Recomputes the basic cardinality parameters based on the order list in the instance. Numbers that are
        recomputed are the number of voters and the number of unique orders.
        """
        num_voters = 0
        for order in self.orders:
            num_voters += self.multiplicity[order]
        self.num_voters = num_voters
        self.num_unique_orders = len(set(self.orders))

    def append_order(self, order):
        """Appends an order to the instance. That function incorporates the new order
        into the instance and updates the set of alternatives if needed.

        :param order: An order.
        :type order: Iterable
        """
        for alt in order:
            if alt not in self.alternatives_name:
                self.alternatives_name[alt] = "Alternative " + str(alt)
        self.num_alternatives = len(self.alternatives_name)

        self.num_voters += 1

        order = tuple((a,) for a in order)
        if order in self.multiplicity:
            self.multiplicity[order] += 1
        else:
            self.orders.append(order)
            self.multiplicity[order] = 1
            self.num_unique_orders += 1

        self.data_type = self.infer_type()

    def append_order_array(self, orders):
        """Appends an array of orders to the instance. That function incorporates the new orders
        into the instance and updates the set of alternatives if needed.

        :param orders: A 2D numpy array where each row represents a preference order.
        :type orders: np.ndarray
        """
        alternatives = set(alt for order in orders for alt in order)
        for alt in alternatives:
            if alt not in self.alternatives_name:
                self.alternatives_name[alt] = "Alternative " + str(alt)
        self.num_alternatives = len(self.alternatives_name)

        self.num_voters += len(orders)

        for order in orders:
            order = tuple((a,) for a in order)
            if order in self.multiplicity:
                self.multiplicity[order] += 1
            else:
                self.orders.append(order)
                self.multiplicity[order] = 1
                self.num_unique_orders += 1

        self.data_type = self.infer_type()

    def append_order_list(self, orders):
        """Appends a list of orders to the instance. That function incorporates the new orders into
        the instance and updates the set of alternatives if needed.

        :param orders: A list of tuples of tuples, each tuple representing a preference order.
        :type orders: list
        """
        alternatives = set(
            alt for order in orders for indif_class in order for alt in indif_class
        )
        for alt in alternatives:
            if alt not in self.alternatives_name:
                self.alternatives_name[alt] = "Alternative " + str(alt)
        self.num_alternatives = len(self.alternatives_name)

        self.num_voters += len(orders)

        for order in orders:
            order = tuple(tuple(a) if isinstance(a, Iterable) else (a,) for a in order)
            if order in self.multiplicity:
                self.multiplicity[order] += 1
            else:
                self.orders.append(deepcopy(order))
                self.multiplicity[order] = 1
                self.num_unique_orders += 1

        self.data_type = self.infer_type()

    def append_vote_map(self, vote_map):
        """Appends a vote map to the instance. That function incorporates the new orders into the instance and
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
        """Populates the instance with a random profile of strict preferences taken from the impartial culture
        distribution. Uses :math:`preflibtools.instances.sampling.urnModel` for sampling.

        :param num_voters: Number of orders to sample.
        :type num_voters: int
        :param num_alternatives: Number of alternatives for the sampled orders.
        :type num_alternatives: int
        """
        self.append_vote_map(generate_IC(num_voters, num_alternatives))

    def populate_IC_anon(self, num_voters, num_alternatives):
        """Populates the instance with a random profile of strict preferences taken from the impartial anonymous
        culture distribution. Uses :class:`preflibtools.instances.sampling` for sampling.

        :param num_voters: Number of orders to sample.
        :type num_voters: int
        :param num_alternatives: Number of alternatives for the sampled orders.
        :type num_alternatives: int
        """
        self.append_vote_map(generate_IC_anon(num_voters, num_alternatives))

    def populate_urn(self, num_voters, num_alternatives, replace):
        """Populates the instance with a random profile of strict preferences taken from the urn distribution.
        Uses :class:`preflibtools.instances.sampling` for sampling.

        :param num_voters: Number of orders to sample.
        :type num_voters: int
        :param num_alternatives: Number of alternatives for the sampled orders.
        :type num_alternatives: int
        :param replace: The number of replacements for the urn model.
        :type replace: int
        """
        self.append_vote_map(generate_urn(num_voters, num_alternatives, replace))

    def populate_mallows(
        self, num_voters, num_alternatives, mixture, dispersions, references
    ):
        """Populates the instance with a random profile of strict preferences taken from a mixture of Mallows'
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
        self.append_vote_map(
            generate_mallows(
                num_voters, num_alternatives, mixture, dispersions, references
            )
        )

    def populate_mallows_mix(self, num_voters, num_alternatives, num_references):
        """Populates the instance with a random profile of strict preferences taken from a mixture of Mallows'
        models for which reference points and dispersion coefficients are independently and identically
        distributed. Uses :class:`preflibtools.instances.sampling` for sampling.

        :param num_voters: Number of orders to sample.
        :type num_voters: int
        :param num_alternatives: Number of alternatives for the sampled orders.
        :type num_alternatives: int
        :param num_references: Number of element
        :type num_references: int
        """
        self.append_vote_map(
            generate_mallows_mix(num_voters, num_alternatives, num_references)
        )

    def __str__(self):
        return "Ordinal-Instance: {} <{},{}>".format(
            self.file_name, self.num_voters, self.num_alternatives
        )

