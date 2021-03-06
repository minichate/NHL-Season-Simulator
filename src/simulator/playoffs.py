import datetime, urllib2
from simulator.models import GameResult
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
from operator import itemgetter
from random import choice, random
from copy import copy

OUTCOMES = [('WIN', 38), ('LOSS', 38), ('OTWIN', 12), ('OTLOSS', 12)]

def weighted_choice(s):
    return choice(sum(([v] * wt for v, wt in s), []))

def tweak():  # Random tiebreak
    return random() / 100

def ordinalize(number):
    if 4 <= number <= 20 or 24 <= number <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][number % 10 - 1]

    return "%s%s" % (number, suffix)

def get_standings(table):
    table_body = table.find('tbody')
    CONF_POINTS = {}

    for row in table_body.findAll('tr'):
        col = row.findAll('td')
        if col[0]['colspan'] != '17':
            team = col[1].find('a')
            team = str(team['rel'])
            CONF_POINTS[team] = int(col[7].contents[0])
    return CONF_POINTS

def get_division(table):
    table_body = table.find('tbody')
    CONF_DIVISION = {}

    for row in table_body.findAll('tr'):
        col = row.findAll('td')
        if col[0]['colspan'] != '17':
            team = col[1].find('a')
            team = str(team['rel'])
            division = col[2].contents[0]
            CONF_DIVISION[team] = str(division)
    return CONF_DIVISION

# WIN or LOSS from perspective of home team
GAME_VALUES = {('home', 'WIN'): 2,
               ('home', 'OTWIN'): 2,
               ('home', 'LOSS'): 0,
               ('home', 'OTLOSS'): 1,
               ('away', 'WIN'): 0,
               ('away', 'OTWIN'): 1,
               ('away', 'LOSS'): 2,
               ('away', 'OTLOSS'): 2}

