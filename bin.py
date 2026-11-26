// EXERCISE 4: LED FADE WITH POTENTIOMETER
// Question: Write a program to fade an LED (change its brightness) with a potentiometer using
//           Arduino Uno.
// Connections: LED anode -> 220 ohm resistor -> D11, LED cathode -> GND
//              Potentiometer outer pins -> 5V and GND, middle pin -> A1

#define LED_PIN 11            // PWM pin (marked ~11 on the board)
#define POTENTIOMETER_PIN A1  // middle pin of the potentiometer

void setup()
{
  pinMode(LED_PIN, OUTPUT);
}

void loop()
{
  int potentiometerValue = analogRead(POTENTIOMETER_PIN);  // 0 to 1023
  int brightness = potentiometerValue / 4;                 // 0 to 255
  analogWrite(LED_PIN, brightness);                        // PWM duty cycle
}


// EXERCISE 5: LED CHASER
// Question: Write a program for LED chasing (a light running back and forth along a row of LEDs)
//           using Arduino Uno.
// Connections: 10 LEDs: each anode -> 220 ohm resistor -> D4 ... D13, all cathodes -> GND

byte ledPin[] = {4, 5, 6, 7, 8, 9, 10, 11, 12, 13};  // the ten LED pins
int ledDelay = 65;          // milliseconds between steps
int direction = 1;          // +1 moves towards pin 13, -1 moves back towards pin 4
int currentLED = 0;         // index of the LED that is lit
unsigned long changeTime;   // time of the last step

void setup()
{
  for (int x = 0; x < 10; x++)
  {
    pinMode(ledPin[x], OUTPUT);
  }
  changeTime = millis();
}

void changeLED()
{
  for (int x = 0; x < 10; x++)             // switch every LED off
  {
    digitalWrite(ledPin[x], LOW);
  }
  digitalWrite(ledPin[currentLED], HIGH);   // light the current LED
  currentLED += direction;                  // move to its neighbour
  if (currentLED == 9)                      // reached the last LED
  {
    direction = -1;
  }
  if (currentLED == 0)                      // back at the first LED
  {
    direction = 1;
  }
}

void loop()
{
  if ((millis() - changeTime) > ledDelay)   // has 65 ms passed?
  {
    changeLED();
    changeTime = millis();
  }
}


// EXERCISE 6: ULTRASONIC DISTANCE MEASUREMENT
// Question: Write a program to measure distance with an ultrasonic sensor (HC-SR04) using
//           Arduino Uno.
// Connections: HC-SR04: VCC -> 5V, TRIG -> D3, ECHO -> D2, GND -> GND

#define echo 2
#define trig 3

long duration;   // echo time in microseconds
int distance;    // distance in centimetres

void setup()
{
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);          // 10 microsecond trigger pulse
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  duration = pulseIn(echo, HIGH);    // how long ECHO stayed HIGH
  distance = duration * 0.034 / 2;   // time to centimetres

  delay(500);
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println("cm");
}


// EXERCISE 7: SERVO MOTOR CONTROL
// Question: Write a program to control the position of a servo motor using a potentiometer and
//           Arduino Uno.
// Connections: Servo: red -> 5V, brown -> GND, orange (signal) -> D9
//              Potentiometer outer pins -> 5V and GND, middle pin -> A0

#include <Servo.h>

Servo myServo;
int potPin = A0;

void setup()
{
  myServo.attach(9);       // signal wire on pin 9
  Serial.begin(9600);
}

void loop()
{
  int potVal = analogRead(potPin);             // 0 to 1023
  int angle = map(potVal, 0, 1023, 0, 180);    // 0 to 180 degrees
  myServo.write(angle);
  Serial.print("Servo angle: ");
  Serial.println(angle);
  delay(15);                                   // let the servo reach the position
}


// EXERCISE 8: MOTION TRIGGERED ALARM
// Question: Design and implement a motion-triggered alarm system using a PIR sensor, buzzer, LED
//           and Arduino Uno.
// Connections: PIR: VCC -> 5V, OUT -> D7, GND -> GND
//              Buzzer + -> D8, buzzer - -> GND
//              LED anode -> 220 ohm resistor -> D13, LED cathode -> GND

const int PIR_PIN = 7;
const int BUZZER_PIN = 8;
const int LED_PIN = 13;

void setup()
{
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  delay(2000);                         // let the PIR sensor settle
  Serial.println("Alarm system armed!");
}

