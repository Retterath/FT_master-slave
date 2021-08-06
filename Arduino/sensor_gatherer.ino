// TODO: Write more code to add Serial support & somehow to be able to dump the entire memory...
#include <SimpleDHT.h>

#include <TimerOne.h>

#include <LiquidCrystal.h>

#include <EEPROM.h>

int buttonPin = 2;
int lightResistorPin = A3;
int beepPin = 10;
int dht11Pin = 11;

unsigned long sampleTimeout = 300000000;

volatile bool IsPressed = false;
volatile bool ShouldRead = false;
volatile int ScreenState = 0;
volatile int MemAddr = 0;

volatile int lightVal;

volatile byte SensorInterruptsCount = 0;

byte readTemp = -1;
byte readHum = -1;
byte readLight = -1;

byte temperature;
byte humidity;
int sensorErr;

LiquidCrystal lcd = LiquidCrystal(4,5,6,7,8,9);
SimpleDHT11 dht11(dht11Pin);

void setup() {
  lcd.begin(16,2);
  pinMode(lightResistorPin, INPUT);
  pinMode(buttonPin, INPUT);
  pinMode(beepPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  memorySetup();

  attachInterrupt(digitalPinToInterrupt(2), buttonPressed, FALLING); 

  Timer1.initialize(5000000); // every 5 seconds actualize sensor info
  Timer1.attachInterrupt(readSensors);
}

void loop() {
  if (IsPressed) {
    lcd.clear();
    ScreenState = (ScreenState + 1) % 4;
    digitalWrite(beepPin, HIGH);
    delay(150);
    digitalWrite(beepPin, LOW);
    IsPressed = false;
  }

  if (ShouldRead) {
    sensorErr = dht11.read(&temperature, &humidity, NULL);
    if (sensorErr != SimpleDHTErrSuccess) {
        ScreenState = -1;
        lcd.clear();
    }

    lightVal = analogRead(lightResistorPin) / 4;
    ShouldRead = false;
  }

  if (SensorInterruptsCount >= 180) {
    // first writes the light value, temperature value and finally the humidity
    // writes in EEPROM every 15 minutes
    digitalWrite(LED_BUILTIN, HIGH);
    noInterrupts();
  
    EEPROM.write(MemAddr, lightVal);
    MemAddr++;
    if (MemAddr > 1023) {
     memoryLock();
    }
    EEPROM.write(MemAddr, temperature);
    MemAddr++;
    if (MemAddr > 1023) {
      memoryLock();
    }
    EEPROM.write(MemAddr, humidity);
    MemAddr++;
    if (MemAddr > 1023) {
      memoryLock();
    }

    SensorInterruptsCount = 0;
    readTemp = temperature;
    readHum = humidity;
    readLight = lightVal;
    
    interrupts();
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

void buttonPressed() {
  IsPressed = true;
}

void readSensors() {
  ShouldRead = true;
  SensorInterruptsCount++;
}

void memorySetup() { 
  noInterrupts();
  
  // checks if memory is valid, first byte of EEPROM should be set to specific value in order for the program to startup
  if (EEPROM.read(0) != 165) {
    lcd.setCursor(0,0);
    lcd.print("Memory checksum");
    lcd.setCursor(0,1);
    lcd.print("fail !");
    while(1) { }
  }

  bool memoryFull = true;

  // finds the first free address and begins to write there
  for (MemAddr = 1; MemAddr < 1024; MemAddr++) {
    if (EEPROM.read(MemAddr) == 255) {
      memoryFull = false;
      break;
    }
  }

  if (memoryFull) {
      memoryLock();
  }

  // cache last taken measurements
  if (MemAddr < 3) {
    interrupts();
    return;
  }
  
  readLight = EEPROM.read(MemAddr - 3);
  readTemp = EEPROM.read(MemAddr - 2);
  readHum = EEPROM.read(MemAddr - 1);

  interrupts();
}

void memoryLock() {
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Memory full!");
    while(1) { digitalWrite(beepPin, HIGH); }
}

void printLastSaved() {
  lcd.setCursor(0,1);
  if (MemAddr < 3) {
    lcd.print("None");
    return;
  }
  
  lcd.print("L:");
  lcd.print(readLight);
  lcd.print(" T:");
  lcd.print(readTemp);
  lcd.print(" H:");
  lcd.print(readHum);

}