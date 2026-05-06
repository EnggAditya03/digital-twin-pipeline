import json, time, requests, sseclient
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

DITTO_URL    = 'http://localhost:8080'
DITTO_USER   = 'ditto'
DITTO_PASS   = 'ditto'
INFLUX_URL   = 'http://localhost:8086'
INFLUX_TOKEN = 'my-super-secret-token'
INFLUX_ORG   = 'my-org'
INFLUX_BKT   = 'ditto-telemetry'

client    = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def forward_event(event_data):
    try:
        ev = json.loads(event_data)
        thing_id = ev.get('thingId', 'unknown')
        features = ev.get('features', {})
        for feature_name, feature_data in features.items():
            props = feature_data.get('properties', {})
            if 'value' in props and props['value'] is not None:
                point = (Point('ditto_feature')
                    .tag('thing_id', thing_id)
                    .tag('feature',  feature_name)
                    .field('value',  float(props['value']))
                    .time(time.time_ns()))
                write_api.write(bucket=INFLUX_BKT, record=point)
                print(f'Written: {thing_id}/{feature_name} = {props["value"]}', flush=True)
    except Exception as e:
        print(f'Error forwarding event: {e}', flush=True)

def connect_and_listen():
    print('Connecting to Ditto SSE stream...', flush=True)
    url = f'{DITTO_URL}/api/2/things?fields=thingId,features'
    response = requests.get(
        url,
        auth=(DITTO_USER, DITTO_PASS),
        headers={
            'Accept': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        },
        stream=True,
        timeout=None  # No timeout — SSE is a permanent stream
    )
    print(f'Connected! Status: {response.status_code}', flush=True)
    client = sseclient.SSEClient(response)
    for event in client.events():
        if event.data and event.data.strip() not in ('', 'ping'):
            forward_event(event.data)

print('Starting Ditto -> InfluxDB bridge...', flush=True)
while True:
    try:
        connect_and_listen()
    except KeyboardInterrupt:
        print('Bridge stopped.')
        break
    except Exception as e:
        print(f'Connection lost ({e}) — reconnecting in 5s...', flush=True)
        time.sleep(5)
