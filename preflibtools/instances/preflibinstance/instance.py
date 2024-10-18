""" This module describes the main class to deal with PrefLib instances..
"""
import os.path
from os import path

import urllib.request
import re


class PrefLibInstance:
    """This class provide a general template to implement specific classes representing PrefLib
    instances. It should mainly be used as an abstract class.

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
        self.alt_name_pattern = re.compile(r"# ALTERNATIVE NAME (\d+): (.*)")

    def type_validator(self, data_type):
        """Returns a boolean indicating whether the data_type given as argument is a valid one for the python class.

        :param data_type: A strong representing a data type.
        :type data_type: str
        :return: True if the data type is valid for the class and False otherwise.
        :rtype: bool
        """
        pass

    def parse(self, lines, autocorrect=False, header_only=False):
        pass

    def parse_lines(self, lines, autocorrect=False, header_only=False):
        """Parses the lines provided as argument. The parser to be used is deducted from the instance's inner value of
        data_type.

        :param lines: A list of string, each string being one line of the instance to parse.
        :type lines: list
        :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
        :type autocorrect: bool
        :param header_only: A boolean indicating whether we should stop after having read the header. Default is False.
        :type header_only: bool
        """

        if self.type_validator(self.data_type):
            self.parse(lines, autocorrect=autocorrect, header_only=header_only)
        else:
            raise TypeError(
                f"File extension {self.data_type} is not valid for this type of PrefLib "
                "instance. This file cannot be parsed."
            )

    def parse_file(self, filepath, autocorrect=False, header_only=False):
        """Parses the file whose path is provided as argument and populates the PreflibInstance object accordingly.
        The parser to be used is deduced from the file extension.

        :param filepath: The path to the file to be parsed.
        :type filepath: str
        :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
        :type autocorrect: bool
        :param header_only: A boolean indicating whether we should stop after having read the header. Default is False.
        :type header_only: bool
        """

        # Populating basic properties of the instance
        self.file_path = os.path.basename(filepath)
        self.file_name = path.split(filepath)[1]
        self.data_type = path.splitext(filepath)[1][1:]

        # Read the file
        file = open(filepath, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        self.parse_lines(lines, autocorrect=autocorrect, header_only=header_only)

    def parse_str(self, string, data_type, file_name="", autocorrect=False, header_only=False):
        """Parses the string provided as argument and populates the PreflibInstance object accordingly.
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
        :param header_only: A boolean indicating whether we should stop after having read the header. Default is False.
        :type header_only: bool
        """

        self.file_path = "parsed_from_string"
        self.file_name = file_name
        self.data_type = data_type

        self.parse_lines(string.splitlines(), autocorrect=autocorrect, header_only=header_only)

    def parse_url(self, url, autocorrect=False, header_only=False):
        """Parses the file located at the provided URL and populates the PreflibInstance object accordingly.
        The parser to be used (whether the file describes a graph or an order for instance) is deduced based
        on the file extension.

        :param url: The target URL.
        :type url: str
        :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
        :type autocorrect: bool
        :param header_only: A boolean indicating whether we should stop after having read the header. Default is False.
        :type header_only: bool
        """

        data = urllib.request.urlopen(url)
        lines = [line.decode("utf-8").strip() for line in data]
        data.close()

        self.file_path = url
        self.file_name = url.split("/")[-1].split(".")[0]
        self.data_type = url.split(".")[-1]

        self.parse_lines(lines, autocorrect=autocorrect, header_only=header_only)

    def parse_metadata(self, line, autocorrect=False):
        """A helper function that parses metadata.

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

    def set_file_name(self, filepath):
        """Set self.filename according to a given filepath.

        :param filepath: The filepath to a (preflib) file.
        :type filepath: str
        """
        self.file_name = os.path.basename(filepath)

    def write(self, filepath):
        pass

    def write_metadata(self, file):
        """A helper function that writes the metadata in the file.

        :param file: The file to write into as a file object.

        """
        file.write(
            "# FILE NAME: {}\n# TITLE: {}\n# DESCRIPTION: {}\n# DATA TYPE: {}\n# MODIFICATION TYPE: {}\n".format(
                self.file_name,
                self.title,
                self.description,
                self.data_type,
                self.modification_type,
            )
        )
        file.write(
            "# RELATES TO: {}\n# RELATED FILES: {}\n# PUBLICATION DATE: {}\n# MODIFICATION DATE: {}\n".format(
                self.relates_to,
                self.related_files,
                self.publication_date,
                self.modification_date,
            )
        )

    def __str__(self):
        return "PrefLib-Instance: {} <{},{}>".format(
            self.file_name, self.num_voters, self.num_alternatives
        )
