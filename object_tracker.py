import cv2
import sys
import numpy as np

def conv(e,f):
   b=[]
   imagePoints = np.asarray([[40.0,460.0],[100.0,460.0],[40.0,420.0],[100.0,420.0]])
  #imagePoints = np.asarray([[113.0,115.0],[168.0,117.0],[112.0,157.0],[164.0,159.0]])
   objectPoints = np.asarray([[0.0,0.0,360.0],[20.0,0.0,360.0],[0.0,15.0,360.0],[20.0,15.0,360.0]])
   rvec = np.zeros((3,1))
   tvec = np.zeros((3,1))
   rotMat = np.zeros((3,3))
   cameraMatrix = np.asarray([[893.043,0,273.032],[0,893.043,186.014],[0,0,1]])

   cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, None, rvec, tvec)
   cv2.Rodrigues(np.array(rvec), rotMat)


   imageCoordinates = [[e],[f],[1]]

#s = -387.25 + (np.dot(np.linalg.inv(rotMat),tvec)[2][0]/np.dot(np.dot(np.linalg.inv(rotMat),np.linalg.inv(cameraMatrix)),imageCoordinates)[2])
   realCoordinate = np.dot(np.linalg.inv(rotMat),((np.dot(np.linalg.inv(cameraMatrix),imageCoordinates)*304.5)-tvec))
   b.append(realCoordinate[0])
   b.append(realCoordinate[1])
   return b



#Based on the version,the cv2.version gives an output like 3.1.1 .here major_ver will be 3,minor_ver be 1 and subminor_ver be 1. For versions less than 3.3 the tracker function is different. 




