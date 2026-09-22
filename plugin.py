#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core import Plugin, command, watcher, loop
from datetime import datetime


class HelloWorldPlugin(Plugin):
    """Всі метадані з manifest.json"""
    
    @command(
        command="hello_world",
        aliases=["hw", "привіт_світ"],
        description="Say hello world"
    )
    async def hello_cmd(self, event):
        """Основна команда плагіна"""
        emoji = self.get_config("emoji", "👋")
        greeting = self.get_config("greeting", "Hello")
        show_time = self.get_config("show_time", True)
        
        text = self.t("greeting", emoji=emoji, greeting=greeting)
        
        if show_time:
            now = datetime.now().strftime("%H:%M:%S")
            text += f"\n🕐 {self.t('time', time=now)}"
        
        await event.reply(text)
    
    @command("hw_config")
    async def config_cmd(self, event):
        """Показати конфігурацію"""
        text = self.t("config_title")
        text += f"\n• greeting: {self.get_config('greeting')}"
        text += f"\n• show_time: {self.get_config('show_time')}"
        text += f"\n• emoji: {self.get_config('emoji')}"
        await event.reply(text)
    
    @command("hw_set")
    async def set_cmd(self, event):
        """Змінити конфігурацію: /hw_set key value"""
        parts = event.raw_text.split(maxsplit=2)
        if len(parts) < 3:
            await event.reply(self.t("set_usage"))
            return
        
        key = parts[1]
        value = parts[2]
        
        # Конвертуємо bool
        if value.lower() in ["true", "yes", "1"]:
            value = True
        elif value.lower() in ["false", "no", "0"]:
            value = False
        
        if self.set_config(key, value):
            await event.reply(self.t("set_success", key=key, value=value))
        else:
            await event.reply(self.t("set_error", key=key))
    
    @watcher(pattern="hello world")
    async def hello_watcher(self, event):
        """Реагує на 'hello world'"""
        await event.reply(self.t("watcher_response"))
    
    @loop(interval=1800, start_immediately=False)
    async def status_loop(self):
        """Лог кожні 30 хвилин"""
        self.logger.debug(self.t("loop_log", time=datetime.now().strftime("%H:%M:%S")))
    
    async def main(self):
        self.logger.info(self.t("loaded", name=self.name, version=self.version))
        self.logger.info(f"   📋 ID: {self.plugin_id}")
