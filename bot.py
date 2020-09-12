import os
import time
import json, traceback
import config
import sqlite3
import telebot
import logging
import requests
import threading
import urllib.parse as uparse
from time import sleep
from telebot import types
from datetime import date
from datetime import datetime
from waitress import serve
from soccer.bundesliga_table import bundesligatable
from soccer.bundesliga_scores import bundesligascores
from soccer.bundesligacurrentscores import bundesligaLatest
from soccer.epltable import t
from soccer.eplscores import n as EPLSCORES
from soccer.eplcurrentscores import eplLatest
from soccer.mlstable import mlstable
from soccer.mlscores import mlscores
from soccer.mlscurrentscores import mlsLatest
from soccer.laliga_scores import laligacores
from soccer.laliga_table import laligatable
from soccer.laligacurrentscores import laligaLatest
from soccer.ligueone_scores import ligueonescores
from soccer.ligueone_table import ligueonetable
from soccer.ligueonecurrentscores import ligueoneLatest
from soccer.seriea_table import serieatable
from soccer.seriea_scores import serieascores
from soccer.serieacurrentscores import serieaLatest
# from flask import Flask, request, jsonify
import psycopg2

try:
    db = psycopg2.connect(user = config.db_user,
                                  password = config.db_password,
                                  host = config.db_host,
                                  port = config.db_port,
                                  database = config.db_name)

    cursor = db.cursor()
    # Print PostgreSQL Connection properties
    print ( db.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    # Create Users Table
    create_table_query = '''CREATE TABLE IF NOT EXISTS users
          (id SERIAL,
          userId VARCHAR NOT NULL); '''
    
    cursor.execute(create_table_query)
    db.commit()
    print("Table created successfully in PostgreSQL ")

except Exception as error :
    print ("Error occurred", error)

# new bot instance
bot = telebot.TeleBot(config.api_key)

# app = Flask(__name__)

# @app.route("/")
# def index():
#      return 'What\'s good? I am Footy! 🤖'

def bot_polling():
    while True:
        try:
            print("Starting bot polling now. New bot instance started!")
            bot.polling(none_stop=True, interval=config.bot_interval, timeout=config.bot_timeout)
        except Exception as ex:
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(config.bot_timeout, ex))
            bot.stop_polling()
            sleep(config.bot_timeout)
        else:
            bot.stop_polling()
            print("Bot polling loop finished.")
            break

