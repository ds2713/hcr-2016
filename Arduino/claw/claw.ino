#define ENABLE1 (6)
#define ENABLE2 (4)
#define PHASE1 (7)
#define PHASE2 (5)

//UP IS HIGH

void setup() {
  pinMode(ENABLE1, OUTPUT);
  pinMode(ENABLE2, OUTPUT);
  pinMode(PHASE1, OUTPUT);
  pinMode(PHASE2, OUTPUT);
  digitalWrite(PHASE1, HIGH);
  digitalWrite(PHASE2, HIGH);
  digitalWrite(ENABLE1, LOW);
  digitalWrite(ENABLE2, LOW);
}

void loop() {
  digitalWrite(PHASE1, LOW);
  digitalWrite(PHASE2, LOW);
  delay(1000);
  digitalWrite(PHASE1, HIGH);
  digitalWrite(PHASE2, HIGH);
  delay(1300);
}
