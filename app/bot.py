from telebot import TeleBot

from app import TOKEN


bot = TeleBot(token=TOKEN, parse_mode='HTML')
