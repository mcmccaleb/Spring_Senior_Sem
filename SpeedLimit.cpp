//
//  SpeedLimit.cpp
//
//
//  Created by Alyssa Harris on 12/10/13.
//	edited by Matt McCaleb on 12/10/13.
//

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main{
    int speedLimit;
    int goingSpeed;
    int speedingTicket;
    cout<<"What is the speed limit?"<<endl;
    cin>>speedLimit;
    cout<<"How fast were you going?"<<endl;
    cin>>goingSpeed;
    if (goingSpeed < speedLimit){
        cout<<"no ticket!"<<endl;
    }
    else{
		
        //speeding ticket is calculated as follows:
        //$100 fine for the first 10 mph over the speeding limit
        //For every mile above that, $10 is added
    }
    return 0;
}