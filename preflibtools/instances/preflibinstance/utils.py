import os

from preflibtools.instances.preflibinstance.ordinal import OrdinalInstance
from preflibtools.instances.preflibinstance.categorical import CategoricalInstance
from preflibtools.instances.preflibinstance.matching import MatchingInstance


def get_parsed_instance(file_path, autocorrect=False, header_only=False):
    """Infers from the extension of the file given as input the correct instance to use. Parses the file and return
    the instance.

    :param file_path: The path to the file to be parsed.
    :type file_path: str
    :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
        in the file. Default is False.
    :type autocorrect: bool
    :param header_only: A boolean indicating whether we should stop after having read the header. Default is False.
    :type header_only: bool

    :return: The instance with the file already parsed.
    :rtype: :class:`preflibtools.instances.preflibinstance.PrefLibInstance`
    """
    extension = os.path.splitext(file_path)[1]
    if extension in (".soc", ".soi", ".toc", ".toi"):
        instance = OrdinalInstance()
    elif extension == ".cat":
        instance = CategoricalInstance()
    elif extension == ".wmd":
        instance = MatchingInstance()
    else:
        raise TypeError(f"The file extension {extension} corresponds to no known file extension "
                        f"of PrefLib data file.")
    instance.parse_file(file_path, autocorrect=autocorrect, header_only=header_only)
    return instance
