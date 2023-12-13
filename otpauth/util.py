import base64
import io

import qrcode


def qrcode_base64(data: str) -> str:
    qrcode_img = qrcode.make(data)
    file = io.BytesIO()
    qrcode_img.save(file)
    file_bytes = file.getvalue()
    b64 = base64.b64encode(file_bytes).decode()
    return 'data:image/png;charset=utf-8;base64,' + b64


def extract_num_from_str(txt: str) -> str:
    return ''.join([i for i in txt.split() if i.isdigit()])
