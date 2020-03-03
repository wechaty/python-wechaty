"""
interface for puppet
"""
from enum import Enum

class Puppet:
    """
    puppet interface class
    """

    # pylint: disable=R0201
    def message_image(self, message_id: int, image_type: Enum) -> None:
        """
        docstring
        :param message_id:
        :param image_type:
        :return:
        """
        raise NotImplementedError

    def start(self) -> None:
        """
        start the puppet
        :return:
        """
        raise NotImplementedError

