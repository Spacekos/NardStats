import kivy

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.config import Config


Config.set('kivy', 'keyboard_mode', 'systemanddock')
Window.size = (480, 853)

class Container(BoxLayout):
    message_to_client = ObjectProperty()
    player1_info = ObjectProperty()
    player2_info = ObjectProperty()
    player1_name = ObjectProperty()
    player2_name = ObjectProperty()

    turn = list()
    player1_turn = True
    player2_turn = False
    player1_history = list()
    player2_history = list()
    player1_score = 0
    player2_score = 0
    name_player1 = 'Игрок1'
    name_player2 = 'Игрок2'
    player1_duble = {'11' : 0,
                     '22' : 0,
                     '33' : 0,
                     '44' : 0,
                     '55' : 0,
                     '66' : 0
                    }
    player2_duble = {'11': 0,
                     '22': 0,
                     '33': 0,
                     '44': 0,
                     '55': 0,
                     '66': 0
                     }

    def stat_duble(self, player_duble):
        count = 0
        output = ''
        for key, value in player_duble.items():
            if value > 0:
                count += value
                output += f'{key}: {str(value)}\n'
        return f'Выбросил в сумме дублей: {count}\n' \
               f'{output}'

    def back(self):
        if len(self.player1_history) == 0 or len(self.player2_history) == 0:
            self.message_to_client.text = 'Нет записанных ходов для отмены!'
            return None
            #raise Exception('Нет записанных ходов для отмены!')
        if self.player1_turn:
            if self.player2_history[-1][0] == self.player2_history[-1][1]:
                self.player2_score -= self.player2_history[-1][0] * 4
                self.player2_duble[self.turn_to_str(self.player2_history[-1])] -= 1
            else:
                self.player2_score -= sum(self.player2_history[-1])
            self.player2_history = self.player2_history[:-1]
        else:
            if self.player1_history[-1][0] == self.player1_history[-1][1]:
                self.player1_score -= self.player1_history[-1][0] * 4
                self.player1_duble[self.turn_to_str(self.player1_history[-1])] -= 1
            else:
                self.player1_score -= sum(self.player1_history[-1])
            self.player1_history = self.player1_history[:-1]
        self.rev()
        self.info_update()

    def rev(self):
        self.player1_turn = not self.player1_turn
        self.player2_turn = not self.player2_turn


    def info_update(self):
        if self.player1_turn:
            self.message_to_client.text = f'Бросает кубики {self.player1_name.text}'
            self.player1_info.text = f'Статстика игрока: {self.player1_name.text}\n' \
                                     f'\n' \
                                     f'Выбросил в сумее очков: {str(self.player1_score)}\n' \
                                     f'{self.stat_duble(self.player1_duble)}'
        else:
            self.message_to_client.text = f'Бросает кубики {self.player2_name.text}'
            self.player2_info.text = f'Статстика игрока: {self.player2_name.text}\n' \
                                     f'\n' \
                                     f'Выбросил в сумее очков: {str(self.player2_score)}\n' \
                                     f'{self.stat_duble(self.player2_duble)}'

    def turn_to_str(self, turn):
        turn_str = ''
        for i in turn:
            turn_str += str(i)
        return turn_str

    def rec(self):
        self.info_update()
        if len(self.turn) == 2:
            if self.player1_turn:
                self.player1_history.append(self.turn)
                if self.turn[0] == self.turn[1]:
                    self.player1_score += sum(self.turn) * 2
                    self.player1_duble[self.turn_to_str(self.turn)] += 1
                else:
                    self.player1_score += sum(self.turn)
                self.info_update()
                self.rev()
                self.info_update()
                self.turn = list()
                #self.rev()
            else:
                self.player2_history.append(self.turn)
                if self.turn[0] == self.turn[1]:
                    self.player2_score += sum(self.turn) * 2
                    self.player2_duble[self.turn_to_str(self.turn)] += 1
                else:
                    self.player2_score += sum(self.turn)
                self.info_update()
                self.rev()
                self.info_update()
                self.turn = list()
                #self.rev()
            print(self.player1_history)
            print(self.player2_history)

    def press1(self):
        self.turn.append(1)
        self.rec()

    def press2(self):
        self.turn.append(2)
        self.rec()

    def press3(self):
        self.turn.append(3)
        self.rec()

    def press4(self):
        self.turn.append(4)
        self.rec()

    def press5(self):
        self.turn.append(5)
        self.rec()

    def press6(self):
        self.turn.append(6)
        self.rec()

class NardStatsApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    NardStatsApp().run()