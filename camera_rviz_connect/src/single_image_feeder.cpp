#include <pylon/PylonIncludes.h>
// #include <pylon/BaslerUniversalInstantCamera.h>
#include <string>
#include <opencv2/core/core.hpp>
#include "opencv2/highgui/highgui.hpp"
#include <iostream>
#include <chrono>
#include <opencv2/imgproc/imgproc.hpp>


// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using GenApi objects.
using namespace GenApi;

// Namespace for using cout.
using namespace std;

uint16_t width = 1920;
uint16_t height = 1080;
uint8_t fps = 30;
uint16_t narrow_AutoExposureTimeUpperLimit = 1000;
uint16_t wide_AutoExposureTimeUpperLimit = 10000;
String_t PixelFormat = "YCbCr422_8" ;


void Initialize_cam(CInstantCamera& camera);
void background_loop(CInstantCamera& camera);
void visualize(cv::Mat& frame);

int main( int /*argc*/, char* /*argv*/[] )
{

    // The exit code of the sample application.

    int exitCode = 0;
    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {

        // Create an instant camera object with the camera found first.
        CInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        camera.Open();
        Initialize_cam(camera);
        INodeMap& nodemap = camera.GetNodeMap();
        cout << "chunk enable" << camera.ChunkNodeMapsEnable.GetValue() << endl;
        camera.ChunkNodeMapsEnable.SetValue(false);
        cout << "chunk enable_2" << camera.ChunkNodeMapsEnable.GetValue() << endl;



        background_loop(camera);

        camera.Close();
        PylonTerminate();
    }
    catch (const GenericException& e)
    {
        // Error handling.
        cerr << "An exception occurred." << endl
            << e.GetDescription() << endl;
        exitCode = 1;
    }

    // Comment the following two lines to disable waiting on exit.
    cerr << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n');

    // Releases all pylon resources.
    PylonTerminate();

    return exitCode;
}

void Initialize_cam(CInstantCamera& camera){
    String_t cam_name = camera.GetDeviceInfo().GetUserDefinedName();

    INodeMap& nodemap = camera.GetNodeMap();

    // set default configuration
    CEnumParameter (nodemap, "UserSetSelector").SetValue("Default");
    CCommandParameter(nodemap, "UserSetLoad").Execute();

    CIntegerParameter ( nodemap, "Width" ).SetValue(width);
    CIntegerParameter ( nodemap, "Height" ).SetValue(height);
    CEnumParameter (nodemap, "PixelFormat").SetValue(PixelFormat);
    CFloatParameter (nodemap, "AcquisitionFrameRate").SetValue(fps);
    CEnumParameter (nodemap, "ExposureAuto").SetValue("Continuous");

    if (cam_name == "Wide"){
        CFloatParameter(nodemap,"AutoExposureTimeUpperLimit").SetValue(wide_AutoExposureTimeUpperLimit);
    }
    else if (cam_name == "Narrow"){
        CFloatParameter(nodemap,"AutoExposureTimeUpperLimit").SetValue(narrow_AutoExposureTimeUpperLimit);
        CBooleanParameter(nodemap, "ReverseX").SetValue(true);
        CBooleanParameter(nodemap, "ReverseY").SetValue(true);

    }

}

void visualize(cv::Mat& frame){ 
    cv::cvtColor(frame, frame, cv::COLOR_BGR2RGB);
    string windowName = "frame"; //Name of the window
    cv::namedWindow(windowName); // Create a window
    cv::imshow(windowName, frame);
    cv::waitKey(1);
}


class ImageHandler : public CImageEventHandler
{
public:
    CImageFormatConverter format_converter;
    CPylonImage image_converted;

    chrono::steady_clock::time_point time_old = chrono::steady_clock::now();
    chrono::steady_clock::time_point time_new = chrono::steady_clock::now();
    float duration;

    ImageHandler(){
        format_converter.OutputPixelFormat = PixelType_RGB8packed;
        format_converter.OutputBitAlignment = OutputBitAlignment_MsbAligned;
    }
    void OnImageGrabbed( CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult )
    {
        cout << "OnImageGrabbed event for device " << camera.GetDeviceInfo().GetUserDefinedName()<< endl;
        cv::Mat image;
        if (ptrGrabResult->GrabSucceeded()){

            format_converter.Convert(image_converted, ptrGrabResult);
            image = cv::Mat(ptrGrabResult->GetHeight(), ptrGrabResult->GetWidth(), CV_8UC3, (uint8_t *) image_converted.GetBuffer());
            visualize(image);
            time_new = chrono::steady_clock::now();
            duration = chrono::duration_cast<std::chrono::microseconds>(time_new - time_old).count();  //micro seconds
            time_old = time_new;
            cout << "rate = " << 1000000/(duration) << endl;  //Hz

        }
        else{
            std::cout << "Error: " << std::hex << ptrGrabResult->GetErrorCode() << std::dec << " " << ptrGrabResult->GetErrorDescription() << std::endl;
        }
    }
};

void background_loop(CInstantCamera& camera){

    CImageEventHandler* image_handler = new ImageHandler;
    camera.RegisterImageEventHandler( image_handler, RegistrationMode_Append, Cleanup_Delete );
    camera.StartGrabbing( GrabStrategy_LatestImageOnly, GrabLoop_ProvidedByInstantCamera );

    try{

        while (camera.IsGrabbing()){
            continue;
        }
    }
    catch (const GenericException& e) {
        // Error handling.
        cerr << "An exception occurred." << endl << e.GetDescription() << endl;
        camera.StopGrabbing();
        camera.DeregisterImageEventHandler(image_handler);
        camera.Close();
        cv::destroyAllWindows();
    }
    

    return;
}