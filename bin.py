// ==============================================================================
// EX4: FADE AN LED WITH A POTENTIOMETER
// Question: Turn the pot and the LED gets brighter or dimmer. The Arduino reads 0 to 1023 and
//           writes 0 to 255 as PWM.
// Connections: 5V -> Potentiometer: end 1
//              A0 -> Potentiometer: wiper (middle)
//              GND -> Potentiometer: end 2
//              D9 (~) -> LED + 220 Ω: anode (+) via 220 Ω
//              GND -> LED + 220 Ω: cathode (−)
// ==============================================================================

// Ex4: Fade LED brightness with a potentiometer
const int LED_PIN = 9;        // PWM pin (marked ~)
const int POT_PIN = A0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int potValue = analogRead(POT_PIN);   // 0..1023
  int brightness = potValue / 4;        // 0..255
  analogWrite(LED_PIN, brightness);
}


// ==============================================================================
// EX5: LED CHASER
// Question: Six LEDs light one after another, bounce back at the ends, and the speed is set by
//           one delay value.
// Connections: D2 -> 6 LEDs (220 Ω each): LED1 anode
//              D3 -> 6 LEDs (220 Ω each): LED2 anode
//              D4 -> 6 LEDs (220 Ω each): LED3 anode
//              D5 -> 6 LEDs (220 Ω each): LED4 anode
//              D6 -> 6 LEDs (220 Ω each): LED5 anode
//              D7 -> 6 LEDs (220 Ω each): LED6 anode
//              GND -> 6 LEDs (220 Ω each): all cathodes
// ==============================================================================

// Ex5: LED chaser - light bounces left <-> right (millis, no delay)
int ledPin[] = {2, 3, 4, 5, 6, 7};
int ledDelay = 100;            // ms: chase speed
int direction = 1;             // +1 right, -1 left
int currentLED = 0;
unsigned long changeTime;

void setup() {
  for (int x = 0; x < 6; x++) pinMode(ledPin[x], OUTPUT);
  changeTime = millis();
}

void changeLED() {
  for (int x = 0; x < 6; x++) digitalWrite(ledPin[x], LOW);  // all off
  digitalWrite(ledPin[currentLED], HIGH);                     // current on
  currentLED += direction;
  if (currentLED == 5) direction = -1;   // right end
  if (currentLED == 0) direction = 1;    // left end
}

void loop() {
  if ((millis() - changeTime) > ledDelay) {
    changeLED();
    changeTime = millis();
  }
}


// ==============================================================================
// EX6: DISTANCE WITH AN ULTRASONIC SENSOR (HC-SR04)
// Question: Send a 10 µs pulse on TRIG, measure how long ECHO stays HIGH, and convert it to
//           centimetres.
// Connections: 5V -> HC-SR04: VCC
//              D9 -> HC-SR04: TRIG
//              D10 -> HC-SR04: ECHO
//              GND -> HC-SR04: GND
// ==============================================================================

// Ex6: Distance with HC-SR04
const int trig = 9;
const int echo = 10;
long duration;
float distance;

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trig, LOW);  delayMicroseconds(2);
  digitalWrite(trig, HIGH); delayMicroseconds(10);  // 10 us pulse
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2;     // cm
  delay(500);
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
}


// ==============================================================================
// EX7: SERVO CONTROLLED BY A POTENTIOMETER
// Question: Turn the pot to rotate the servo between 0° and 180°, and print the angle on the
//           Serial Monitor.
// Connections: 5V -> Potentiometer: end 1
//              A0 -> Potentiometer: wiper (middle)
//              GND -> Potentiometer: end 2
//              5V -> Micro servo: red (V+)
//              D9 (~) -> Micro servo: signal (orange)
//              GND -> Micro servo: brown (GND)
// ==============================================================================

// Servo motor control with a potentiometer (program from the Lab 3 handout, Exercise 7)
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


// ==============================================================================
// EX7 ADVANCED: SERVO MOTOR CONTROLLED BY TWO PUSH BUTTONS (4-leg buttons)
// Question: Write a program to control the position of a servo motor with two push buttons.
//           One button turns the servo towards 180 degrees and the other towards 0 degrees in
//           15 degree steps. Holding a button keeps the servo moving, and pressing both
//           together returns it to the centre (90 degrees). Show the angle on the Serial Monitor.
// Connections: Servo: red -> 5V, brown -> GND, orange (signal) -> D9
//              Button 1: one leg -> D2, the diagonally opposite leg -> GND
//              Button 2: one leg -> D3, the diagonally opposite leg -> GND
//              No resistors needed: the Arduino's internal pull-up resistors are used.
// ==============================================================================

#include <Servo.h>

