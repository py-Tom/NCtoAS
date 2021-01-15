# NCtoAS
This program translates the numeric code (ISO 6983) generated in CAD / CAM software for CNC machines into the AS language used by Kawasaki robots. Handles differences in code commands, machine kinematics, Euler angles, and motion interpolations. The easy-to-use interface allows you to translate with a few clicks. In addition, it allows you to save the coordinates of the base and the tool for later use.


## How to use
Run main.py and select the correct path for the input and output files. Set the coordinates of the tool and the base of the workpiece (the base should be set as when writing the code for a CNC machine). The generated AS program **should be tested** before loading to a robot (eg K-Roset).


#### Example

1. Define workpiece

2. Program machining process

3. Generate code

4. Translate to AS

5. Test

6. Upload and run
