# -*- coding: utf-8 -*-
"""
qr_code helper utils
"""
import platform
import qrcode   # type: ignore


def qr_terminal(data: str, version=None):
    """
    create qr_code
    :param data: qrcode data
    :param version:1-40 or None
    :return:
    """
    if platform.system() == 'Windows':
        white_block = '▇'
        black_block = '  '
        new_line = '\n'
    else:
        white_block = '\033[0;37;47m  '
        black_block = '\033[0;37;40m  '
        new_line = '\033[0m\n'

    qr = qrcode.QRCode(version)
    qr.add_data(data)
    if version:
        qr.make()
    else:
        qr.make(fit=True)
    output = white_block * (qr.modules_count + 2) + new_line
    for mn in qr.modules:
        output += white_block
        for m in mn:
            if m:
                output += black_block
            else:
                output += white_block
        output += white_block + new_line
    output += white_block * (qr.modules_count + 2) + new_line
    print(output)
