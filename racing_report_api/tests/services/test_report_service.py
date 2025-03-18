import unittest

from racing_report_api.database.models import Driver, RaceInfo, db
from racing_report_api.services.report_service import get_race_report


class TestReportService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.init(':memory:')
        db.connect()
        db.create_tables([Driver, RaceInfo])

    @classmethod
    def tearDownClass(cls):
        db.drop_tables([Driver, RaceInfo])
        db.close()

    def setUp(self):
        Driver.delete().execute()
        RaceInfo.delete().execute()

    def test_get_race_report(self):
        Driver.create(
            abbreviation='SVF',
            full_name='Sebastian Vettel',
            team='FERRARI'
        )
        driver = Driver.get(Driver.abbreviation == 'SVF')

        RaceInfo.create(
            driver=driver,
            event="Monaco 2018 Grand Prix",
            session="Qualification",
            date="2018-05-24",
            start_time="2018-05-24 12:02:58.917",
            end_time="2018-05-24 12:05:58.778"
        )

        report = get_race_report("Monaco 2018 Grand Prix", "Qualification")

        self.assertTrue(hasattr(report, 'results'))
        self.assertEqual(report.date, "2018-05-24")
        self.assertGreaterEqual(len(report.results), 1)

    def test_empty_report(self):
        report = get_race_report('Monaco 2018 Grand Prix', 'Qualification')
        self.assertEqual(report.results, [])
        self.assertEqual(report.disqualified, [])

    def test_partial_data_report(self):
        Driver.create(
            abbreviation='DRR',
            full_name='Daniel Ricciardo',
            team='REDBULL'
        )
        driver = Driver.get(Driver.abbreviation == 'DRR')

        RaceInfo.create(
            driver=driver,
            event='Monaco 2018 Grand Prix',
            session='Qualification',
            date='2018-05-24',
            start_time='2018-05-24 12:10:58.917'
        )

        report = get_race_report('Monaco 2018 Grand Prix', 'Qualification')
        self.assertEqual(len(report.results), 0)
        self.assertEqual(len(report.disqualified), 1)