class PlayoffSimulator(object):
    
    @property
    def completed_sims(self):
        return sum(self.position)

    def scrape_schedule(self):
        page = urllib2.urlopen("http://www.nhl.com/ice/schedulebyseason.htm")
        soup = BeautifulSoup(page)
        table = soup.find("table", {"class":"data schedTbl"})
        table_body = table.find('tbody')
        self.games = []

        for row in table_body.findAll('tr'):
            col = row.findAll('td')
            date = col[0].find('div', {'class': 'skedStartDateSite'}).contents[0]
            date = datetime.datetime.strptime(date, '%a %b %d, %Y').date()

            home = col[2].find('a')
            home = str(home['rel'])

            away = col[1].find('a')
            away = str(away['rel'])

            self.games.append({'home': home, 'away': away, 'date': date,
                               'win_good': 0, 'loss_good': 0})

    def scrape_standings(self):
        page = urllib2.urlopen("http://www.nhl.com/ice/standings.htm?type=con")
        soup = BeautifulSoup(page)
        east_table, west_table = soup.findAll("table", {"class":"data standings Conference"})

        self.east_points = get_standings(east_table)
        self.west_points = get_standings(west_table)
        self.in_playoffs, self.out_playoffs = 0, 0
        
        self.division = {}
        self.division = get_division(east_table)
        self.division.update(get_division(west_table))
        
    def update_points(self, game, result):
        self.points[game['home']] += GAME_VALUES[('home', result)]
        self.points[game['away']] += GAME_VALUES[('away', result)]

    def reverse_points(self, game, result):
        self.points[game['home']] -= GAME_VALUES[('home', result)]
        self.points[game['away']] -= GAME_VALUES[('away', result)]
        
    def get_conference_standing(self):
        divisions, conference, remaining_division = defaultdict(list), [], []
        
        for team, points in self.points.iteritems():
            if team in self.east_points and self.my_team in self.east_points:
                divisions[self.division[team]].append((team, points))
            if team in self.west_points and self.my_team in self.west_points:
                divisions[self.division[team]].append((team, points))
        
        for div in divisions:
            divisions[div].sort(key=itemgetter(1), reverse=True)
            conference.append(divisions[div].pop(0))
            remaining_division += divisions[div]
            
        conference += sorted(remaining_division, key=itemgetter(1), reverse=True)
        return map(itemgetter(0), conference)

    def made_playoffs(self):
        return self.get_conference_standing().index(self.my_team) <= 7

    def made_playoffs_if(self, game, result):
        self.update_points(game, result)
        r = self.made_playoffs()
        self.reverse_points(game, result)
        return r
    
    def update_standing(self):
        self.position[self.get_conference_standing().index(self.my_team)] += 1

    def update_playoffs(self):
        """
        A simulation is defined as "critical" if we suspect that a game between
        non-my-team teams might impact whether my team makes the playoffs.  In
        particular, if 2 points can't move my team from in playoffs to out or
        vice-versa, then no other single game can possibly impact whether my
        team makes the playoffs.  (I haven't thought about tie-breaks.)
        """
        critical = False
        if self.made_playoffs():
            self.in_playoffs += 1
            self.points[self.my_team] -= 4
            if not self.made_playoffs():
                critical = True
            self.points[self.my_team] += 4
        else:
            self.out_playoffs += 1
            self.points[self.my_team] += 4
            if self.made_playoffs():
                critical = True
            self.points[self.my_team] -= 4
            
        return critical

    def update_games_which_matter(self, games):
        for i, game in enumerate(games):
            self.reverse_points(game, game['result'])
            win_good = self.made_playoffs_if(game, 'WIN')
            loss_good = self.made_playoffs_if(game, 'LOSS')
            self.update_points(game, game['result'])

            if win_good and not loss_good:
                self.games[i]['win_good'] += 1
            elif loss_good and not win_good:
                self.games[i]['loss_good'] += 1

    def simulate_once(self):
        self.points = {}
        self.points.update(self.east_points)
        self.points.update(self.west_points)
        
        update_points = self.update_points
        def mapping_function(game):
            result = weighted_choice(OUTCOMES)
            gm = copy(game)
            update_points(game, result)
            gm['result'] = result
            return gm
        
        sim_games = map(mapping_function, self.games)
            
        for key in self.points.keys():
            self.points[key] += tweak()
        
        self.update_standing()
            
        critical = self.update_playoffs()
        if critical:
            self.update_games_which_matter(sim_games)

    def report(self):
        game_results = []
        
        for game in self.games:
            game_result = GameResult()
            game_result.home = game['home']
            game_result.away = game['away']
            game_result.date = game['date'] 
            game_result.home_win_good = game['win_good']
            game_result.home_loss_good = game['loss_good']
            
            if game['win_good'] > game['loss_good']:
                root_for = 'root for %s' % game['home']
                game_result.desired = game['home']
            elif game['win_good'] < game['loss_good']:
                root_for = 'root for %s' % game['away']
                game_result.desired = game['away']
            else:
                root_for = 'don\'t care'
                game_result.desired = None
                
            game_results.append(game_result)
            
            print "(team: %s) %s: %s vs %s: %s (%s %s)" % (self.my_team, game['date'],
                                                game['home'],
                                                game['away'],
                                                root_for,
                                                game['win_good'],
                                                game['loss_good'])
            
        print "(team: %s) %s" % (self.my_team, self.position)
        
        return game_results
            
    def run(self):
        start = datetime.datetime.now()
        for _ in xrange(self.completed_sims, self.completed_sims + self.N):
            try:
                self.simulate_once()
                if self.completed_sims % 1000 == 0:
                    print '(team: %s) Have run %s simulations...' % (self.my_team, self.completed_sims)
                    print datetime.datetime.now() - start
                    start = datetime.datetime.now()
            except KeyboardInterrupt:
                break
        # print "%s %s" % (self.in_playoffs, self.out_playoffs)
        
        return self.report()
        
    def init(self, N, my_team):
        self.my_team = my_team
        self.N = N
        self.position = [0] * 15

    def __init__(self):
        self.scrape_schedule()
        self.scrape_standings()
        self.position = [0] * 15

# PlayoffSimulator().run()
