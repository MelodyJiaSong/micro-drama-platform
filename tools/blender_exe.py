# -*- coding: utf-8 -*-
"""Blender 可执行文件的唯一出处。环境变量 BLENDER（`.claude/settings.local.json` 的 env，本机路径）优先，
旧名 BLENDER_BIN 兼容，都没有就用本仓库约定的安装位置。"""
from __future__ import annotations

import os

BLENDER = (os.environ.get("BLENDER") or os.environ.get("BLENDER_BIN")
           or r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe")
