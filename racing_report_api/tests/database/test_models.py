import unittest

from racing_report_api.database.models import Driver, RaceInfo, db


class TestModels(unittest.TestCase):

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

    def test_create_driver(self):
        driver = Driver.create(
            abbreviation='SVF',
            full_name='Sebastian Vettel',
            team='FERRARI'
        )
        self.assertEqual(driver.abbreviation, 'SVF')

    def test_race_start_end_relations(self):
        driver = Driver.create(
            abbreviation='SVF',
            full_name='Sebastian Vettel',
            team='FERRARI'
        )

        race_start = RaceInfo.create(
            driver=driver,
            event="Monaco 2018 Grand Prix",
            session="Qualification",
            date="2018-05-24",
            start_time='2018-05-24 12:02:58.917'
        )

        race_start.end_time = '2018-05-24 12:05:58.917'
        race_start.save()

        self.assertEqual(race_start.driver.full_name, 'Sebastian Vettel')
        self.assertEqual(race_start.driver.team, 'FERRARI')
