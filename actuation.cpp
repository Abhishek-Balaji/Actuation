#include <stdlib.h>
#include <stdio.h>
#include<unistd.h>
#include <dynamixel_sdk.h>                                  // Uses Dynamixel SDK library
#include<math.h>

// Initialize PortHandler instance.Set the port path.Get methods and members of PortHandlerLinux or PortHandlerWindows
dynamixel::PortHandler *portHandler = dynamixel::PortHandler::getPortHandler("/dev/ttyUSB0");

// Initialize PacketHandler instance.Set the protocol version.Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
dynamixel::PacketHandler *packetHandler = dynamixel::PacketHandler::getPacketHandler(1.0);

//Function for actuating the bot with velocities for 4 wheels
int move(int vel1,int vel2,int vel3,int vel4)
{ packetHandler->write2ByteTxRx(portHandler, 7, 32, vel1);
  packetHandler->write2ByteTxRx(portHandler, 1, 32, vel2);
  packetHandler->write2ByteTxRx(portHandler, 5, 32, vel3);
  packetHandler->write2ByteTxRx(portHandler, 8, 32, vel4);
return 0;}


int main()
{

  // Open port
  if (portHandler->openPort()){printf("%s","Succeeded to open the port!\n");}
  else
  {printf("%s","Failed to open the port!\n");printf("%s","Press any key to terminate...\n");
  return 0;}

  // Set port baudrate
  if (portHandler->setBaudRate(1000000))
  {printf("Succeeded to change the baudrate!\n");}
  else
{printf("Failed to change the baudrate!\n");printf("Press any key to terminate...\n");
return 0;}


float x2,y2,x1=0.23,y1=0.28,X,Y,dis,time_a,time_d,xc,yc,dev;
int ang=0,ang_c=0,m,t=0,cont;
char k;
FILE *fc,*f;
f=fopen("pixelcoordinate.txt","r");
fc=fopen("data_centriod.txt","r");
scanf(f,"%d",&m);
for(t=0;t<m;t++)
{
if(t)
{
fscanf(fc,"%f %f",&xc,&yc);
xc/=100;yc/=100;
printf("%f %f\n",xc,yc);
dev=sqrt(((xc-x1)*(xc-x1))+((yc-y1)*(yc-y1)));

if (dev>=0.1)
{
x1=xc;y1=yc;}
}

X=x2-x1;Y=y2-y1;dis=sqrt((X*X)+(Y*Y));
ang_c+=ang;
time_d=dis/(0.205483286*57/40);time_a=0.040019751*abs(ang);
if (X==0 && Y==0)
{ang=0;}
else
{
  if (ang<=180 && ang>=0)
      { move(300,300,300,300);
       usleep(time_a*1000000);}

  else if (ang>=-180 && ang<0)
      { move(1323,1323,1323,1323);
       usleep(time_a*1000000);}

}
move(0,0,0,0);

move(300,1323,1323,300);
usleep(time_d*2000000*0.73/0.91);

  move(0,0,0,0);
  x1=x2,y1=y2;}
  portHandler->closePort();
  return 0;}
