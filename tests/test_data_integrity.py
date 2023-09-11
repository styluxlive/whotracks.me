from operator import itemgetter
import unittest

from whotracksme.data import load_tracker_db, DataSource


class TestDataIntegrity(unittest.TestCase):

    def setUp(self):
        self.conn = load_tracker_db()
        self.ds = DataSource()

    def test_all_trackers_have_db_entry(self):
        trackers = self.ds.trackers
        cur = self.conn.cursor()
        app_ids = [row.id for row in trackers.get_snapshot()]
        db_trackers = cur.execute(
            f"""select id, category_id from trackers where id IN ({','.join([f"'{id}'" for id in app_ids])}) order by id"""
        ).fetchall()
        self.assertEqual(set(app_ids), set(map(itemgetter(0), db_trackers)))
        # check all have a category
        without_category = list(filter(lambda tracker: tracker[1] is None, db_trackers))
        self.assertEqual([], without_category)

    def test_all_companies_have_db_entry(self):
        companies = self.ds.companies
        cur = self.conn.cursor()
        company_ids = sorted([row.id for row in companies.get_snapshot()])

        # company_id can be a company id or tracker id
        db_companies = cur.execute(
            f"""select id from companies where id IN ({','.join([f"'{id}'" for id in company_ids])}) order by id"""
        ).fetchall()
        db_trackers = cur.execute(
            f"""select id, category_id from trackers where id IN ({','.join([f"'{id}'" for id in company_ids])}) order by id"""
        ).fetchall()
        self.assertEqual(set(company_ids), set(map(itemgetter(0), db_companies)) | set(map(itemgetter(0), db_trackers)))


if __name__ == '__main__':
    unittest.main()
