void initADC(uint16_t *sig){
  adc_init(ADC, 84000000, 20000000, 1000);
  adc_configure_timing(ADC, 0, ADC_SETTLING_TIME_0, 0);
  adc_configure_trigger(ADC, ADC_TRIG_SW, 1); // Disable hardware trigger.
  adc_disable_interrupt(ADC, 0xFFFFFFFF); // Disable all ADC interrupts.
  adc_disable_all_channel(ADC);
  adc_enable_channel(ADC, ADC_CHANNEL_0);
  // adc_start(ADC);
  ADC->ADC_RPR=(uint32_t)sig;   // DMA buffer
  ADC->ADC_RCR=N_BUFFER;
  ADC->ADC_PTCR=1;
}
