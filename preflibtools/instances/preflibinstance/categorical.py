import re
from copy import deepcopy
from math import ceil
from os import path

from preflibtools.instances.preflibinstance.instance import PrefLibInstance


class CategoricalInstance(PrefLibInstance):
    """This is the class representing a PrefLib instance of categorical preferences. It basically contains the data and
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
        self.data_type = "cat"

        # If a filePath is given as argument, we parse it immediately
        if len(file_path) > 0:
            self.parse_file(file_path)

    def type_validator(self, data_type):
        return data_type == "cat"

    def parse(self, lines, autocorrect=False, header_only=False):
        """Parses the strings provided as argument, assuming that the latter describes categorical preferences.

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
        cat_name_pattern = re.compile(r"# CATEGORY NAME (\d+): (.*)")
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith("#"):
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
                            while (
                                cat_name + "__" + str(tmp)
                                in self.categories_name.values()
                            ):
                                tmp += 1
                            self.categories_name[cat] = cat_name + "__" + str(tmp)
                        else:
                            self.categories_name[cat] = cat_name
                else:
                    self.parse_metadata(line, autocorrect=autocorrect)
            else:
                break

        if header_only:
            return

        # The rest of the lines are about the preferences
        pref_pattern = re.compile(r"{[\d,]+?}|[\d,]+|{}")
        for line in lines[i:]:
            # The first element indicates the multiplicity of the order
            multiplicity, pref_str = line.strip().replace(" ", "").split(":")
            multiplicity = int(multiplicity)
            pref = []
            for group in re.findall(pref_pattern, pref_str):
                if group == "{}":
                    pref.append(tuple())
                elif group.startswith("{"):
                    group = group[1:-1]
                    pref.append(
                        tuple(
                            int(alt.strip()) for alt in group.split(",") if len(alt) > 0
                        )
                    )
                else:
                    for alt in group.split(","):
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
            self.recompute_cardinality_param()

    def factorise_instance(self, reset_multiplicity=False):
        """Factorises the instance, i.e., remove duplicated preferences and updates the
        multiplicity dictionary accordingly.
        """
        if reset_multiplicity:
            self.multiplicity = dict()
        new_pref_list = []
        for ballot in self.preferences:
            if ballot not in self.multiplicity:
                self.multiplicity[ballot] = 1
                new_pref_list.append(ballot)
            else:
                self.multiplicity[ballot] += 1
                if ballot not in new_pref_list:
                    new_pref_list.append(ballot)

    def recompute_cardinality_param(self):
        """Recomputes the basic cardinality parameters based on the preferences list in the
        instance. Numbers that are recomputed are the number of voters and the number of unique
        preferences.
        """
        self.num_voters = sum(self.multiplicity.values())
        self.num_unique_preferences = len(set(self.preferences))

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
                "# NUMBER ALTERNATIVES: {}\n# NUMBER VOTERS: {}\n# NUMBER UNIQUE PREFERENCES: {}\n".format(
                    self.num_alternatives, self.num_voters, self.num_unique_preferences
                )
            )
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
                        pref_str += "{}, "
                    elif len(category) == 1:
                        pref_str += str(category[0]) + ", "
                    else:
                        pref_str += (
                            "{" + ", ".join((str(alt) for alt in category)) + "}, "
                        )
                file.write(
                    "{}: {}\n".format(self.multiplicity[pref], pref_str.strip(", "))
                )

    @classmethod
    def from_ordinal(
        cls,
        instance,
        num_indif_classes=None,
        size_truncators=None,
        relative_size_truncators=None,
        category_name=None,
    ):
        """Converts an ordinal instance into a categorical one. The parameters `size_truncators` and
        `relative_size_truncators` determine where breaking points are.

        :param instance: The ordinal instance.
        :type instance: preflibtools.instances.preflibinstance.OrdinalInstance

        :param num_indif_classes: List of number of indifference classes. Each category will contain the union of the
            alternatives present in the specified number of positions of the ranking. If not all ranked alternative fit
            in the provided categories, and additional one will be created. This parameter cannot be used together with
            `size_truncators` and/or `relative_size_truncators`.

        :param size_truncators: List of truncation points. Each category will contain at least the truncation point
            number of alternatives. In case of ties, all tied alternatives are in the same category. If not all ranked
            alternative fit in the provided categories, and additional one will be created. This parameter cannot be
            used together with `num_indif_classes` and/or `relative_size_truncators`.
        :type size_truncators: list of int

        :param relative_size_truncators: List of truncation points expressed in relative terms with respect to the total
            number of alternatives ranked. The truncation points will thus differ for each order. All categories
            need to be described. In case the values do not add up to one, they are normalised. This parameter
            cannot be used together with `num_indif_classes` and/or `size_truncators`.
        :type relative_size_truncators: list of float

        :param category_name: List of category names.
        :type category_name: list of str
        """
        if (
            sum(
                (
                    num_indif_classes is None,
                    size_truncators is None,
                    relative_size_truncators is None,
                )
            )
            < 2
        ):
            raise ValueError(
                "You can only use one of the paramters 'num_indif_classes', 'size_truncators' and "
                "'relative_size_truncators'"
            )
        if (
            sum(
                (
                    num_indif_classes is None,
                    size_truncators is None,
                    relative_size_truncators is None,
                )
            )
            == 3
        ):
            raise ValueError(
                "You need to specify the value of at least one of theparamters 'num_indif_classes', "
                "'size_truncators' or 'relative_size_truncators'"
            )
        if relative_size_truncators and sum(relative_size_truncators) != 1:
            total = sum(relative_size_truncators)
            relative_size_truncators = [
                trunc / total for trunc in relative_size_truncators
            ]

        cat_instance = cls()
        cat_instance.file_path = instance.file_path
        cat_instance.file_name = instance.file_name
        cat_instance.data_type = "cat"
        cat_instance.modification_type = instance.modification_type
        cat_instance.relates_to = instance.relates_to
        cat_instance.related_files = instance.related_files
        cat_instance.title = instance.title
        cat_instance.description = instance.description
        cat_instance.publication_date = instance.publication_date
        cat_instance.modification_date = instance.modification_date
        cat_instance.num_alternatives = instance.num_alternatives
        cat_instance.alternatives_name = deepcopy(instance.alternatives_name)
        cat_instance.preferences = []

        preferences = []
        multiplicities = []
        for order, multiplicty in instance.multiplicity.items():
            pref = []
            if size_truncators or relative_size_truncators:
                if relative_size_truncators:
                    size_truncators = [
                        int(ceil(len(order) * truncation_point))
                        for truncation_point in relative_size_truncators
                    ]
                order_index = 0
                for truncation_point in size_truncators:
                    alts = []
                    while len(alts) < truncation_point and order_index < len(order):
                        alts.extend(order[order_index])
                        order_index += 1
                    pref.append(tuple(alts))
                    if order_index >= len(order):
                        break
                if order_index < len(order):
                    pref.append(
                        tuple(
                            a
                            for indif_class in order[order_index:]
                            for a in indif_class
                        )
                    )
            elif num_indif_classes:
                order_index = 0
                for num in num_indif_classes:
                    alts = []
                    for k in range(order_index, min(len(order), order_index + num)):
                        alts.extend(order[k])
                    order_index += num
                    pref.append(tuple(alts))
                if order_index < len(order):
                    pref.append(
                        tuple(
                            a
                            for indif_class in order[order_index:]
                            for a in indif_class
                        )
                    )
            preferences.append(pref)
            multiplicities.append(multiplicty)

        num_categories = max(len(pref) for pref in preferences)
        for index, preference in enumerate(preferences):
            while len(preference) < num_categories:
                preference.append(tuple())
            preference = tuple(preference)
            cat_instance.preferences.append(preference)
            cat_instance.multiplicity[preference] = multiplicities[index]

        cat_instance.num_categories = num_categories
        for k in range(num_categories):
            cat_instance.categories_name[str(k + 1)] = "Cat_" + str(k + 1)

        cat_instance.num_unique_preferences = len(cat_instance.preferences)
        cat_instance.recompute_cardinality_param()

        return cat_instance

    def __str__(self):
        return "Categorical-Instance: {} <{},{}>".format(
            self.file_name, self.num_voters, self.num_alternatives
        )

