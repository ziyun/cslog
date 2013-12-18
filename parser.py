from datetime import datetime


class CSTime(object):


    @staticmethod
    def parse(line):
        d = line[2:23]
        parts = d.split(' - ')
        month, day, year = map(int, parts[0].split('/'))
        hour, minute, second = map(int, parts[1].split(':'))
        return datetime(year, month, day, hour, minute, second)


class FactoryMatch(object):


    def __init__(self):
        self.actions = []
        self.actions.append(MapName)


    def process(self, fp):
        f = open(fp, 'r')
        output = None
        for line in f:
            output = self.process_line(line)
            if output is not None:
                break
        return output


    def process_line(self, line):
        output = None
        for a in self.actions:
            if a.match(line):
                output = a.execute(line)
                break
        return output


class MapName(object):


    @staticmethod
    def match(line):
        if line[25:36] == "Loading map":
            return True
        return False


    @staticmethod
    def execute(line):
        output = {}
        output['created_on'] = CSTime.parse(line)
        output['map'] = line[38:-2]
        return output


class FactoryEvent(object):


    def __init__(self):
        self.actions = []
        self.actions.append(AttackEvent)
        self.actions.append(KillEvent)
        self.actions.append(ScoreEvent)


    def process(self, line):
        for a in self.actions:
            if a.match(line):
                return a.execute(line)


class ScoreEvent(object):


    @staticmethod
    def match(line):
        if line[0:4] == "Team":
            parts = line.split(' ')
            if parts[2] == "scored":
                return True
        return False


    @staticmethod
    def execute(line):
        parts = line.split(' ')
        team = parts[1].strip('"')
        score = int(parts[3].strip('"'))
        return team, score


class AttackEvent(object):


    @staticmethod
    def match(line):
        if line[0] == '"' and line[-1:] == ')':
            if ' attacked ' in line:
                return True
        return False


    @staticmethod
    def execute(line):
        parts = line.split(" with ")
        event = Player2Player.execute(parts[0])
        damage = Damage.execute(parts[1])
        return event, damage


class KillEvent(object):


    @staticmethod
    def match(line):
        if line[0] == '"' and (line[-1] == '"' or line [-1] == ')'):
            if ' killed ' in line:
                return True
        return False

    @staticmethod
    def execute(line):
        parts = line.split(' with ')
        event = Player2Player.execute(parts[0])
        damage = Damage.execute(parts[1])
        return event, damage
        '''
        if line[-10:] == '(headshot)':
            headshot = True
        else:
            headshot = False
        parts = line.split(" with ")
        event = Player2Player.execute(parts[0])
        if parts[1][-1:] == ')':
            headshot = True
            weapon = parts[1][1:-12]
        else:
            headshot = False
            weapon = parts[1][1:-1]
        kill = {'headshot':headshot, 'weapon':weapon}
        return event, kill
        '''


class Player2Player(object):


    @staticmethod
    def execute(line):
        # player_a, action, player_b
        parts = line[1:].split('"')[:-1]
        player_a = Player.execute(parts[0])
        action = parts[1].strip(' ')
        player_b = Player.execute(parts[2])
        output = {'player_a':player_a, 'player_b':player_b, 'action':action}
        return output


class Player(object):


    @staticmethod
    def execute(line):
        parts = line.split("<")
        output = {}
        output['alias'] = parts[0]
        parts = map(lambda x: x.strip(">"), parts[1:])
        try:
            output['number'] = parts[0]
            output['steam_id'] = parts[1]
            output['team'] = parts[2]
        except:
            print line
            raise Exception("FUCK")
        return output


class Damage(object):


    @staticmethod
    def execute(line):
        parts = line.split(' (')
        output = {}
        output['weapon'] = parts[0].strip('"')
        for i in map(lambda x: x[:-1].split(' '), parts[1:]):
            if i[0] == 'hitgroup':
                value = ' '.join(map(lambda x: x.strip('"'), i[1:]))
            elif i[0] == 'headshot':
                value = True
            else:
                value = int(i[1].strip('"'))
            output[i[0]] = value
        return output