const int SERVO_PIN = 9;
const int BTN_UP = 2;                  // turns towards 180 degrees
const int BTN_DOWN = 3;                // turns towards 0 degrees
const int STEP = 15;                   // degrees moved per step
const unsigned long REPEAT_MS = 200;   // time between steps (also removes button bounce)

Servo myServo;
int angle = 90;                        // start at the centre
unsigned long lastMove = 0;

void setup()
{
  pinMode(BTN_UP, INPUT_PULLUP);       // pin reads HIGH normally, LOW when pressed
  pinMode(BTN_DOWN, INPUT_PULLUP);
  myServo.attach(SERVO_PIN);
  myServo.write(angle);
  Serial.begin(9600);
  Serial.println("Servo ready at 90 degrees");
}

void loop()
{
  bool upPressed = digitalRead(BTN_UP) == LOW;
  bool downPressed = digitalRead(BTN_DOWN) == LOW;

  if ((upPressed || downPressed) && millis() - lastMove >= REPEAT_MS)
  {
    if (upPressed && downPressed)
    {
      angle = 90;                      // both buttons: back to the centre
    }
    else if (upPressed)
    {
      angle = angle + STEP;
    }
    else
    {
      angle = angle - STEP;
    }

    angle = constrain(angle, 0, 180);  // never go past the servo's limits
    myServo.write(angle);
    lastMove = millis();

    Serial.print("Servo angle: ");
    Serial.println(angle);
  }
}


// ==============================================================================
// EX8: MOTION-TRIGGERED ALARM
// Question: When the PIR sensor sees motion, the LED turns on, the buzzer beeps two tones, and
//           the Serial Monitor prints an alarm message.
// Connections: 5V -> PIR sensor: VCC
//              D7 -> PIR sensor: OUT
//              GND -> PIR sensor: GND
//              D8 -> Piezo buzzer: +
//              GND -> Piezo buzzer: −
//              D12 -> LED + 220 Ω: anode via 220 Ω
//              GND -> LED + 220 Ω: cathode
// ==============================================================================

// Ex8: Motion triggered alarm (PIR + buzzer + LED)
const int PIR_PIN = 7;
const int BUZZER_PIN = 8;
const int LED_PIN = 12;

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int motionDetected = digitalRead(PIR_PIN);
  if (motionDetected == HIGH) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("MOTION DETECTED - ALARM!");
    tone(BUZZER_PIN, 1000, 500); delay(600);
    tone(BUZZER_PIN, 1500, 500); delay(600);
  } else {
    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);
  }
}


// ==============================================================================
// EX9: AUTOMATIC AC CONTROL WITH COLAB GRAPH
// Question: Read temperature with a TMP36. Above 25 °C the green LED (AC ON) lights, otherwise
//           the red LED (AC OFF) lights. Then plot the readings in Colab, with temperature and
//           humidity together.
// Connections: 5V -> TMP36: left (Vs)
//              A0 -> TMP36: middle (Vout)
//              GND -> TMP36: right (GND)
//              D8 -> Green LED (AC ON): anode via 220 Ω
//              GND -> Green LED (AC ON): cathode
//              D9 -> Red LED (AC OFF): anode via 220 Ω
//              GND -> Red LED (AC OFF): cathode
// ==============================================================================

// Ex9: Automatic AC control. T > 25 C -> AC ON (green), else OFF (red)
const int TEMP_PIN = A0;
const int GREEN_LED = 8;   // AC ON
const int RED_LED   = 9;   // AC OFF
const float THRESHOLD = 25.0;

void setup() {
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  Serial.begin(9600);
  Serial.println("time_s,temp_C,ac");       // CSV header
}

void loop() {
  int raw = analogRead(TEMP_PIN);
  float voltage = raw * 5.0 / 1024.0;
  float tempC = (voltage - 0.5) * 100.0;    // TMP36

  int ac = (tempC > THRESHOLD);
  digitalWrite(GREEN_LED, ac ? HIGH : LOW);
  digitalWrite(RED_LED,   ac ? LOW : HIGH);

  Serial.print(millis() / 1000);
  Serial.print(",");
  Serial.print(tempC, 1);
  Serial.print(",");
  Serial.println(ac);
  delay(1000);
}


# ==============================================================================
# COLAB: TEMPERATURE AND HUMIDITY GRAPHS (EX9, EX10)
# Question: The five Colab steps: build or read the data, put it in a DataFrame, plot
#           temperature, plot humidity, then plot both together with two y-axes.
# ==============================================================================

# Google Colab: Temperature & Humidity analysis (Ex9 graph / Ex10)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# paste Tinkercad Serial Monitor temperatures here, one per line
serial_temp = """24.7
25.2
26.1
27.4
28.0
27.1
26.3
25.6
24.9
24.2"""

temp = [float(x) for x in serial_temp.split()]
n = len(temp)
np.random.seed(1)
humidity = np.round(np.random.uniform(40, 80, n), 1)   # simulated humidity

