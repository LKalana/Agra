/*
 * PROGRAM : AGRAMU SERVER
 * AUTHOR  : LIYANAGE KALANA PERERA
 * DATE    : 2023.12.28 --> 20:04 PM
 * 
 * 
 * NOTE: --> AGRAMU SERVER WILL TURN OUR ESP8266 INTO A WEB SERVER THAT WE CAN USE 
 *           AS A TELEMETRY SYSTEM.
 *       --> WE CAN USE MULTIPLE FIELD SENSORS TO OBTAIN FIELD DATA. 
 *       --> TO AVOID ANY ISSUES, USE CORRECT WIFI SSID AND PASSWORD.
 *       
 * SIMPLY ESP8266 WILL READ EACH SENSOR AT GIVEN INTERVALS(AS CLIENT REQUESTS).
 * 
 * 
 * 
*/

#include <ESP8266WiFi.h>

String  ClientRequest;
WiFiServer server(80);
// NOTIFY THE CONNECTION IS OK.
void conn_est(int stat)
{
  pinMode(D0,OUTPUT);
  switch(stat)
  {
    case 0:digitalWrite(D0,LOW);
           break;
    case 1:for(int i=0;i<10;i++)
            {
              digitalWrite(D0,HIGH);
              delay(50);
              digitalWrite(D0,LOW);
              delay(50);
            }
           digitalWrite(D0,HIGH);
           break;
  }
}
int CNT = 0; // COUNT VARIABLE.
void setup()
{
  conn_est(0); // CONNECTION STATUS.
  ClientRequest = "";
  Serial.begin(9600);
  WiFi.disconnect();
  delay(3000);
  Serial.println("START");
  WiFi.begin("SLT-4G_1F24E4","6C22B7E5"); // HOME NETWORK.
  while ((!(WiFi.status() == WL_CONNECTED))){
    delay(300);
    Serial.print("..");
  }
  conn_est(1); // CONNECTION STATUS.
  Serial.println("CONNECTED");
  Serial.println("AVAILABLE IP IS:");
  Serial.println((WiFi.localIP().toString()));
  server.begin();
}

void loop()
{
  while(CNT < 1000)
  {
    WiFiClient client = server.available();
    if (!client) { return; }
    while(!client.available()){  delay(1); }
    ClientRequest = (client.readStringUntil('\r'));
    ClientRequest.remove(0, 5);
    ClientRequest.remove(ClientRequest.length()-9,9);
    Serial.println("Inbound Request");
    Serial.println(ClientRequest);
    // WE CAN USE THIS "client.println" TO WRITE TO CLIENT.
    client.println("HTTP/1.1 200 OK");
    client.println("");
    client.print("COM OK");
    client.print(" ");
    client.println(CNT);
    delay(1);
    client.flush();
    delay(100);
    CNT ++;
  }
  CNT = 0;// RESET THE COUNT.
}
