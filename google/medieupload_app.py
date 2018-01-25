import google.auth
import google.auth.transport.requests as tr_requests
import os
import io

from google.resumable_media.requests import Download
from google.resumable_media.requests import ResumableUpload
from google.resumable_media.requests import SimpleUpload

def simple_download(bucket, blob) :
    url_template = (
        u'https://www.googleapis.com/download/storage/v1/b/'
        u'{bucket}/o/{blob_name}?alt=media')
    media_url = url_template.format(bucket = bucket, blob_name = blob)
    print('simple_download from url : ', media_url)
    download = Download(media_url)
    response = download.consume(transport)
    print('download.finished : ', download.finished)
    print('response : ', response)
    print('response.headers[Content-Length]', response.headers[u'Content-Length'])
    print('len(response.content)', len(response.content))

def simple_upload(bucket, blob, filename) :
    url_template = (
        u'https://www.googleapis.com/upload/storage/v1/b/{bucket}/o?'
        u'uploadType=resumable')
    upload_url = url_template.format(bucket=bucket)
    print('resumable_upload to url : ', upload_url)
    chunk_size = 1024 * 1024 * 1
    upload = SimpleUpload(upload_url)

    stream = open(filename, u'rb')
    total_bytes = os.path.getsize(filename)
    print("file %s, size %d"%(filename, total_bytes))
    metadata = {u'name': filename}

    content_type = u'text/plain'
    response = upload.transmit(transport, stream, content_type)

    print("response.headers[u'Location']", response.headers[u'Location'])
    json_response = response.json()
    print("done, json response : ", json_response)

def resumable_upload(bucket, blob, filename) :
    url_template = (
        u'https://www.googleapis.com/upload/storage/v1/b/{bucket}/o?'
        u'uploadType=resumable&name=myobj')
    upload_url = url_template.format(bucket=bucket)
    print('resumable_upload to url : ', upload_url)
    chunk_size = 1024 * 1024 * 1
    upload = ResumableUpload(upload_url, chunk_size)

    stream = open(filename, u'rb')
    total_bytes = os.path.getsize(filename)
    print("file %s, size %d"%(filename, total_bytes))

    metadata = {u'name': filename}

    # response = upload.initiate(transport, stream, metadata, u'text/plain', total_bytes = total_bytes)
    response = upload.initiate(transport, stream, metadata, u'text/plain')
    print("upload.resumable_url : ", upload.resumable_url)
    print("response.headers[u'Location']", response.headers[u'Location'])
    print("total %d, upload.total_bytes %d"%(total_bytes, upload.total_bytes))
    print("response.headers[u'X-GUploader-UploadID']", response.headers[u'X-GUploader-UploadID'])
    while not upload.finished or total_bytes > upload.total_bytes :
        response0 = upload.transmit_next_chunk(transport)
        print("total %d, upload.total_bytes %d"%(total_bytes, upload.total_bytes))
    json_response = response0.json()
    print("done, json response : ", json_response)

if __name__ == '__main__' :
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "e:\\xyj\\journal\\_all.blue.solutions\\google.service.account\\james-freeswtich-gsr-f2fafcbb54f6.json"
    print("env GOOGLE_APPLICATION_CREDENTIALS : ", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    # adc, project = google.auth.default()
    # print("google auth, adc %s, project %s"%(adc, project))
    # transport = tr_requests.AuthorizedSession(adc)

    ro_scope = u'https://www.googleapis.com/auth/devstorage.read_only'
    credentials, project = google.auth.default(scopes=(ro_scope,))
    print("google auth, credential %s, project %s"%(credentials, project))
    transport = tr_requests.AuthorizedSession(credentials)

    if False :
        simple_download('freeswitch-gsr', 'out.wav')

    if True :
        simple_upload('freeswitch-gsr', 'out.wav', 'e:\\tmp\\dwhelper\\out.wav')
        # resumable_upload('freeswitch-gsr', 'out.wav', 'e:\\tmp\\dwhelper\\out.wav')

    if False :
        data = b'Some not too large content.'
        resumable_upload_data('freeswitch-gsr', 'out.wav', data)

    print('- done -')

