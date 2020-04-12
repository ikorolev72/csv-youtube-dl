# Download a video from youtube using a CSV file and convert it according to the rules

## Version
#### 1.2 20200412

#### Whats new
1.2 20200412
  
  + Added watermark position
  + Added moveMaskWidthPercent  - possibility move mask to left or right from center ( for `make_veritcal=1` videos )

1.1.1 20200411
  
  + Fixed errors
  + Video codec changed to h264

1.0 20200409
  + initial version

## How to install

Requred: python3, youtube-dl, ffmpeg v4

#### youtube-dl
For macOS you can use docs [How to Install YouTube-dl on Mac](https://techwiser.com/how-to-install-youtube-dl-on-mac/) or [Install youtube-dl on Mac OSX](http://macappstore.org/youtube-dl/)

#### ffmpeg
Please, check the version of installed ffmpeg (`ffmpeg -version`) and if it beolw than 4, then you need install new version ( current 4.2.2 )
Binaries for MacOS can be downloaded [here](https://ffmpeg.zeranoe.com/builds/)



install application
```bash
git clone https://github.com/ikorolev72/csv-youtube-dl.git
cd csv-youtube-dl

```


## How to run
Make the copy of config file `data/config.json` and edit required values. 
Check values in `data/test.csv` and then simple run script.
```bash
cp data/config.json data/config.json.orig
vi data/config.json
vi data/test.csv

python3 do_video.py --csv data/test.csv
```

## Usage
You can define alternative config file with `--config` option :
``` bash
usage: python3 do_video.py -d file.csv [-h] [-c CONFIG] [-v]

arguments:
  -d file.csv           csv file with data
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to config file
  -v, --version         show program's version number and exit
```  


## Config format

Sample of config:
``` json
{
  "general": {    
    "youtube-dl" : "youtube-dl", // you can set there absolute path, if this program unavaliable by PATH 
    "ffmpeg": "ffmpeg",  // you can set there absolute path, if this program unavaliable by PATH 
    "ffprobe": "ffprobe", // you can set there absolute path, if this program unavaliable by PATH 
    "ffmpegLogLevel": "info", // set log level: debug, info, warning, error, alert, etc
    "tmpDir": "tmp",   // path for temporary files
    "outputDir": "./output"  // path for output files
  },
  "video": {
    "watermarkFile" : "images/watermark.png", // path to watermark image
    "watermarkPosition" : "top-right", // values: bottom-right( default), bottom-left, bottom-middle, top-right, top-left, top-middle, center-right, center-left, center-middle
    "moveMaskWidthPercent" : 50, //  you can move crop part to left or right. Values: from 0 to 100, default - 50 ( center ). 0 - left part, 100 - right.
    "width": 852, 
    "height": 480
  }
 }
```

## CSV data file format
```csv
id,time_start,time_finish,link,make_vertical,placeholder,both_sides,watermark
1,100,115,https://www.youtube.com/watch?v=l8Dd9hnMLYc,0,images/placeholder.jpg,0,1
2,11,26,https://www.youtube.com/watch?v=-_4qtEnC_68,0,images/placeholder.jpg,1,0
```
Notes:
Header with column names - required!
 + id
 + time_start (in seconds)
 + time_finish (in seconds from the start of the video)
 + link (link to a youtube video from the start of the video)
 + make_vertical (boolean). if make_vertical = 1, then ffmpeg cuts a 9:16 vertical fragment from the video (symmetrical relative to the center of the video) from "time_start" to "time_finish". IF make_vertical = 0, then 
ffmpeg coverts the 16:9 original video to 9:16 with two black strips on either side
 + placeholder (a jpg file name) . if "placeholder" is not empty, ffmpeg places a static jpg placeholder on both sides or top/bottom as "both_sides"
 + both_sides (integer ) 1 = top & bottom, 2 = only top-side, 3 = only bottom-side
 + Watermark  - (a jpg/png file name) watermark in the botton right corner




##  Bugs
##  ------------

##  Licensing
  ---------
	GNU

  Contacts
  --------

     o korolev-ia [at] yandex.ru
     o http://www.unixpin.com
