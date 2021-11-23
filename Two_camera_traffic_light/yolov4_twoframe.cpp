#include <iostream>
#include <queue>
#include <iterator>
#include <sstream>
#include <fstream>
#include <iomanip>
#include <chrono>
#include <string> 

#include "opencv2/core.hpp"
#include "opencv2/dnn.hpp"
#include "opencv2/dnn/all_layers.hpp"

#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"

// using namespace std


constexpr float CONFIDENCE_THRESHOLD = 0;
constexpr float NMS_THRESHOLD = 0.4;
constexpr int NUM_CLASSES = 5;

// colors for bounding boxes
const cv::Scalar colors[] = {
    {0, 255, 255},
    {255, 255, 0},
    {0, 255, 0},
    {255, 0, 0}
};
const auto NUM_COLORS = sizeof(colors)/sizeof(colors[0]);

int main()
{
    std::vector<std::string> class_names;
    {
        std::ifstream class_file("classes.txt");
        if (!class_file)
        {
            std::cerr << "failed to open classes.txt\n";
            return 0;
        }

        std::string line;
        while (std::getline(class_file, line))
            class_names.push_back(line);
    }

    cv::VideoCapture source("/home/fyp2selfdriving/Documents/traffic_light/yolov4/darknet/video/traffic_light_compressed.mp4");
    cv::VideoCapture source2("/home/fyp2selfdriving/Documents/traffic_light/yolov4/darknet/video/traffic_lights.mp4");

    auto net = cv::dnn::readNetFromDarknet("/home/fyp2selfdriving/Documents/traffic_light/yolov4/darknet/cfg/yolov4-custom.cfg", "/home/fyp2selfdriving/Documents/traffic_light/yolov4/training/yolov4-custom_best.weights");
    net.setPreferableBackend(cv::dnn::DNN_BACKEND_CUDA);
    net.setPreferableTarget(cv::dnn::DNN_TARGET_CUDA_FP16);
    // net.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
    // net.setPreferableTarget(cv::dnn::DNN_TARGET_CPU);
    // net.setInputsNames("input");
    // net.setInputShape((2,3,608,608));
    auto output_names = net.getUnconnectedOutLayersNames();

    cv::Mat frame, frame2, blob;
    std::vector<cv::Mat> detections;
    std::vector<cv::Mat> samples(2);

    // std::cout << "model loaded" << std::endl;

    while(cv::waitKey(1) < 1)
    {
        source >> frame;
        source2 >> frame2;
        if (frame.empty() or frame2.empty())
        {
            cv::waitKey();
            break;
        }

        samples[0] = frame;
        samples[1] = frame2;

        auto total_start = std::chrono::steady_clock::now();
        cv::dnn::blobFromImages(samples, blob, 0.00392, cv::Size(608, 608), cv::Scalar(), true, false, CV_32F);
        // std::cout << blob.size << std::endl;
        net.setInput(blob);

        auto dnn_start = std::chrono::steady_clock::now();
        net.forward(detections, output_names);
        auto dnn_end = std::chrono::steady_clock::now();

        std::vector<cv::Range> ranges;

        for (int z = 0; z < 2; z++)
        {
            std::vector<int> indices[NUM_CLASSES];
            std::vector<cv::Rect> boxes[NUM_CLASSES];
            std::vector<float> scores[NUM_CLASSES];

            for (auto& output : detections)
            {
            
                const auto num_boxes = output.size[1];
                for (int i = 0; i < num_boxes; i++)
                {
                    auto x = output.at<float>(z,i, 0) * samples[z].cols;
                    auto y = output.at<float>(z,i, 1) * samples[z].rows;
                    auto width = output.at<float>(z,i, 2) * samples[z].cols;
                    auto height = output.at<float>(z,i, 3) * samples[z].rows;
                    cv::Rect rect(x - width/2, y - height/2, width, height);

                    for (int c = 0; c < NUM_CLASSES; c++)
                    {
                        auto confidence = *output.ptr<float>(z,i, 5 + c);
                        if (confidence >= CONFIDENCE_THRESHOLD)
                        {
                            boxes[c].push_back(rect);
                            scores[c].push_back(confidence);
                        }
                    }
                }
                // }
            }

            // std::cout << sizeof(boxes) << std::endl;

            // std::cout << scores.size() << std::endl;

            // std::cout << "scores and boxes done" << std::endl;
            for (int c = 0; c < NUM_CLASSES; c++)
                cv::dnn::NMSBoxes(boxes[c], scores[c], 0.0, NMS_THRESHOLD, indices[c]);
            
            for (int c= 0; c < NUM_CLASSES; c++)
            {
                for (size_t i = 0; i < indices[c].size(); ++i)
                {
                    const auto color = colors[c % NUM_COLORS];

                    auto idx = indices[c][i];
                    const auto& rect = boxes[c][idx];
                    cv::rectangle(samples[z], cv::Point(rect.x, rect.y), cv::Point(rect.x + rect.width, rect.y + rect.height), color, 3);

                    std::ostringstream label_ss;
                    label_ss << class_names[c] << ": " << std::fixed << std::setprecision(2) << scores[c][idx];
                    auto label = label_ss.str();
                    
                    int baseline;
                    auto label_bg_sz = cv::getTextSize(label.c_str(), cv::FONT_HERSHEY_COMPLEX_SMALL, 1, 1, &baseline);
                    cv::rectangle(samples[z], cv::Point(rect.x, rect.y - label_bg_sz.height - baseline - 10), cv::Point(rect.x + label_bg_sz.width, rect.y), color, cv::FILLED);
                    cv::putText(samples[z], label.c_str(), cv::Point(rect.x, rect.y - baseline - 5), cv::FONT_HERSHEY_COMPLEX_SMALL, 1, cv::Scalar(0, 0, 0));
                }
            }
            // std::cout << "nms done" << std::endl;
        
            auto total_end = std::chrono::steady_clock::now();

            float inference_fps = 1000.0 / std::chrono::duration_cast<std::chrono::milliseconds>(dnn_end - dnn_start).count();
            float total_fps = 1000.0 / std::chrono::duration_cast<std::chrono::milliseconds>(total_end - total_start).count();
            std::ostringstream stats_ss;
            stats_ss << std::fixed << std::setprecision(2);
            stats_ss << "Inference FPS: " << inference_fps << ", Total FPS: " << total_fps;
            auto stats = stats_ss.str();
                
            int baseline;
            auto stats_bg_sz = cv::getTextSize(stats.c_str(), cv::FONT_HERSHEY_COMPLEX_SMALL, 1, 1, &baseline);
            cv::rectangle(samples[z], cv::Point(0, 0), cv::Point(stats_bg_sz.width, stats_bg_sz.height + 10), cv::Scalar(0, 0, 0), cv::FILLED);
            cv::putText(samples[z], stats.c_str(), cv::Point(0, stats_bg_sz.height + 5), cv::FONT_HERSHEY_COMPLEX_SMALL, 1, cv::Scalar(255, 255, 255));

            cv::namedWindow("output"+std::to_string(z),cv::WINDOW_NORMAL);

            // std::cout << "visualizing" << std::endl;
            cv::imshow("output"+std::to_string(z), samples[z]);

        }
        auto total_end = std::chrono::steady_clock::now();
        float total_fps = 1000.0 / std::chrono::duration_cast<std::chrono::milliseconds>(total_end - total_start).count();
        std::cout << "Total FPS: "<< total_fps << std::endl;
    }

    return 0;
}