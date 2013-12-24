class Profile(object):


    def __init__(self, profile_id, steam_id):
        self._profile_id = profile_id
        self._steam_id = steam_id
        self._alias = []


    @property
    def profile_id(self):
        return self._profile_id


    @property
    def steam_id(self):
        return self._steam_id


    def add_alias(self, alias):
        if alias not in self._alias:
            self._alias.append(alias)
            return True
        return False


    def has_alias(self, alias):
        if alias not in self._alias:
            return False
        return True


class ProfileContainer(object):


    def __init__(self):
        self.reset()


    def populate(self, steam_id, profile_id):
        if steam_id not in self._profiles:
            self._profiles[steam_id] = Profile(profile_id, steam_id)


    def add_alias(self, profile_id, alias):
        steam_id = self.get_steam_id(profile_id)
        if steam_id is None:
            raise Exception("Unable to find steam_id")
        if steam_id not in self._profiles:
            self._profiles[steam_id] = []
        if not self._profiles[steam_id].has_alias(alias):
            self._profiles[steam_id].add_alias(alias)

    
    def get_steam_id(self, profile_id):
        for p in self._profiles.values():
            if p.profile_id == profile_id:
                return p.steam_id


    def get_profile_id(self, steam_id):
        try:
            return self._profiles[steam_id].profile_id
        except KeyError:
            return None


    def check(self, steam_id, alias):
        try:
            if self._profiles[steam_id].has_alias(alias):
                return True
        except KeyError:
            pass
        self.add_new(steam_id, alias)
        return False


    def add_new(self, steam_id, alias):
        if steam_id not in self._new:
            self._new[steam_id] = []
        if alias not in self._new[steam_id]:
            self._new[steam_id].append(alias)


    @property
    def has_new(self):
        return True if len(self._new) > 0 else False


    @property
    def new(self):
        return self._new


    def submit_and_update(self, db):
        c = db.cursor()
        self._submit(c)
        self.reset()
        self._update(c)
        c.close()
        db.commit()


    def _submit(self, c):
        for k, v in self._new.iteritems():
            c.execute("INSERT INTO `Profile` (`steam_id`) "\
                      "VALUES ('{}');".format(k))
            c.execute("SELECT LAST_INSERT_ID();")
            profile_id = c.fetchone().values()[0]
            for alias in v:
                c.execute("INSERT INTO `Alias` (`profile_id`, `alias`) "\
                          "VALUES ({}, '{}');".format(profile_id, alias))


    def update(self, db):
        c = db.cursor()
        self._update(c)
        c.close()
        db.commit()


    def _update(self, c):
        rows = c.execute("SELECT `profile_id`, `steam_id` FROM `Profile`;")
        for r in c.fetchall():
            self.populate(r['steam_id'], r['profile_id'])
        rows = c.execute("SELECT `profile_id`, `alias` FROM `Alias`;")
        for r in c.fetchall():
            self.add_alias(r['profile_id'], r['alias'])


    def reset(self):
        self._profiles = {}
        self._new = {}
 

class AliasContainer(object):


    def __init__(self):
        self._aliases = {}


    def add(self, steam_id, alias):
        if steam_id not in self._aliases:
            self._aliases[steam_id] = []
            self._aliases[steam_id].append(alias)
            return True
        elif not self.contains(steam_id, alias):
            self._aliases[steam_id].append(alias)
            return True
        else:
            return False


    def contains(self, steam_id, alias):
        try:
            if alias in self._aliases[steam_id]:
                return True
            return False
        except KeyError:
            return False


    def __str__(self):
        return json.dumps(self._aliases, indent=4)


class WeaponContainer(object):


    def __init__(self):
        self._weapons = {}


    def populate(self, db, table="Weapon"):
        c = db.cursor()
        c.execute("SELECT `name`, `weapon_id` FROM `{}` WHERE 1;".format(table))
        for row in c.fetchall():
            self.add(row['name'], int(row['weapon_id']))
        c.close()


    def add(self, name, weapon_id):
        self._weapons[name] = weapon_id


    def get_weapon_id(self, name):
        return self._weapons[name]
