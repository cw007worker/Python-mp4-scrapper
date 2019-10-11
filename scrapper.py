#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
    Script for work with m8u8 file,
    to get .ts from url and build it to mp4
    Copyright (C) 2019
    Konstantin Nesterov <pardusurbanus@protonmail.com>
"""
import argparse
import sys
import subprocess
import requests

def main():
  
  parser = argparse.ArgumentParser()
  
  parser.add_argument("-m", "--m8u8-url", type=str, help='Path to the m8u8 playlist file')
  parser.add_argument("-f", "--ffmpeg-path", type=str, help='Path to the ffmpeg binary')
  args = parser.parse_args()
  print(args)

  if args.m8u8_url:
    ts_filenames = [line.rstrip() for line in 
                    requests.get(args.m8u8_url).text.split('\n') 
                    if line.rstrip().endswith('.ts')]
    baseurl = args.m8u8_url.replace((args.m8u8_url.split('/')[-1]),"")
    if args.ffmpeg_path:
      ffbin = args.ffmpeg_path
      with open("video.ts", "wb") as f:
        for file in ts_filenames:
          res = requests.get("{}{}".format(baseurl,file),stream=True)
          if res.status_code == 200:
            for chunk in res:
              f.write(chunk)
      subprocess.run([ffbin, '-i', "video.ts", 'video.mp4'])    
    else:
      print("Check ffmpeg binary patch")
      sys.exit(2)
  else:
      print("Check m8u8 url")
      sys.exit(2)

if __name__ == "__main__":
  main()

