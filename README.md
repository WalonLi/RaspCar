# RaspCar

```
mjpg_streamer command...
$ ./mjpg_streamer -i “./input_uvc.so -y -f 30 -r 1024×768” -o “./output_http.so -w ./www”

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
```


```
GNU GENERAL PUBLIC LICENSE
Copyright (C) 2015  WalonLi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```