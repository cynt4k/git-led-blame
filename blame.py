import requests
import json
import time
import gitlab
import matrix
from rgbmatrix import graphics

class Blame(object):

    def __init__(self, api: gitlab.GitlabHelper, display: matrix.Display):
        self.api = api
        self.display = display
        self.canvas = self.display.matrix.CreateFrameCanvas()
        self.font_ok = graphics.Font()
        self.font_ok.LoadFont('4x6.bdf')
        self.font_ok_color = graphics.Color(0, 30, 200)
        self.circle_ok_color = graphics.Color(100, 255, 40)
        self.circle_error_color = graphics.Color(255, 0, 0)

    def run(self):
        while True:
            self.canvas.Clear()
            project = self.api.get_project()
            # self.draw_ok(project['name'])
            self.draw_error('sepp')
            self.canvas = self.display.matrix.SwapOnVSync(self.canvas)
            time.sleep(20)

    def draw_ok(self, name: str):
        canvas = self.canvas
        graphics.DrawText(self.canvas, self.font_ok, 0, 8, self.font_ok_color, name)
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




if __name__ == "__main__":
    helper = gitlab.GitlabHelper('https://git.cynt4k.de/api/v4', 39, 'kVFN3qCjHkJFVeMv5jJB')
    display = matrix.Display(50)
    blamer = Blame(helper, display)
    blamer.run()
    # project = helper.get_project()

    # canvas = display.matrix.CreateFrameCanvas()
    # font = graphics.Font()
    # font.LoadFont('font.bdf')
    # textColor = graphics.Color(255, 255, 0)
    # pos = canvas.width

    # while True:
    #     canvas.Clear()
    #     graphics.DrawText(canvas, font, pos, 10, textColor, project['name'])
    #     graphics.DrawCircle(canvas, 20, 20, 10, textColor)
    #     time.sleep(2)
    #     canvas = display.matrix.SwapOnVSync(canvas)


    # helper.get_pipeline(39)
    # pipelines = helper.get_last_failed()
    # helper.check_if_ok('master')
    # pipelines = get_pipelines(
    #     'https://git.cynt4k.de/api/v4/projects/39/pipelines', 'kVFN3qCjHkJFVeMv5jJB')
