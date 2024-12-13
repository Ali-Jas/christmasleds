import time
import serial
import random

ser = serial.Serial(port='COM4', baudrate=115200, timeout=1)
serFinish=False
# Open the serial port


# Send data

def main():
  if not ser.is_open:
    ser.open()
  for a in range(10000):
    #print(f"loep[{a}]")
    loop()
    time.sleep(0.001)
  ser.close()
  


# Wait for a specific prompt
def loop():
  while True:
      response=""
      if ser.in_waiting > 0:
        response = ser.readline().decode().strip()
      if response == 'Arduino is ready':
        #print("serial is alive")
        acommand='BOD##'
        ser.write(acommand.encode())
      elif response == 'ReadyForData':
        #print("can send data")
        longstring=""
        loop=0
        for a in range(180):
          longstring += format(random.randrange(0, 255), '02x').upper()
          #longstring += random.choice(['00', '7F', 'FF'])
          loop+=1
        longstring=f"{longstring}##EOD##"
        acommand=longstring + '\r\n'
        ser.write(acommand.encode())
      elif response == "color_datastring_received":
         #print("done!")
         break

if __name__ == "__main__":
  main()