df = pd.DataFrame({"Time": range(1, n + 1),
                   "Temperature": temp, "Humidity": humidity})
df.to_csv("sensor_data.csv", index=False)

# Ex10 variant: read an uploaded CSV instead
# from google.colab import files; files.upload()
# df = pd.read_csv("sensor_data.csv")

print(df.head())
print("Avg Temp:", df.Temperature.mean(), "Max Temp:", df.Temperature.max())
print("Avg Hum :", df.Humidity.mean(),    "Max Hum :", df.Humidity.max())

# 1) Temperature vs Time
plt.figure(figsize=(7, 4))
plt.plot(df.Time, df.Temperature, marker="o", color="red")
plt.title("Temperature vs Time"); plt.xlabel("Time (s)")
plt.ylabel("Temperature (C)"); plt.grid(True); plt.show()

# 2) Humidity vs Time
plt.figure(figsize=(7, 4))
plt.plot(df.Time, df.Humidity, marker="s", color="blue")
plt.title("Humidity vs Time"); plt.xlabel("Time (s)")
plt.ylabel("Humidity (%)"); plt.grid(True); plt.show()

# 3) COMBINED (Ma'am asked for this)
fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(df.Time, df.Temperature, "r-o", label="Temperature (C)")
ax1.set_xlabel("Time (s)"); ax1.set_ylabel("Temperature (C)", color="red")
ax2 = ax1.twinx()                                       # second y-axis
ax2.plot(df.Time, df.Humidity, "b-s", label="Humidity (%)")
ax2.set_ylabel("Humidity (%)", color="blue")
plt.title("Temperature and Humidity vs Time")
fig.legend(loc="upper right", bbox_to_anchor=(0.88, 0.88)); ax1.grid(True)
plt.show()


// ==============================================================================
// ASSIGNMENT 1: SMART STREET LIGHT SYSTEM
// Question: Detect day and night with an LDR. The street-light LED turns ON in darkness and OFF
//           in daylight, and the code also reports the energy saved.
// Connections: 5V -> LDR + 10 kΩ divider: LDR top → 5V
//              A0 -> LDR + 10 kΩ divider: junction (LDR + 10k)
//              GND -> LDR + 10 kΩ divider: 10 kΩ bottom → GND
//              D9 (~) -> LED + 220 Ω: anode via 220 Ω
//              GND -> LED + 220 Ω: cathode
// ==============================================================================

// A1: Smart street light. LDR + 10k divider on A0, street-light LED on D9.
const int LDR = A0, LED = 9;
const int DARK = 400;
unsigned long onMs = 0, totalMs = 0, last;

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
  last = millis();
}

void loop() {
  int light = analogRead(LDR);          // low = dark, high = bright
  bool dark = (light < DARK);
  digitalWrite(LED, dark ? HIGH : LOW); // ON at night, OFF in daylight

  unsigned long now = millis(), dt = now - last; last = now;
  totalMs += dt;
  if (dark) onMs += dt;                 // time the lamp was ON

  Serial.print("Light: "); Serial.print(light);
  Serial.print(dark ? "  NIGHT  LED ON" : "  DAY    LED OFF");
  Serial.print("  | Energy saved: ");
  Serial.print(100.0 * (totalMs - onMs) / totalMs, 0);
  Serial.println("%");
  delay(500);
}


// ==============================================================================
// ASSIGNMENT 2: MOTION DETECTION SECURITY ALARM
// Question: Detect motion with a PIR sensor, turn on the buzzer and warning LED, and print an
//           alert on the Serial Monitor.
// Connections: 5V -> PIR sensor: VCC
//              D2 -> PIR sensor: OUT
//              GND -> PIR sensor: GND
//              D8 -> Piezo buzzer: +
//              GND -> Piezo buzzer: −
//              D13 -> LED + 220 Ω: anode via 220 Ω
//              GND -> LED + 220 Ω: cathode
// ==============================================================================

// A2: Motion detection security alarm. PIR OUT D2, buzzer D8, warning LED D13.
const int PIR = 2, BUZZ = 8, LED = 13;

