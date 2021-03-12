import math
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player, Group

from django.conf import settings
import string
import random
import time

debug = True
"""Instructions Pages"""


class Instrucciones(Page):

    def is_displayed(self):
        return self.participant.vars['non_smoker'] != True

    def vars_for_template(self):
        return dict(participant_id=self.participant.label)


class Introduction(Page):

    def is_displayed(self):
        return self.participant.vars['non_smoker'] != True

    def vars_for_template(self):
        return dict(participant_id=self.participant.label)
    pass


class QuizPage(Page):
    _allow_custom_attributes = True
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['non_smoker'] != True

    # timeout_seconds = Constants.timer

    def get_form_fields(self):
        return [self.player.current_field()]

    def error_message(self, values):
        player = self.player

        current_field = player.current_field()
        correct_answer = Constants.quiz_fields[current_field]

        if values[current_field] != correct_answer:  # if answer is incorrect in current field
            # counting incorrect attempts
            player.q_incorrect_attempts += 1
            # telling the player the correct answer
            self.player.quiz_incorrect_answer = 'Alternativa incorrecta. La respuesta correcta es "' \
                                                + str(Constants.quiz_answers[player.quiz_page_counter]) + '"'
            return self.player.quiz_incorrect_answer

    def vars_for_template(self):
        player = self.player
        quiz_questions = Constants.quiz_questions

        index = player.quiz_page_counter
        return {'participant_id': self.participant.label,
                'question': quiz_questions[index],
                'page_number': index + 1,
                'incorrect_answer': player.quiz_incorrect_answer, }

    def before_next_page(self):
        player = self.player
        player.quiz_page_counter += 1

        if self.timeout_happened:
            player.q_timeout = 1
        if player.q_timeout == 1 and player.q_incorrect_attempts == 0:
            player.q_validation = 1
        if player.q_incorrect_attempts == 0 and self.timeout_happened is False:
            player.num_correct += 1
            player.quiz_earnings += Constants.payment_per_answer
            if player.quiz_page_counter == 1:
                self.participant.vars['ea1'] += 1
            if player.quiz_page_counter == 2:
                self.participant.vars['ea2'] += 1
            if player.quiz_page_counter == 3:
                self.participant.vars['ea3'] += 1
            if player.quiz_page_counter == 4:
                self.participant.vars['ea4'] += 1

        self.participant.vars['quiz_earnings'] += player.quiz_earnings
        player.error_sequence += str(player.q_incorrect_attempts)
        player.timeout_sequence += str(player.q_timeout)
        player.q_timeout = 0
        player.q_incorrect_attempts = 0

        # Adds quiz earnings to player's payoff
        self.participant.vars['quiz_earnings'] = self.player.quiz_earnings.to_real_world_currency(self.session)
        self.participant.vars['quiz_questions_correct'] = self.player.num_correct
        self.player.payoff = self.player.quiz_earnings


class QuizResults(Page):

    def is_displayed(self):
        return self.participant.vars['non_smoker'] != True

    form_model = 'player'
    form_fields = ['quiz_dec_2']

    def vars_for_template(self):
        return {'participant_id': self.participant.label,
                'quiz_earnings': self.participant.vars['quiz_earnings']*4,
                }


class QuizTimeout(Page):
    _allow_custom_attributes = True

    def vars_for_template(self):
        player = self.player
        quiz_questions = Constants.quiz_questions

        index = player.quiz_page_counter - 1
        return {'question': quiz_questions[index],
                'answer': Constants.quiz_answers[index]}

    def is_displayed(self):
        player = self.player
        if player.q_validation == 1 and self.participant.vars['is_mobile'] is False:
            return True
        else:
            return False

    def before_next_page(self):
        self.player.q_validation = 0

class partII_overview(Page):
    def is_displayed(self):
        return self.participant.vars['non_smoker'] != True
    def vars_for_template(self):
        return dict(participant_id=self.participant.label)

class Control(Page):

    def is_displayed(self):
        return self.participant.vars['non_smoker'] != True

    form_model = 'player'
    form_fields = ['control_1', 'control_2', 'control_3']

    def vars_for_template(self):
        return dict(participant_id=self.participant.label)

    def before_next_page(self):
        if self.player.control_1 == 0 and self.player.control_2 == 0 and self.player.control_3 == 0:
            self.player.participant.vars['non_smoker'] = True

class Control2(Page):

    def is_displayed(self):
        return self.participant.vars['non_smoker'] != True

    form_model = 'player'
    form_fields = ['control_formato']

    def vars_for_template(self):
        return dict(participant_id=self.participant.label)

    def before_next_page(self):
        if self.player.control_1 == 0 and self.player.control_2 == 0 and self.player.control_3 == 0:
            self.player.participant.vars['non_smoker'] = True

class Non_smoker(Page):

    def is_displayed(self):
        return self.participant.vars['non_smoker'] == True

    form_model = 'player'

    def vars_for_template(self):
        return dict(participant_id=self.participant.label)

class Payment(Page):
    def is_displayed(self):
        return self.participant.vars['non_smoker'] == True

    def vars_for_template(self):
        return {'participant_id': self.participant.label,
                'quiz_earnings': self.participant.vars['quiz_earnings']*4,
                'numero': self.participant.vars['quiz_questions_correct'],
                'ea1': self.participant.vars['ea1'],
                'ea2': self.participant.vars['ea2'],
                'ea3': self.participant.vars['ea3'],
                'ea4': self.participant.vars['ea4'],
                'pago_final': self.participant.vars['quiz_earnings'] / 25  + 5
                }

# Add QuizPage as questions on your quiz
page_sequence = [
    Instrucciones,
    Introduction,
    QuizPage,
    QuizPage,
    QuizPage,
    QuizPage,
    QuizResults,
    partII_overview,
    Control,
    Control2,
    Non_smoker,
    Payment
]