class ServerCommand:
    request_frame = b'request'
    frame_chunk_received = b'chunk_received'


class ClientCommand:
    frame_sent = b'sent'
