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

uint32_t width = 1920;
uint32_t height = 1080;
uint8_t fps = 30;
uint16_t narrow_AutoExposureTimeUpperLimit = 10000;
uint16_t wide_AutoExposureTimeUpperLimit = 10000;
String_t PixelFormat = "YCbCr422_8" ;

intptr_t narrow_cam_id = 0;
intptr_t wide_cam_id = 1;

void Initialize_cam(CInstantCamera& camera);
void background_loop(CInstantCameraArray& cameras);
void visualize(cv::Mat& frame);

int main( int /*argc*/, char* /*argv*/[] )
{

    // The exit code of the sample application.

    int exitCode = 0;
    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Get the transport layer factory.
        CTlFactory& tlFactory = CTlFactory::GetInstance();

        // Get all attached devices and exit application if no device is found.
        DeviceInfoList_t devices;
        if (tlFactory.EnumerateDevices( devices ) == 0)
        {
            throw RUNTIME_EXCEPTION( "No camera present." );
        }

        // Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        CInstantCameraArray cameras(devices.size());

        // Create and attach all Pylon Devices.
        for (size_t i = 0; i < cameras.GetSize(); ++i)
        {
            cameras[i].Attach( tlFactory.CreateDevice( devices[i] ) );
            Initialize_cam(cameras[i]);

            // Print the model name of the camera.
            cout << "Using device " << cameras[i].GetDeviceInfo().GetUserDefinedName() << endl;
        }




        background_loop(cameras);

        // cameras.Close();
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
    if (camera.IsOpen() == false){
        camera.Open();
    }
    camera.ChunkNodeMapsEnable.SetValue(false);

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
        camera.SetCameraContext(wide_cam_id);
    }
    else if (cam_name == "Narrow"){
        CFloatParameter(nodemap,"AutoExposureTimeUpperLimit").SetValue(narrow_AutoExposureTimeUpperLimit);
        CBooleanParameter(nodemap, "ReverseX").SetValue(true);
        CBooleanParameter(nodemap, "ReverseY").SetValue(true);
        camera.SetCameraContext(narrow_cam_id);
    }

}

void visualize(cv::Mat& frame, intptr_t cam_id){ 
    cv::cvtColor(frame, frame, cv::COLOR_BGR2RGB);
    string windowName = "frame_"+to_string(cam_id); //Name of the window
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
        intptr_t cam_id = camera.GetCameraContext();
        cv::Mat image;
        if (ptrGrabResult->GrabSucceeded()){

            format_converter.Convert(image_converted, ptrGrabResult);
            image = cv::Mat(height, width, CV_8UC3, (uint8_t *) image_converted.GetBuffer());
            visualize(image,cam_id);
            time_new = chrono::steady_clock::now();
            duration = chrono::duration_cast<std::chrono::microseconds>(time_new - time_old).count();  //micro seconds
            time_old = time_new;
            if (cam_id == narrow_cam_id){
                cout << "\t\t\t\t\t\tnarrow rate = " << 1000000/(duration) << endl;  //Hz

            }
            else{
                cout << "wide rate = " << 1000000/(duration) << endl;  //Hz
            }

        }
        else{
            std::cout << "Error: " << std::hex << ptrGrabResult->GetErrorCode() << std::dec << " " << ptrGrabResult->GetErrorDescription() << std::endl;
        }
    }
};

void background_loop(CInstantCameraArray& cameras){

    uint8_t cam_count = cameras.GetSize();
    CImageEventHandler* image_handlers [cam_count];

    for (uint8_t i=0;i<cam_count;i++){
        image_handlers[i] = new ImageHandler;
        cameras[i].RegisterImageEventHandler(image_handlers[i], RegistrationMode_Append, Cleanup_Delete);
    }
    cameras.StartGrabbing(GrabStrategy_LatestImageOnly, GrabLoop_ProvidedByInstantCamera);
    // CImageEventHandler* image_handler = new ImageHandler;
    // camera.RegisterImageEventHandler( image_handler, RegistrationMode_Append, Cleanup_Delete );
    // camera.StartGrabbing( GrabStrategy_LatestImageOnly, GrabLoop_ProvidedByInstantCamera );

    try{
        while (cameras.IsGrabbing()){
            continue;
        }
    }
    catch (const GenericException& e) {
        // Error handling.
        cerr << "An exception occurred." << endl << e.GetDescription() << endl;
        cameras.StopGrabbing();
        for(uint8_t i=0;i<cam_count;i++){
            cameras[i].DeregisterImageEventHandler(image_handlers[i]);
            cameras[i].Close();
        }
        // camera.DeregisterImageEventHandler(image_handler);
        // camera.Close();
        cv::destroyAllWindows();
    }
    

    return;
}