(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__' :
 
	# Set up tracker.
	# Instead of KCF, you can also use
	a=[] 
        cntroid=[]
        conv_c=[]
	tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
	tracker_type = tracker_types[2] #change the choice of tracker here
	#For versions less than  3.3 the cv2.Tracker|tracker name|_create() is different
	
	if int(minor_ver) < 3:
		tracker = cv2.Tracker_create(tracker_type)
	else:
		if tracker_type == 'BOOSTING':
			tracker = cv2.TrackerBoosting_create()
		if tracker_type == 'MIL':
			tracker = cv2.TrackerMIL_create()
		if tracker_type == 'KCF':
			tracker = cv2.TrackerKCF_create()
		if tracker_type == 'TLD':
			tracker = cv2.TrackerTLD_create()
		if tracker_type == 'MEDIANFLOW':
			tracker = cv2.TrackerMedianFlow_create()
		if tracker_type == 'GOTURN':
			tracker = cv2.TrackerGOTURN_create()
		if tracker_type == 'MOSSE':
			tracker = cv2.TrackerMOSSE_create()
		if tracker_type == "CSRT":
			tracker = cv2.TrackerCSRT_create()
 
	# Read video
	video = cv2.VideoCapture(0)   #we create an object for the videocapture class and get input from the 0-laptop camera , 1-webcam, ".mp4" - to track an object in a video
 
	# Exit if video not opened.
	if not video.isOpened():
		print "Could not open video"
		sys.exit()
	 
	img=cv2.imread('frame1.jpg')
	
	if img is None:

		while True:
			ok, frame = video.read()

			cv2.imshow("Select ROI", frame)
			#cv2.waitKey() returns a 32 Bit integer value (might be  dependent on the platform).    The key input is in ASCII which is an 8 Bit integer value. So you only care about these 8 bits and want all other bits to be 0. This you can achieve with:

			key = cv2.waitKey(1) & 0xff  
			if key == ord("i"):
				bbox = cv2.selectROI(frame, False)
				p1 = (int(bbox[0]), int(bbox[1]))
				p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
				a.append(p1[0])
				a.append(p1[1])
				a.append(p2[0])
				a.append(p2[1])
				p_cent = (int(bbox[0] + (bbox[2]/2)), int(bbox[1] + (bbox[3]/2)))
                                cntroid.append(p_cent[0])
                                cntroid.append(p_cent[1])
                                
                                conv_c=conv(cntroid[0],cntroid[1])
                                
                                
                                with open('coordinate_lines.txt', 'r') as f:
                                       pts=f.read()
                                pts_len=pts[0]
                                print pts[0]
                                for i in range(0,((pts_len)-1)):
                                  for j in range(0,1):
                                      cv2.line(img, (pts[i][j], pts[i][(j+1)]), (pts[(i+1)][j], pts[(i+1)][(j+1)]), (0,0,0), 2)         
                                with open('data_centriod.txt', 'w') as f:
				 
				  f.write('%d %d\n' % (conv_c[0],conv_c[1]) )
                               # f = open('data_centroid.txt', 'wb')
                                #for i in range(len(cntroid)):
    				#	f.write("%i\n" % cntroid[i])
				#f.close()
				#print p_cent  
                                del cntroid[:]
				
				with open('data_tracker.txt', 'w') as f:
					for i in range(0,4):
						f.write('%d\n' % a[i])
					
				cv2.rectangle(frame, p1, p2, (50,50,255), 2, 1)
				ok = tracker.init(frame, bbox)
				break
		
 
	# Read first frame.
		ok, frame = video.read()
		if not ok:
			print 'Cannot read video file'
			sys.exit()
 
		while True:
			# Read a new frame
			ok, frame = video.read()
			if not ok:
				break
			 
			# Start timer 
			# getTickCount() :function returns the number of clock-cycles after a reference event (like the moment machine was switched ON) to the moment this function is called. So if you call it before and after the function execution, you get number of clock-cycles used to execute a function.
			timer = cv2.getTickCount()
	 
			# Update tracker
			ok, bbox = tracker.update(frame)
			bbox = tuple(map(float, bbox))
	 
			# Calculate Frames per second (FPS)
			fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
	 
			# Draw bounding box
			if ok:
				# Tracking success
				p1 = (int(bbox[0]), int(bbox[1]))
				p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
				cv2.rectangle(frame, p1, p2, (0,215,0), 2, 5) #255 bgr values
				
				image = frame[int(bbox[1]):int(bbox[1] + bbox[3]),int(bbox[0]):int(bbox[0] + bbox[2])]
				cv2.imwrite("frame1.jpg", image)
                                
                                
				
				p_cent = (int(bbox[0] + (bbox[2]/2)), int(bbox[1] + (bbox[3]/2)))
                                cntroid.append(p_cent[0])
                                cntroid.append(p_cent[1])
                                
                                conv_c=conv(cntroid[0],cntroid[1])
                               
                                with open('data_centriod.txt', 'w') as f:
				 
				  f.write('%d %d\n' % (conv_c[0],conv_c[1]) )
     
                                with open('coordinate_lines.txt', 'r') as f:
                                       pts=f.read()
                                for i in range(0,(len(pts)-1)):
                                  for j in range(0,1):
                                    cv2.line(img, (pts[i][j], pts[i][(j+1)]), (pts[(i+1)][j], pts[(i+1)][(j+1)]), (0,0,0), 2)                           
                               # f = open('data_centroid.txt', 'wb')
                                #for i in range(len(cntroid)):
    				#	f.write("%i\n" % cntroid[i])
				#f.close()
				#print p_cent  
                                del cntroid[:]
				
			else :
				# Tracking failure
				cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
	 
			# Display tracker type on frame
			cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
		 
			# Display FPS on frame
			cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
                        b=[int(bbox[0]), int(bbox[1])]
                        #print b
	 	
			# Display result
			cv2.imshow("Tracking", frame)
	 
			# Exit if ESC pressed
			k = cv2.waitKey(1) & 0xff
			if k == 27 : break

	else:
		
		ok, frame = video.read()
		
		# Initialize bounding boxes	 
		bbox=[]
		f=open('data_tracker.txt',"r")
		for line in f:
			bbox.append(line.strip('\n'))

		bbox = tuple(map(float, bbox))	

		# Get points for rectangle	
		p1 = (int(bbox[0]), int(bbox[1]))
		p2 = (int(bbox[2]), int(bbox[3]))
		cv2.rectangle(frame, p1, p2, (50,50,255), 2, 1)

		# Get the tracker
		ok  = tracker.init(frame, (p1[0], p1[1], p2[0]-p1[0], p2[1]-p1[1]))	 #it is initializing  a bounding box to an img
		
		# Read first frame.
		ok, frame = video.read()
		if not ok:
			print 'Cannot read video file'
			sys.exit()
				
		while True:
			
			# Read a new frame
			ok, frame = video.read()
			if not ok:
				break

			# Start timer 
			# getTickCount() :function returns the number of clock-cycles after a reference event (like the moment machine was switched ON) to the moment this function is called. So if you call it before and after the function execution, you get number of clock-cycles used to execute a function.
			timer = cv2.getTickCount()
			
		 	# Update tracker
			ok, bbox = tracker.update(frame)
		 
		 	# Calculate Frames per second (FPS)
			fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
			# Draw bounding box
			if ok:
				# Tracking success
				p1 = (int(bbox[0]), int(bbox[1]))
				p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
				cv2.rectangle(frame, p1, p2, (0,215,0), 2, 5) #255 bgr values  
                                b=[int(bbox[0]), int(bbox[1])]
                                #print b
                                a.append(p1[0])
				a.append(p1[1])
				a.append(p2[0])
				a.append(p2[1])
				p_cent = (int(bbox[0] + (bbox[2]/2)), int(bbox[1] + (bbox[3]/2)))
                                
                                cntroid.append(p_cent[0])
                                cntroid.append(p_cent[1])
                                
                                conv_c=conv(cntroid[0],cntroid[1])
                               
                                with open('data_centriod.txt', 'w') as f:
				 
				  f.write('%d %d\n' % (conv_c[0],conv_c[1]) )
                               # f = open('data_centroid.txt', 'wb')
                                #for i in range(len(cntroid)):
    				#	f.write("%i\n" % cntroid[i])
				#f.close()
				#print p_cent  
                                del cntroid[:]
			else :
				# Tracking failure
				cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
			#  Display tracker type on frame
			cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
	 
			# Display FPS on frame
			cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
			# Display result
			cv2.imshow("Tracking", frame)
 
			# Exit if ESC pressed
			k = cv2.waitKey(1) & 0xff
			if k == 27 : break

