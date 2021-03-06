from picamera import PiCamera
from picamera.array import PiRGBArray
from threading import Thread

class PiVideoStream:
    def __init__(self, resolution = (640, 480), framerate = 32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.hflip = True
        self.camera.vflip = True
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format = "bgr", use_video_port = True)
        self.frame = None
        self.stopped = False
    def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
    def update(self):
    	# keep looping infinitely until the thread is stopped
    	for f in self.stream:
    		# grab the frame from the stream and clear the stream in
    		# preparation for the next frame
    		self.frame = f.array
    		self.rawCapture.truncate(0)

    		# if the thread indicator variable is set, stop the thread
    		# and resource camera resources
    		if self.stopped:
    			self.stream.close()
    			self.rawCapture.close()
    			self.camera.close()
    			return
    def read(self):
    	# return the frame most recently read
    	return self.frame

    def stop(self):
    	# indicate that the thread should be stopped
    	self.stopped = True
