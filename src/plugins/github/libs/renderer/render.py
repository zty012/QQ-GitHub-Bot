#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2021-05-14 17:09:12
@LastEditors    : yanyongyu
@LastEditTime   : 2022-09-17 15:48:37
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from pathlib import Path
from typing import Literal

import jinja2
from githubkit.rest import Issue

from .globals import (
    get_issue_repo,
    get_pull_request,
    get_issue_timeline,
    get_pull_request_diff,
)
from .filters import (
    markdown_gfm,
    review_state,
    relative_time,
    markdown_title,
    find_dismissed_review,
)

env = jinja2.Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=["jinja2.ext.loopcontrols"],
    loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates"),
    enable_async=True,
)

env.filters["markdown_title"] = markdown_title
env.filters["markdown_gfm"] = markdown_gfm
env.filters["relative_time"] = relative_time
env.filters["review_state"] = review_state
env.filters["find_dismissed_review"] = find_dismissed_review

env.globals["get_issue_repo"] = get_issue_repo
env.globals["get_issue_timeline"] = get_issue_timeline
env.globals["get_pull_request"] = get_pull_request
env.globals["get_pull_request_diff"] = get_pull_request_diff


async def issue_to_html(issue: Issue, theme: Literal["light", "dark"] = "light") -> str:
    template = env.get_template("views/issue.html.jinja")
    return await template.render_async(issue=issue, theme=theme)


async def pr_diff_to_html(
    issue: Issue, theme: Literal["light", "dark"] = "light"
) -> str:
    template = env.get_template("views/diff.html.jinja")
    return await template.render_async(issue=issue, theme=theme)
