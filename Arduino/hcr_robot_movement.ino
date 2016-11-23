///PREFIXES:
/*666, head
 *555, claw 
 *444, lift
 */

#define HEADDIR (6) //pins out
#define HEADSTEP (7)
#define STEPS (200) //steps per rotation

#define PIN_A0 (8)
#define PIN_A1 (9) //pins for A4988 microstepping
#define PIN_A2 (10)
#define ZEROLIFT (11)
#define ENABLELIFT (4)
#define ENABLECLAW (2)
#define PHASELIFT (5)
#define PHASECLAW (3)

#define DELAY (200)
#define LIFTSPEEDUP (47) //mm per second
#define LIFTSPEEDDOWN (57) //mm per second
#define CLAWSPEED (39) //mm per second

#define PREFIXHEAD (666) //ENSURE ALL COMMANDS SENT HERE ARE IN THE FORM ###,val where ### is the identifier prefix
#define PREFIXCLAW (555)
#define PREFIXLIFT (444)
#define PREFIXCALIBRATE (333)
#define PREFIXSHAKEHANDS (111)
#define PREFIXCHANGEIDLE (420)

#define LIFTMAX (460)
#define CLAWMAX (52)

int msteprot;        //val is the angle by which the motor should move, with any positive or negative float being valid.
float temp;
float temp2;
String stemp;
char motion;
float liftpos=0;
float clawpos=0;
float headpos=0;
bool canidle=1;

void setup() {
  Serial.begin(9600);
  pinMode(HEADDIR,OUTPUT);
  pinMode(HEADSTEP,OUTPUT);
  pinMode(ENABLELIFT, OUTPUT);
  pinMode(ENABLECLAW, OUTPUT);
  pinMode(PHASELIFT, OUTPUT);
  pinMode(PHASECLAW, OUTPUT);
  pinMode(ZEROLIFT, INPUT);
  digitalWrite(ENABLELIFT, HIGH);
  digitalWrite(ENABLECLAW, HIGH);
  digitalWrite(PHASELIFT, HIGH);
  digitalWrite(PHASECLAW, HIGH);
  setmstephead(16);
  calibrate_arm();
}

void loop() {
  while(Serial.available()==0){
    
    if (canidle){
    idle();}
    
    }
  temp=Serial.parseFloat(); //read the prefix part, ignoring the comma
  temp2=Serial.parseFloat(); //read the angle part after the comma
  
  switch(round(temp)){
    case PREFIXHEAD :
      //movehead(abs(temp2),getdir(temp2));
      moveheadto(temp2);
    break;
    case PREFIXCLAW :
      //moveclaw(abs(temp2),getdir(temp2));
      moveclawto(temp2);
    break;
    case PREFIXLIFT :
      //movelift(abs(temp2),getdir(temp2));
      moveliftto(temp2);
    break;
    case PREFIXCALIBRATE :
      calibrate_arm();
      calibrate_head();
    break;
    case PREFIXSHAKEHANDS :
      shake_hands();
    break;
    case PREFIXCHANGEIDLE :
      canidle=!canidle;
      break;
  }
}

void movehead(float angle, bool dir){
  int x;

  digitalWrite(HEADDIR,dir);

  for(x=0; x < (int)round(angle*STEPS*msteprot/360); x++)
  {
    digitalWrite(HEADSTEP,HIGH);
    delay(1);
    digitalWrite(HEADSTEP,LOW);
    delay(1);
  }
  headpos+=(angle)*((2*dir)-1);
}

void moveheadto(float angle){
  movehead(abs(angle-headpos),getdir(angle-headpos));
  Serial.print("head position: ");
  Serial.println(headpos);
}

void setmstephead(int newmstep){

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

void movelift(float distance, bool dir){
  //dir 1 = up, dir 0 = down
    digitalWrite(PHASELIFT, dir);
    digitalWrite(ENABLELIFT, LOW);
    if (dir==true){
    delay(1000*distance/LIFTSPEEDUP);
    liftpos+=(distance);}
    if (dir==false){
    delay(1000*distance/LIFTSPEEDDOWN);
    liftpos-=(distance);}
    digitalWrite(ENABLELIFT, HIGH);
    Serial.print("lift position: ");
    Serial.println(liftpos);
}

void moveliftto(float distance){
  if (distance>=0 and distance<=LIFTMAX){
  movelift(abs(liftpos-distance),getdir(distance-liftpos));}
  else if (distance<0){
    moveliftto(0);
  }
  else if (distance>LIFTMAX){
    moveliftto(LIFTMAX);
  }
}

void moveclaw(float distance, bool dir){
  //dir 1 = open, dir 0 = close
    digitalWrite(PHASECLAW, dir);
    digitalWrite(ENABLECLAW, LOW);
    delay(1000*distance/CLAWSPEED);
    digitalWrite(ENABLECLAW, HIGH);
    clawpos+=(distance)*((2.0*dir)-1);
    Serial.print("claw position: ");
    Serial.println(clawpos);
}

void moveclawto(float distance){
  if (distance>=0 and distance<=CLAWMAX){
  moveclaw(abs(clawpos-distance),getdir(distance-clawpos));}
  else if (distance<0){
    moveclawto(0);
  }
  else if (distance>CLAWMAX){
    moveclawto(CLAWMAX);
  }
}

bool getdir(float a){
  if (a<0){
    return false;
  }
  if (a>=0){
    return true;
  }
}


void shake_hands(){
  moveliftto(200);
  moveclawto(20);
  moveheadto(0);
  delay(800);
  moveclawto(10);  
  movelift(25,0);
  movelift(25,1);
  movelift(25,0);
  movelift(25,1);
  moveclawto(20); 
}

void idle(){
  float a = random(200);
  if (a>198){
    moveheadto(random(-40,40));
  }
  else{
    delay(10);
  }
}

void calibrateclaw(){
  moveclaw(60,0);
  clawpos=0;
  moveclaw(5,1);
}

void calibratelift(){
  movelift(20,0);
  while (!digitalRead(ZEROLIFT)){
   movelift(10,0);
  }
  liftpos=0;
  movelift(20,1);
  Serial.print("lift position: ");
  Serial.println(liftpos);
}

void calibrate_head(){
  headpos=0;
}
void calibrate_arm(){
  calibratelift();
  calibrateclaw();
}

