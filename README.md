# RaspCar

```

setting...

sudo apt-get install subversion
svn co https://svn.code.sf.net/p/mjpg-streamer/code/ mjpg-streamer

sudo apt-get install libjpeg8-dev
sudo apt-get install imagemagick

cd mjpg-streamer/mjpg-streamer/
sudo make

crontab -e
@reboot /home/pi/Downloads/mjpg-streamer/mjpg-streamer/start.sh

$ cd /home/pi/Downloads/mjpg-streamer/mjpg-streamer/
$ ./mjpg_streamer -i "./input_uvc.so -y -f 30 -r 1024x768" -o "./output_http.so -w ./www"


Backup...

input
-d  specify device
-r  resolution
-f  fps
-y  YUYV format
-q  quality
-l  led blink or not

output
-w  streamer page
-p  port
-c  account manager
-n  option command...?

Reference website
http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/
http://www.ntex.tw/wordpress/545.html/
http://blog.csdn.net/harryching/article/details/27311947

Env
PYTHONPATH:/usr/local/lib/python3.4/site-packages
```

