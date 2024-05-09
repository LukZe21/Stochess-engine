#include <iostream>
#include <vector>
#include <utility>



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
