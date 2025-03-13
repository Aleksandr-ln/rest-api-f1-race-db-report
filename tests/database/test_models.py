import unittest

from database.models import Driver, RaceEnd, RaceStart, db


class TestModels(unittest.TestCase):

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

    def test_create_driver(self):
        driver = Driver.create(
            abbreviation='SVF', full_name='Sebastian Vettel', team='FERRARI')
        self.assertEqual(driver.abbreviation, 'SVF')

    def test_race_start_end_relations(self):
        driver = Driver.create(
            abbreviation='SVF', full_name='Sebastian Vettel', team='FERRARI')
        race_start = RaceStart.create(
            driver=driver, start_time='2018-05-24 12:02:58.917')
        race_end = RaceEnd.create(
            driver=driver, end_time='2018-05-24 12:05:58.917')
        self.assertEqual(race_start.driver.full_name, 'Sebastian Vettel')
        self.assertEqual(race_end.driver.team, 'FERRARI')
