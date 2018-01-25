'''
Google GSR stream async(?) examle
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
import os
# [END import_libraries]


def gen_chunk(stream_file, chunk_size) :
    with io.open(stream_file, 'rb') as audio_file:
        while True :
            content = audio_file.read(chunk_size)
            if len(content) == 0 :
                break;
            # print("will yield content, len %d"%len(content))
            yield content

# [START def_transcribe_streaming]
def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    if False :
        # [START migration_streaming_request]
        with io.open(stream_file, 'rb') as audio_file:
            content = audio_file.read()
        # In practice, stream should be a generator yielding chunks of audio data.
        stream = [content]

    stream = gen_chunk(stream_file, 1024 * 1024 * 2)
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)
    print("requests type :", type(requests))

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
    streaming_config = types.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    # [START migration_streaming_response]
    responses = client.streaming_recognize(streaming_config, requests)
    print("responses type : ", type(responses))
    # [END migration_streaming_request]

    count = 0
    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        count = count + 1
        print("count %d, response type : \n%s"%(count, type(response)))
        print("response : \n%s"%(dir(response)))
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print('Transcript: {}'.format(alternative.transcript))
    # [END migration_streaming_response]
# [END def_transcribe_streaming]


if __name__ == '__main__':
    if False :
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('stream', help='File to stream to the API')
        args = parser.parse_args()
        transcribe_streaming(args.stream)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "e:\\xyj\\journal\\_all.blue.solutions\\google.service.account\\Google Voice AGI-49236c65bec6.json"
    print("env GOOGLE_APPLICATION_CREDENTIALS : ", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    transcribe_streaming("e:\\tmp\\dwhelper\\out.wav")
    print("Done")

    #    gs://freeswtich-gsr/out.wav

