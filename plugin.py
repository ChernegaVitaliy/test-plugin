#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core import Plugin, command


class TestPlugin(Plugin):
    name = "TestPlugin"
    author = "Test Author"
    version = "1.0.0"
    description = "Test plugin for download testing"
    category = "Test"
    
    @command("test_download")
    async def test_cmd(self, event):
        await event.reply("✅ Плагін успішно завантажено з GitHub!")
    
    async def main(self):
        self.logger.info("✅ Test plugin loaded from GitHub!")
