import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from app.core.config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET

class InfluxDBService:
    def __init__(self):
        self.client = influxdb_client.InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        self.bucket = INFLUXDB_BUCKET
        self.org = INFLUXDB_ORG
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
    
    def write_sensor_data(self, drone_id: str, mission_id: int, 
                          sensor_type: str, value: float, unit: str):
        """Skriv sensor-data til InfluxDB"""
        point = influxdb_client.Point("sensor_reading") \
            .tag("drone_id", drone_id) \
            .tag("mission_id", str(mission_id)) \
            .tag("sensor_type", sensor_type) \
            .tag("unit", unit) \
            .field("value", float(value)) \
            .time(influxdb_client.utc_now())
        
        self.write_api.write(bucket=self.bucket, org=self.org, record=point)
    
    def query_recent_sensor_data(self, drone_id: str, minutes: int = 5):
        """Hent siste X minutter med sensor-data"""
        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: -{minutes}m)
            |> filter(fn: (r) => r["drone_id"] == "{drone_id}")
            |> filter(fn: (r) => r["_field"] == "value")
            |> yield(name: "mean")
        '''
        result = self.query_api.query(org=self.org, query=query)
        return result