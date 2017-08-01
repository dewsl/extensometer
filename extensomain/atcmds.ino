#define ATCMD 		"AT"
#define ATECMDTRUE	"ATE"
#define ATECMDFALSE	"ATE0"
#define SENDIRP		"AT+IRP"	// send IR pulse
#define OKSTR 		"OK"
#define ERRORSTR	"ERROR"
#define SAMPLEULTRASONIC	"AT+UTS"

bool ate=true;

void getArguments(String at_cmd, String *arguments){
	int i_from = 0, i_to = 0, i_arg = 0;
	bool f_exit = true;
	String sub;

	// find '=' sign
	i_from = at_cmd.indexOf('=');

	do{
		i_to = at_cmd.indexOf(',',i_from+1);
		if (i_to < 0){
			sub = at_cmd.substring(i_from+1);
			f_exit = false;
		}
		else sub = at_cmd.substring(i_from+1,i_to);

		arguments[i_arg] = sub;
		i_from = i_to;
		i_arg += 1;

	} while(f_exit);

}
void getATCommand(){
	String serial_line, command;
	int i_equals = 0;
	
	do{
		serial_line = Serial1.readStringUntil('\r\n');
	}while(serial_line == "");
	serial_line.toUpperCase();
	serial_line.replace("\r","");

	// echo command if ate is set, default true
	if (ate) Serial1.println(serial_line);

	// get characters before '='
	i_equals = serial_line.indexOf('=');
	if (i_equals == -1) command = serial_line;
	else command = serial_line.substring(0,i_equals);

	// Serial.println(command);
	
	if (command == ATCMD)
		Serial1.println(OKSTR);
	else if (command == ATECMDTRUE){
		ate = true;
		Serial1.println(OKSTR);
	}
	else if (command == ATECMDFALSE){
		ate = false;
		Serial1.println(OKSTR);
	}
	else if (command == SAMPLEULTRASONIC){
		
		getUltrasonicWave(0);
	}
	else if (command == SENDIRP){
		sendIRPulse();
	}
	else{
		Serial1.println(ERRORSTR);
	}

}
