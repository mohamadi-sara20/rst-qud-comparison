# rst-qud-comparison

# Data 
The annotated data consists of 14 blogposts as well as chunks of 14 podcast transcripts. In some podcasts transcripts, more than one chunk of text has been annotated. This is indicated by a ```{episode_name}_p{chunk_id}```. For instance, two chunks have been taken from the DELL003 transcript and the filenames indicate those chunks as ```DELL003_Transkript_p1``` and ```DELL003_Transkript_p2```. 

# Conversion
To convert, use the convert_rst2qud script. The script needs an input directory and an output directory. The input directory should contain parenthetical RST trees. Look at ```rst/parenthetical``` directory to see expected input samples. 

```
python3 convert_rst2qud.py rst/parenthetical qud-output
```

(We will update this repository to make it possible to go from an .rs3 xml file to a QUD-like format.)

