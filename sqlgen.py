class FactorySql(object):


    def __init__(self):
        self._actions = []
        self._actions.append(AttackSql)
        self._actions.append(KillSql)


    def process(self, match_id, event, damage):
        for a in self._actions:
            if a.match(event, damage):
                return a.generate(match_id, event, damage)


class MatchSql(object):


    @staticmethod
    def generate(map_name, created_on, t_score, ct_score):
        sql = 'INSERT INTO `Match` (`map`, `created_on`, `terrorist`, '\
              '`counter_terrorist`) VALUES ("{}", "{}", {}, {});'
        return sql.format(map_name, created_on, t_score, ct_score)


    @staticmethod
    def insert(db, map_name, created_on, t_score, ct_score):
        c = db.cursor()
        c.execute(MatchSql.generate(map_name, created_on, t_score, ct_score))
        c.execute('SELECT LAST_INSERT_ID();')
        match_id = c.fetchone()
        c.close()
        db.commit()
        return match_id.values()[0]


class ActionSql(object):


    @staticmethod
    def get_team(player):
        if player['team'] == 'TERRORIST':
            return 1
        elif player['team'] == 'CT':
            return 0
        raise Exception("No team found")


class AttackSql(object):


    @staticmethod
    def match(event, damage):
        if event['action'] == 'attacked':
            return True


    @staticmethod
    def generate(match_id, event, damage):
        team = ActionSql.get_team(event['player_a'])
        return AttackInsert(match_id,
                            event['player_a']['steam_id'],
                            event['player_b']['steam_id'],
                            damage['weapon'],
                            damage['hitgroup'],
                            int(damage['damage']),
                            int(damage['damage_armor']),
                            team)


class KillSql(object):


    @staticmethod
    def match(event, kill):
        if event['action'] == 'killed':
            return True
        return False

 
    @staticmethod
    def generate(match_id, event, kill):
        try:
            headshot = int(kill['headshot'])
        except KeyError:
            headshot = 0
        team = ActionSql.get_team(event['player_a'])
        return KillInsert(match_id,
                          event['player_a']['steam_id'],
                          event['player_b']['steam_id'],
                          kill['weapon'],
                          headshot,
                          team)


class AttackInsert(object):


    sql = 'INSERT INTO `Attack` (`match_id`, `player_a`, `player_b`, '\
          '`team`, `weapon`, `hitgroup`, `damage`, `damage_armor`) '\
          'VALUES ({},"{}","{}",{},"{}","{}",{},{});'


    def __init__(self, match_id, player_a, player_b, weapon, hitgroup, damage, 
                 damage_armor, team):
        self.match_id = match_id
        self.player_a = player_a
        self.player_b = player_b
        self.team = team
        self.weapon = weapon
        self.hitgroup = hitgroup
        self.damage = int(damage)
        self.damage_armor = int(damage_armor)


    def generate(self, pc):
        player_a = pc.get_profile_id(self.player_a)
        player_b = pc.get_profile_id(self.player_b)
        if player_a is None or player_b is None:
            raise Exception("Cannot find player's steam_id")
        return AttackInsert.sql.format(self.match_id,
                                       player_a,
                                       player_b,
                                       self.team,
                                       self.weapon,
                                       self.hitgroup,
                                       self.damage,
                                       self.damage_armor)


class KillInsert(object):


    sql = 'INSERT INTO `Kill` (`match_id`, `player_a`, `player_b`, `weapon`, '\
          '`headshot`,`team`) VALUES ({},"{}","{}","{}",{},{});'


    def __init__(self, match_id, player_a, player_b, weapon, headshot, team):
        self.match_id = match_id
        self.player_a = player_a
        self.player_b = player_b
        self.weapon = weapon
        self.headshot = int(headshot)
        self.team = team


    def generate(self, pc):
        player_a = pc.get_profile_id(self.player_a)
        player_b = pc.get_profile_id(self.player_b)
        if player_a is None or player_b is None:
            raise Exception("Cannot find player's steam_id")
        return KillInsert.sql.format(self.match_id,
                                     player_a,
                                     player_b,
                                     self.weapon,
                                     self.headshot,
                                     self.team)
