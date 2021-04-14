from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

debug = True


doc = """
Cuestionarios dinámicos para observar el entendimiento de los participantes y 
componentes fundamentales para su participación en el resto de experimentos
"""


# TODO: randomize question order
class Constants(BaseConstants):
    """
    Description:
        Inherits oTree Class BaseConstants. Defines constants for
        the experiment these will remain unchanged
    """

    players_per_group = None
    instructions_template = "Quiz_1/InstruccionesB.html"
    contact_template = "Quiz_1/Contactenos.html"
    instructions_button = "Quiz_1/Instructions_Button.html"
    num_rounds = 1
    timer = 20
    payment_per_answer = c(5)

    name_in_url = 'Cigarettes_experiment_1'  # name in webbrowser

    # Initial amount allocated to each player
    endowment = c(100)
    multiplier = 3
    n_rounds = 2  # for using it on the instructions in initial quiz

    '''Quiz Answers'''

    # Answers according to the code
    quiz_fields = dict(
        question_1_response=3,
        question_2_response=2,
        question_3_response=3,
        question_4_response=3,
    )

    quiz_questions = ['¿De qué trata el cuestionario que se brindará en la PARTE II de la sesión?',
                      '¿Cuántas opciones se encuentran en la  PARTE II?',
                      '¿Cuál de los siguientes temas no se preguntarán en la PARTE III?',
                      '¿En qué consiste la PARTE IV?']

    # Displayed answers
    quiz_answers = ['Decisiones de consumo de cigarrillos',
                    'Tres opciones',
                    'Información académica',
                    'Completar cuestionarios sobre la preferencia intertemporal']

    # Write here your possible choices as [number, string_with_choice]
    q1_choices = [[1, 'Valoración a ciertos atributos de los cigarrillos'],
                 [2, 'Frecuencia de consumo de cigarrillos'],
                 [3, 'Decisiones de consumo de cigarrillo'],
                 [4, 'Decisiones de consumo de bebidas alcohólicas']]

    q2_choices = [[1, 'Dos opciones'],
                 [2, 'Tres opciones'],
                 [3, 'Cuatro opciones'],
                 [4, 'Cinco opciones']]

    q3_choices = [[1, 'Información sobre consumo de cigarillos'],
                 [2, 'Información sobre datos generales'],
                 [3, 'Información académica']]

    q4_choices = [[1, 'Indicar qué tan de acuerdo estás con los enunciados presentados'],
                 [2, 'Elegir entre dos opciones específicas presentadas'],
                 [3, 'Completar cuestionarios sobre la preferencia intertemporal'],
                 [4, 'Resolver una ecuación diferencial']]

    format_choices = [[1, 'Suelto'],
                     [2,'Cajetilla']]

    # To randomize the order in which the answers are presented
    random.SystemRandom().shuffle(q1_choices)
    random.SystemRandom().shuffle(q2_choices)
    random.SystemRandom().shuffle(q3_choices)
    random.SystemRandom().shuffle(q4_choices)
    random.SystemRandom().shuffle(format_choices)

class Subsession(BaseSubsession):
    """
    Description:
        Inherits oTree Class BaseSubsession. Defines subsession for
        the experiment.
    Input:
        None
    Output:
        None
    """

    def creating_session(self):
        for p in self.get_players():
            p.participant.vars['final_payoff'] = 0
            p.participant.vars['quiz_payoff'] = 0
            p.participant.vars['quiz_earnings'] = 0
            p.participant.vars['ea1'] = 0
            p.participant.vars['ea2'] = 0
            p.participant.vars['ea3'] = 0
            p.participant.vars['ea4'] = 0
            p.participant.vars['non_smoker'] = False

class Group(BaseGroup):
    """
    Description:
        Inherits BaseGroup oTree class. Assigns group characteristics.
    Input:
        None
    Output:
        None
    """


class Player(BasePlayer):
    """
    Description:
        Inherits oTree class BasePlayer. Defines player characteristics.
    Input:
        None
    Output:
        None
    """

    #Definir el  pay-off del sistema
    def set_payoffs(self):
        p.payoff = self.player.quiz_earnings

    time_spent_on_instructions = models.FloatField(initial=0)

    # Preguntas del escenario de control
    control_1 = models.IntegerField(label="Durante el año 2021, ¿Usted ha consumido cigarrillos?", choices=[[0, "No"], [1, "Sí"]], widget=widgets.RadioSelect)
    control_2 = models.IntegerField(label="Durante el año 2020, ¿Usted ha consumido cigarrillos?", choices=[[0, "No"], [1, "Sí"]], widget=widgets.RadioSelect)
    control_3 = models.IntegerField(label="Antes del confinamiento (2019), ¿Usted ha consumido cigarrillos?", choices=[[0, "No"], [1, "Sí"]], widget=widgets.RadioSelect)

    def current_field(self):
        return 'question_{}_response'.format(self.quiz_page_counter + 1)

    quiz_incorrect_answer = models.StringField(initial=None)
    quiz_respuesta_incorrecta = models.StringField(initial=None)

    # IP field
    player_ip = models.StringField()
    current_practice_page = models.IntegerField(initial=0)

    '''Quiz'''

    # Counter of the questions answered correctly on the first try
    num_correct = models.IntegerField(initial=0)
    quiz_page_counter = models.IntegerField(initial=0)
    # Inc Attemp per question
    q_incorrect_attempts = models.IntegerField(initial=0)
    q_timeout = models.IntegerField(initial=0)
    q_validation = models.IntegerField(initial=0)
    q_attempts = models.IntegerField(initial=0)
    error_sequence = models.CharField(initial='')
    timeout_sequence = models.CharField(initial='')

    question_1_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q1_choices)
    question_2_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q2_choices)
    question_3_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q3_choices)
    question_4_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q4_choices)
    control_formato = models.IntegerField(label="¿Cuál fue el formato de cigarrillos que más compró o prefiere?", widget=widgets.RadioSelect, choices=Constants.format_choices)

    quiz_earnings = models.CurrencyField(initial=0)

    # Hidden Field for detecting bots
    quiz_dec_2 = models.LongStringField(blank=True)
