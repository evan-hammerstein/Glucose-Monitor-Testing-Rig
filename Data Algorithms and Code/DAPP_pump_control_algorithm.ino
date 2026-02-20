#define MAX_ENTRIES 100

// ---------- Global Storage ----------
int timestamps[MAX_ENTRIES];
float concentrations[MAX_ENTRIES];
int currentIndex = 0;

float compositeFlowRate_mLmin = 0.1;  // Main input!
float currentGlucoseFlowRate_mLmin = 0.0;
float currentPBSFlowRate_mLmin = 0.0;

float channelInternalDiameter_mm = 1.5;
float preIntersectionChannelLength_mm = 100.0;

String inputBuffer = "";
bool dataReceived = false;

// ---------- Setup ----------
void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Ready to receive CSV data...");
}

// ---------- Loop ----------
void loop() {
  if (!dataReceived) {
    while (Serial.available()) {
      char c = Serial.read();
      if (c == '\n') {
        processLine(inputBuffer);
        inputBuffer = "";
      } else {
        inputBuffer += c;
      }
    }

    if (currentIndex > 0 && !Serial.available()) {
      dataReceived = true;
      Serial.println("CSV received. Running schedule...");
      runPumpSchedule();
    }
  }
}

// ---------- Parse CSV Line ----------
void processLine(String line) {
  int commaIndex = line.indexOf(',');
  if (commaIndex == -1 || currentIndex >= MAX_ENTRIES) {
    Serial.println("Invalid line or buffer full.");
    return;
  }

  timestamps[currentIndex] = line.substring(0, commaIndex).toInt();
  concentrations[currentIndex] = line.substring(commaIndex + 1).toFloat();
  currentIndex++;
}

// ---------- Convert Composite Flow Rate → Velocity ----------
float convertFlowRateToVelocity(float totalFlowRate_mLmin, float innerDiameter_mm) {
  float Q_total = totalFlowRate_mLmin / (1e6 * 60.0);  // m³/s
  float diameter_m = innerDiameter_mm / 1000.0;
  float radius = diameter_m / 2.0;
  float area = 3.14159 * radius * radius;  // m²
  float velocity_m_per_sec = Q_total / area;
  return velocity_m_per_sec * 1000.0;  // mm/s
}

// ---------- Flow Rate Calculator ----------
void calculatePumpFlowRates_mLmin(float compositeFlowRate_mLmin, float desiredConc, float C1, float C2) {
  float Q_total = compositeFlowRate_mLmin / (1e6 * 60.0);  // m³/s
  float deltaC = C1 - C2;
  float Q1 = (deltaC != 0) ? Q_total * (desiredConc - C2) / deltaC : 0;
  float Q2 = Q_total - Q1;

  currentGlucoseFlowRate_mLmin = Q1 * 1e6 * 60.0;
  currentPBSFlowRate_mLmin = Q2 * 1e6 * 60.0;
}

// ---------- Delay Calculator ----------
void getPumpDelays_ms(float flowRate1_mLmin, float flowRate2_mLmin, float innerDiameter_mm, float channelLength_mm, int &delay1_ms, int &delay2_ms) {
  float Q1 = flowRate1_mLmin / (1e6 * 60.0);
  float Q2 = flowRate2_mLmin / (1e6 * 60.0);

  float diameter_m = innerDiameter_mm / 1000.0;
  float radius = diameter_m / 2.0;
  float area = 3.14159 * radius * radius;

  float v1 = (Q1 > 0) ? Q1 / area : 0;
  float v2 = (Q2 > 0) ? Q2 / area : 0;

  float t1 = (v1 > 0) ? (channelLength_mm / 1000.0) / v1 : -1;
  float t2 = (v2 > 0) ? (channelLength_mm / 1000.0) / v2 : -1;

  delay1_ms = 0;
  delay2_ms = 0;

  if (t1 < 0 || t2 < 0) return;

  if (t1 > t2) {
    delay2_ms = (int)((t1 - t2) * 1000);
  } else if (t2 > t1) {
    delay1_ms = (int)((t2 - t1) * 1000);
  }
}

// ---------- Main Control Loop ----------
void runPumpSchedule() {
  for (int i = 0; i < currentIndex; i++) {
    float targetConc = concentrations[i];

    // Calculate individual pump flows
    calculatePumpFlowRates_mLmin(compositeFlowRate_mLmin, targetConc, 0.020, 0.0);

    // Calculate delay to synchronize arrivals
    int delay1 = 0;
    int delay2 = 0;
    getPumpDelays_ms(currentGlucoseFlowRate_mLmin, currentPBSFlowRate_mLmin,
                     channelInternalDiameter_mm, preIntersectionChannelLength_mm,
                     delay1, delay2);

    // Output for now (replace with pump control logic later)
    Serial.print("At time ");
    Serial.print(timestamps[i]);
    Serial.print("s | Target Conc: ");
    Serial.print(targetConc);
    Serial.print(" M | Glucose: ");
    Serial.print(currentGlucoseFlowRate_mLmin, 3);
    Serial.print(" mL/min | PBS: ");
    Serial.print(currentPBSFlowRate_mLmin, 3);
    Serial.print(" mL/min | Delays → G: ");
    Serial.print(delay1);
    Serial.print(" ms, P: ");
    Serial.print(delay2);
    Serial.println(" ms");

    delay(1000); // simulate time between actions
  }
}
