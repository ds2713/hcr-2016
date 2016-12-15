//pin definitions
#define HEADDIR (6) //pins out
#define HEADSTEP (7)
#define PIN_A0 (11)
#define PIN_A1 (12) //pins for A4988 microstepping
#define PIN_A2 (13)
#define ZEROLIFT (8)
#define TILT1 (9)
#define TILT2 (10)
#define ENABLELIFT (4)
#define ENABLECLAW (2)
#define PHASELIFT (5)
#define PHASECLAW (3)
#define ZEROTILT (A0)
#define TONEOUT (A3)
//constant definitions
#define STEPS (200) //steps per rotation
#define DELAY (200)
#define LIFTSPEEDUP (47) //mm per second
#define LIFTSPEEDDOWN (57) //mm per second
#define CLAWSPEED (39) //mm per second
#define TILTSPEEDBASE (28) //degrees per second (A in equation)
#define TILTSPEEDSUB (100) //constant B in equation Speed = A - Bsin(posavg-c)
#define TILTANGLENEUTRAL (9) //angle at which centre of mass is in middle (C in equation)
#define LIFTMAX (400)
#define CLAWMAX (52)
#define TILTMAX (15)
#define TILTMIN (-15)
#define TILTVOLTAGE (3)
//prefix definitions
#define PREFIXHEAD (666) //ENSURE ALL COMMANDS SENT HERE ARE IN THE FORM ###,val where ### is the identifier prefix
#define PREFIXCLAW (555)
#define PREFIXLIFT (444)
#define PREFIXTILT (333)
#define PREFIXCALIBRATE (123)
#define PREFIXSHAKEHANDS (111)
#define PREFIXCHANGEIDLE (420)
#define PREFIXYES (777)
#define PREFIXNO (888)
#define PREFIXPLAY (999)
#define PREFIXTONE (990)
#define PREFIXCHECKHANDS (876)
//tone definitions
#define C (262)
#define D (294)
#define E (330)
#define F (349)
#define G (392)
#define A (440)
#define B (494)
#define C2 (523)

int msteprot;        //val is the angle by which the motor should move, with any positive or negative float being valid.
float temp;
float temp2;
String stemp;
char motion;
float liftpos=0;
float clawpos=0;
float headpos=0;
float tiltpos=0;
float tiltspeed=28;
bool canidle;
int idlecount=0;
/*_____________________________________________
 * music definitions
 * 1  hello
 * 2  affirmative
 * 3  negative
 * 4  R2D2
_______________________________________________*/
int hello[]={8,A,G,E,C,D,B,F,C};
int affirmative[]={2,C,F};
int negative[]={2,F,C};
int R2D2[]={16,A,G,E,C,D,B,F,C,A,G,E,C,D,B,F,C};

void setup() {
  Serial.begin(9600);
  pinMode(HEADDIR,OUTPUT);
  pinMode(HEADSTEP,OUTPUT);
  pinMode(ENABLELIFT, OUTPUT);
  pinMode(ENABLECLAW, OUTPUT);
  pinMode(PHASELIFT, OUTPUT);
  pinMode(PHASECLAW, OUTPUT);
  pinMode(ZEROLIFT, INPUT);
  pinMode(TILT1, OUTPUT);
  pinMode(TILT2, OUTPUT);
  digitalWrite(TILT1, LOW);
  digitalWrite(TILT2, LOW);
  digitalWrite(ENABLELIFT, HIGH);
  digitalWrite(ENABLECLAW, HIGH);
  digitalWrite(PHASELIFT, HIGH);
  digitalWrite(PHASECLAW, HIGH);
  setmstephead(16);
  canidle=0;
  calibrate_arm();
  calibrate_tilt();
  calibrate_head();
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
      calibrate_tilt();
    break;
    case PREFIXSHAKEHANDS :
      shake_hands();
    break;
    case PREFIXCHANGEIDLE :
      canidle=!canidle;
    break;
    case PREFIXTILT :
      movetiltto(temp2);
    break;
    case PREFIXYES :
      yes();
    break;
    case PREFIXNO :
      no();
    break;
    case PREFIXTONE :
      testtone();
    break;
    ////////////////////////////////////
    case PREFIXPLAY :
      switch (round(temp2)){
        case 1:
          playtone(hello);
        break;
        case 2:
          playtone(affirmative);
        break;
        case 3:
          playtone(negative);
        break;
        case 4:
          playtone(R2D2);
        break;
      }  
    break;
  }
  Serial.print('c');
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
  //Serial.print("head position: ");
  //Serial.println(headpos);
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
    //Serial.print("lift position: ");
    //Serial.println(liftpos);
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
    //Serial.print("claw position: ");
    //Serial.println(clawpos);
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

