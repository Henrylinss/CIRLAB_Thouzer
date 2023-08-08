#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include<iostream>
#include <cstdlib>
#include <cstring>
#include <cctype>
#include <thread>
#include <chrono>
// #include "mqtt/async_client.h"
using namespace std;

class Send{
public:
    string api;
    int Do(char* api, char* ip, int PORT);
};
