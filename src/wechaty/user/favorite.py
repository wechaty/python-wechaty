"""
Favorite for Contact Message
"""


# pylint: disable=R
class Favorite:
    """
    favorite object which handle the url_link content
    """
    def __init__(self, favorite_id: str):
        self.favorite_id = favorite_id
        raise NotImplementedError

    def get_id(self):
        """
        get favorite_id
        :return:
        """
        return self.favorite_id
