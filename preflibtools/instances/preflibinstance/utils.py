import os

from preflibtools.instances.preflibinstance.ordinal import OrdinalInstance
from preflibtools.instances.preflibinstance.categorical import CategoricalInstance
from preflibtools.instances.preflibinstance.matching import MatchingInstance


def get_parsed_instance(file_path, header_only=False):
    """Infers from the extension of the file given as input the correct instance to use. Parses the file and return
    the instance.

    :param file_path: The path to the file to be parsed.
    :type file_path: str
    :param header_only: A boolean indicating whether we should stop after having read the header. Default is False.
    :type header_only: bool

    :return: The instance with the file already parsed.
    :rtype: :class:`preflibtools.instances.preflibinstance.PrefLibInstance`
    """
    extension = os.path.splitext(file_path)[1]
    if extension in (".soc", ".soi", ".toc", ".toi"):
        if header_only:
            instance = OrdinalInstance()
            instance.parse_file(file_path, header_only=True)
            return instance
        return OrdinalInstance(file_path)
    elif extension == ".cat":
        if header_only:
            instance = CategoricalInstance()
            instance.parse_file(file_path, header_only=True)
            return instance
        return CategoricalInstance(file_path)
    elif extension == ".wmd":
        if header_only:
            instance = MatchingInstance()
            instance.parse_file(file_path, header_only=True)
            return instance
        return MatchingInstance(file_path)
    else:
        raise TypeError(f"The file extension {extension} corresponds to no known file extension "
                        f"of PrefLib data file.")
