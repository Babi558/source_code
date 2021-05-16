#include <Adafruit_Sensor.h>
#include <DHT.h>

// Dht pin
#define DHTPIN 3
//Type of DTH
#define DHTTYPE DHT11

//For soil moisture
const int analogInPin = A0;

int sensorValue = 0; // value read from the pot
int soil_moisture = 0;

//Motor values
int on = 8;
int off = 9;

//DTH init
DHT dht = DHT(DHTPIN, DHTTYPE);

void setup()
{
  //delay(2000);
  Serial.begin(9600);
  dht.begin();
  pinMode(on, OUTPUT);
  pinMode(off, OUTPUT);
}

void loop()
{
  //Sensor values
  sensorValue = analogRead(analogInPin);
  soil_moisture = map(sensorValue, 0, 1023, 0, 100); //maps the adc values to 0 to 100%

  // Read the temperature as Celsius
  float temp_c = dht.readTemperature();

  //Read heat index
  float room_humid = dht.readHumidity();

  if (isnan(room_humid) || isnan(temp_c) || soil_moisture < 0)
  {
    Serial.println("Failed to read from DHT and moisture sensor!");
    return;
  }

  Serial.print(soil_moisture);
  Serial.print(" ");
  Serial.print(temp_c);
  Serial.print(" ");
  Serial.print(room_humid);
  Serial.print(" ");

  //Test case
  if (temp_c > 32 || room_humid > 45 || soil_moisture > 50)
  {
    //Pump on
    digitalWrite(on, HIGH);
    digitalWrite(off, LOW);
    Serial.print("ON");
    Serial.println();
    delay(1000);
  }
  else
  {
    //Pump off
    digitalWrite(on, LOW);
    digitalWrite(off, HIGH);
    Serial.print("OFF");
    Serial.println();
    delay(1000);
  }
}
