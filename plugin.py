#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core import Plugin, command


class TestPlugin(Plugin):
    """Всі метадані з manifest.json"""

    @command("test_download")
    async def test_cmd(self, event):
        prefix = self.get_config("prefix", "🔊")
        await event.reply(f"{prefix} ✅ Плагін успішно завантажено з GitHub!")

    async def main(self):
        self.logger.info(f"✅ {self.name} v{self.version} by {self.author} loaded!")
        self.logger.info(f"   ID: {self.plugin_id}")
