// Licensed under CC BY-NC-ND 4.0
// Aleksandar Valov August, 2021
// You MAY NOT use this software for commerical purposes, nor distribute any derivatives of it anywhere. 
// Appropriate credit should be given when distributing this work.

#include <SimpleDHT.h>

#include <TimerOne.h>

#include <LiquidCrystal.h>

#include <EEPROM.h>


// ############################################################
// Initialize pins to be used.
// # buttonLCDPin - pin for pull-up button  OUTPUT
// # lightResistorPin - pin for photoresistor /sensor for incoming light/ INPUT
// # beepPin - active buzzer, optional INPUT
// # dht11Pin - pin for the DHT11 sensor INPUT
// # LED_BUILTIN - using the buildin LED to indicate EEPROM activity
// ############################################################
int buttonLCDPin = 2;
int lightResistorPin = A3;
int beepPin = 10;
int dht11Pin = 11;

// ############################################################
// Sensor sampling options.
// # sampleTimeout - Indicates time in microseconds to pass before reading values of the sensors, MUST BE bigger than the sample frequency of the sensor (1000000 = 1 MHz)
// # interruptsToPassBeforeWriting - Indicates number of sensor interrupts to pass before writing values to EEPROM
// ############################################################
unsigned long sampleTimeout = 5000000;  // >= 1000000
int interruptsToPassBeforeWriting = 12; // 180

// ############################################################
// States variables that are manipulated in interrupts.
// # IsLCDPressed (buttonLCDPressed()) - when button for LCD is pressed by user
// # IsSerialPressed - set to true once the ISR for writing to EEPROM finishes; initializes the ISR for serial transfer to host PC
// # ShouldRead (readSensors()) - called as a timer interrupt when sampleTimeout seconds pass
// # ScreenState - dictates current state of LCD dispay. 4 valid states are defined:
//                 # State 0 - Shows current light readings
//                 # State 1 - Shows current humidity readings
//                 # State 2 - Shows current temperature readings
//                 # State 3 - Shows the most recently written sensor values into the EEPROM
//                 # State -1 - Displayed when error is detected during sensor readings
// # SensorInterruptsCount (readSensors()) - counts each time sensors are being read; used for writing to EEPROM
// ############################################################
volatile bool IsLCDPressed = false;
volatile bool IsSerialPressed = false;
volatile bool ShouldRead = false;
volatile int ScreenState = 0;
volatile int MemAddr = 0;

volatile int lightVal;

volatile byte SensorInterruptsCount = 0;

// ############################################################
// Cache of the internal EEPROM memory, loaded on startup;
// Used in order to reduce EEPROM load.
// ############################################################
volatile byte* eepromCache = NULL;

byte temperature;
byte humidity;
int sensorErr;

// ############################################################
// LCD display hooked up at 4,5,6,7,8,9 pins. See schematic.
// ############################################################
LiquidCrystal lcd = LiquidCrystal(4,5,6,7,8,9);
SimpleDHT11 dht11(dht11Pin);

