from unittest import TestCase
import os

from preflibtools.instances.dataset import read_info_file


class TestDataset(TestCase):

    def test_read_info_file(self):
        example_file_content = """
Name: Boardgames Geek Ranking

Abbreviation: boardgames

Tags: Election

Series Number: 00041

Publication Date: 2022-09-25

Description: <p>Simple description</p>

Required Citations: Example required citations

Selected Studies: Some selected studies

file_name, modification_type, relates_to, title, description, publication_date
00041-00000001.soi, original, , Alltime, , 2022-09-25
00041-00000001.soc, induced, 00041-00000001.soi, Alltime, Complete preferences extracted from the soi file, 2022-09-25
"""

        file_name = "info_file.txt"

        with open(file_name, "w") as file:
            file.write(example_file_content)

        results = read_info_file(file_name)

        # check dataset metadata
        assert results["description"] == "<p>Simple description</p>"
        assert results["citations"] == "Example required citations"
        assert results["studies"] == "Some selected studies"
        assert results["series"] == "00041"
        assert results["tags"] == ["Election"]
        assert results["abb"] == "boardgames"
        assert results["name"] == "Boardgames Geek Ranking"

        # check files metadata
        files_metadata = results["files"]

        first_file = files_metadata["00041-00000001.soi"]
        assert first_file["file_name"] == "00041-00000001.soi"
        assert first_file["modification_type"] == "original"
        assert first_file["relates_to"] == ""
        assert first_file["title"] == "Alltime"
        assert first_file["description"] == ""
        assert first_file["publication_date"] == "2022-09-25"

        second_file = files_metadata["00041-00000001.soc"]
        assert second_file["file_name"] == "00041-00000001.soc"
        assert second_file["modification_type"] == "induced"
        assert second_file["relates_to"] == "00041-00000001.soi"
        assert second_file["title"] == "Alltime"
        assert (
            second_file["description"]
            == "Complete preferences extracted from the soi file"
        )
        assert second_file["publication_date"] == "2022-09-25"

        os.remove(file_name)