void loop()
{
  int motionDetected = digitalRead(PIR_PIN);

  if (motionDetected == HIGH)
  {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("MOTION DETECTED - ALARM!");
    tone(BUZZER_PIN, 1000, 500);       // 1000 Hz for 500 ms
    delay(600);
    tone(BUZZER_PIN, 1500, 500);       // 1500 Hz for 500 ms
    delay(600);
  }
  else
  {
    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);
  }
}


// EXERCISE 9: AUTOMATIC AC CONTROL BASED ON TEMPERATURE
// Question: Design an automatic temperature monitoring system using Arduino Uno and a TMP36
//           sensor, where an LED representing an air conditioner turns ON when the temperature
//           is above 25 C and OFF when it is 25 C or below.
// Connections: TMP36: left pin (+Vs) -> 5V, middle pin (Vout) -> A0, right pin -> GND
//              Green LED (AC ON) anode -> 220 ohm -> D8, red LED (AC OFF) anode -> 220 ohm -> D9, cathodes -> GND

const int tempPin = A0;
const int greenLED = 8;   // AC ON
const int redLED = 9;     // AC OFF

void setup()
{
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  int sensorValue = analogRead(tempPin);            // 0 to 1023
  float voltage = sensorValue * 5.0 / 1024.0;       // reading to volts
  float temperature = (voltage - 0.5) * 100.0;      // volts to degrees Celsius

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  if (temperature > 25)
  {
    digitalWrite(greenLED, HIGH);
    digitalWrite(redLED, LOW);
    Serial.println("AC Status: ON");
  }
  else
  {
    digitalWrite(greenLED, LOW);
    digitalWrite(redLED, HIGH);
    Serial.println("AC Status: OFF");
  }

  Serial.println("----------------");
  delay(1000);
}


# EXERCISE 10: TEMPERATURE AND HUMIDITY DATA ANALYSIS (GOOGLE COLAB)
# Question: Develop an IoT-based data monitoring system using a Temperature and Humidity
#           dataset. Import the dataset into Google Colab as a Pandas DataFrame, analyse the
#           data, and plot Temperature vs Time, Humidity vs Time and a combined graph.
# Run in Google Colab (Python). No circuit is needed.

# ---- Cell 1: libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- Cell 2: create a 24-hour dataset and save it as a CSV file
np.random.seed(42)                       # same "random" numbers every run
hours = np.arange(24)
time = pd.date_range("2026-10-18 00:00", periods=24, freq="h")
temperature = 26 + 5 * np.sin((hours - 9) * np.pi / 12) + np.random.normal(0, 0.5, 24)
humidity = 60 - 12 * np.sin((hours - 9) * np.pi / 12) + np.random.normal(0, 1.5, 24)

data = pd.DataFrame({
    "Time": time,
    "Temperature": temperature.round(1),
    "Humidity": humidity.round(1),
})
data.to_csv("temp_humidity.csv", index=False)

# ---- Cell 3: import the CSV into a Pandas DataFrame and check it
df = pd.read_csv("temp_humidity.csv", parse_dates=["Time"])
print(df.head(10))
print(df.shape)
print(df.describe())

# ---- Cell 4: Temperature vs Time
plt.figure(figsize=(10, 4))
plt.plot(df["Time"], df["Temperature"], color="red", marker="o")
plt.title("Temperature vs Time")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# ---- Cell 5: Humidity vs Time
plt.figure(figsize=(10, 4))
plt.plot(df["Time"], df["Humidity"], color="blue", marker="s")
plt.title("Humidity vs Time")
plt.xlabel("Time")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# ---- Cell 6: combined graph
plt.figure(figsize=(10, 4))
plt.plot(df["Time"], df["Temperature"], color="red", marker="o", label="Temperature (°C)")
plt.plot(df["Time"], df["Humidity"], color="blue", marker="s", label="Humidity (%)")
plt.title("Temperature and Humidity vs Time")
plt.xlabel("Time")
plt.ylabel("Value")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ---- Cell 7: analyse the trends
print("Average temperature:", round(df["Temperature"].mean(), 1), "°C")
print("Highest temperature:", df["Temperature"].max(), "°C at", df.loc[df["Temperature"].idxmax(), "Time"])
print("Lowest temperature :", df["Temperature"].min(), "°C at", df.loc[df["Temperature"].idxmin(), "Time"])
print("Average humidity   :", round(df["Humidity"].mean(), 1), "%")
print("Correlation (T, H) :", round(df["Temperature"].corr(df["Humidity"]), 2))