void movetilt(float angle, bool dir){
  if (dir==0){
    analogWrite(TILT1,TILTVOLTAGE*255/4.0);
    delay(1000*(angle/tiltspeed));
    digitalWrite(TILT1,LOW);
    tiltpos-=angle;
  }
  else{
    analogWrite(TILT2,TILTVOLTAGE*255/4.0);
    delay(1000*(angle/tiltspeed));
    digitalWrite(TILT2,LOW);
    tiltpos+=angle;
  }
  //Serial.print("tilt angle: ");
  //Serial.println(tiltpos);
}

void movetiltto(float angle){
  tiltspeed=getavgspeed(angle,tiltpos);
  //Serial.print("predicted tilt speed: ");
  //Serial.println(tiltspeed);
  if (angle>=TILTMIN and angle<=TILTMAX){
  movetilt(abs(angle-tiltpos),getdir(angle-tiltpos));
  }
  else if (angle<TILTMIN){
    movetiltto(TILTMIN);
  }
  else if (angle>TILTMAX){
    movetiltto(TILTMAX);
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

float avg(float a, float b){
  float c = (a+b)/2;
  return c;
}

float degtorad(float a){
  float b = ((a*PI)/180);
  return b;
}

float getavgspeed(float angle, float tiltpos){
  float c;
  float d;
  if (abs(angle-TILTANGLENEUTRAL)>=abs(tiltpos-TILTANGLENEUTRAL)){
    c=-1;
  }
  if (abs(angle-TILTANGLENEUTRAL)<abs(tiltpos-TILTANGLENEUTRAL)){
    c=1;
  }
  d = TILTSPEEDBASE - c*TILTSPEEDSUB*(1-cos(degtorad(avg(tiltpos,angle)-TILTANGLENEUTRAL)));
  return d;
}

void shake_hands(){
  moveliftto(LIFTMAX);
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

void yes(){
  movetilt(4,1);
  for(int i=0;i<2;i++){
    movetilt(8,0);
    movetilt(8,1);
  }
  movetilt(4,0);
}

void no(){
  movetiltto(-10);
  movehead(10,1);
  for(int i=0;i<2;i++){
    movehead(20,0);
    movehead(20,1);
  }
  movehead(10,0);
  movetiltto(0);
}

void testtone(){
  tone(TONEOUT,C,500);
  delay(500);
  tone(TONEOUT,D,500);
  delay(500);
  tone(TONEOUT,E,500);
  delay(500);
  tone(TONEOUT,F,500);
  delay(500);
  tone(TONEOUT,G,500);
  delay(500);
  tone(TONEOUT,A,500);
  delay(500);
  tone(TONEOUT,B,500);
  delay(500);
  tone(TONEOUT,C2,500);
  delay(500);
}

void playtone(int a[]){
  for(int i=1;i<a[0]+1;i++){
    tone(TONEOUT,a[i],100);
    delay(100);
  }
}

void idle(){
  float a = random(200);
  float b = random(800);
  float c = 0;
  if (a>198){
    moveheadto(random(-20,20));
  }
  else{
    delay(10);
  }
  if (b>796){
    c=random(TILTMIN/2,TILTMAX/2);
    movetiltto(c);
    idlecount++;
  }
  else{
    delay(10);
  }
  if (idlecount>=10){
    calibrate_tilt();
    idlecount=0;
    movetiltto(c);
  }
}

void checkhands(){
  movetiltto(15);
  moveheadto(30);
  moveclawto(0);
  delay(3000);
  moveheadto(-30);
  delay(100);
  moveheadto(0);
  calibrate_tilt();
  movetiltto(-15);
  delay(1000);
  moveclawto(6);
  delay(500);
  moveclawto(0);
  delay(400);
  moveclawto(6);
  moveclawto(0);
  delay(1000);
  movetiltto(15);
  moveheadto(20);
  calibrate_tilt();
}

void calibrate_claw(){
  moveclaw(60,0);
  clawpos=0;
  moveclaw(5,1);
}

void calibrate_lift(){
  movelift(20,0);
  while (!digitalRead(ZEROLIFT)){
   movelift(10,0);
  }
  liftpos=0;
  movelift(20,1);
  //Serial.print("lift position: ");
  //Serial.println(liftpos);
}

void calibrate_head(){
  headpos=0;
}

void calibrate_tilt(){
  while(!digitalRead(ZEROTILT)){
    movetilt(1,1);
  }
  movetilt(20,0);
  tiltpos=0;
}

void calibrate_arm(){
  calibrate_lift();
  calibrate_claw();
}