@bot.message_handler(commands=['start'])
def send_welcome(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Soccer', 'Help')
    cid = m.chat.id
    select_exist = """select exists(select userId from users where "userid" = CAST(%s AS VARCHAR));"""
    record_to_insert = [m.from_user.id]
    cursor.execute(select_exist, record_to_insert)
    check = cursor.fetchone()
    if check[0] == False:
      print("Falsely",check)
      postgres_insert_query = """ INSERT INTO users (userId) VALUES (%s)"""
      cursor.execute(postgres_insert_query, record_to_insert)
      db.commit()
      count = cursor.rowcount
      print (count, "Record inserted successfully into users table")
    else:
      print("Truly",check)
      count = cursor.rowcount
      print (count, "Record already exists")
    line1 = '`Hi {},` I\'m Footy 🤖!\n\nI provide sports update which includes fixtures, table, scores, news straight to your DM with ease after scraping and exploring the web 😊🚀\n\nAll updates are gotten from\n• [Livescores](livescores.com)\n• [NewsApi](http://newsapi.org)\n\nPress any button below to interact with me. You will love using me to get sports information\n\nMade with ❤️ in 🇳🇬'
    msg = line1
    bot.send_message(cid, msg.format(m.from_user.first_name), reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

# main menu
@bot.message_handler(regexp="👈 Main Menu")
def main_menu(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Soccer', 'Help')
    cid = m.chat.id
    user_msg = 'Return to the main menu.\n\n'
    bot.send_message(cid, user_msg, reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

# help details
@bot.message_handler(regexp="Help")
def command_help(m):
    cid = m.chat.id
    help_text = "Footy 🤖: Send my creator *@Mastersam07* a private message if you need help with anything."
    bot.send_message(cid, help_text, parse_mode='Markdown', disable_web_page_preview="True")

# soccer
@bot.message_handler(regexp="⚽ Soccer")
def send_soccer(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('🏴󠁧󠁢󠁥󠁮󠁧󠁿 England', '🇫🇷 France')
    user_markup.row('🇩🇪 Germany', '🇮🇹 Italy')
    user_markup.row('🇪🇸 Spain', '🇺🇸 United States')
    user_markup.row('👈 Main Menu')
    cid = m.chat.id
    user_msg = 'Soccer information from leagues around the world.\n\n'
    bot.send_message(cid, user_msg, reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

@bot.message_handler(regexp="👈 Back")
def soccer_back(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('🏴󠁧󠁢󠁥󠁮󠁧󠁿 England', '🇫🇷 France')
    user_markup.row('🇩🇪 Germany', '🇮🇹 Italy')
    user_markup.row('🇪🇸 Spain', '🇺🇸 United States')
    user_markup.row('⚽ Latest',)
    user_markup.row('👈 Main Menu')
    cid = m.chat.id
    user_msg = 'Return to main soccer options.\n\n'
    bot.send_message(cid, user_msg, reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

# england section
@bot.message_handler(regexp="🏴󠁧󠁢󠁥󠁮󠁧󠁿 England")
def send_england(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ EPL Scores', '⚽ EPL Table')
    user_markup.row('⚽ EPL Results(Last 7 days)', '👈 Back')
    cid = m.chat.id
    user_msg = 'English Premier League scores and table.\n\n'
    bot.send_message(cid, user_msg, reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

@bot.message_handler(regexp="⚽ EPL Scores")
def send_eplLatest(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + eplLatest)
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ EPL Table")
def send_epltable(m):
  rank = t
  user_msg = rank
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ EPL Results(Last 7 days)")
def send_eplscores(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + EPLSCORES)
  bot.reply_to(m, user_msg)

# france section
@bot.message_handler(regexp="🇫🇷 France")
def send_france(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Ligue 1 Scores', '⚽ Ligue 1 Table')
    user_markup.row('⚽ Ligue 1 Results(Last 7 days)', '👈 Back')
    cid = m.chat.id
    user_msg = 'French League scores and table.\n\n'
    bot.send_message(cid, user_msg, reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

@bot.message_handler(regexp="⚽ Ligue 1 Scores")
def send_ligueonelatest(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + ligueoneLatest)
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ Ligue 1 Table")
def send_ligueonetable(m):
  rank = ligueonetable
  user_msg = rank
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ Ligue 1 Results(Last 7 days)")
def send_ligueonescores(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + ligueonescores)
  bot.reply_to(m, user_msg)

# germany section
@bot.message_handler(regexp="🇩🇪 Germany")
def send_germany(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Bundesliga Scores', '⚽ Bundesliga Table')
    user_markup.row('⚽ Bundesliga Results(Last 7 days)', '👈 Back')
    cid = m.chat.id
    user_msg = 'German League scores and table.\n\n'
    bot.send_message(cid, user_msg, reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

@bot.message_handler(regexp="⚽ Bundesliga Scores")
def send_bundesligalatest(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + bundesligaLatest)
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ Bundesliga Table")
def send_bundesligatable(m):
  rank = bundesligatable
  user_msg = rank
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ Bundesliga Results(Last 7 days)")
def send_bundesligascores(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + bundesligascores)
  bot.reply_to(m, user_msg)

# italy section
@bot.message_handler(regexp="🇮🇹 Italy")
def send_italy(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Serie A Scores', '⚽ Serie A Table')
    user_markup.row('⚽ Serie A Results(Last 7 days)', '👈 Back')
    cid = m.chat.id
    user_msg = 'Serie A scores and table.\n\n'
    bot.send_message(cid, user_msg, reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

@bot.message_handler(regexp="⚽ Serie A Scores")
def send_seriealatest(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + serieaLatest)
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ Serie A Table")
def send_serieatable(m):
  rank = serieatable
  user_msg = rank
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ Serie A Results(Last 7 days)")
def send_serieascores(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + serieascores)
  bot.reply_to(m, user_msg)

# spain section
@bot.message_handler(regexp="🇪🇸 Spain")
def send_spain(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ La Liga Scores', '⚽ La Liga Table')
    user_markup.row('⚽ La Liga A Results(Last 7 days)', '👈 Back')
    cid = m.chat.id
    user_msg = 'Spanish League scores and table.\n\n'
    bot.send_message(cid, user_msg, reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

@bot.message_handler(regexp="⚽ La Liga Scores")
def send_laligalatest(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + laligaLatest)
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ La Liga Table")
def send_laligatable(m):
  rank = laligatable
  user_msg = rank
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ La Liga A Results(Last 7 days)")
def send_laligascores(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + laligacores)
  bot.reply_to(m, user_msg)

# united states section
@bot.message_handler(regexp="🇺🇸 United States")
def send_unitedstates(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ MLS Scores', '⚽ MLS Table')
    user_markup.row('⚽ MLS Results(Last 7 days)', '👈 Back')
    cid = m.chat.id
    user_msg = 'MLS scores and table.\n\n'
    bot.send_message(cid, user_msg, reply_markup=user_markup, parse_mode="Markdown", disable_web_page_preview="True")

@bot.message_handler(regexp="⚽ MLS Scores")
def send_mlslatest(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + mlsLatest)
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ MLS Table")
def send_mlstable(m):
  rank = mlstable
  user_msg = rank
  bot.reply_to(m, user_msg)

@bot.message_handler(regexp="⚽ MLS Results(Last 7 days)")
def send_mlscores(m):
  d = date.today()
  user_msg = (str(d) + "\n \n" + mlscores)
  bot.reply_to(m, user_msg)


polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()

# keep main program running while bot runs threaded
if __name__ == "__main__":
    # serve(app)
    while True:
        try:
            sleep(120)
        except KeyboardInterrupt:
            break
