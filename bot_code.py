from pythorhead import Lemmy
from pythorhead.types import SortType, ListingType, FeatureType
from config import settings
import logging
import sqlite3
import time
import requests
import json
import os
import re
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

include_com = None

def login():
    global lemmy
    
    lemmy = Lemmy("https://" + settings.INSTANCE)
    lemmy.log_in(settings.USERNAME, settings.PASSWORD)

    if settings.INCLUDE:
        global include_com
        srch_com = lemmy.community.get(name=settings.INCLUDE)
        include_com = srch_com['community_view']['community']['id']
        
    
    return lemmy

def create_table(conn, table_name, table_definition):
    curs = conn.cursor()
    curs.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} {table_definition}''')
    conn.commit()
    logging.debug(f"Checked/created {table_name} table")
    
def check_dbs():
    try:
        with sqlite3.connect('resources/log.db') as conn:
        #create or check confirmed posts table
            create_table(conn, 'conf_posts', '(post_id INT, poster_id INT)')

        #create or check confirmed comments table
            create_table(conn, 'conf_comments', '(comment_id INT, poster_id INT)')
            
        #create or check community exclusions table
            create_table(conn, 'exclusions', '(community_id INT)')

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Exception in _query: {e}")
  
def connect_to_log_db():
    return sqlite3.connect('resources/log.db')



def check_comments():
    recent_comments = lemmy.comment.list(limit=settings.POLL_AMOUNT, sort=SortType.New, type_=ListingType.All, max_depth=1)
    
    regex_pattern = re.compile(settings.TRIGGER, re.IGNORECASE)
    
    for comment in recent_comments:
        comment_id = comment['comment']['id']
        post_id = comment['comment']['post_id']
        comment_text = comment['comment']['content']
        comment_poster = comment['comment']['creator_id']
        community_id = comment['post']['community_id']
        username = comment['creator']['name']
        
        # scan all comments
        if re.search(regex_pattern,comment_text):
            
            #check mode
            if settings.INCLUDE:
                if community_id != include_com:
                    continue
            
            #check community exclusions
            if check_community_exclusions(community_id) == "excluded":
                continue
            
            if check_log_db(comment_id) == "duplicate":
                continue
            
            #get random response from bot:
            bot_responses = settings.RESPONSES.split(';')
            random_response = random.choice(bot_responses).format(username=username)
            
            lemmy.comment.create(post_id=post_id,content=random_response,parent_id=comment_id)
            add_comment_to_db(comment_id, comment_poster)
            continue
        
def check_community_exclusions(community_id):
    try:
        with connect_to_log_db() as conn:
            query = '''SELECT community_id FROM exclusions WHERE community_id=?'''
            community_check = execute_sql_query(conn, query, (community_id,))
            
            if community_check:
                return "excluded"   
            
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return "error"    
       
        
def check_log_db(comment_id):
    try:
        with connect_to_log_db() as conn:
            action_query = '''SELECT comment_id FROM conf_comments WHERE comment_id=?'''
            comment_match = execute_sql_query(conn, action_query, (comment_id,))

            if comment_match:
                return "duplicate"   
                
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return "error"

def add_comment_to_db(comment_id, comment_poster):
    try:          
        logging.debug("Adding new comment to db")
        with connect_to_log_db() as conn:
            sqlite_insert_query = """INSERT INTO conf_comments (comment_id, poster_id) VALUES (?,?);"""
            data_tuple = (comment_id, comment_poster,)
            execute_sql_query(conn, sqlite_insert_query, data_tuple)

            logging.debug("Added comment to db")
            return "added"
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return "error"
        
def execute_sql_query(connection, query, params=()):
    with connection:
        curs = connection.cursor()
        curs.execute(query, params)
        return curs.fetchone()
    
def clear_notifications():
    try:
        notif = lemmy.comment.get_replies(True,1)
        all_notifs = notif['replies']
    except:
        logging.info("Error with connection, retrying...")
        login()
        return
    
    for notif in all_notifs:
        reply_id = notif['comment_reply']['id']
        lemmy.comment.mark_as_read(reply_id,True)
        
def check_pms():
    pm = lemmy.private_message.list(True, 1)
    private_messages = pm['private_messages']
    
    community = None
    
    for pm in private_messages:
        pm_sender = pm['private_message']['creator_id']
        pm_context = pm['private_message']['content']
        pm_id = pm['private_message']['id']
      
        if pm_context.split(" ")[0] == "#exclude":
            community = pm_context.split(" ")[1]
            
            if community is not None:
                community_details = lemmy.community.get(name=community)
                community_id = community_details['community_view']['community']['id']
            else:
                lemmy.private_message.create("Sorry, I couldn't find that community to exclude. Make sure that the format is `community_name@instance.tld`, i.e. `test@lemmy.zip`.",pm_sender)
                lemmy.private_message.mark_as_read(pm_id,True)
                
            is_moderator = False
                
            for moderator_info in community_details['moderators']:
                if moderator_info['moderator']['id'] == pm_sender:
                    is_moderator = True
                    break  # Stop the loop as soon as we find a matching moderator

                if not is_moderator:
                    # If pm_sender is not a moderator, send a private message
                    lemmy.private_message.create("As you are not a moderator in this community, you are not able to add an exclusion. \n\n If you think this is a mistake, please message [Demigodrick](/u/demigodrick@lemmy.zip)", pm_sender)
                    lemmy.private_message.mark_as_read(pm_id, True)
                    continue
            
            if is_moderator == True:
                if add_exclusion(community_id) == "added":
                    lemmy.private_message.create("Hi, that community has been added to my exclusion list.",pm_sender)
                    lemmy.private_message.mark_as_read(pm_id, True)


                
            
def add_exclusion(community_id):
    try:          
        with connect_to_log_db() as conn:
            sqlite_insert_query = """INSERT INTO exclusions (community_id) VALUES (?);"""
            data_tuple = (community_id,)
            execute_sql_query(conn, sqlite_insert_query, data_tuple)

            logging.debug("Added exclusion to db")
            return "added"
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return "error"            
                