from otree.api import *

# for recaptcha
from otree.settings import RECAPTCHA_URL, RECAPTCHA_SECRET_KEY, RECAPTCHA_SITE_KEY
import requests

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'recaptcha_demo'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    recaptcha_token = models.StringField()
    recaptcha_score = models.FloatField()


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['recaptcha_token']

    def js_vars(player: Player):
        return dict(
            recaptcha_site_key=RECAPTCHA_SITE_KEY
        )

    def vars_for_template(player: Player):
        return dict(
            recaptcha_site_key=RECAPTCHA_SITE_KEY
        )

    def before_next_page(player: Player, timeout_happened):
        res = check_recaptcha(player.recaptcha_token)
        player.recaptcha_score = res['score']

class Results(Page):
    def is_displayed(player: Player):
        return player.recaptcha_score >= 0.5

class BotDropOut(Page):
    def is_displayed(player: Player):
        return player.recaptcha_score < 0.5

def check_recaptcha(token):
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    }
    res = requests.post(RECAPTCHA_URL, data=data)
    return res.json()

def creating_session(subsession: Subsession):
    if not RECAPTCHA_SECRET_KEY or not RECAPTCHA_SITE_KEY:
        raise Exception("You must set RECAPTCHA_SECRET_KEY and RECAPTCHA_SITE_KEY in settings.py")


page_sequence = [MyPage, Results, BotDropOut]
