# test_cam: test.cpp
# 	g++ test.cpp -o test_cam -I /media/fyp/sdCard/pylon/include -L /media/fyp/sdCard/pylon/lib -l pylonbase  -l GCBase_gcc_v3_1_Basler_pylon

# Makefile for Basler pylon sample program
.PHONY: all clean

# The program to build
NAME       ?= test

# Installation directories for pylon
PYLON_ROOT ?= /media/fyp/sdCard/pylon
CV_ROOT ?=  /media/fyp/sdCard/cv2_build/cv2_build

# Build tools and flags
LD         := $(CXX)
CPPFLAGS   := $(shell $(PYLON_ROOT)/bin/pylon-config --cflags)
CXXFLAGS   := #e.g., CXXFLAGS=-g -O0 for debugging
LDFLAGS    := $(shell $(PYLON_ROOT)/bin/pylon-config --libs-rpath)
LDLIBS     := $(shell $(PYLON_ROOT)/bin/pylon-config --libs)

CVCPPFLAGS 	:= -I $(CV_ROOT)/include/opencv4
CVLDFLAGS 	:= -L $(CV_ROOT)/lib -lopencv_core -lopencv_highgui -lopencv_videoio -lopencv_imgproc -lopencv_dnn -lopencv_imgcodecs

# Rules for building
all: $(NAME)

$(NAME): $(NAME).o
	$(LD) $(LDFLAGS) -o $@ $^ $(LDLIBS) $(CVLDFLAGS)

$(NAME).o: $(NAME).cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $< $(CVCPPFLAGS)

clean:
	$(RM) $(NAME).o $(NAME)

