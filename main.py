from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import time


class PongPaddle(Widget):
    score = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity1 = ReferenceListProperty(velocity_x, velocity_y)
    last_time = 0

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

    def move_player2(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        self.last_time = current_time
        self.center_y = self.velocity_y * elapsed_time + self.center_y
    
    def updatePosition(self):
        self.pos = Vector(*self.velocity1) + self.pos


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    

    def serve_ball(self, vel=(10, 1)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def serve_paddle(self, vel=(0, 5)):
        self.player2.center = self.center
        self.player2.velocity1 = vel

    def update(self, dt):

        self.ball.move()
        self.player2.move_player2()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went off to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        # bot_enemy easy mode
        # if self.ball.x >= (self.right - self.x)/2:
        speed = 500
        if (self.ball.y >= self.player2.y and self.ball.top <= self.player2.top):
            self.player2.velocity_y = 0
        elif (self.ball.y < self.player2.center_y):
            self.player2.velocity_y = -speed
        elif (self.ball.top > self.player2.center_y):
            self.player2.velocity_y = speed
            

        # bot_enemy hard mode
        # self.player2.center_y  = self.ball.y

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        # if touch.x > self.width - self.width / 3:
        #     self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()