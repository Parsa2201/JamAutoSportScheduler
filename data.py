from typing import List, Tuple, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class SportType(Enum):
    RUNNING = 0
    SWIMMING = 1
    CYCLING = 2
    PING_PONG = 3
    CHESS = 4
    BADMINTON = 5
    VOLLEYBALL = 6
    BASKETBALL_3 = 7
    BASKETBALL = 8
    FOOTBALL = 9

TeamSports = (SportType.VOLLEYBALL, SportType.BASKETBALL_3, SportType.BASKETBALL, SportType.FOOTBALL)
TwoPlayerSports = (SportType.PING_PONG, SportType.CHESS, SportType.BADMINTON)
SinglePlayerSports = (SportType.RUNNING, SportType.SWIMMING, SportType.CYCLING)

class Sport(BaseModel):
    sport_type: int
    time_slots: Optional[list[Tuple[datetime, datetime]]]

    def change_times(self, time_slots: list[Tuple[datetime, datetime]]):
        self.time_slots = time_slots
    
    def is_team_sport(self) -> bool:
        return self.sport_type in TeamSports
    
    def is_two_player_sport(self) -> bool:
        return self.sport_type in TwoPlayerSports
    
    def is_single_player_sport(self) -> bool:
        return self.sport_type in SinglePlayerSports

class Player(BaseModel):
    id: str
    sports: list[Sport]

class Team(BaseModel):
    id: str
    sport: Sport
    players: list[Player]

class BaseConstraint(BaseModel):
    type: int

class PlayerShouldPlaySport(BaseConstraint):
    player: Player
    sport: Sport

    def __init__(self, player: Player, sport: Sport):
        self.type = 0
        self.player = player
        self.sport = sport

class TeamShouldPlay(BaseConstraint):
    team: Team

    def __init__(self, team: Team):
        self.type = 1
        self.team = team

class PlayerShouldNotPlaySport(BaseConstraint):
    player: Player
    sport: Sport

    def __init__(self, player: Player, sport: Sport):
        self.type = 2
        self.player = player
        self.sport = sport

class TeamShouldNotPlay(BaseConstraint):
    team: Team

    def __init__(self, team: Team):
        self.type = 3
        self.team = team

class PlayerBetterNotPlayAtTimeSlot(BaseConstraint):
    player: Player
    time_slot: Tuple[datetime, datetime]
    priority: int

    def __init__(self, player: Player, time_slot: Tuple[datetime, datetime], priority: int):
        self.type = 4
        self.player = player
        self.time_slot = time_slot
        self.priority = priority

# TODO: Add more constraints

class Data:
    def __init__(self):
        self.players = []
        self.teams = []
        self.sports = [Sport(sport_type=sport_type, time_slots=[(datetime.now(), datetime.now())]) 
                       for sport_type in SportType]

        self.constraints = []
    
    def add_player(self, player: Player):
        self.players.append(player)
    
    def add_players(self, players: list[Player]):
        self.players.extend(players)

    def add_team(self, team: Team):
        self.teams.append(team)
    
    def add_teams(self, teams: list[Team]):
        self.teams.extend(teams)
    
    def add_sport(self, sport: Sport):
        self.sports.append(sport)

    def add_sports(self, sports: list[Sport]):
        self.sports.extend(sports)

    def get_player(self, player_id: str) -> Player | None:
        return next(filter(lambda p: p.id == player_id, self.players), None)
    
    def get_team(self, team_id: str) -> Team | None:
        return next(filter(lambda t: t.id == team_id, self.teams), None)
    
    def get_sport(self, sport_type: int) -> Sport | None:
        return next(filter(lambda s: s.sport_type == sport_type, self.sports), None)
    
    def add_constraint(self, constraint: BaseConstraint):
        self.constraints.append(constraint)

    def remove_all_constraints(self):
        self.constraints.clear()