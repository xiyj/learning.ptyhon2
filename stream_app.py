'''
stream/trunk
'''

#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.
Example usage:
    python transcribe_streaming.py resources/audio.raw
"""

# [START import_libraries]
import argparse
import io
# [END import_libraries]


def gen_chunk(stream_file, chunk_size) :
    with io.open(stream_file, 'rb') as audio_file:
        while True :
            content = audio_file.read(chunk_size)
            if len(content) == 0 :
                break;
            print("will yield content, len %d"%len(content))
            yield content


def transcribe_streaming(stream_file):

    for i, chunk in enumerate(gen_chunk(stream_file, 512)):
        print("chunk %d, type : %s, len %d, content : %s"%(i, type(chunk), len(chunk), chunk))
        print("decoded chunk :  \n%s"%(chunk.decode("utf-8")))

if __name__ == '__main__':
    # transcribe_streaming('e:\\tmp\\dwhelper\\out.wav')
    # transcribe_streaming('e:\\tmp\\dwhelper\\Five black fuckers are excitingly fondling and fucking one s.mp4');
    transcribe_streaming('e:\\programdata\\anaconda3\\envs\\learning\\lib\\site-packages\\six.py')
