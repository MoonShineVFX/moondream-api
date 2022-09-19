import pytest

datas = [
    {
        "create": 1663561309,
        "creator": "test",
        "file_name": "file_2.mp4",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/video/file_2.mp4",
        "id": "93b4764783d04468b449b0ac477446c8",
        "path": "session/video/",
        "size": 1572966,
        "thumb_url": None,
        "type": "video"
    },
    {
        "create": 1663561309,
        "creator": "test",
        "file_name": "file_8T1riaM.jpg",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM.jpg",
        "id": "7e01fcc4fe94469680355a03f295a958",
        "path": "session/image/",
        "size": 367167,
        "thumb_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM_thumb.jpg",
        "type": "image"
    },
    {
        "create": 1663561389,
        "creator": "test",
        "file_name": "file_2.mp4",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/video/file_2.mp4",
        "id": "cdef79cec24f4735adcff8ab5b8ed06e",
        "path": "session/video/",
        "size": 1572966,
        "thumb_url": None,
        "type": "video"
    },
    {
        "create": 1663561389,
        "creator": "test",
        "file_name": "file_8T1riaM.jpg",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM.jpg",
        "id": "752a3723e5fc470faefddbea5448eac3",
        "path": "session/image/",
        "size": 367167,
        "thumb_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM_thumb.jpg",
        "type": "image"
    },
    {
        "create": 1663561450,
        "creator": "test",
        "file_name": "file_2.mp4",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/video/file_2.mp4",
        "id": "ecae1c9df56848559196bf4a119f3e2c",
        "path": "session/video/",
        "size": 1572966,
        "thumb_url": None,
        "type": "video"
    },
    {
        "create": 1663561450,
        "creator": "test",
        "file_name": "file_8T1riaM.jpg",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM.jpg",
        "id": "175dc36d73534b75b484314d1034fa7f",
        "path": "session/image/",
        "size": 367167,
        "thumb_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM_thumb.jpg",
        "type": "image"
    },
    {
        "create": 1663561478,
        "creator": "test",
        "file_name": "file_2.mp4",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/video/file_2.mp4",
        "id": "a1b823ec4cda459db434e92b6fc9e59b",
        "path": "session/video/",
        "size": 1572966,
        "thumb_url": None,
        "type": "video"
    },
    {
        "create": 1663561478,
        "creator": "test",
        "file_name": "file_8T1riaM.jpg",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM.jpg",
        "id": "228e4754c96747e9af76ea825f8d83ba",
        "path": "session/image/",
        "size": 367167,
        "thumb_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM_thumb.jpg",
        "type": "image"
    }
]


class TestGroup:
    def test_download(self, test_client):
        res = test_client.post('/session/download', datas={'datas': datas})
