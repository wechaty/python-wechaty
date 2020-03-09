"""
message object which handle the message sending
"""


# pylint: disable=R0903
class Message:
    """
    message object which can handle the message sending
    """
    def __init__(self):
        """
        initialization
        """
        raise NotImplementedError

    @classmethod
    def load(cls, msg_id: str) -> "Message":
        """
        load message
        """
        raise NotImplementedError

    async def ready(self):
        """
        sync load message
        """
        raise NotImplementedError
