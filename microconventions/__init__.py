from microconventions.url_conventions import API_URL, FAILOVER_API_URL, api_url, failover_api_url, get_config
from microconventions.conventions import KeyConventions, StreamConventions, ValueConventions, MicroConventions
from microconventions.key_conventions import new_key, create_key, maybe_create_key, animal_from_key, shash,\
    animal_from_code, key_difficulty, code_from_code_or_key
from microconventions.type_conventions import Genus, Family, Activity
from microconventions.rating_conventions import RatingVariety
from microconventions.leaderboard_conventions import LeaderboardVariety
from microconventions.stats_conventions import nudged, is_discrete, evenly_spaced_percentiles, cdf_values,\
    quantize, discrete_pdf, discrete_cdf, sign_changes, is_process
