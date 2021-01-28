class ServerCommand:
    request_authorized = b'authorized'
    frame_chunk_received = b'received'


class ClientCommand:
    request_permission_to_send_frame = b'request'
    frame_sent = b'sent'
