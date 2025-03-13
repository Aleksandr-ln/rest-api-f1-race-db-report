import unittest

from database.models import Driver, RaceEnd, RaceStart, db
from REST_API_report_of_Monaco_2018_Racing.services.report_service import \
    get_race_report


class TestReportService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.init(':memory:')
        db.connect()
        db.create_tables([Driver, RaceStart, RaceEnd])

    @classmethod
    def tearDownClass(cls):
        db.drop_tables([Driver, RaceStart, RaceEnd])
        db.close()

    def setUp(self):
        Driver.delete().execute()
        RaceStart.delete().execute()
        RaceEnd.delete().execute()

    def test_get_race_report(self):
        Driver.create(abbreviation='SVF',
                      full_name='Sebastian Vettel', team='FERRARI')
        driver = Driver.get(Driver.abbreviation == 'SVF')
        RaceStart.create(driver=driver, start_time='2018-05-24 12:02:58.917')
        RaceEnd.create(driver=driver, end_time='2018-05-24 12:05:58.917')

        report = get_race_report()
        self.assertTrue(hasattr(report, 'results'))
        self.assertGreaterEqual(len(report.results), 1)

    def test_empty_report(self):
        report = get_race_report()
        self.assertEqual(report.results, [])
        self.assertEqual(report.disqualified, [])

    def test_partial_data_report(self):
        Driver.create(abbreviation='DRR',
                      full_name='Daniel Ricciardo', team='REDBULL')
        driver = Driver.get(Driver.abbreviation == 'DRR')
        RaceStart.create(driver=driver, start_time='2018-05-24 12:10:58.917')

        report = get_race_report()
        self.assertEqual(len(report.results), 0)
        self.assertEqual(len(report.disqualified), 1)
