"""unit test for urllink"""
from __future__ import annotations

from unittest import TestCase
from wechaty.user.url_link import UrlLink, GithubUrlLinkParser




class TestUrlLink(TestCase):
    def setUp(self) -> None:
        self.sample_issue_link = 'https://github.com/wechaty/python-wechaty/issues/339'
        self.sample_issue_comment_link = 'https://github.com/wechaty/python-wechaty/issues/339'

def test_create():
    """unit test for creating"""
    UrlLink.create(
        url='https://github.com/wechaty/python-wechaty/issues/339',
        title='title',
        thumbnail_url='thu',
        description='simple desc'
    )


def test_github_payload():
    parser = GithubUrlLinkParser()
    
    
    
