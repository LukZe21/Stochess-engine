#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <utility>


int BOARD_SIZE = 8;

enum class Piece { EMPTY, PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING};

enum Color { WHITE, BLACK};

struct ChessPiece{
    Piece piece;
    Color color;
};

using Board = std::vector<std::vector<ChessPiece>>;

void getMoves(int mouseX, int mouseY, std::vector<std::pair<int,int>> whitePiecesLocation){
    for(const auto& pair: whitePiecesLocation){
        if(mouseX>=pair.first && mouseX<=pair.second){
            std::cout<<"PIECE OUT";
        }
    }
}


Board initializeBoard(){
    Board board(BOARD_SIZE, std::vector<ChessPiece>(BOARD_SIZE, { Piece::EMPTY, Color::WHITE}));

    // white deck
    board[0][0] = {Piece::ROOK, Color::WHITE};
    board[0][1] = {Piece::KNIGHT, Color::WHITE};
    board[0][2] = {Piece::BISHOP, Color::WHITE};
    board[0][3] = {Piece::QUEEN, Color::WHITE};
    board[0][4] = {Piece::KING, Color::WHITE};
    board[0][5] = {Piece::BISHOP, Color::WHITE};
    board[0][6] = {Piece::KNIGHT, Color::WHITE};
    board[0][7] = {Piece::ROOK, Color::WHITE};
    board[1][0] = {Piece::PAWN, Color::WHITE};
    board[1][1] = {Piece::PAWN, Color::WHITE};
    board[1][2] = {Piece::PAWN, Color::WHITE};
    board[1][3] = {Piece::PAWN, Color::WHITE};
    board[1][4] = {Piece::PAWN, Color::WHITE};
    board[1][5] = {Piece::PAWN, Color::WHITE};
    board[1][6] = {Piece::PAWN, Color::WHITE};
    board[1][7] = {Piece::PAWN, Color::WHITE};

    // black deck
    board[7][0] = {Piece::ROOK, Color::BLACK};
    board[7][1] = {Piece::KNIGHT, Color::BLACK};
    board[7][2] = {Piece::BISHOP, Color::BLACK};
    board[7][3] = {Piece::QUEEN, Color::BLACK};
    board[7][4] = {Piece::KING, Color::BLACK};
    board[7][5] = {Piece::BISHOP, Color::BLACK};
    board[7][6] = {Piece::KNIGHT, Color::BLACK};
    board[7][7] = {Piece::ROOK, Color::BLACK};
    board[6][0] = {Piece::PAWN, Color::BLACK};
    board[6][1] = {Piece::PAWN, Color::BLACK};
    board[6][2] = {Piece::PAWN, Color::BLACK};
    board[6][3] = {Piece::PAWN, Color::BLACK};
    board[6][4] = {Piece::PAWN, Color::BLACK};
    board[6][5] = {Piece::PAWN, Color::BLACK};
    board[6][6] = {Piece::PAWN, Color::BLACK};
    board[6][7] = {Piece::PAWN, Color::BLACK};

    return board;

}


int move(Color color, int position){
    if(color == Color::BLACK){
        position -= 1;
    }
    else if(color==Color::WHITE){
        position += 1;
    }

    return position;
}

void drawBoard(Board& board);

int main(){
    int uInputRow;
    int uInputColumn;

    std::map<std::string, std::string> pieces;


    Board board = initializeBoard();

    drawBoard(board);


    do{
        std::cout << "\nChoose row - ";
        std::cin >> uInputRow;
        std::cout << "\nChoose column - ";
        std::cin >> uInputColumn;

        int pos = move(board[uInputRow][uInputColumn].color, uInputRow);
        
        std::cout << pos << '\n';

        ChessPiece temp = board[uInputRow][uInputColumn];
        board[uInputRow][uInputColumn] = {Piece::EMPTY, Color::WHITE};
        // std::cout << "Choose index:\n";
        // std::cout << "Choose row - ";
        // std::cin >> uInputRow;
        // std::cout << "\nChoose column - ";
        // std::cin >> uInputColumn;
        board[pos][uInputColumn] = temp;

        drawBoard(board); 
    }while(uInputRow != 90);


    return 0;
}



void drawBoard(Board& board){
    int idx = 0;
    for(int i=0; i<board.size(); i++){
        for(int j=0; j<board.size(); j++){
            switch (board[i][j].piece) {
                case Piece::EMPTY:
                    std::cout << ".";
                    break;
                case Piece::PAWN:
                    std::cout << (board[i][j].color == Color::WHITE ? "P" : "p");
                    break;
                case Piece::ROOK:
                    std::cout << (board[i][j].color == Color::WHITE ? "R" : "r");
                    break;
                case Piece::KNIGHT:
                    std::cout << (board[i][j].color == Color::WHITE ? "N" : "n");
                    break;
                case Piece::BISHOP:
                    std::cout << (board[i][j].color == Color::WHITE ? "B" : "b");
                    break;
                case Piece::QUEEN:
                    std::cout << (board[i][j].color == Color::WHITE ? "Q" : "q");
                    break;
                case Piece::KING:
                    std::cout << (board[i][j].color == Color::WHITE ? "K" : "k");
                    break;
            }
            std::cout<< " ";
        }
        std::cout<< " " <<idx;
        std::cout<< std::endl;
        idx += 1;
    }
    std::cout<< "0 1 2 3 4 5 6 7";
    
}