void setup() {
  lcd.begin(16,2);
  pinMode(lightResistorPin, INPUT);
  pinMode(buttonLCDPin, INPUT);
  pinMode(beepPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  memorySetup();

  attachInterrupt(digitalPinToInterrupt(buttonLCDPin), buttonLCDPressed, FALLING); 

  Timer1.initialize(sampleTimeout); 
  Timer1.attachInterrupt(readSensors);
}

void loop() {
  if (IsLCDPressed) {
    // ############################################################
    // Interrupt Service Routine for LCD button press (changing screen state)
    // ############################################################
    lcd.clear();
    ScreenState = (ScreenState + 1) % 4;
    digitalWrite(beepPin, HIGH);
    delay(150);
    digitalWrite(beepPin, LOW);
    IsLCDPressed = false;
  }

  if (IsSerialPressed) {
    // ############################################################
    // Interrupt Service Routine for serial communication
    // ############################################################
    int transferResult = startSerialTransfer();
    if (transferResult != 0) {
      digitalWrite(beepPin, HIGH);
      delay(300);
      digitalWrite(beepPin, LOW);
    }
    IsSerialPressed = false;
  }

  if (ShouldRead) {
    // ############################################################
    // Interrupt Service Routine for sampling sensors; Timer interrupted
    // ############################################################
    sensorErr = dht11.read(&temperature, &humidity, NULL);
    if (sensorErr != SimpleDHTErrSuccess) {
        ScreenState = -1;
        lcd.clear();
    }

    lightVal = analogRead(lightResistorPin) / 4;
    ShouldRead = false;
  }

  if (SensorInterruptsCount >= interruptsToPassBeforeWriting) {
    // ############################################################
    // Interrupt Service Routine for writing sensor data to EEPROM; Timer interrupted - conditionally from readSensors()
    // Once data is written, initiate transfer with host PC.
    // ############################################################
    digitalWrite(LED_BUILTIN, HIGH);
    noInterrupts();
  
    eepromCache[MemAddr] = lightVal;
    EEPROM.write(MemAddr, lightVal);
    MemAddr++;
    if (MemAddr > 1023) {
     memoryLock();
    }

    eepromCache[MemAddr] = temperature;
    EEPROM.write(MemAddr, temperature);
    MemAddr++;
    if (MemAddr > 1023) {
      memoryLock();
    }

    eepromCache[MemAddr] = humidity;
    EEPROM.write(MemAddr, humidity);
    MemAddr++;
    if (MemAddr > 1023) {
      memoryLock();
    }

    SensorInterruptsCount = 0;
    
    interrupts();
    IsSerialPressed = true;
    digitalWrite(LED_BUILTIN, LOW);
  }

  if (ScreenState == 1) {
    lcd.setCursor(0,0);
    lcd.print("Humidity level");
    lcd.setCursor(7,1);
    lcd.print((int)humidity);
    lcd.print(" %");
  }
  else if (ScreenState == 0) {
    lcd.setCursor(0,0);
    lcd.print("Light readings");
    lcd.setCursor(7,1);
    lcd.print("    ");
    lcd.setCursor(7,1);
    
    lcd.print(lightVal);
  }
  else if (ScreenState == 2) {
    lcd.setCursor(0,0);
    lcd.print("Temperature");
    lcd.setCursor(7,1);
    lcd.print((int)temperature);
    lcd.print(" C*");
  }
  else if (ScreenState == 3) {
    lcd.setCursor(0,0);
    lcd.print("Last saved");
    printLastSaved();
  }
  else {
    lcd.setCursor(0,0);
    lcd.print("Bad readings");
    lcd.setCursor(0,1);
    lcd.print("Code:");
    lcd.print(sensorErr);
    digitalWrite(beepPin, HIGH);
  }

  
  delay(200);
}

void buttonLCDPressed() {
  IsLCDPressed = true;
}

void readSensors() {
  ShouldRead = true;
  SensorInterruptsCount++;
}

void memorySetup() { 
    // ############################################################
    // Sets up EEPROM memory to use.
    // ############################################################
  noInterrupts();
  
  // Check value at address 0x00 for a specific checksum.
  if (EEPROM.read(0) != 165) {
    lcd.setCursor(0,0);
    lcd.print("Memory checksum");
    lcd.setCursor(0,1);
    lcd.print("fail !");
    while(1) { }
  }

  eepromCache = new byte[1024];

  bool memoryFull = true;

  // Find the first free memory address.
  for (MemAddr = 1; MemAddr < 1024; MemAddr++) {
    byte readVal = EEPROM.read(MemAddr);
    if (readVal == 255) {
      memoryFull = false;
      break;
    }
    eepromCache[MemAddr] = readVal;
  }

  if (memoryFull) {
      memoryLock();
  }

  interrupts();
}

int startSerialTransfer() {
    // ############################################################
    // Starts serial communication with host PC. Communication procedure:
    // 1. Start communication channel and waits host to send ACK message. If no confirmation - fail.
    // 2. Starts dumping written sensor values in EEPROM to Serial
    // 3. After iterating all values in eeprom - send DM_END and terminate
    // RETURNS: 0 - successful transfer, -1 - no host listener, -2 - no confirmation received
    // ############################################################
    Serial.begin(14400);
    Serial.println("DM_RDY");
    int communicationTimeout = 5000;
    while (Serial.available() == 0) {
      communicationTimeout--;
      if (communicationTimeout <= 0) {
        Serial.end();
        return -1;
      }
    }

    String receivedMsg = Serial.readString();
    if (receivedMsg != "DM_ACK") {
      Serial.end();
      return -2;
    }

    for (int addr = 1; addr < MemAddr; addr++) {
      Serial.println(eepromCache[addr]);
    }

    Serial.print("DM_END");
    Serial.end();
    return 0;
}

void memoryLock() {
    // ############################################################
    // Called when EEPROM memory is full; locks the microcontroller.
    // ############################################################
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Memory full!");
    while(1) { digitalWrite(beepPin, HIGH); }
}

void printLastSaved() {
    // ############################################################
    // Prints the most recently written (cached) sensor values.
    // ############################################################
  lcd.setCursor(0,1);
  if (MemAddr < 3) {
    lcd.print("None");
    return;
  }
  
  lcd.print("L:");
  lcd.print(eepromCache[MemAddr - 3]);
  lcd.print(" T:");
  lcd.print(eepromCache[MemAddr - 2]);
  lcd.print(" H:");
  lcd.print(eepromCache[MemAddr - 1]);

}
