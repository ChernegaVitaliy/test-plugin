#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
echo/plugin.py - Плагін Echo
"""

import asyncio
import random
from datetime import datetime

from core import Plugin, command, watcher, loop


class EchoPlugin(Plugin):
    """
    Плагін Echo.
    
    Відповідає на команди /echo, /hello, /time.
    Реагує на повідомлення з текстом.
    """
    
    # Метадані
    name = "Echo"
    author = "UserBot Team"
    version = "1.0.0"
    description = "Echo plugin with multiple commands"
    category = "Utilities"
    
    # Конфігурація за замовчуванням
    config = {
        "prefix": "🔊",
        "uppercase": False,
        "reverse": False
    }
    
    async def on_load(self) -> None:
        """Викликається при завантаженні плагіна"""
        self.logger.info(self.t("plugin_loaded", version=self.version))
        self.logger.info(f"Config: {self._config_data}")
        self.logger.info(self.t("config_info", prefix=self.get_config("prefix", "🔊")))
    
    async def on_unload(self) -> None:
        """Викликається при вивантаженні плагіна"""
        self.logger.info(self.t("plugin_unloaded"))
    
    async def on_config_change(self, key: str, old_value, new_value) -> None:
        """Викликається при зміні конфігурації"""
        self.logger.info(self.t("config_changed", key=key, value=new_value, old=old_value))
    
    # ============ КОМАНДИ ============
    
    @command(
        command="echo",
        aliases=["повтори"],
        description="Repeat your message",
        usage="/echo <text>"
    )
    async def echo_command(self, event):
        """
        Команда /echo.
        Повторює текст користувача.
        """
        # Отримуємо текст після команди
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2:
            await event.reply(self.t("echo_usage"))
            return
        
        text = parts[1]
        
        # Застосовуємо налаштування
        if self.get_config("uppercase", False):
            text = text.upper()
        
        if self.get_config("reverse", False):
            text = text[::-1]
        
        prefix = self.get_config("prefix", "🔊")
        
        # Відправляємо відповідь
        await event.reply(f"{prefix} {text}")
    
    @command(
        command="hello",
        aliases=["привіт", "hi"],
        description="Greet user",
        usage="/hello"
    )
    async def hello_command(self, event):
        """
        Команда /hello.
        Вітає користувача з випадковим привітанням.
        """
        greetings = [
            self.t("greeting_1"),
            self.t("greeting_2"),
            self.t("greeting_3"),
            self.t("greeting_4"),
            self.t("greeting_5")
        ]
        
        greeting = random.choice(greetings)
        
        # Отримуємо ім'я користувача
        sender = await event.get_sender()
        name = sender.first_name or self.t("unknown_user")
        
        await event.reply(self.t("hello_response", name=name, greeting=greeting))
    
    @command(
        command="time",
        aliases=["час", "now"],
        description="Show current time",
        usage="/time"
    )
    async def time_command(self, event):
        """
        Команда /time.
        Показує поточний час і дату.
        """
        now = datetime.now()
        
        await event.reply(self.t(
            "time_response",
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            week_day=self._get_weekday(now.weekday())
        ))
    
    @command(
        command="config_echo",
        aliases=["ce", "настройки"],
        description="Show or change plugin config",
        usage="/config_echo [key] [value]"
    )
    async def config_command(self, event):
        parts = event.raw_text.split(maxsplit=2)
    
        if len(parts) < 2:
            config_text = self.t("config_show")
            config_text += f"\n• prefix: {self.get_config('prefix')}"
            config_text += f"\n• uppercase: {self.get_config('uppercase')}"
            config_text += f"\n• reverse: {self.get_config('reverse')}"
            await event.reply(config_text)
            return
    
        key = parts[1]
        if len(parts) < 3:
            await event.reply(self.t("config_usage").format(key=key))
            return
    
        value = parts[2]
    
        if value.lower() in ["true", "yes", "1"]:
            value = True
        elif value.lower() in ["false", "no", "0"]:
            value = False
    
        old_value = self.get_config(key)
    
        if self.set_config(key, value):
            await event.reply(
                self.t("config_changed_reply").format(
                    key=key,
                    old=old_value,
                    new=value
                )
            )
        else:
            await event.reply(self.t("config_invalid_key").format(key=key))
    
    # ============ WATCHER ============
    
    @watcher(pattern="!echo", only_private=False)
    async def echo_watcher(self, event):
        """
        Watcher для повідомлень !echo.
        Відповідає на !echo в будь-якому чаті.
        """
        await event.reply(self.t("watcher_response", text=event.raw_text))
    
    @watcher(pattern="бот", only_private=False)
    async def bot_watcher(self, event):
        """
        Watcher для повідомлень зі словом "бот".
        """
        await event.reply(self.t("bot_mentioned"))
    
    # ============ LOOP ============
    
    @loop(interval=3600.0, start_immediately=False)  # кожну годину
    async def status_loop(self):
        """
        Циклічна задача, яка виконується щогодини.
        Логує статус плагіна.
        """
        self.logger.debug(self.t("status_loop_log", time=datetime.now().strftime("%H:%M:%S")))
    
    # ============ MAIN ============
    
    async def main(self) -> None:
        """
        Головна функція плагіна.
        Виконується при завантаженні.
        """
        self.logger.info(self.t("main_started"))
        
        # Запускаємо фоновий таймер
        asyncio.create_task(self._background_task())
    
    # ============ ДОПОМІЖНІ МЕТОДИ ============
    
    async def _background_task(self):
        """Приклад фонової задачі"""
        counter = 0
        while True:
            await asyncio.sleep(300)  # кожні 5 хвилин
            counter += 1
            if counter % 12 == 0:  # кожну годину
                self.logger.debug(self.t("background_log", count=counter))
    
    def _get_weekday(self, weekday):
        """Повертає назву дня тижня"""
        days = {
            0: self.t("day_monday"),
            1: self.t("day_tuesday"),
            2: self.t("day_wednesday"),
            3: self.t("day_thursday"),
            4: self.t("day_friday"),
            5: self.t("day_saturday"),
            6: self.t("day_sunday")
        }
        return days.get(weekday, str(weekday))
