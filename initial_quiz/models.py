from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

debug = True

author = "Nestor Iván Apaza & Luis Fernando Leyva"

doc = """
Dynamic Quiz for Understanding of a Design 
"""


class Constants(BaseConstants):
    """
    Description:
        Inherits oTree Class BaseConstants. Defines constants for
        the experiment these will remain unchanged
    """
    players_per_group = None
    players_per_group_pg = 4
    instructions_template = 'dedollarization/Instructions.html'
    contact_template = 'dedollarization/Contactenos.html'
    num_rounds = 1
    timer = 20
    payment_per_answer = c(5)

    name_in_url = 'Initial_Quiz'  # name in webbrowser

    # """Amount allocated to each player"""
    endowment = c(10)
    multiplier = 2

    '''Quiz Answers'''
    # TODO: Edit questions and answers (coded and displayed answers)

    # Answers according to the code
    quiz_fields = dict(
        question_1_response=1,
        question_2_response=3,
        question_3_response=3,
        question_4_response=0,
    )

    quiz_questions = ['q1',
                      'q2',
                      'q3',
                      'q4']

    preguntas_quiz = ['¿A qué grupo perteneces?',
                      '¿Durante el juego, en qué casos cambias de grupo?',
                      '¿En qué caso es posible intercambiar de objeto con tu socio?',
                      '¿Cuántos puntos obtendrás si decides mantener el bien de consumo durante una ronda adicional?']

    # Displayed answers
    quiz_answers = ['Rojo', 'En ningún caso cambias de grupo', 'Cuando un integrante posee un bien de consumo y '
                                                                  'el otro, una ficha', 0]
    respuestas_quiz = ['Rojo', 'En ningún caso cambias de grupo', 'Cuando un integrante posee un bien de consumo y '
                                                                  'el otro, una ficha', " '0', porque el bien de consumo "
                                                                                        "te da puntos solamente en la "
                                                                                        "ronda que lo recibes"]

    # Possible choices
    q1_choices = [[0, 'Azul'], [1, 'Rojo']]
    q1_respuestas = [[0, 'Azul'], [1, 'Rojo']]
    q2_choices = [[1, 'Cuando recibes una moneda azul de tu socio'],
                  [2, 'Cuando le entregas una moneda azul a tu socio'],
                  [3, 'En ningún caso cambias de grupo']]
    q3_choices = [[1, 'Cuando ambos tienen un bien de consumo'],
                  [2, 'Cuando ambos tienen fichas de diferentes colores'],
                  [3, 'Cuando un integrante posee un bien de consumo y el otro, una ficha']]
    q4_choices = [[0, '0'],
                  [10, '10'],
                  [50, '50']]
    # To randomize the order in which the answers are presented
    random.SystemRandom().shuffle(q1_choices)
    random.SystemRandom().shuffle(q2_choices)
    random.SystemRandom().shuffle(q3_choices)
    random.SystemRandom().shuffle(q4_choices)


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

    time_spent_on_instructions = models.FloatField(initial=0)

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
                                              choices=Constants.q1_respuestas)
    question_2_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q2_choices)
    question_3_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q3_choices)
    question_4_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q4_choices)
    quiz_earnings = models.CurrencyField(initial=0)

    # For detecting bots
    quiz_dec_2 = models.LongStringField(blank=True)
    
    
    
      '''Preguntas de control - Test Fagestrom'''
     
     # Variables de addición
     
     # Nivel de dependencia: (Bajo; 0-3) (Bajo; 4-5) (Alto; 6-10)
        
    adiccion_1 = models.IntegerField(label="¿Cuántos minutos pasan entre el momento de levantarse y fumar el primer cigarrillo?", choices=[[3,"5 o menos"],[2,"De 6 a 30"], [1,"De 31 a 60"], [0,"Más de 60"]])
    
    adiccion_2 = models.IntegerField(label="¿Encuentras dificultad para abstenerte de fumar en lugares dónde está prohibido?", choices=[[1,"Sí"],[0,"No"]])
    
    adiccion_3 = models.IntegerField(label="¿Qué cigarrillo te costaría más abandonar?", choices=[[1,"El primero de la mañana"],[0,"Cualquier otros"]])
        
    adiccion_4 = models.IntegerField(label="¿Cuántos cigarrillos fumas al día?", choices=[[0,"Menos de 11"],[1,"Entre 11 y 20"], [2,"Entre 21 y 30"],[3,"Más de 30"]])
    
    adiccion_5 =  models.IntegerField(label="¿Fumas más durante las primeras horas de la mañana que durante el resto del día?", choices=[[1,"Sí"],[0,"No"]])
 
    adiccion_6 =  models.IntegerField(label="¿Fumas cuando no te encuentras bien o cuando estás enfermo?", choices=[[1,"Sí"],[0,"No"]])
    
        '''Preguntas de control - Consumidor'''
    
    formato_preferido = models.IntegerField(label="¿Qué formato prefiere usualmente?", choices=[[0,"Cajetilla"],[1,"Suelto"]])
    
    estres = models.IntegerField(label="¿Cómo considera su nivel de estrés actual?", choices=[[0,"No vivenció"],[1,"No me siento estresado"],[2,"Me siento poco estresado"],[3,"Me siento muy estresado"]])
    
    entorno = models.IntegerField(label="¿Cómo considera su entorno social?", choices=[[0,"Ninguno fuma"],[1,"Algunos fuman"],[2,"La mayoría fuma"],[3,"Todos fuman"]])
                                                                                                
    alcohol = models.BooleanField(label="¿Consume alcohol regularmente?", choices [[true, "Sí"], [false,"No"]])
     
    situacion = models.IntegerField(label="¿Cuáles eran sus situaciones preferentes de consumo?", choices=[[1,"Reuniones sociales"],[2,"Entornos sociales entre 2-5 personas"],[3,"De forma solitaria"])
                                                                                                                                                                                   
    marca = models.IntegerField(blank=True, choices=[[1,"Lucky Strike"],[2,"Hamilton"],[3,"Pall Mall"],[4,"Malboro"],[5,"Otros"])                                                                                                                                    
                                                                                                
       '''Preguntas de control - Sociodemográficas'''
        
    sexo =  models.IntegerField(label="¿A qué género pertenece?", choices=[[0,"Mujer"],[1,"Hombre"]])
        
    percibido = models.BooleanField(label="¿De la última caja que compró, ¿Recuerda de qué trataba la imagen disuasoría?", choices [[true, "Sí"], [false,"No"]])
        
    talla = models.IntegerField(label="¿Cuál es tu talla actual?")
    
    peso = models.IntegerField(label="¿Cuál es tu peso actual?")

    estados = models.IntegerField(label="¿Cómo considera su estado de salud actual?", choices=[[0,"Muy mala"],[1,"Mala"],[2,"Buena"],[3,"Muy buena"]])
    
