
from flask import jsonify, request, Response
from kswic_objs import *
from kswic_config import *
import base64
import struct

@jsonp
def getWinAuthInfo():
    
    # Some magic to decode an NTLM auth header for username/domain/pc info
    auth_type = 'NTLM'
    actual_header = request.headers.get('Authorization', '')
    expected_signature = b'NTLMSSP\x00'
    msg = base64.b64decode(actual_header[len(auth_type):])
    signature = msg[0:8]

    if signature != expected_signature:
        jsonify(success=False,
                error="Mismatch on NTLM message signature, expecting: %s, actual: %s" % (expected_signature,
                                                                                            signature)
        )

    try:
        domain_length = str(int.from_bytes(msg[28:29], 'little'))
        domain_offset = str(int.from_bytes(msg[32:33], 'little'))
        user_length = str(int.from_bytes(msg[36:37], 'little'))
        user_offset = str(int.from_bytes(msg[40:41], 'little'))
        host_length = str(int.from_bytes(msg[44:45], 'little'))
        host_offset = str(int.from_bytes(msg[48:49], 'little'))
        domain_txt = msg[int(domain_offset):int(domain_offset)+int(domain_length):2].decode()
        user_txt = msg[int(user_offset):int(user_offset)+int(user_length):2].decode()
        host_txt = msg[int(host_offset):int(host_offset)+int(host_length):2].decode()

        if user_length == "0":
            return Response("NTLM non-cached Credentials not provided - please don't send cached creds for auth endpoint!", 401, {'WWW-Authenticate':'Basic realm="NTLM non-cached Credentials not provided"'})

    except Exception as e:
        jsonify(success=False,
                error="Error trying to decode NTLM auth header",
                exception=str(repr(e))
        )

    if user_txt:
        return jsonify(success=True,
                       domain_txt=domain_txt,
                       user_txt=user_txt,
                       host_txt=host_txt,
                       message='Please contact Matthew.Brown1@ascension.org with any questions.')
    else:
        return jsonify(success=False,
                       error="Error, no NTLM auth header found")



