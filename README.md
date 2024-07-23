This script wil read the data from the serialport of the magneto meter and stores it in an Influx Database.
The data format from is DD.MM.YY HH:MM:SS: X,ddddd,Y,ddddd,Z,ddddd EoL


The script will parse the date, time, X-Data, Y-Data, and Z-Data in ASCII format from the serial port, and store these values in the InfluxDB database when it encounters the EoL marker.

Since the data comes in every second, the script needs to continuously read and process the data in a loop.
The while True loop continuously reads lines from the serial port, processes them immediately. 
Adjust the serial port and database connection details as needed.

To achieve this, you will need to install the necessary libraries and set up the InfluxDB client on your Raspberry Pi.

# Prerequisites
Install necessary Python packages:

sudo apt-get update
sudo apt-get install python3-pip
pip3 install pyserial influxdb
Set up InfluxDB:
Make sure you have InfluxDB installed and running. If not, you can install it using the following commands:

sudo apt-get update
sudo apt-get install influxdb
sudo systemctl start influxdb
sudo systemctl enable influxdb
Create the InfluxDB database:
Open the InfluxDB CLI by typing influx in your terminal and then create the database:

sql
Copy code
CREATE DATABASE magneto


# Reading and Writing Data:

The script reads a line from the serial port, decodes it, and strips any whitespace.
If a line is read, it is parsed using parse_serial_data().
If the parsed data is valid, it is written to InfluxDB using write_to_influxdb().

# Error Handling:

The script includes basic error handling to catch and print exceptions, ensuring that the loop continues running even if a single read or write operation fails.


# Running the Script
Ensure the serial device is connected and the port is correct.
Run the script:

python3 Read2DB.py
