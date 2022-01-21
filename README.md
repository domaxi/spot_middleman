# spot_middleman

Spot Middleman is a Python application that handles the information flow between SPOT-IT-3D and the client.

## Installation Guide
Run the installation script to install the dependencies.
```
pip install -r /path/to/requirements.txt
```

Run the server using this command:
```
python3 server.py
```
# Documentation
SPOT-IT-3D will output frames with annotated information, which will be POST-ed onto the middleman. GET requests can be sent to the middleman to retrieve these frames. An added functionality is the conversion of relative coordinates to absolute coordinates in Latitude and Longitude, given a specific set of base coordinates. The following will document the various methods used.
> Base URL: "localhost:5000"

This process can be observed in the following flow chart:

<b>Latestframe & Listframe</b>

![This is a flowchart showing the process for the data stream](https://github.com/domaxi/spot_middleman/assets/images/Data Stream.png)

<b>Convert Coordinates</b>

![This is a flowchart showing the process for the convert function](https://github.com/domaxi/spot_middleman/assets/images/Convert.png)

## Format of JSON Packet
````
{
	"Detections" :
	[
		{
			“Frame-Number” : <Frame No.>,
			[
				“ID” : <ID No.>,
				“XYZ-Coordinates :
				[
					<X-Coordinate>
					<Y-Coordinate>
					<Z-Coordinate>
				]
			,
				“ID” : <ID No.>,
				“XYZ-Coordinates :
				[
					<X-Coordinate>
					<Y-Coordinate>
					<Z-Coordinate>
				]
			],
			<etc.>
		},
		{
		<Subsequent data>
		}
	]
}
````		
**Example**
````
{
	"Detections" :
	[
		{
			"Frame-Number" : "1",
			[
				"ID" : 0,
				"XYZ-Coordinates" : 
				[
					-5.5999999999999996,
					3.8100000000000001,
					10.17
				],
				"ID" : 1,
				"XYZ-Coordinates" : 
				[
					-5.5999999999999996,
					3.8100000000000001,
					10.17
				]
			]
		}
	]
}
````

## Latest Frame
````>> /latestframe ````
#### == GET ==
Returns JSON Object
Returns the latest frame available in the middleman.

\~Error Handling\~
- **Empty Buffer**
If there is no frame in the buffer, it will return:
> {'error': '404 Not Found: Frame not found. There is no frame(s) added to the frame buffer.'}
 - **Additional Parameters**
 Additional parameters in the URL after /latestframe
 > {'error': '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'}
 - **JSON File In Request**
 There will not be any issues experienced by the user.
 
 - **Additional Parameters In Request**
 The additional parameters will be discarded. The request parser only recognizes "Detections" as the argument.
 
#### == POST ==
Adds JSON object to the buffer array.  
If the buffer array is full (based on buffer size), the oldest frame will be overridden.  
This method takes in 3 main arguments:
````id````
Refers to frame ID number. **This field is required.**
````cameras````
Number of cameras in one frame. **This field is required.**
````objects````
Number of objects in one frame. **This field is required.**

\~Error Handling\~
- **Empty Frame**
An empty frame is posted to the middleman. The JSON packet has an empty "Detections" field.
> {'error': {'Detections': 'Please provide detection data in the request'}}
- **Non-JSON File**
A file of filetype other than JSON is posted to the middleman.
> {'error': {'Detections': 'Please provide detection data in the request'}}
- **Additional Parameters**
 Additional parameters in the URL after /latestframe
 > {'error': '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'}

## List Frames
````>> /listframes ````
#### == GET ==
Returns a JSON object.  
Returns the array of all frames in the buffer.  
Maximum size of array is the maximum size of the buffer.

\~Error Handling\~
- **Empty Buffer**
If there is no frame in the buffer, it will return:
> {'error': '404 Not Found: Frame not found. There is no frame(s) added to the frame buffer.'}
 - **Additional Parameters**
 Additional parameters in the URL after /latestframe
 > {'error': '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'}
 - **JSON File In Request**
 There will not be any issues experienced by the user.
 
 - **Additional Parameters In Request**
 The additional parameters will be discarded. The request parser only recognizes "Detections" as the argument.
## Convert
````>> /convert````
#### == POST ==
Returns JSON object.  
Returns the absolute position based on the relative position and benchmark position of cameras.  
This method takes in five arguments:

````base_lat````

Ranges from -90 degrees to +90 degrees

````base_long````

Ranges from -180 degrees to +180 degrees

> Latitude and Longitude are in units of degrees, arc-minutes, and arc-seconds

> 1 degree = 60 arc-minutes

> 1 arc-minute = 60 arc-seconds

````object_x````

Ranges from -inf to +inf

````object_z````

Ranges from 0 to +inf

````heading````

Ranges from 0 to 360 degrees
