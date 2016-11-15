#define ROTDIR (5) //pins out
#define ROTSTEP (6)
#define STEPS (200) //steps per rotation

#define PIN_A0 (9)
#define PIN_A1 (10) //pins for A4988 microstepping
#define PIN_A2 (11)

#define PREFIX (666) //ENSURE ALL COMMANDS SENT HERE ARE IN THE FORM ###,val where ### is the identifier prefix to prevent false commands.
int msteprot;        //val is the angle by which the motor should move, with any positive or negative float being valid.
float temp;
float temp2;
String stemp;

void setup() {
  Serial.begin(9600);
  pinMode(ROTDIR,OUTPUT);
  pinMode(ROTSTEP,OUTPUT);
  setmsteprot(16);
}

void loop() {
  Serial.println("how far to move angle? (degrees)");
  while(Serial.available()==0){}
  temp2=Serial.parseFloat(); //read the prefix part, ignoring the comma
  temp=Serial.parseFloat(); //read the angle part after the comma
  if (temp2==PREFIX){
  
  if (temp<0){
    moverot(abs(temp),0);
  }
  else{
    moverot(abs(temp),1);
  }
  
  }
}

void moverot(float angle, bool dir){
  int x;

  digitalWrite(ROTDIR,dir);

  for(x=0; x < (int)round(angle*STEPS*msteprot/360); x++)
  {
    digitalWrite(ROTSTEP,HIGH);
    delay(1);
    digitalWrite(ROTSTEP,LOW);
    delay(1);
  }
}

void moverotto(float angle, bool dir){
  
}

void setmsteprot(int newmstep){

msteprot=newmstep;

  
  switch(newmstep){
    case 1:
    digitalWrite(PIN_A0,LOW);
    digitalWrite(PIN_A1,LOW);
    digitalWrite(PIN_A2,LOW);
    break;
    case 2:
    digitalWrite(PIN_A0,HIGH);
    digitalWrite(PIN_A1,LOW);
    digitalWrite(PIN_A2,LOW);
    break;
    case 4:
    digitalWrite(PIN_A0,LOW);
    digitalWrite(PIN_A1,HIGH);
    digitalWrite(PIN_A2,LOW);
    break;
    case 8:
    digitalWrite(PIN_A0,HIGH);
    digitalWrite(PIN_A1,HIGH);
    digitalWrite(PIN_A2,LOW);
    break;
    case 16:
    digitalWrite(PIN_A0,HIGH);
    digitalWrite(PIN_A1,HIGH);
    digitalWrite(PIN_A2,HIGH);
    break;
    default:
    digitalWrite(PIN_A0,LOW);
    digitalWrite(PIN_A1,LOW);
    digitalWrite(PIN_A2,LOW);
    break;
  }
}

float extract(float a, float b){
  
}