void setup() {
  pinMode(PIR, INPUT);
  pinMode(BUZZ, OUTPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
  Serial.println("Security system armed");
}

void loop() {
  if (digitalRead(PIR) == HIGH) {
    digitalWrite(LED, HIGH);
    tone(BUZZ, 1500);
    Serial.println("ALERT: Intruder detected!");
  } else {
    digitalWrite(LED, LOW);
    noTone(BUZZ);
  }
  delay(200);
}


// ==============================================================================
// ASSIGNMENT 3: SMART REFRIGERATOR MONITORING SYSTEM
// Question: Monitor fridge temperature. Safe range is 0 to 4 °C: green LED = SAFE, yellow = TOO
//           COLD (slow beep), red = TOO WARM (fast beep).
// Connections: 5V -> TMP36: left (Vs)
//              A0 -> TMP36: middle (Vout)
//              GND -> TMP36: right (GND)
//              D2 -> Green LED (SAFE): anode via 220 Ω
//              GND -> Green LED (SAFE): cathode
//              D3 -> Yellow LED (TOO COLD): anode via 220 Ω
//              GND -> Yellow LED (TOO COLD): cathode
//              D4 -> Red LED (TOO WARM): anode via 220 Ω
//              GND -> Red LED (TOO WARM): cathode
//              D8 -> Piezo buzzer: +
//              GND -> Piezo buzzer: −
// ==============================================================================

const int SENSOR_PIN = A0;
const int GREEN_LED = 2;
const int YELLOW_LED = 3;
const int RED_LED = 4;
const int BUZZER = 8;

const float SAFE_MIN = 0.0;
const float SAFE_MAX = 4.0;
const float HYSTERESIS = 0.5;

const int SAFE = 0;
const int TOO_COLD = 1;
const int TOO_WARM = 2;

int state = SAFE;
unsigned long lastRead = 0;

float readTempC() {
  long sum = 0;
  for (int i = 0; i < 10; i++) {
    sum += analogRead(SENSOR_PIN);
    delay(5);
  }
  float v = (sum / 10.0) * 5.0 / 1024.0;
  return (v - 0.5) * 100.0;
}

int classify(float t, int cur) {
  if (t > SAFE_MAX) return TOO_WARM;
  if (t < SAFE_MIN) return TOO_COLD;
  if (cur == TOO_WARM && t > SAFE_MAX - HYSTERESIS) return TOO_WARM;
  if (cur == TOO_COLD && t < SAFE_MIN + HYSTERESIS) return TOO_COLD;
  return SAFE;
}

void setup() {
  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  Serial.begin(9600);
  Serial.println("Smart Refrigerator Monitor started");
}

void loop() {
  unsigned long now = millis();

  if (now - lastRead >= 1000) {
    lastRead = now;
    float t = readTempC();
    state = classify(t, state);
    Serial.print("Temperature: ");
    Serial.print(t, 1);
    Serial.print(" C  Status: ");
    if (state == SAFE) Serial.println("SAFE");
    else if (state == TOO_COLD) Serial.println("TOO COLD");
    else Serial.println("UNSAFE - TOO WARM");
  }

  boolean fast = (now / 250) % 2;
  boolean slow = (now / 1000) % 2;

  digitalWrite(GREEN_LED, state == SAFE ? HIGH : LOW);
  digitalWrite(YELLOW_LED, state == TOO_COLD ? HIGH : LOW);
  digitalWrite(RED_LED, (state == TOO_WARM && fast) ? HIGH : LOW);

  if (state == TOO_WARM && fast) tone(BUZZER, 2000);
  else if (state == TOO_COLD && slow) tone(BUZZER, 1000);
  else noTone(BUZZER);
}


// ==============================================================================
// ASSIGNMENT 4: SMART WATER TANK LEVEL MONITORING
// Question: Measure the distance to the water surface with an ultrasonic sensor and show Full,
//           Medium or Empty with LEDs.
// Connections: 5V -> HC-SR04: VCC
//              D9 -> HC-SR04: TRIG
//              D10 -> HC-SR04: ECHO
//              GND -> HC-SR04: GND
//              D5 -> Green LED (FULL): anode via 220 Ω
//              GND -> Green LED (FULL): cathode
//              D6 -> Yellow LED (MEDIUM): anode via 220 Ω
//              GND -> Yellow LED (MEDIUM): cathode
//              D7 -> Red LED (EMPTY): anode via 220 Ω
//              GND -> Red LED (EMPTY): cathode
// ==============================================================================

// A4: Water tank level. Ultrasonic on top of the tank: small distance = full tank.
// TRIG D9, ECHO D10. LEDs: green D5 (FULL), yellow D6 (MEDIUM), red D7 (EMPTY)
const int trig = 9, echo = 10, G = 5, Y = 6, R = 7;

void setup() {
  pinMode(trig, OUTPUT); pinMode(echo, INPUT);
  pinMode(G, OUTPUT); pinMode(Y, OUTPUT); pinMode(R, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trig, LOW);  delayMicroseconds(2);
  digitalWrite(trig, HIGH); delayMicroseconds(10);
  digitalWrite(trig, LOW);
  float d = pulseIn(echo, HIGH) * 0.034 / 2;     // cm
  digitalWrite(G, d < 10);
  digitalWrite(Y, d >= 10 && d <= 20);
  digitalWrite(R, d > 20);
  Serial.print("Distance: "); Serial.print(d);
  Serial.println(d < 10 ? " cm  FULL" : (d <= 20 ? " cm  MEDIUM" : " cm  EMPTY"));
  delay(500);
}


// ==============================================================================
// ASSIGNMENT 5: SERVO CONTROL WITH A POTENTIOMETER
// Question: Read the potentiometer, map the value to a servo angle, and display the current
//           angle on the Serial Monitor.
// ==============================================================================

// Servo motor control with a potentiometer (program from the Lab 3 handout, Exercise 7)
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


# ==============================================================================
# ASSIGNMENT 6: CSV TEMPERATURE AND HUMIDITY ANALYSIS IN COLAB
# Question: Import a CSV into a Pandas DataFrame, plot temperature vs time and humidity vs time,
#           and calculate average and maximum values.
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# If you were given a CSV, upload it:  from google.colab import files; files.upload()
# Otherwise create a sample one:
np.random.seed(2)
pd.DataFrame({"Time": range(1, 21),
              "Temperature": np.round(np.random.uniform(22, 34, 20), 1),
              "Humidity": np.round(np.random.uniform(40, 80, 20), 1)}).to_csv("data.csv", index=False)

df = pd.read_csv("data.csv")            # import CSV -> Pandas DataFrame
print(df.head())
df.info()

plt.plot(df.Time, df.Temperature, "r-o")
plt.title("Temperature vs Time"); plt.xlabel("Time"); plt.ylabel("Temperature (C)")
plt.grid(True); plt.show()

plt.plot(df.Time, df.Humidity, "b-s")
plt.title("Humidity vs Time"); plt.xlabel("Time"); plt.ylabel("Humidity (%)")
plt.grid(True); plt.show()

print("Average Temp:", df.Temperature.mean(), " Max Temp:", df.Temperature.max())
print("Average Humidity:", df.Humidity.mean(), " Max Humidity:", df.Humidity.max())


// ==============================================================================
// ASSIGNMENT 7: SMART FAN AUTOMATION SYSTEM (DC MOTOR)
// Question: Monitor temperature, turn the fan motor ON above 30 °C, and OFF when the temperature
//           falls below the threshold.
// Connections: 5V -> TMP36: left (Vs)
//              A0 -> TMP36: middle (Vout)
//              GND -> TMP36: right (GND)
//              D8 -> NPN transistor: Base (via 1 kΩ)
//              GND -> NPN transistor: Emitter
//              5V -> DC motor (fan): terminal 1
//              5V -> Diode across motor: stripe (cathode)
// ==============================================================================

// A7: Smart fan. TMP36 on A0. D8 -> 1k -> NPN base; motor between 5V and collector.
// Fan ON above 30 C, OFF below. Prints CSV for Colab.
const int FAN = 8;
const float THRESHOLD = 30.0;

void setup() {
  pinMode(FAN, OUTPUT);              // A0 needs no pinMode
  Serial.begin(9600);
  Serial.println("time_s,temp_c,fan");
}

void loop() {
  float temp = (analogRead(A0) * 5.0 / 1024.0 - 0.5) * 100.0;
  int fan = temp > THRESHOLD;        // 1 = ON, 0 = OFF
  digitalWrite(FAN, fan);            // HIGH turns the transistor (and motor) ON

  Serial.print(millis() / 1000); Serial.print(",");
  Serial.print(temp, 1);         Serial.print(",");
  Serial.println(fan);
  delay(1000);
}


# ==============================================================================
# ASSIGNMENT 8: ENVIRONMENTAL DASHBOARD IN COLAB
# Question: Generate or import temperature and humidity data, plot graphs with Matplotlib,
#           display summary statistics, and write a simple environmental monitoring report.
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(3)
n = 30
df = pd.DataFrame({"Time": range(1, n + 1),
                   "Temperature": np.round(np.random.uniform(22, 36, n), 1),
                   "Humidity": np.round(np.random.uniform(35, 80, n), 1)})

fig, ax = plt.subplots(2, 2, figsize=(11, 7))          # the dashboard
ax[0, 0].plot(df.Time, df.Temperature, "r-o"); ax[0, 0].set_title("Temperature")
ax[0, 1].plot(df.Time, df.Humidity, "b-s");    ax[0, 1].set_title("Humidity")
ax[1, 0].scatter(df.Temperature, df.Humidity); ax[1, 0].set_title("Temperature vs Humidity")
ax[1, 0].set_xlabel("Temp (C)"); ax[1, 0].set_ylabel("Humidity (%)")
ax[1, 1].hist(df.Temperature, bins=6, color="orange"); ax[1, 1].set_title("Temperature distribution")
for a in ax.flat: a.grid(True)
plt.tight_layout(); plt.show()

print(df.describe())                                    # summary statistics
print("---- ENVIRONMENTAL REPORT ----")
print("Average temperature:", round(df.Temperature.mean(), 1), "C, max", df.Temperature.max())
print("Average humidity   :", round(df.Humidity.mean(), 1), "%, min", df.Humidity.min())
print("Readings above 30 C:", (df.Temperature > 30).sum(), "of", n)


// ==============================================================================
// ASSIGNMENT 9: SMART GREENHOUSE MONITORING SYSTEM
// Question: Use simulated temperature and humidity values, define alert thresholds, and raise
//           alerts when conditions leave the safe limits (temperature above 35 °C, humidity
//           below 40 %).
// Connections: 5V -> TMP36: left (Vs)
//              A0 -> TMP36: middle (Vout)
//              GND -> TMP36: right (GND)
//              5V -> Potentiometer (humidity): end 1
//              A1 -> Potentiometer (humidity): wiper (middle)
//              GND -> Potentiometer (humidity): end 2
//              D8 -> Red LED (TEMP alert): anode via 220 Ω
//              GND -> Red LED (TEMP alert): cathode
//              D9 -> Yellow LED (HUMIDITY alert): anode via 220 Ω
//              GND -> Yellow LED (HUMIDITY alert): cathode
// ==============================================================================

// A9: Smart greenhouse. TMP36 on A0, pot on A1 = simulated humidity (0..100 %).
// Red LED D8 = temperature alert (T > 35 C). Yellow LED D9 = humidity alert (H < 40 %).
const int TEMP_ALERT = 8, HUM_ALERT = 9;
const float TEMP_MAX = 35.0;
const int   HUM_MIN  = 40;

void setup() {
  pinMode(TEMP_ALERT, OUTPUT);
  pinMode(HUM_ALERT, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  float t = (analogRead(A0) * 5.0 / 1024.0 - 0.5) * 100.0;
  int h = map(analogRead(A1), 0, 1023, 0, 100);

  bool hot = (t > TEMP_MAX);
  bool dry = (h < HUM_MIN);
  digitalWrite(TEMP_ALERT, hot);
  digitalWrite(HUM_ALERT, dry);

  Serial.print("Temp: "); Serial.print(t, 1);
  Serial.print(" C  Humidity: "); Serial.print(h); Serial.print(" %");
  if (hot) Serial.print("  ALERT: too hot");
  if (dry) Serial.print("  ALERT: too dry");
  Serial.println();
  delay(1000);
}


# ==============================================================================
# ASSIGNMENT 10: CLOUD-BASED IOT DATA LOGGER
# Question: Generate 100 temperature and humidity readings in Colab, store them in a CSV file,
#           upload to Google Sheets, and create charts and observations.
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(0)
df = pd.DataFrame({"Time": range(1, 101),               # 100 readings
                   "Temperature": np.round(np.random.uniform(20, 35, 100), 1),
                   "Humidity": np.round(np.random.uniform(40, 80, 100), 1)})
df.to_csv("sensor_log.csv", index=False)                # store in CSV

# Upload to Google Sheets: from google.colab import files; files.download("sensor_log.csv")
# then open Google Sheets > File > Import > Upload.
print(df.describe())

fig, ax1 = plt.subplots(figsize=(9, 4))                 # chart
ax1.plot(df.Time, df.Temperature, "r");  ax1.set_ylabel("Temperature (C)", color="red")
ax2 = ax1.twinx()
ax2.plot(df.Time, df.Humidity, "b");     ax2.set_ylabel("Humidity (%)", color="blue")
ax1.set_xlabel("Reading no."); plt.title("100 logged readings"); ax1.grid(True); plt.show()

print("Observation: temperature ranged from", df.Temperature.min(), "to", df.Temperature.max(),
      "and humidity from", df.Humidity.min(), "to", df.Humidity.max())


// ==============================================================================
// MINI PROJECT: SMART HOME MONITORING SYSTEM
// Question: Integrate temperature monitoring, motion detection, smart lighting and AC/fan
//           control, and show the live status on an LCD. Deliverables: circuit diagram, program
//           code, simulation screenshot, flowchart, experimental results, conclusion.
// Connections: 5V -> TMP36: left (Vs)
//              A0 -> TMP36: middle (Vout)
//              GND -> TMP36: right (GND)
//              5V -> LDR + 10 kΩ divider: LDR top → 5V
//              A1 -> LDR + 10 kΩ divider: junction
//              GND -> LDR + 10 kΩ divider: 10 kΩ bottom → GND
//              5V -> PIR sensor: VCC
//              D2 -> PIR sensor: OUT
//              GND -> PIR sensor: GND
//              5V -> LCD 16×2 I2C: VCC
//              GND -> LCD 16×2 I2C: GND
//              A4 -> LCD 16×2 I2C: SDA
//              A5 -> LCD 16×2 I2C: SCL
//              D4 -> AC LED + 220 Ω: anode
//              GND -> AC LED + 220 Ω: cathode
//              D5 (~) -> Fan motor via NPN: NPN base (via 1 kΩ)
//              GND -> Fan motor via NPN: emitter → GND
//              D8 -> Motion LED + 220 Ω: anode
//              GND -> Motion LED + 220 Ω: cathode
//              D9 (~) -> Room light LED + 220 Ω: anode
//              GND -> Room light LED + 220 Ω: cathode
// ==============================================================================

/*
  Smart Home Monitoring System
  Board  : Arduino Uno R3 (Tinkercad)
  Inputs : TMP36 (A0), LDR (A1), PIR (D2)
  Outputs: LCD 16x2 I2C (A4/A5), Room light LED (D9),
           Motion LED (D8), AC LED (D4), Fan motor via NPN (D5)
*/

#include <Adafruit_LiquidCrystal.h>

// ----- Pin map -----
const int TEMP_PIN   = A0;
const int LDR_PIN    = A1;
const int PIR_PIN    = 2;
const int AC_PIN     = 4;
const int FAN_PIN    = 5;    // PWM
const int MOTION_LED = 8;
const int LIGHT_PIN  = 9;    // PWM

// ----- Settings -----
const int FAN_ON_TEMP = 25;                  // fan starts at this temperature (C)
const int AC_ON_TEMP  = 30;                  // AC starts at this temperature (C)
const int DARK_LEVEL  = 400;                 // LDR reading below this = dark
const unsigned long LIGHT_HOLD_MS = 10000;   // light stays on 10 s after last motion

Adafruit_LiquidCrystal lcd(0);               // I2C address 0x20 (Tinkercad default)

bool occupied = false;
unsigned long lastMotionTime = 0;

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(AC_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(MOTION_LED, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);

  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.setBacklight(1);
  lcd.print("Smart Home");
  lcd.setCursor(0, 1);
  lcd.print("Starting...");
  delay(1500);
}

void loop() {
  // 1. Read sensors
  int tempRaw = analogRead(TEMP_PIN);
  float tempC = (tempRaw * 5.0 / 1024.0 - 0.5) * 100.0;  // TMP36: 10 mV per C, 0.5 V offset
  int lightLevel = analogRead(LDR_PIN);                  // low = dark, high = bright
  bool motion = (digitalRead(PIR_PIN) == HIGH);

  // 2. Motion detection: room stays occupied for 10 s after last motion
  if (motion) {
    occupied = true;
    lastMotionTime = millis();
  } else if (occupied && millis() - lastMotionTime > LIGHT_HOLD_MS) {
    occupied = false;
  }
  digitalWrite(MOTION_LED, motion ? HIGH : LOW);

  // 3. Smart lighting: ON only when the room is occupied AND dark
  int brightness = 0;
  if (occupied && lightLevel < DARK_LEVEL) {
    brightness = map(lightLevel, 0, DARK_LEVEL, 255, 60);  // darker room = brighter light
  }
  analogWrite(LIGHT_PIN, brightness);

  // 4. AC / fan control
  int fanSpeed = 0;        // PWM value 0-255
  bool acOn = false;
  if (tempC >= AC_ON_TEMP) {
    fanSpeed = 255;
    acOn = true;
  } else if (tempC >= FAN_ON_TEMP) {
    fanSpeed = map((long)tempC, FAN_ON_TEMP, AC_ON_TEMP, 120, 255);  // faster as it gets hotter
  }
  analogWrite(FAN_PIN, fanSpeed);
  digitalWrite(AC_PIN, acOn ? HIGH : LOW);
  int fanPercent = fanSpeed * 100L / 255;

  // 5. Show status on LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(tempC, 1);
  lcd.print("C  M:");
  lcd.print(motion ? "YES" : "NO");
  lcd.setCursor(0, 1);
  lcd.print(brightness > 0 ? "L:ON  " : "L:OFF ");
  lcd.print("F:");
  lcd.print(fanPercent);
  lcd.print("% ");
  lcd.print(acOn ? "AC" : "");

  // 6. Log readings to Serial Monitor (used for Experimental Results)
  Serial.print("Temp: ");         Serial.print(tempC, 1);
  Serial.print(" C | Light: ");   Serial.print(lightLevel);
  Serial.print(" | Motion: ");    Serial.print(motion ? "YES" : "NO");
  Serial.print(" | Room: ");      Serial.print(occupied ? "Occupied" : "Empty");
  Serial.print(" | Lamp PWM: ");  Serial.print(brightness);
  Serial.print(" | Fan: ");       Serial.print(fanPercent);
  Serial.print("% | AC: ");       Serial.println(acOn ? "ON" : "OFF");

  delay(500);
}


// ==============================================================================
// PRACTICE D1 · FAN AUTOMATION (> 30 °C)
// Question: Fan automation (> 30 °C). Built from: Ex9 with one LED/motor.
// ==============================================================================

// Fan ON above 30 C, OFF below. TMP36 on A0, fan LED on D8.
const int TEMP_PIN = A0, FAN = 8;
void setup() { pinMode(FAN, OUTPUT); Serial.begin(9600); }
void loop() {
  float t = (analogRead(TEMP_PIN) * 5.0 / 1024.0 - 0.5) * 100.0;
  digitalWrite(FAN, t > 30.0 ? HIGH : LOW);
  Serial.print("Temp: "); Serial.print(t, 1);
  Serial.println(t > 30.0 ? " C  FAN ON" : " C  FAN OFF");
  delay(1000);
}


// ==============================================================================
// PRACTICE D2 · WATER TANK LEVEL (FULL / MEDIUM / EMPTY)
// Question: Water tank level (Full / Medium / Empty). Built from: Ex6 + three LEDs.
// ==============================================================================

// Ultrasonic on top of tank: small distance = full tank.
// TRIG D9, ECHO D10. LEDs: green D5 (FULL), yellow D6 (MEDIUM), red D7 (EMPTY)
const int trig = 9, echo = 10, G = 5, Y = 6, R = 7;
void setup() {
  pinMode(trig, OUTPUT); pinMode(echo, INPUT);
  pinMode(G, OUTPUT); pinMode(Y, OUTPUT); pinMode(R, OUTPUT);
  Serial.begin(9600);
}
void loop() {
  digitalWrite(trig, LOW);  delayMicroseconds(2);
  digitalWrite(trig, HIGH); delayMicroseconds(10);
  digitalWrite(trig, LOW);
  float d = pulseIn(echo, HIGH) * 0.034 / 2;
  digitalWrite(G, d < 10);
  digitalWrite(Y, d >= 10 && d <= 20);
  digitalWrite(R, d > 20);
  Serial.print("Distance: "); Serial.print(d);
  Serial.println(d < 10 ? " cm  FULL" : (d <= 20 ? " cm  MEDIUM" : " cm  EMPTY"));
  delay(500);
}


// ==============================================================================
// PRACTICE D3 · GREENHOUSE (T > 35 °C, HUMIDITY < 40 %)
// Question: Greenhouse (T > 35 °C, humidity < 40 %). Built from: Ex9 + a pot as humidity.
// ==============================================================================

// TMP36 on A0. Pot on A1 stands in for humidity (0..100 %).
// Fan LED D8 when T > 35 C. Pump LED D9 when humidity < 40 %.
const int FAN = 8, PUMP = 9;
void setup() { pinMode(FAN, OUTPUT); pinMode(PUMP, OUTPUT); Serial.begin(9600);
  Serial.println("time_s,temp_C,humidity"); }
void loop() {
  float t = (analogRead(A0) * 5.0 / 1024.0 - 0.5) * 100.0;
  int h = map(analogRead(A1), 0, 1023, 0, 100);
  digitalWrite(FAN,  t > 35.0 ? HIGH : LOW);
  digitalWrite(PUMP, h < 40 ? HIGH : LOW);
  Serial.print(millis() / 1000); Serial.print(",");
  Serial.print(t, 1); Serial.print(","); Serial.println(h);
  delay(1000);
}


// ==============================================================================
// PRACTICE D4 · SMART STREET LIGHT (LDR)
// Question: Smart street light (LDR). Built from: Ex4 idea, digital output.
// ==============================================================================

// LDR + 10k resistor divider on A0. LED on D9 turns ON in the dark.
// Check direction in Tinkercad: if it is reversed, swap < and >.
const int LDR = A0, LED = 9;
void setup() { pinMode(LED, OUTPUT); Serial.begin(9600); }
void loop() {
  int light = analogRead(LDR);
  digitalWrite(LED, light < 400 ? HIGH : LOW);
  Serial.print("Light: "); Serial.println(light);
  delay(300);
}


# ==============================================================================
# PRACTICE D5 · CLOUD DATA LOGGER: 100 READINGS → CSV (COLAB ONLY)
# Question: Cloud data logger: 100 readings → CSV (Colab only). Built from: Colab tab.
# ==============================================================================

import numpy as np, pandas as pd
np.random.seed(0)
df = pd.DataFrame({
    "Time": range(1, 101),
    "Temperature": np.round(np.random.uniform(20, 35, 100), 1),
    "Humidity":    np.round(np.random.uniform(40, 80, 100), 1)})
df.to_csv("sensor_log.csv", index=False)
print(df.describe())          # count, mean, min, max
# Google Sheets: Colab -> files.download("sensor_log.csv"), then File > Import in Sheets
