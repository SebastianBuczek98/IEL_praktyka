// DS18B20 podlaczyc do pinu 3, DHT11 do pinu 2 w Arduino. Czujniki zasilane sa napieciem 5V.

  #include <OneWire.h>            // komunikacja z czujnikiem 1 (1Wire)
  #include <DallasTemperature.h>  // obsluga czujnika 1
  #include <DHT.h>                // obsluga czujnika 2
  #include <Wire.h>               // biblioteki lcd (komunikacja I2C)
  #include <LiquidCrystal_I2C.h>  // biblioteki lcd
  #include <EtherCard.h>          // biblioteka do obslugi modulu ethernet ENC28J80
  #include <IPAddress.h>
  #include <TimerOne.h>           // obsluga przerwania - ethernet
  #include <string.h>
  
  #define STATIC 1                // set to 1 to disable DHCP (adjust myip/gwip values below)  - problemy z polaczeniem (w takim wypadku zamienic na 1)
  #define DHT11_PIN 2             // przypisanie pinu 2 czujnikowi 2 (DHT11)
  int oneWireBus = 3;             // przypisanie pinu 3 czujnikowi 3 (DS18B20)


  volatile float temp1 =0.0;           // zadelarowanie zmiennej temp1 (DS18B20)
  volatile int temp2 = 0;         // zadelarowanie zmiennej temp2 (DHT11)

  char buf1[5];
  char buf2[5];
//  char buf3[20];
  
  OneWire oneWire(oneWireBus);
  DallasTemperature sensors(&oneWire);
  DHT dht;

  LiquidCrystal_I2C lcd(0x3F, 16, 2); // adres modulu LCD

  char zxc[5];

  #if STATIC
  static byte myip[] = {192,168,107,7};                 // ethernet interface ip address
  static byte gwip[] = {192,168,107,254};               // gateway ip address
  unsigned int myport = 8888;
  #endif
  static byte mymac[] = { 0x2,0x8,0x25,0x7,0x44,0x11 }; // ethernet mac address - must be unique on your network
  
  byte Ethernet::buffer[500]; // tcp/ip send and receive buffer

  void udpSerialPrint(uint16_t port, uint8_t ip[4],uint16_t src_port, const char *data, uint16_t len){
  IPAddress src(ip[0], ip[1], ip[2], ip[3]);
  Serial.print("Adres zrodlowy: ");
  Serial.println(src);
  Serial.print("Port zrodlowy: ");
  Serial.println(src_port);
  Serial.print("Jakis port: : ");
  Serial.println(port);
  Serial.print("Wiadomosc: ");
  Serial.println(data);
  //int check = (int)data;
  //Serial.println(data);
  //ether.sendUdp(data, 12, port, ip, src_port);
  //ether.makeUdpReply(buf1, sizeof buf1, src_port);
  if(*data=='1') ether.makeUdpReply(buf1, sizeof buf1, src_port);
  else ether.makeUdpReply(buf2, sizeof buf2, src_port);
}
  
  void setup(){
    Serial.begin(57600);
    
    Serial.println("Odczyt temperatury z czujnika DS18B20 i DHT11");
    sensors.begin();
    sensors.setResolution(12);
  
    dht.setup(DHT11_PIN);
  
    if (ether.begin(sizeof Ethernet::buffer, mymac, SS) == 0)
      Serial.println( "Failed to access Ethernet controller");
    #if STATIC
      ether.staticSetup(myip, gwip);
    #else
      if (!ether.dhcpSetup())
        Serial.println("DHCP failed");
    #endif
  
    ether.printIp("IP:  ", ether.myip);
    ether.printIp("GW:  ", ether.gwip);
    ether.printIp("DNS: ", ether.dnsip);
  
    lcd.begin();      //inicjalizacja LCD
    lcd.backlight();  //
  
    Timer1.initialize(100000);           // obsluga przerwania - ethernet (ping do ok 100ms - zbyt duża czestosc przerwan moze zakłócać pracę pozostałych peryferiów)
    Timer1.attachInterrupt(ethercomms);  // obsluga przerwania - ethernet
  
    if(ether.begin(sizeof Ethernet::buffer, mymac) == 0)
    Serial.println("Nie udalo sie polaczyc z kontrolerem");
    #if STATIC
    ether.staticSetup(myip,gwip);
    #endif
   
    ether.udpServerListenOnPort(&udpSerialPrint, myport);
  }
  
  BufferFiller bfill;
  
  void loop(){
  
    sensors.requestTemperatures();
    temp1 = sensors.getTempCByIndex(0);
    temp2 = dht.getTemperature();
    
    int temp1mod = (int)(temp1*100);

//    sprintf(buf3,"%i",0);
    
    sprintf(buf1,"%i",temp1mod);
    sprintf(buf2,"%i",temp2);
    Serial.println(buf1);
    Serial.println(buf2);
   
//    strcat(buf3, buf1);
//    strcat(buf3, buf2);
//    Serial.println(buf3);
    
    Serial.print("Wartosc temperatury DS18B20:");
    Serial.print(temp1);
    Serial.print("*C");
    if (temp2>10){
      Serial.print(" oraz DHT11:");
      Serial.print(temp2);
      Serial.println("*C");
    }
    else Serial.println("");
  
    delay(100);
  
    lcd.setCursor(1,0);
    lcd.print("Temp1 = ");
    lcd.print(temp1);
  
    lcd.setCursor(1,1);
    lcd.print("Temp2 = ");
    lcd.print(temp2);
  }
  
  void ethercomms(){
  
      // obsluga modulu ethernetowego w przerwaniu triggerowanym timerem pozwala na 
      // jego plynne dzialanie niezaleznie od innych wykonywanych przez mikrokontroler zadan

      ether.packetLoop(ether.packetReceive());
      //ether.udpServerListenOnPort(&udpSerialPrint, myport);
  }
