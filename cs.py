'''
Delete logs after parsing
Create database schema
Connect to MySQL and load data
Use CodeIgniter to display front end
Favorite weapon
Headshot count
General shot area breakdown
Kills on other players
total kill count
suicides?
wins
win percentage
shots
hits
kills
kills per shot
rounds played
rounds won
deaths kill to death ratio
knife fights
bombs planted?
Don't parse a log file unless the log is completed
Add time to each action
Add maps to events
'''
import os
import sys
import MySQLdb.cursors
import json
from adt import ProfileContainer
from parser import FactoryEvent
from parser import FactoryMatch
from sqlgen import FactorySql
from sqlgen import MatchSql


def get_logs(fp=None):
    output = []
    if fp is None:
        fp = os.getcwd()
    for i in os.listdir(fp):
        if len(i) < 12:
            continue
        if i[-3:] == 'log' and i[0] == 'l':
            output.append("{}/{}".format(fp, i))
    return output


def get_mysql():
    creds = get_db_credentials()
    creds['cursorclass'] = MySQLdb.cursors.DictCursor
    return MySQLdb.connect(**creds)


def get_db_credentials():
    fp = open('db.txt', 'r')
    creds = {}
    for i in fp:
        data = i.strip(' \r\n\t').split('=')
        if len(data) != 2:
            raise Exception("Wrong format for mysql creds")
        if data[0] == 'port':
            value = int(data[1])
        else:
            value = data[1]
        creds[data[0]] = value
    return creds


def get_alias(db=None):
    c = db.cursor()
    rows = c.execute("SELECT `steam_id`, `alias` FROM `Alias`;")
    aliases = AliasContainer()
    if rows == 0:
        return aliases
    for r in c.fetchall():
        aliases.add(r['steam_id'], r['alias'])
    return aliases


def sql_execute(sql):
    db = get_mysql()
    c = db.cursor()
    for i in sql:
        c.execute(i)
        if len(c.messages) > 0:
            raise Exception(c.messages)
    c.close()
    db.commit()
    db.close()


def process_log(fp,  pc):
    f = open(fp, 'r')
    factory = FactoryEvent()
    output = []
    for line in f:
        data = factory.process(line[25:-1])
        if data is None:
            continue
        event = data[0]
        try:
            pc.check(event['player_a']['steam_id'], event['player_a']['alias'])
            pc.check(event['player_b']['steam_id'], event['player_b']['alias'])
        except KeyError:
            pass
        except TypeError:
            pass
        output.append(data)
    return output


def update_profiles(db, pc):
    if pc.has_new:
        pc.submit_and_update(db)


def generate_queries(match_id, events):
    factory_sql = FactorySql()
    queries = []
    for i in events:
        if not (isinstance(i[0], dict) and isinstance(i[1], dict)):
            continue
        event = i[0]
        damage = i[1]
        sql = factory_sql.process(match_id, event, damage)
        if sql is None:
            continue
        queries.append(sql)
    return queries


def execute_queries(db, pc, queries):
    c = db.cursor()
    for q in queries:
        try:
            c.execute(q.generate(pc))
        except:
            print type(q)
    c.close()
    db.commit()


def process():
    logs = get_logs('logs')
    db = get_mysql()
    pc = ProfileContainer()
    pc.update(db)
    fm = FactoryMatch()
    fe = FactoryEvent()
    for i in range(0, len(logs), 2):
        try:
            match = logs[i]
            events = logs[i+1]
        except IndexError:
            continue
        if not (is_log_finish(match) and is_log_finish(events)):
            continue
        match_data = fm.process(match)
        event_data = process_log(events, pc)
        update_profiles(db, pc)
        score = get_match_score(event_data)
        if score['terrorist'] is None or score['counter_terrorist'] is None:
            continue
        match_id = MatchSql.insert(db, match_data['map'], 
                                   match_data['created_on'].isoformat(),
                                   score['terrorist'],
                                   score['counter_terrorist'])
        queries = generate_queries(match_id, event_data)
        execute_queries(db, pc, queries)


def get_match_score(event_data):
    ct_score = None
    t_score = None
    for i in reversed(event_data):
        if isinstance(i[0], str):
            if i[0] == 'CT':
                ct_score = i[1]
            elif i[0] == 'TERRORIST':
                t_score = i[1]
        if ct_score is not None and t_score is not None:
            break
    return {"terrorist":t_score, "counter_terrorist":ct_score}


def is_log_finish(fp):
    try:
        last_line = open(fp, 'r').readlines()[-1:][0][25:-1]
    except:
        return False
    if last_line == "Log file closed":
        return True
    return False


if __name__ == '__main__':
    process()
