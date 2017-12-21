int liquid = 7;

int liquid_level = 0;

void setup() {
  Serial.begin(9600);
  pinMode(liquid, INPUT); 
}

void loop() {
  liquid_level = digitalRead(liquid);
  if (liquid_level == 1)
  {
    Serial.println("1, Liquid detected");
  }
  else 
  {
    Serial.println("0, No liquid");
  }
  delay(1000);
}

