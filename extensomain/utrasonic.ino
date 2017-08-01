#define TWAITPIN 25
#define IRLEDPIN 26
#define IRPULSEMAX 10

bool data_filled = 0;

static uint16_t sig[N_BUFFER];
uint8_t edge = 0;

uint32_t t_wait = 100;  // t_wait value in millis
uint8_t ir_pulse_counter = 0;
bool verbose_out = true;

void stopTimer3(){
  REG_PIOB_ODSR ^= (1<<TWAITPIN);
  edge += 1;
  if (edge>1){
    edge = 0;
    Timer3.stop();
  }
}

void isrTimer2(){
  REG_PIOB_ODSR ^= (1<<IRLEDPIN);
  ir_pulse_counter += 1;
  if (ir_pulse_counter == IRPULSEMAX){
    ir_pulse_counter = 0;
    Timer2.stop();
  }
}

void startWaitTimer(){  
	
	// delay(1000);      
	Timer3.start(100); // Calls every 50ms
}

void sampleSignal(uint16_t ch){
  initADC(sig);

  adc_start(ADC);
  delay(10);  
  adc_stop(ADC);
}

void sendIRPulse(){
  // pinMode(22, OUTPUT);
  REG_PIOB_OER = (1<<IRLEDPIN);
  REG_PIOB_ODSR &= ~(1<<IRLEDPIN);
  ir_pulse_counter = 0;
  Timer2.attachInterrupt(isrTimer2);
  Timer2.setFrequency(76000);
  Timer2.start();
  // while(1);
}

void getUltrasonicWave(uint16_t channel){
	//reset
  digitalWrite(2, HIGH);
  delay(100);
  digitalWrite(2, LOW); 
	
	// setup gpios and registers
  Timer3.attachInterrupt(stopTimer3);

                                                                

  // send IR pulse her
  sendIRPulse();
  //while (ir_pulse_counter<IRPULSEMAX);

  // start t_wait timer
  Timer3.start(t_wait);
  
  //Serial.write("before sample");
  sampleSignal(channel);
  //Serial.write("helloTin");
  //Serial.write(channel);

  int sizesignal = sizeof(sig);
  int i;
  //Serial.write(sizesignal);
  i=0;
  while(i<N_BUFFER){
    Serial1.println(sig[i]);
    //Serial.println();
    i=i+1;
  }
  Serial1.println("DONE");
}











