#include <iostream>
#include <vector>
#include <utility>
#include <map>
#include <string>
#include <cstring>


extern "C"{
    const char* getPosition(int mouseX, int mouseY, const char* pos_index[8][8]){
        return pos_index[mouseX/100][mouseY/100];
    }
}
