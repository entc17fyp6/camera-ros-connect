#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <iomanip>

int main()
{
    std::fstream in("homography_matrix.txt");
    std::string line;
    int i = 0;
    int j = 0;
    float M[3][3]={};

    while (std::getline(in, line))
    {
        float value;
        std::stringstream ss(line);
        j = 0;
        while (ss >> value){
            M[i][j] = value;
            j++;
        }
        ++i;
    }
    for(int x=0;x<3;x++){
        for(int y=0;y<3;y++){
            std::cout << std::fixed << std::setprecision(14) << M[x][y] << "  ";
        }
        std::cout << "\n";
    }
}