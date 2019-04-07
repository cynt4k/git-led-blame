import sys
import requests
import json
import time
import gitlab
import settings
import matrix
from rgbmatrix import graphics

class Blame(object):

    def __init__(self, api: gitlab.GitlabHelper, display: matrix.Display, branch: str):
        self.api = api
        self.display = display
        self.branch = branch
        self.canvas = self.display.matrix.CreateFrameCanvas()
        self.font_ok = graphics.Font()
        self.font_ok.LoadFont('4x6.bdf')
        self.font_ok_color = graphics.Color(0, 30, 200)
        self.circle_ok_color = graphics.Color(100, 255, 40)
        self.font_error = self.font_ok
        self.font_error_color = graphics.Color(255, 0, 0)
        self.circle_error_color = graphics.Color(255, 0, 0)
        self.font_info = self.font_ok
        self.font_info_color = graphics.Color(255, 255, 255)

    def run(self):
        counter = settings.CHECK_INTERVAL
        while True:
            self.canvas.Clear()
            try:
                is_ok = False
                if counter == settings.CHECK_INTERVAL:
                    project = self.api.get_project()
                    is_ok = self.api.check_if_ok(self.branch)
                    counter = 0

                if is_ok:
                    self.draw_ok(project['name'])
                else:
                    pipeline = self.api.get_last_failed(branch=self.branch)
                    if counter % 2:
                        self.draw_error_blame(pipeline['user']['username'])
                    else:
                        self.draw_error(self.branch)

            except Exception as e:
                print(e)
                sys.stdout.flush()
                self.draw_internal_error(e)
            

            # self.draw_ok(project['name'])
            # self.draw_error('sepp')
            # self.draw_error_blame('sepp')
            self.canvas = self.display.matrix.SwapOnVSync(self.canvas)
            time.sleep(1)
            counter += 1

    def draw_internal_error(self, e: Exception):
        start_error = self.calc_horizontal_center(len(settings.INTERNAL_ERROR), 4, 0, self.display.matrix.width)
        graphics.DrawText(self.canvas, self.font_error, start_error, 19, self.font_error_color, settings.INTERNAL_ERROR)

    def draw_ok(self, name: str):
        canvas = self.canvas
        start_headline = self.calc_horizontal_center(len(name), 4, 0, self.display.matrix.width)
        graphics.DrawText(self.canvas, self.font_ok, start_headline, 8, self.font_ok_color, name)
        graphics.DrawCircle(self.canvas, 32, 20, 10, self.circle_ok_color)

        x_pos = 27
        y_pos = 21
        for i in range(0, 4):
            canvas.SetPixel(x_pos + i, y_pos + i, 255, 255, 255)
        
        x_pos = 31
        y_pos = 25
        for i in range(0, 9):
            canvas.SetPixel(x_pos +i, y_pos - i, 255, 255, 255)

    def draw_error(self, name: str):
        canvas = self.canvas
        graphics.DrawCircle(self.canvas, 12, 16, 10, self.circle_error_color)

        x_pos = 8
        y_pos = 20
        for i in range(0, 9):
            canvas.SetPixel(x_pos + i, y_pos - i, 255, 255, 255)
        
        x_pos = 8
        y_pos = 12
        for i in range(0, 9):
            canvas.SetPixel(x_pos +i, y_pos + i, 255, 255, 255)

        graphics.DrawText(self.canvas, self.font_error, 26, 14, self.font_error_color, 'FAILED ON')
        graphics.DrawText(self.canvas, self.font_info, 26, 24, self.font_info_color, name)


    def draw_error_blame(self, name: str):
        canvas = self.canvas

        start_info = self.calc_horizontal_center(len(settings.BLAME_TEXT_HEADER), 4, 0, self.display.matrix.width)
        start_name = self.calc_horizontal_center(len(name), 4, 0, self.display.matrix.width)

        graphics.DrawText(self.canvas, self.font_info, start_info, 10, self.font_info_color, settings.BLAME_TEXT_HEADER)
        graphics.DrawText(self.canvas, self.font_info, start_name, 18, self.font_info_color, name)

        start_info = self.calc_horizontal_center(len(settings.BLAME_TEXT_FOOTER), 4, 0, self.display.matrix.width)
        graphics.DrawText(self.canvas, self.font_info, start_info, 28, self.font_info_color, settings.BLAME_TEXT_FOOTER)

    def calc_horizontal_center(self, text_length: int, font_width: int, x_start: int, x_end: int) -> int:
        if text_length * font_width >= x_end - x_start:
            return x_start

        size = text_length * font_width

        size_half = int(size / 2)
        x_half = int((x_end - x_start) / 2 + x_start)
        return x_half - size_half






if __name__ == "__main__":
    helper = gitlab.GitlabHelper(settings.GITLAB_URL, settings.GITLAB_PROJECT, settings.GITLAB_AUTH)
    display = matrix.Display(settings.DISPLAY_BRIGHTNESS)
    blamer = Blame(helper, display, settings.GITLAB_BRANCH)
    blamer.run()
