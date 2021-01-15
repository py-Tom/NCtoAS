# NCtoAS
This program translates the numeric code (ISO 6983) generated in CAD / CAM software for CNC machines into the AS language used by Kawasaki robots. Handles differences in code commands, machine kinematics, Euler angles, and motion interpolations. The easy-to-use interface allows you to translate with a few clicks. In addition, it allows you to save the coordinates of the base and the tool for later use.


## How to use
Run main.py and select the correct path for the input and output files. Set the coordinates of the tool and the base of the workpiece (the base should be set as when writing the code for a CNC machine). The generated AS program **should be tested** before loading to a robot (eg K-Roset).


#### Example

1. Define the workpiece, program the machining process and generate the G-code.

<img src="/_examples/CAD.png" width="318" height="406" /> <img src="/_examples/CAM.png" width="318" height="406" />

2. Translate

<img src="/_examples/NCtoAS-interface.png" />

3. Test

<img src="/_examples/K-roset.png" />

4. Upload and run

<img src="/_examples/cropped_test.gif" width="466" height="350" />

