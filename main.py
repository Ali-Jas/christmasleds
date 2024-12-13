import serial
import time
import random
from PIL import Image
import os

# Set up the serial connection (make sure the port matches your Arduino's port)
ser = serial.Serial('COM4', 115200, timeout=1)
serReady = True
time.sleep(3)  # Wait for the connection to initialize

def main():
    getmultiplehex()
    #read_response()
    #ser.close()

def get_hex_color(image, x, y):
    # Get the RGB value of the pixel at (x, y)
    r, g, b = image.getpixel((x, y))
    # Convert the RGB value to a hexadecimal color code
    return "0x" + "{:02x}{:02x}{:02x}".format(r, g, b).upper()


def send_string(data):
    global serReady
    ser.write((data + '\n').encode())  # Send the string to the Arduino
    serReady = False
    #print(f"Sent: {data}")

def read_response():
    global serReady
    print('getting response')
    response = ser.readline().strip()
    print(f"response direct:{response}")
    if response == b'##ACK##Strip\r\n':
        serReady = True
        print("direct hit")
    counter=0
    while response != b'##ACK##Strip\r\n':
        response = ser.readline().strip()
        print(f"{counter}:{response}")
        if response == b'##ACK##Strip\r\n':
            serReady = True
            print(f"hit {counter}")
            break;
        if counter >= 100:
            serReady = False
            break;
        time.sleep(0.01)
        counter+=1
    return serReady

def createStringWithArray():
    aArray={}
    possibleValues=[0,127,255]
    num1val=hex(random.choice(possibleValues))[2:].upper().zfill(2)
    num2val=hex(random.choice(possibleValues))[2:].upper().zfill(2)
    num3val=hex(random.choice(possibleValues))[2:].upper().zfill(2)
    newstring=f"0x{num1val}{num2val}{num3val}"
    return newstring

def getmultiplehex():
    directory="images"
    for filename in os.listdir(directory): 
        image_path = os.path.join(directory, filename)
        print(f"{image_path}")
        image = Image.open(image_path)
    
        # Define the spots (x, y coordinates)
        #spots = [(0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0), (0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0), (0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0), (0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0), (0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0), (0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0)]
        #spots = [(0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0), (0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0)]
        spots = [(0,1), (1,1), (2,1), (3,1), (4,1)] 
        # Get the hexadecimal color codes for the defined spots
        hex_colors = [get_hex_color(image, x, y) for x, y in spots]
    
        maxrange=len(spots)
        print(maxrange)
        rounds=0
        buildstring=""
        # Print the hexadecimal color codes
        send_string("##BOD##Strip")
            
        for spot, hex_color in zip(spots, hex_colors):
            #print(f"Spot {rounds}: {hex_color}")
            if read_response():
                send_string(f"pos[{rounds}]:{hex_color}")
            rounds+=1
        if read_response():
            send_string("##EOD##Strip")
        return "OK"


if __name__ == "__main__":
    main()
