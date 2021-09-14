from pypylon import pylon
import numpy as np
import cv2
import time
from matplotlib import pyplot as plt

# class EventPrinter(pylon.ConfigurationEventHandler):
#     def OnAttach(self, camera):
#         print(f'Before attaching the camera {camera}')

#     def OnAttached(self, camera):
#         print(f'Attached: {camera.GetDeviceInfo()}')

#     def OnOpen(self, camera):
#         print('Before opening')

#     def OnOpened(self, camera):
#         print('After Opening')

#     def OnDestroy(self, camera):
#         print('Before destroying')

#     def OnDestroyed(self, camera):
#         print('After destroying')

#     def OnClosed(self, camera):
#         print('Camera Closed')

#     def OnDetach(self, camera):
#         print('Detaching')

#     def OnGrabStarted(self, camera):
#         print('Grab started')
#         time.sleep(2)


# class ImageEventPrinter(pylon.ImageEventHandler):
#     def OnImagesSkipped(self, camera, countOfSkippedImages):
#         print("OnImagesSkipped event for device ", camera.GetDeviceInfo().GetModelName())
#         print(countOfSkippedImages, " images have been skipped.")
#         print()

#     def OnImageGrabbed(self, camera, grabResult):
#         print("OnImageGrabbed event for device ", camera.GetDeviceInfo().GetModelName())

#         # Image grabbed successfully?
#         if grabResult.GrabSucceeded():
#             print("SizeX: ", grabResult.GetWidth())
#             print("SizeY: ", grabResult.GetHeight())
#             img = grabResult.GetArray()
#             print("Gray values of first row: ", img[0])
#             print()
#         else:
#             print("Error: ", grabResult.GetErrorCode(), grabResult.GetErrorDescription())


# tl_factory = pylon.TlFactory.GetInstance()
# camera = pylon.InstantCamera()
# # camera.RegisterConfiguration(EventPrinter(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)
# # camera.RegisterImageEventHandler(ImageEventPrinter(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

# camera.Attach(tl_factory.CreateFirstDevice())

# camera.Open()
# camera.StartGrabbing(1)

# grab = camera.RetrieveResult(2000, pylon.TimeoutHandling_Return)
# if grab.GrabSucceeded():
#     img = grab.GetArray()
#     print(img.shape)

# camera.Close()
# print (img.shape)

# from pypylon import pylon

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# demonstrate some feature access
new_width = camera.Width.GetValue() - camera.Width.GetInc()
if new_width >= camera.Width.GetMin():
    camera.Width.SetValue(new_width)

numberOfImagesToGrab = 100
camera.StartGrabbingMax(numberOfImagesToGrab)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data.
        print("SizeX: ", grabResult.Width)
        print("SizeY: ", grabResult.Height)
        img = grabResult.Array
        print("Gray value of first pixel: ", img[0, 0])

    grabResult.Release()
camera.Close()