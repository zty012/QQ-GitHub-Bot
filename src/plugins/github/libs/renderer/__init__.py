#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2021-03-09 16:45:25
@LastEditors    : yanyongyu
@LastEditTime   : 2022-09-16 04:09:34
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from datetime import timedelta

from githubkit.rest import Issue

from src.plugins.redis import cache
from src.plugins.playwright import get_new_page

from .render import issue_to_html


@cache(ex=timedelta(minutes=10))
async def _gen_image(html: str, width: int, height: int) -> bytes | None:
    async with get_new_page(viewport={"width": width, "height": height}) as page:
        await page.set_content(html)
        return await page.screenshot(full_page=True)


async def issue_to_image(
    issue: Issue,
    width: int = 800,
    height: int = 300,
) -> bytes | None:
    html = await issue_to_html(issue)
    return await _gen_image(html, width, height)