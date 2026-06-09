from racesharp.race_lookup import lookup_race
from racesharp.analyzer import analyze_race

def race_command(track, time):

    race = lookup_race(track, time)

    return analyze_race(race)
