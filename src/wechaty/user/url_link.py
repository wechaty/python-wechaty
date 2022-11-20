"""
UrlLink for Contact Message
"""
from __future__ import annotations

from typing import (
    Optional,
    Type
)
from urllib3 import get_host
from wechaty_puppet import UrlLinkPayload, get_logger

from wechaty.utils.link import get_url_metadata

from dataclasses import dataclass
from typing import Dict, List
from abc import abstractmethod
from github import Github
from github.Repository import Repository

from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment

from github.Issue import Issue
from github.IssueComment import IssueComment

from wechaty_puppet.schemas.url_link import UrlLinkPayload


log = get_logger('UrlLink')


class UrlLinkParser:
    # valid host-name of one parser
    host_names: List[str] = []
    
    @classmethod
    def can_parser(cls, url: str) -> bool:
        if not cls.host_names:
            raise ValueError(f"please set valid host-names for parser, eg: ['github']")
        
        _, host_name, _ = get_host(url)
        return host_name in cls.host_names

    @abstractmethod
    def parse(self, url: str) -> UrlLinkPayload:
        raise NotImplementedError("<parse> method must be overried by sub-class of <UrlLinkParser>")


class GithubUrlLinkParser(UrlLinkParser):
    """Parse Urllink by url"""

    host_names: List[str] = ['github']

    def __init__(self, token: Optional[str] = None):
        self._github = Github(login_or_token=token)
        self._repositories: Dict[str, Repository] = {}
    
    @staticmethod
    def can_parser(url: str) -> bool:
        """the source of url

        Args:
            url (str): github urllink

        Returns:
            bool: wheter is github based urll
        """
        _, host_name, _ = get_host(url)
        return host_name
        
    def parse(self, url: str) -> UrlLinkPayload:
        """parse url-link as payload

        Args:
            url (str): the url-of link

        Returns:
            UrlLinkPayload: the instance of final url-link payload
        """
        pass

    def get_repo(self, repo_name: str) -> Repository:
        """get Repository instance which can fetch the issue/pull-request info

        Args:
            repo_name (str): the full name of repo, eg: wechaty/python-wechaty

        Returns:
            Repository: the repository instance
        """
        if repo_name in self._repositories:
            return self._repositories[repo_name]

        repo = self._github.get_repo(repo_name)
        self._repositories[repo_name] = repo
        return repo

    def get_pr_payload(self, repo_name: str, pr_id: int) -> UrlLinkPayload:
        """get pull-request main-body info

        Args:
            repo_name (str): the full name of repo
            pr_id (int): the is of pull-request

        Returns:
            UrlLinkPayload: the UrlLink payload
        """
        repo: Repository = self.get_repo(repo_name)
        pull_request: PullRequest = repo.get_pull(pr_id)
        payload = UrlLinkPayload(
            url=pull_request.html_url,
            title=pull_request.title,
            description=pull_request.body,
            thumbnailUrl=pull_request.user.avatar_url
        )
        return payload
    
    def get_pr_comment_payload(self, repo_name: str, pr_id: int, comment_id: int, comment_type: str = 'issue') -> UrlLinkPayload:
        """get comment of pull-request, which can be issue or review comment

        Args:
            repo_name (str): the full name of repo
            pr_id (int): the id of pr
            comment_id (int): the id of target comment
            comment_type (str, optional): issue/review. Defaults to 'issue'.

        Returns:
            UrlLinkPayload: _description_
        """
        repo: Repository = self.get_repo(repo_name)
        pull_request: PullRequest = repo.get_pull(pr_id)
        if comment_type == 'issue':
            comment: PullRequestComment = pull_request.get_issue_comment(comment_id)
        else:
            comment: PullRequestComment = pull_request.get_review_comment(comment_id)

        payload = UrlLinkPayload(
            url=comment.html_url,
            title=pull_request.title,
            description=comment.body,
            thumbnailUrl=comment.user.avatar_url
        )
        return payload

    def get_issue_payload(self, repo_name: str, issue_id: int) -> UrlLinkPayload:
        """get the issue body

        Args:
            repo_name (str): the full name of repo
            issue_id (int): the id of issue

        Returns:
            UrlLinkPayload: the UrlLink payload instance
        """
        repo: Repository = self.get_repo(repo_name)
        issue: Issue = repo.get_issue(issue_id)
        payload = UrlLinkPayload(
            url=issue.html_url,
            title=issue.title,
            description=issue.body,
            thumbnailUrl=issue.user.avatar_url
        )
        return payload

    def get_issue_comment_payload(self, repo_name: str, issue_id: int, comment_id: int) -> UrlLinkPayload:
        """the issue comment payload

        Args:
            repo_name (str): the full-name of repo
            issue_id (int): the id of target issue
            comment_id (int): the comment id of the specific issue

        Returns:
            UrlLinkPayload: the UrlLink payload instance
        """
        repo: Repository = self.get_repo(repo_name)
        issue: Issue = repo.get_issue(issue_id)
        comment: IssueComment = issue.get_comment(comment_id)

        payload = UrlLinkPayload(
            url=comment.html_url,
            title=issue.title,
            description=comment.body,
            thumbnailUrl=comment.user.avatar_url
        )
        return payload


class UrlLink:
    """
    url_link object which handle the url_link content
    """

    def __init__(
        self,
        payload: UrlLinkPayload,
    ):
        """
        initialization
        :param payload:
        """
        self.payload: UrlLinkPayload = payload

    @classmethod
    def create(
        cls: Type[UrlLink],
        url: str,
        title: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        description: Optional[str] = None
    ) -> UrlLink:
        """
        create urllink from url string
        """
        log.info('create url_link for %s', url)

        metadata = get_url_metadata(url)

        payload = UrlLinkPayload(url=url)
     
        payload.title = title or metadata.get('title', None)
        payload.thumbnailUrl = thumbnail_url or metadata.get('image', None)
        payload.description = description or metadata.get('description', None)
        return UrlLink(payload)

    def __str__(self) -> str:
        """
        UrlLink string format output
        :return:
        """
        return 'UrlLink<%s>' % self.payload.url

    @property
    def title(self) -> str:
        """
        get UrlLink title
        :return:
        """
        return self.payload.title or ''

    @property
    def thumbnailUrl(self) -> str:
        """
        get thumbnail url
        :return:
        """
        return self.payload.thumbnailUrl or ''

    @property
    def description(self) -> str:
        """
        get description
        :return:
        """
        return self.payload.description or ''

    @property
    def url(self) -> str:
        """
        get url
        :return:
        """
        return self.payload.url or ''
