# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time
import ftplib
import requests
moisture = 'default'
refill = 'default'


# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

"""Sean's Code"""
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
"""Sean's Code"""


# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} |'.format(*range(8)))
print('-' * 15)
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*8

    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Print the ADC values.
    print('| {0:>4} | {1:>4} |'.format(*values))
    """Sean's Code"""
    for i in range(2):
        if(i == 0):
            if(mcp.read_adc(i) >= 513):
                GPIO.output(17, GPIO.LOW)
                moisture = 'Dry soil, watering!'
                print moisture
            else:
                 GPIO.output(17, GPIO.HIGH)
                 moisture = 'Moist soil.'
                 print moisture
        elif(i == 1):
            dataWater = (785 - mcp.read_adc(i)) * 0.293255132
            dataWater = round(dataWater, 2)
            if(mcp.read_adc(i) <= 614):
                refill = 'The water source is: ' + str(dataWater) + '% full. No need to refill.'
                print refill
            if(mcp.read_adc(i) < 699 and mcp.read_adc(i) >= 615):
                refill = 'The water source is: ' + str(dataWater) + '% full. Refill soon.'
                print refill
            if(mcp.read_adc(i) < 785 and mcp.read_adc(i) > 699):
                refill = 'The water source is: ' + str(dataWater) + '% full. Refill as soon as possible.'
                print refill
            if(mcp.read_adc(i) >= 785):
                refill = 'The water source is: 0% full. Refill necessary.'
                print refill
    # copy of input_data.py implemented into loop. -Matt's Code-
    r = requests.post('http://ese205soilsolutions-env.xba2aybskw.us-east-2.elasticbeanstalk.com/input',
                      data={'id': '1', 'moisture': moisture, 'water': refill})
    time.sleep(2)






    
