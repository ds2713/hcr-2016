#define ENABLELIFT (6)
#define ENABLECLAW (4)
#define PHASELIFT (7)
#define PHASECLAW (5)
#define DELAY (200)

//UP IS HIGH

char motion;

void setup() {
  Serial.begin(9600);
  pinMode(ENABLELIFT, OUTPUT);
  pinMode(ENABLECLAW, OUTPUT);
  pinMode(PHASELIFT, OUTPUT);
  pinMode(PHASECLAW, OUTPUT);
  digitalWrite(ENABLELIFT, HIGH);
  digitalWrite(ENABLECLAW, HIGH);
  digitalWrite(PHASELIFT, HIGH);
  digitalWrite(PHASECLAW, HIGH);
}

void loop() {

  if (Serial.available()) {
    motion = Serial.read();
    switch(motion){
      case 'u':
        digitalWrite(ENABLELIFT, LOW);
        digitalWrite(PHASELIFT, HIGH);
        delay(DELAY);
        break;
      case 'd':
        digitalWrite(ENABLELIFT, LOW);
        digitalWrite(PHASELIFT, LOW);
        delay(DELAY);
        break;
      case 'o':
        digitalWrite(ENABLECLAW, LOW);
        digitalWrite(PHASECLAW, HIGH);
        delay(DELAY);
        break;
      case 'c':
        digitalWrite(ENABLECLAW, LOW);
        digitalWrite(PHASECLAW, LOW);
        delay(DELAY);
        break;
    }
  }
  digitalWrite(ENABLELIFT, HIGH);
  digitalWrite(ENABLECLAW, HIGH);
}
