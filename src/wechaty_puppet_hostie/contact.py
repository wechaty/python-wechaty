from chatie_grpc.wechaty import ContactPayloadResponse
from chatie_grpc.wechaty import ContactGender as ChatieContactGender
from chatie_grpc.wechaty import ContactType as ChatieContactType

from wechaty_puppet import ContactPayload, ContactGender, ContactType
from wechaty_puppet_hostie.utils import get_common_attributes

CONTACT_GENDER_MAP = {
    ChatieContactGender.CONTACT_GENDER_FEMALE.name: ContactGender.Female,
    ChatieContactGender.CONTACT_GENDER_MALE.name: ContactGender.Male,
    ChatieContactGender.CONTACT_GENDER_UNSPECIFIED.name: ContactGender.Unknown
}

CONTACT_TYPE_MAP = {
    ChatieContactType.CONTACT_TYPE_PERSONAL.name: ContactType.Personal,
    ChatieContactType.CONTACT_TYPE_OFFICIAL.name: ContactType.Official,
    ChatieContactType.CONTACT_TYPE_UNSPECIFIED.name: ContactType.Unknown
}


def get_contact_payload_from_response(response: ContactPayloadResponse
                                      ) -> ContactPayload:
    """
    :param response:
    :return:
    """
    payload_data = response.to_dict()
    common_attributes = get_common_attributes(payload_data, ContactPayload)
    common_attributes['type'] = CONTACT_TYPE_MAP[payload_data['type']]
    common_attributes['gender'] = CONTACT_GENDER_MAP[payload_data['gender']]
    return ContactPayload(**common_attributes)


