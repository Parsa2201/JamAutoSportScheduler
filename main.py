import fastapi
from data import *
from datetime import datetime
import schedule

app = fastapi.FastAPI()
data = Data()

@app.post("/add-player")
def add_player(player: Player):
    if data.get_player(player.id) is not None:
        return {"status": "error", "message": "Player already exists"}
    
    data.add_player(player)
    return {"status": "ok"}

@app.post("/add-players")
def add_players(players: list[Player]):
    data.add_players(players)
    return {"status": "ok"}

@app.post("/add-team")
def add_team(team: Team):
    data.add_team(team)
    return {"status": "ok"}

@app.post("/add-teams")
def add_teams(teams: list[Team]):
    data.add_teams(teams)
    return {"status": "ok"}

# @app.post("/add-sport")
# def add_sport(sport: Sport):
#     data.add_sport(sport)
#     return {"status": "ok"}

# @app.post("/add-sports")
# def add_sports(sports: list[Sport]):
#     data.add_sports(sports)
#     return {"status": "ok"}

@app.patch("/change-sport-times")
def change_sport_times(sport_type: int, time_slots: List[Tuple[str, str]]):
    sport = data.get_sport(sport_type)
    if sport is None:
        return {"status": "error", "message": "Sport not found"}
    
    sport.change_times([(datetime.fromisoformat(start), datetime.fromisoformat(end)) for start, end in time_slots])
    return {"status": "ok"}

@app.post("/add-constraint/player-should-play-sport")
def add_player_should_play_sport(player_id: str, sport_type: int):
    player = data.get_player(player_id)
    if player is None:
        return {"status": "error", "message": "Player not found"}
    
    sport = data.get_sport(sport_type)
    if sport is None:
        return {"status": "error", "message": "Sport not found"}
    
    data.add_constraint(PlayerShouldPlaySport(player, sport))
    return {"status": "ok"}

@app.post("/add-constraint/team-should-play")
def add_team_should_play(team_id: str):
    team = data.get_team(team_id)
    if team is None:
        return {"status": "error", "message": "Team not found"}
    
    data.add_constraint(TeamShouldPlay(team))
    return {"status": "ok"}

@app.post("/add-constraint/player-should-not-play-sport")
def add_player_should_not_play_sport(player_id: str, sport_type: int):
    player = data.get_player(player_id)
    if player is None:
        return {"status": "error", "message": "Player not found"}
    
    sport = data.get_sport(sport_type)
    if sport is None:
        return {"status": "error", "message": "Sport not found"}
    
    data.add_constraint(PlayerShouldNotPlaySport(player, sport))
    return {"status": "ok"}

@app.post("/add-constraints/team-should-not-play")
def add_team_should_not_play(team_id: str):
    team = data.get_team(team_id)
    if team is None:
        return {"status": "error", "message": "Team not found"}
    
    data.add_constraint(TeamShouldNotPlay(team))
    return {"status": "ok"}

@app.post("/add-constraints/player-better-not-play-at-time-slot")
def add_player_better_not_play_at_time_slot(player_id: str, start: str, end: str, priority: int):
    player = data.get_player(player_id)
    if player is None:
        return {"status": "error", "message": "Player not found"}
    
    data.add_constraint(PlayerBetterNotPlayAtTimeSlot(player, datetime.fromisoformat(start), datetime.fromisoformat(end), priority))
    return {"status": "ok"}

# TODO: Add more endpoints for adding constraints

@app.delete("/remove-all-constraints")
def remove_all_constraints():
    data.remove_all_constraints()
    return {"status": "ok"}

@app.get("/schedule")
def calculate_schedule():
    return schedule.find_schedule(data)