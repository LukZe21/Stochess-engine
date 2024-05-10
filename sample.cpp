#include <iostream>
#include <vector>
#include <utility>
#include <map>
#include <string>
#include <cstring>


class Piece{
    public:
        std::string name;
        std::string position;
        char color;

        void setValues(const std::string& name, const std::string& position, char color){
            this->name = name;
            this->position = position;
            this->color = color;

        }
        void printValues(){
            std::cout << name << std::endl;
            std::cout << position << std::endl;
            std::cout << color << std::endl;
        }

};

extern "C"{
    __declspec(dllexport) void PrintValues(Piece *self, const std::string& name, const std::string& position, char color) {self->setValues(name, position, color);}
    __declspec(dllexport) void printValies(Piece *self) {self->printValues();}

}



extern "C"{
    const char* getPosition(int mouseX, int mouseY, const char* pos_index[8][8]){
        return pos_index[mouseX/100][mouseY/100];
    }
}