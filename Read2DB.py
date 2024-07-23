import serial
from influxdb import InfluxDBClient
import datetime

# Configure serial port
SERIAL_PORT = '/dev/ttyUSB0'    # Pas aan aan de poort van de Pi
BAUD_RATE = 9600
TIMEOUT = 1

# Configure InfluxDB
INFLUXDB_ADDRESS = 'localhost'  # IP adres van de Pi waarop Influx draait
INFLUXDB_PORT = 8086            # Influx poort (hoeft niet gewijzigd te worden)
INFLUXDB_USER = 'root'          # Influx gebruiker
INFLUXDB_PASSWORD = 'root'      # Influx wachtwoord
INFLUXDB_DATABASE = 'magneto'   # Influx database naam

def init_influxdb_client():
    client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, INFLUXDB_DATABASE)
    return client

def write_to_influxdb(client, data):
    json_body = [
        {
            "measurement": "datetime_measurement",
            "tags": {
                "sensor": "datetime_sensor"
            },
            "time": data['timestamp'],
            "fields": {
                "date": data['date'],
                "time": data['time'],
                "X_data": data['X_data'],
                "Y_data": data['Y_data'],
                "Z_data": data['Z_data']
            }
        }
    ]
    client.write_points(json_body)

def parse_serial_data(line):
    try:
        # Remove the EoL marker and separate the fields
        data_parts = line.strip().split(' ')
        
        if data_parts[-1] != 'EoL':
            raise ValueError("EoL marker not found")
        
        # Extract date, time, and data part
        date_str, time_str = data_parts[0], data_parts[1]
        x_data_str, y_data_str, z_data_str = data_parts[2], data_parts[3], data_parts[4]
        
        # Extract the X, Y, and Z values
        x_value = float(x_data_str.split(',')[1])
        y_value = float(y_data_str.split(',')[1])
        z_value = float(z_data_str.split(',')[1])
        
        # Combine date and time for the timestamp
        datetime_str = f"{date_str} {time_str}"
        timestamp = datetime.datetime.strptime(datetime_str, '%d.%m.%y %H:%M:%S').isoformat() + 'Z'

        data = {
            'timestamp': timestamp,
            'date': date_str,
            'time': time_str,
            'X_data': x_value,
            'Y_data': y_value,
            'Z_data': z_value
        }
        
        return data
    except Exception as e:
        print(f"Failed to parse data: {e}")
        return None

def main():
    influxdb_client = init_influxdb_client()
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    
    while True:
        try:
            line = ser.readline().decode('ascii').strip()
            if line:
                data = parse_serial_data(line)
                if data:
                    write_to_influxdb(influxdb_client, data)
                    print(f"Data written: {data}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
