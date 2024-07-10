from data import *
from pycsp3 import *

running_schedule: VarArray
swimming_schedule: VarArray
cycling_schedule: VarArray
ping_pong_schedule: VarArray
chess_schedule: VarArray
badminton_schedule: VarArray
volleyball_schedule: VarArray
basketball_3_schedule: VarArray
basketball_schedule: VarArray
football_schedule: VarArray

def find_schedule(data: Data):
    players: list[Player] = data.players
    teams: list[Team] = data.teams
    sports: list[Sport] = data.sports
    constraints: list[BaseConstraint] = data.constraints


    # define variables and domains
    running_dom = [player.id for player in players if SportType.RUNNING.value in player.sports]
    if len(running_dom) != 0:
        running_schedule = VarArray(size=len(data.get_sport(SportType.RUNNING.value).time_slots), dom=running_dom)
    
    swimming_dom = [player.id for player in players if SportType.SWIMMING.value in player.sports]
    if len(swimming_dom) != 0:
        swimming_schedule = VarArray(size=len(data.get_sport(SportType.SWIMMING.value).time_slots),dom=swimming_dom)
    
    cycling_dom = [player.id for player in players if SportType.CYCLING.value in player.sports]
    if len(cycling_dom) != 0:
        cycling_schedule = VarArray(size=len(data.get_sport(SportType.CYCLING.value).time_slots), dom=cycling_dom)
    
    ping_pong_dom = [player.id for player in players if SportType.PING_PONG.value in player.sports]
    if len(ping_pong_dom) != 0:
        ping_pong_schedule = VarArray(size=[len(data.get_sport(SportType.PING_PONG.value).time_slots), 2], dom=ping_pong_dom)
    
    chess_dom = [player.id for player in players if SportType.CHESS.value in player.sports]
    if len(chess_dom) != 0:
        chess_schedule = VarArray(size=[len(data.get_sport(SportType.CHESS.value).time_slots), 2], dom=chess_dom)
    
    badminton_dom = [player.id for player in players if SportType.BADMINTON.value in player.sports]
    if len(badminton_dom) != 0:
        badminton_schedule = VarArray(size=[len(data.get_sport(SportType.BADMINTON.value).time_slots), 2], dom=badminton_dom)
    
    volleyball_dom = [team.id for team in teams if SportType.VOLLEYBALL.value == team.sport.sport_type]
    if len(volleyball_dom) != 0:
        volleyball_schedule = VarArray(size=[len(data.get_sport(SportType.VOLLEYBALL.value).time_slots), 2], dom=volleyball_dom)
    
    basketball_3_dom = [team.id for team in teams if SportType.BASKETBALL_3.value == team.sport.sport_type]
    if len(basketball_3_dom) != 0:
        basketball_3_schedule = VarArray(size=[len(data.get_sport(SportType.BASKETBALL_3.value).time_slots), 2], dom=basketball_3_dom)
    
    basketball_dom = [team.id for team in teams if SportType.BASKETBALL.value == team.sport.sport_type]
    if len(basketball_dom) != 0:
        basketball_schedule = VarArray(size=[len(data.get_sport(SportType.BASKETBALL.value).time_slots), 2], dom=basketball_dom)
    
    football_dom = [team.id for team in teams if SportType.FOOTBALL.value == team.sport.sport_type]
    if len(football_dom) != 0:
        football_schedule = VarArray(size=[len(data.get_sport(SportType.FOOTBALL.value).time_slots), 2], dom=football_dom)
    
    # define constraints
    for constraint in constraints:
        if isinstance(constraint, PlayerShouldPlaySport):
            Define_PlayerShouldPlaySport(constraint)
    
    # solve
    if solve() is SAT:
        return {
            SportType.RUNNING: [running_schedule[i].value for i in range(len(running_schedule)) if running_schedule is not None],
            SportType.SWIMMING: [swimming_schedule[i].value for i in range(len(swimming_schedule)) if swimming_schedule is not None],
            SportType.CYCLING: [cycling_schedule[i].value for i in range(len(cycling_schedule)) if cycling_schedule is not None],
            SportType.PING_PONG: [[ping_pong_schedule[i][0].value, ping_pong_schedule[i][1].value] for i in range(len(ping_pong_schedule)) if ping_pong_schedule is not None],
            SportType.CHESS: [[chess_schedule[i][0].value, chess_schedule[i][1].value] for i in range(len(chess_schedule)) if chess_schedule is not None],
            SportType.BADMINTON: [[badminton_schedule[i][0].value, badminton_schedule[i][1].value] for i in range(len(badminton_schedule)) if badminton_schedule is not None],
            SportType.VOLLEYBALL: [[volleyball_schedule[i][0].value, volleyball_schedule[i][1].value] for i in range(len(volleyball_schedule)) if volleyball_schedule is not None],
            SportType.BASKETBALL_3: [[basketball_3_schedule[i][0].value, basketball_3_schedule[i][1].value] for i in range(len(basketball_3_schedule)) if basketball_3_schedule is not None],
            SportType.BASKETBALL: [[basketball_schedule[i][0].value, basketball_schedule[i][1].value] for i in range(len(basketball_schedule)) if basketball_schedule is not None],
            SportType.FOOTBALL: [[football_schedule[i][0].value, football_schedule[i][1].value] for i in range(len(football_schedule)) if football_schedule is not None]
        }
    else:
        return None

def Define_PlayerShouldPlaySport(constraint: PlayerShouldPlaySport):
    schedule: VarArray
    if constraint.sport.sport_type == SportType.RUNNING:
        schedule = running_schedule
    elif constraint.sport.sport_type == SportType.SWIMMING:
        schedule = swimming_schedule
    elif constraint.sport.sport_type == SportType.CYCLING:
        schedule = cycling_schedule
    elif constraint.sport.sport_type == SportType.PING_PONG:
        schedule = ping_pong_schedule
    elif constraint.sport.sport_type == SportType.CHESS:
        schedule = chess_schedule
    elif constraint.sport.sport_type == SportType.BADMINTON:
        schedule = badminton_schedule
    
    if constraint.sport.is_single_player_sport() and schedule is not None:
        satisfy(
                Exist(schedule, lambda i: schedule[i] == constraint.player.id),
                )
    else: # two-player sport
        satisfy(
                Exist(schedule, lambda i: schedule[i][0] == constraint.player.id or schedule[i][1] == constraint.player.id)
                )