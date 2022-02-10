import logging
from datetime import datetime, timedelta

import pandas as pd


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class AirQuality:
    def __init__(self, particle_sensor_id, humidity_sensor_id):
        self.sds_id = particle_sensor_id
        self.dht_id = humidity_sensor_id
        self._sds_df = None
        self._dht_df = None

    def import_data(self, days=1):
        for day in range(days):
            now = datetime.now()-timedelta(days=day)
            date = now.strftime("%Y-%m-%d")

            sds_url = f'http://archive.sensor.community/{date}/{date}_sds011_sensor_{self.sds_id}.csv'

            dht_url = f'http://archive.sensor.community/{date}/{date}_dht22_sensor_{self.dht_id}.csv'

            logging.debug(f"Importing data for {date}")

            try:
                self._sds_df = pd.read_csv(sds_url, sep=';')
                self._sds_df.dropna(how='all', axis=1, inplace=True)

                # TODO: INSERT INTO sds_data (timestamp, P1, P2) VALUES()
            except:
                logging.warning(f"could not read sds data for {date}")

            try:
                self._dht_df = pd.read_csv(dht_url, sep=';')
                self._dht_df.dropna(how='all', axis=1, inplace=True)

                # TODO: INSERT INTO dht_data (timestamp, P1, P2) VALUES()
            except:
                logging.warning(f"could not read dht data for {date}")

    def get_particle_dataframe(self):
        return self._sds_df

    def get_humidity_dataframe(self):
        return self._sds_df

    def _try_load_dht_csv(self, days=1):
        data = []
        for day in range(days):
            now = datetime.now()-timedelta(days=day)
            date = now.strftime("%Y-%m-%d")
            logging.debug(f"Importing data for {date}")

            try:
                dht_url = dht_url = f'http://archive.sensor.community/{date}/{date}_dht22_sensor_{self.dht_id}.csv'

                dht_df = pd.read_csv(dht_url, sep=';')
                dht_df.dropna(how='all', axis=1, inplace=True)
                data.append(dht_df)

            except:
                logging.warning('could not read data for %(date)')

        return pd.concat(data, axis=0)


if __name__ == "__main__":
    location = AirQuality(3659, 3660)
    location.import_data(4)
