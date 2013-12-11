//
//  SpeedLimit.cpp
//
//
//  Created by Alyssa Harris on 12/10/13.
//	edited by Matt McCaleb on 12/10/13.
//  edited by Kory yates on 12/11/13

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main{
    int speedLimit;
    int goingSpeed;
    int speedingTicket;
	int reckless;//calculations for reckless driving
    cout<<"What is the speed limit?"<<endl;
    cin>>speedLimit;
    cout<<"How fast were you going?"<<endl;
    cin>>goingSpeed;
	reckless=speedLimit+40;
    if (goingSpeed <= speedLimit){
        cout<<"no ticket!"<<endl;
    }
	//causes the speeder to go to jail if they go a curtain speed over the limit
	else if(goingSpeed >= reckless){
		cout<<"You are going to jail for reckless driving"<<endl;
	}
    else{
		
        //speeding ticket is calculated as follows:
        //$100 fine for the first 10 mph over the speeding limit
        //For every mile above that, $10 is added
		speedingTicket = 100;
		if (goingSpeed - speedLimit > 10)
			speedingTicket += (goingSpeed - speedLimit) * 10;
		cout << "your ticket it is $" << speedingTicket << ".00, slow down!" << endl;

    }
    return 0;
}