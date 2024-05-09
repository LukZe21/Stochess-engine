#include <iostream>
#include <vector>
#include <utility>
#include <map>
#include <string>
#include <cstring>



extern "C" {
    const char* getMoves(int mouseX, int mouseY, const int* whitePiecesLocation, int numLocations) {
        for (int i = 0; i < numLocations; i += 1) {
            if (mouseX <= whitePiecesLocation[i] && mouseY <= whitePiecesLocation[i + 1]) {
                return "PIECE OUT";
            }
        }
        return "NOTHING";
    }
}

extern "C"{
    const char* getPosition(int mouseX, int mouseY, const char* pos_index[8][8]){
        return pos_index[mouseX/100][mouseY/100];
    }
}






// extern "C"{
//     const char* movePiece(const char* position, std::map<std::string, std::string>& board){
//         for(const auto& pos: board){
//             if(pos.second.compare(position) == 0 && pos.first.compare(" ") != 0){
//                 return pos.first.c_str();
//             }
//         }   

//     }
    
// }

// int main(){

//     std::map<std::string, std::string> board = {
//         {"b_rook1", "a8"}, {"b_knight1", "b8"}, {"b_bishop1", "c8"}, {"b_queen", "d8"}, {"b_king", "e8"}, {"b_bishop2", "f8"}, {"b_knight2", "g8"}, {"b_rook2", "h8"},
//         {"b_pawn1", "a7"}, {"b_pawn2", "b7"}, {"b_pawn3", "c7"}, {"b_pawn4", "d7"}, {"b_pawn5", "e7"}, {"b_pawn6", "f7"}, {"b_pawn7", "g7"}, {"b_pawn8", "h7"},
//         {"empty", "a6"}, {"empty", "b6"}, {"empty", "c6"}, {"empty", "d6"}, {"empty", "e6"}, {"empty", "f6"}, {"empty", "g6"}, {"empty", "h6"},
//         {"empty", "a5"}, {"empty", "b5"}, {"empty", "c5"}, {"empty", "d5"}, {"empty", "e5"}, {"empty", "f5"}, {"empty", "g5"}, {"empty", "h5"},
//         {"empty", "a4"}, {"empty", "b4"}, {"empty", "c4"}, {"empty", "d4"}, {"empty", "e4"}, {"empty", "f4"}, {"empty", "g4"}, {"empty", "h4"},
//         {"empty", "a3"}, {"empty", "b3"}, {"empty", "c3"}, {"empty", "d3"}, {"empty", "e3"}, {"empty", "f3"}, {"empty", "g3"}, {"empty", "h3"},
//         {"w_pawn1", "a2"}, {"w_pawn2", "b2"}, {"w_pawn3", "c2"}, {"w_pawn4", "d2"}, {"w_pawn5", "e2"}, {"w_pawn6", "f2"}, {"w_pawn7", "g2"}, {"w_pawn8", "h2"},
//         {"w_rook1", "a1"}, {"w_knight1", "b1"}, {"w_bishop1", "c1"}, {"w_queen", "d1"}, {"w_king", "e1"}, {"w_bishop2", "f1"}, {"w_knight2", "g1"}, {"w_rook2", "h1"}
// };

//     const char* check = movePiece("c3", board);
//     std:: cout << check;

//     return 0;
// }