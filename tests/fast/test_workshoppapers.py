import os.path
import re
import unittest
import yaml


class TestWorkshopPapers(unittest.TestCase):
    def setUp(self) -> None:
        """
        Parse our data files and combine them into a dictionary.
        """
        data_files = [
            'authors',
            'workshoppapers',
            'workshops'
        ]

        self.data = {}
        for data_current in data_files:
            with open('_data/{}.yml'.format(data_current)) as f:
                self.data[data_current] = yaml.load(f)

    def test_parse_yaml(self) -> None:
        """
        Confirm all YAML from setUp successfully parses.
        """
        pass

    def test_workshoppapers_authors_exist(self) -> None:
        """
        Confirm all authors referenced by a paper actually exist.
        """
        for id_workshoppaper, workshoppaper in self.data['workshoppapers'].items():
            self.assertIn(
                'authors',
                workshoppaper,
                '{} missing authors'.format(id_workshoppaper)
            )

            for id_author in workshoppaper['authors']:
                self.assertIn(
                    id_author,
                    self.data['authors'],
                    '{} references author {} not found in authors.yml'.format(id_workshoppaper, id_author)
                )

    def test_workshoppapers_sequential(self) -> None:
        """
        Confirm workshop papers are numbered sequentially.

        This can also help in detecting two workshops with the same ID.
        """
        numbers = []
        for id_workshoppaper, workshoppaper in self.data['workshoppapers'].items():
            self.assertRegex(
                workshoppaper['pubnum'],
                'W.([\d]+)',
                '{} illegal pubnum'.format(id_workshoppaper)
            )

            numbers.append(
                int(
                    re.search(
                        'W.([\d]+)',
                        workshoppaper['pubnum']
                    ).group(1)
                )
            )

        for count in range(0, len(numbers)):
            numbers.remove(count + 1)

        self.assertEqual(
            0,
            len(numbers)
        )

    def test_workshoppapers_workshop_exist(self) -> None:
        """
        Confirm all workshops referenced by a paper actually exist.
        """
        for id_workshoppaper, workshoppaper in self.data['workshoppapers'].items():
            id_workshop = workshoppaper['workshop']
            self.assertIn(
                id_workshop,
                self.data['workshops'],
                '{} references workshop {} not found in workshops.yml'.format(id_workshoppaper, id_workshop)
            )

    def test_workshoppapers_files_exist(self) -> None:
        """
        Confirm all files references by a paper actually exist.
        """
        for id_workshoppaper, workshoppaper in self.data['workshoppapers'].items():
            # Papers may have a PDF
            if 'localpdf' in workshoppaper:
                file_path = workshoppaper['localpdf']
                self.assertTrue(
                    os.path.isfile('publications/{}'.format(file_path)),
                    '{} references localpdf {} not found in publications/'.format(id_workshoppaper, file_path)
                )

                file_name = os.path.basename(file_path)
                self.assertRegexpMatches(
                    file_name,
                    '^[a-z0-9\-\.]*$',
                    '{} file name contains illegal characters'.format(id_workshoppaper)
                )
