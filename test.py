import unittest
import hourly_report, daily_report


class TestDailyMethods(unittest.TestCase):
    def setUp(self):
        hourly_data = hourly_report.pull_data()
        self.stations_info = hourly_data["stations_info"]
        self.stations_status = hourly_data["stations_status"]
        self.hourly_report = hourly_report.hourly_report(
            self.stations_status["data"]["stations"]
        )

    def tearDown(self):
        pass

    def test_least_available(self):
        report = self.hourly_report
        least = report[0]["num_bikes_available"] + report[0]["num_ebikes_available"]
        is_least = True

        for i in range(1, len(report)):
            curr = report[i]["num_bikes_available"] + report[i]["num_ebikes_available"]
            is_least = is_least and (curr >= least)

        self.assertTrue(is_least)

    def test_most_available(self):
        report = self.hourly_report
        most = report[-1]["num_bikes_available"] + report[-1]["num_ebikes_available"]
        is_most = True

        for i in range(1, len(report)):
            curr = report[i]["num_bikes_available"] + report[i]["num_ebikes_available"]
            is_most = is_most and (curr <= most)

        self.assertTrue(is_most)


if __name__ == "__main__":
    unittest.main()
