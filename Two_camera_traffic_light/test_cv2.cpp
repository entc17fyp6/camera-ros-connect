
#include <string>
#include <opencv2/opencv.hpp>
#include <iostream>
#include "opencv2/imgcodecs.hpp"


using namespace std;



int main( int /*argc*/, char* /*argv*/[] )
{
    string windowName = "aa";
    cv::Mat image = cv::imread("/home/fyp/Desktop/test.png");
    cv::namedWindow(windowName); // Create a window
    cv::imshow(windowName, image);
    cv::waitKey(0);
}
