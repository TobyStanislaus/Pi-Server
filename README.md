# Pi-Server
The code that actually classifys whether a person is in the image or not - and then sends that to the Pi-nerf-gun

This project is an automatic nerf gun shooter. What the gun will be able to do is see if there is a person there, and if there is it will shoot.

For first go at this project, I planned on putting the model on the raspberry pi and run it locally from there. At first, I had a Pi2.  Additionally, for the pulling the trigger part, I bought a servo which I hoped would be strong enough to pull the trigger(Servo).

I used the YOLOv8 model (https://github.com/akanametov/yolo-face), for reliable detection of a person. Additionally, I started a quick demo testing that the model would work with a live stream of video on a webcam on my computer, of which it did very well.

Then, I set up the raspberry pi and hooked it up to a monitor and added other ways to connect to it (RealVNC and VSCode remote-ssh connections) Once done with that, I started by manipulating the LEDs on the PiFace module on the Pi (of which I don't need for this project)

Then I started to manipulate the servo, getting it to go to a certain angle and back repeatedly.

Then, I put it all together, and I got the first successful demo of the gun done, with a webcam that was not on the gun and a servo strapped on with only duct tape. However, when a face came up on the webcam, the gun would shoot.

Additionally, I upgraded to a Pi4 to speed up processing speed. Furthermore, I tried to increase processing speed by removing the OS on the pi and replace it with a more lightweight version, but that was tedious, and processing speed was unchanged.

PROBLEMS:
The gun is a funny shape - it is very difficult to fuse the webcam and other components onto the gun.
Time to process is very slow

What I am experimenting with now is sending pictures from the pi to the computer, for the computer to process, using mosquito to connect to the network to communicate.
