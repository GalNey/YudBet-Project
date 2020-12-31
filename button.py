__author__ = "Gal Neystadt"

import pygame

def create_txt_obj(txt, txt_size, color, font="freesansbold.ttf"):
    font = pygame.font.Font(font, txt_size)
    text = font.render(txt, True, color)

    return text

class Button(object):
    def __init__(self, screen, width, height, left_loc, top_loc, txt="", txt_size=2, txt_x=999, txt_y=999, bg_color=(0,0,0), txt_color =(0,0,0), is_active=True):
        self.screen = screen
        self.width = width
        self.height = height
        self.left_loc = left_loc
        self.top_loc = top_loc
        self.txt = txt
        self.txt_size = txt_size
        self.txt_x = txt_x
        self.txt_y = txt_y
        self.bg_color = bg_color
        self.txt_color = txt_color
        self.is_active = is_active


    def draw_button(self, no_bg=True):

        self.no_bg = no_bg

        if self.txt_x != 999:
            x_location = self.txt_x + self.left_loc
        else:
            x_location = self.left_loc + self.width / 4

        if self.txt_y != 999:
            y_location = self.txt_y + self.top_loc
        else:
            y_location = self.top_loc + self.height / 2 - self.txt_size / 2

        # pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
        pygame.draw.rect(self.screen, self.bg_color, [self.left_loc, self.top_loc, self.width, self.height], no_bg)

        if self.txt != "":
            text = create_txt_obj(self.txt, self.txt_size, self.txt_color)
            self.screen.blit(text, (x_location, y_location))


    def activate(self):
        self.is_active = True


    def deactivate(self):
        self.is_active = False


    def clean_up(self):

        pygame.draw.rect(self.screen, self.bg_color, [self.left_loc, self.top_loc, self.width, self.height], False)
        pygame.display.flip()


    def get_text(self):
        return self.txt


    def set_text(self, txt):
        self.clean_up()
        self.txt = txt


    def set_bg_color(self, color):
        self.bg_color = color
        self.draw_button()


    def set_txt_color(self, color):
        self.txt_color = color


    def set_txt_size(self, new_size):
        self.txt_size = new_size


    def is_clicked(self, loc):
        x = loc[0]
        y = loc[1]
        if self.is_active:
            if x >= self.left_loc and x <= self.left_loc + self.width:
                if y >= self.top_loc and y <= self.top_loc + self.height:
                    return True

        return False


    def get_middle(self):
        return (self.left_loc + self.width / 2), (self.top_loc + self.height / 2)


    def get_middle_above_txt(self):
        return (self.left_loc + self.width / 2), (self.top_loc + self.txt_y)


    def get_middle_below_txt(self):
        return (self.left_loc + self.width / 2), (self.top_loc + self.txt_y + self.txt_size)


if __name__ == "__main__":
    window_width = 480
    window_height = 360

    pygame.init()
    size = (window_width, window_height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Network Manager")

    #screen, width, height, left_loc, top_loc, txt="", txt_size = 2, txt_x=0, txt_y=0, bg_color=(160,160,160), txt_color =(0,0,0)
    b1 = Button(screen, 100, 100, 0, 0, "Hello", 20)
    b1.draw_button() #5,5)
    pygame.display.flip()



    finish = False
    while not finish:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
                break
            '''
            if event.type == pygame.MOUSEBUTTONUP:
                if b1.is_clicked(pygame.mouse.get_pos()):
                    print "inside"
                else:
                    print "outside"
            '''