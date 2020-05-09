from typing import Dict

from chatie_grpc.wechaty import MessageType as ChatieMessageType, \
    MessagePayloadResponse

from wechaty_puppet import EventMessagePayload, MessageType


# TODO -> this should be improved later
from wechaty_puppet_hostie.utils import get_common_attributes

MESSAGE_TYPE_MAP: Dict[ChatieMessageType, MessageType] = {
    ChatieMessageType.MESSAGE_TYPE_MINI_PROGRAM.name: MessageType.MiniProgram,
    ChatieMessageType.MESSAGE_TYPE_LOCATION.name: MessageType.Location,
    ChatieMessageType.MESSAGE_TYPE_URL.name: MessageType.Url,
    ChatieMessageType.MESSAGE_TYPE_CONTACT.name: MessageType.Contact,
    ChatieMessageType.MESSAGE_TYPE_TEXT.name: MessageType.Text,
    ChatieMessageType.MESSAGE_TYPE_AUDIO.name: MessageType.Audio
}


def get_message_payload_from_response(response: MessagePayloadResponse
                                      ) -> EventMessagePayload:
    """
    :param response:
    :return:
    """
    payload_data = response
    common_attributes = get_common_attributes(
        payload_data, EventMessagePayload)

    common_attributes['message_id'] = payload_data.get(
        'id', None)
    message_type = payload_data.get('type', None)
    if message_type is None:
        raise ValueError('message response data is invalid, '
                         'not contains type field <%s>',
                         payload_data)
    common_attributes['type'] = MESSAGE_TYPE_MAP[message_type]
    payload = EventMessagePayload(**common_attributes)
    return payload


