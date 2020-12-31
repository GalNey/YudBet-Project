from button import *
import pygame
#import thorpy

def reset_bg(screen,pic="main_bg.png"): # will draw new background to erase what currently on screen
    img = pygame.image.load(pic)
    screen.blit(img, (0, 0))

def build_main_screen(screen):  # present which actions user want to do- watch live video or see picture
    reset_bg(screen, "main_bg_detect.png")

    # screen, width, height, left_loc, top_loc, txt="", txt_size = 2, txt_x=0, txt_y=0, bg_color=(160,160,160), txt_color =(0,0,0)
    watch_live = Button(screen, 520, 40, 100, 100, "Watch Live Video", 20, txt_x=180, txt_y=10, txt_color=(0, 0, 0))
    watch_live.draw_button()

    see_picture = Button(screen, 520, 40, 100, 200, "See Identified Objects In Pictures", 20, txt_x=100, txt_y=10, txt_color=(0, 0, 0))
    see_picture.draw_button()

    exit = Button(screen, 70, 40, 600, 480, "Exit", 20, txt_x=14, txt_y=12, txt_color=(0, 0, 0))
    exit.draw_button()

    Manager = create_txt_obj("By Gal Neystadt, 2020", 15, (160, 0, 0))
    screen.blit(Manager, (280, 520))

    return watch_live, see_picture, exit

def build_watch_live(screen, camera_names_list):  # let the user choose which camera he wants to watch
    reset_bg(screen)

    watch = create_txt_obj("Watch Live Video", 30, (0, 0, 0))
    screen.blit(watch, (230, 50))

    Manager = create_txt_obj("Press on one of the camera names to see it's live broadcast", 15, (160, 0, 0))
    screen.blit(Manager, (150, 95))

    # screen, width, height, left_loc, top_loc, txt="", txt_size = 2, txt_x=0, txt_y=0, bg_color=(160,160,160), txt_color =(0,0,0)
    #connect = Button(screen, 100, 40, 570, 120, "Connect", 20, txt_x=8, txt_y=10, txt_color=(0, 0, 0))
    #connect.draw_button()

    refresh = Button(screen, 100, 40, 570, 120, "Refresh", 20, txt_x=12, txt_y=12, txt_color=(0, 0, 0))
    refresh.draw_button()

    back = Button(screen, 70, 40, 600, 480, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    back.draw_button()

    #back = Button(screen, 200, 400, 200, 120, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    #back.draw_button()

    cameras = []

    if len(camera_names_list) == 0:
        tmp = Button(screen, 200, 400, 60, 120, "No cameras available", 16, txt_x=15, txt_y=190, txt_color=(160, 0, 0), is_active=False)
        tmp.draw_button()
        cameras.append(tmp)

    cnt = 0
    for c_name in camera_names_list:
        cam = Button(screen, 200, 400 / len(camera_names_list), 60, 120 + cnt *(400 / len(camera_names_list)), c_name, 20, txt_x=30, txt_y=200 / len(camera_names_list) - 10, txt_color=(0, 0, 0))
        cam.draw_button()
        cameras.append(cam)

        cnt += 1

    return back, cameras, refresh

def build_photo_list(screen, photo_list, loc):  # let the user choose which photo he wants to see

    num = str(photo_list[1])
    if "." in num:
        num = num[:num.find(".")]
    photo_list = photo_list[0]

    reset_bg(screen)

    watch = create_txt_obj("See Identified Photos", 30, (0, 0, 0))
    screen.blit(watch, (215, 50))

    scroll = create_txt_obj("see more photos by using forward and previous buttons", 15, (160, 0, 0))
    screen.blit(scroll, (155, 95))

    options = create_txt_obj("Press on one of the photos to see options", 15, (160, 0, 0))
    screen.blit(options, (210, 120))

    # screen, width, height, left_loc, top_loc, txt="", txt_size = 2, txt_x=0, txt_y=0, bg_color=(160,160,160), txt_color =(0,0,0)
    _next = Button(screen, 100, 40, 570, 120, "Next", 20, txt_x=25, txt_y=10, txt_color=(0, 0, 0))
    _next.draw_button()

    previous = Button(screen, 100, 40, 570, 180, "Previous", 20, txt_x=7, txt_y=12, txt_color=(0, 0, 0))
    previous.draw_button()

    back = Button(screen, 70, 40, 600, 480, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    back.draw_button()

    see_all = Button(screen, 100, 40, 570, 240, "See All", 20, txt_x=14, txt_y=10, txt_color=(0, 0, 0))
    see_all.draw_button()

    see_bm = Button(screen, 100, 40, 570, 300, "See BM", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    see_bm.draw_button()



    order = create_txt_obj("PhotoId | Date | CameraId | CameraName", 10, (0, 0, 0))
    screen.blit(order, (62, 170))


    count = create_txt_obj("page " + str(loc) + " of " + str(num), 10, (0, 0, 0))
    screen.blit(count, (415, 200))

    photos = []
    cnt = 0


    #sorted_data = photo_list[1:].replace("\\", "").replace("'", "").replace(",", "").replace(")", "").split("(")
    for c_name in photo_list:
        pht = Button(screen, 350, 370 / 10, 60, 187 + cnt * (370 / 10),
                     c_name.replace(" ", " | "), 15, txt_x=10, txt_y=200 / 10 - 10, txt_color=(0, 0, 0))
        pht.draw_button()
        photos.append(pht)

        cnt += 1

    return photos, back, _next, previous, see_bm, see_all


def build_back_screen(screen): #this screen will be presented while there is live video presented
    reset_bg(screen)

    back = Button(screen, 70, 40, 600, 480, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    back.draw_button()

    return back

def build_back_screen_with_photo(screen, picture): #this screen will be presented while there is live video presented
    #reset_bg(screen)

    picture = pygame.image.fromstring(picture, (640, 480), "RGB")
    picture = pygame.transform.scale(picture, (720, 540))
    screen.blit(picture, (0, 0))

    back = Button(screen, 70, 40, 600, 480, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    back.draw_button()

    return back


def build_options_for_photo(screen, photo_info, picture):  # present extra options to operate on picture
    reset_bg(screen)

    picture = pygame.image.fromstring(picture, (640, 480), "RGB")
    picture = pygame.transform.scale(picture, (240, 180))
    screen.blit(picture, (425, 100))

    pic_info = photo_info[4:].replace(" ", "").split("|")
    pic_info = "Info: Date- " + pic_info[0] + ", Camera ID- " + pic_info[1] + ", Camera Name- " + pic_info[2]
    info = create_txt_obj(pic_info, 18, (0, 0, 0))
    screen.blit(info, (55, 50))

    # screen, width, height, left_loc, top_loc, txt="", txt_size = 2, txt_x=0, txt_y=0, bg_color=(160,160,160), txt_color =(0,0,0)
    seeP = Button(screen, 300, 40, 55, 100, "See Photo In Full Screen", 20, txt_x=30, txt_y=10, txt_color=(0, 0, 0))
    seeP.draw_button()

    dele = Button(screen, 300, 40, 55, 166, "Delete Photo", 20, txt_x=90, txt_y=10, txt_color=(0, 0, 0))
    dele.draw_button()

    bookMark = Button(screen, 300, 40, 55, 233, "BookMark Photo", 20, txt_x=70, txt_y=12, txt_color=(0, 0, 0))
    bookMark.draw_button()

    unbookMark = Button(screen, 300, 40, 55, 300, "UnBookMark Photo", 20, txt_x=55, txt_y=12, txt_color=(0, 0, 0))
    unbookMark.draw_button()

    gtxt = Button(screen, 300, 40, 55, 366, "Get Text Of Photo", 20, txt_x=66, txt_y=12, txt_color=(0, 0, 0))
    gtxt.draw_button()

    stxt = Button(screen, 300, 40, 55, 433, "Set Text Of Photo", 20, txt_x=66, txt_y=12, txt_color=(0, 0, 0))
    stxt.draw_button()


    back = Button(screen, 70, 40, 600, 480, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    back.draw_button()

    return seeP, dele, bookMark, unbookMark, gtxt, stxt, back

def build_show_text(screen, text):  # builds screen where current text of picture is shown
    reset_bg(screen)

    cur = create_txt_obj("Current text:", 20, (0, 0, 0))
    screen.blit(cur, (32, 50))

    cur = create_txt_obj(text, 20, (160, 0, 0))
    screen.blit(cur, (32, 80))

    back = Button(screen, 70, 40, 600, 480, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    back.draw_button()

    return back

def build_get_text(screen, text):  # builds screen where collecting text for picture
    reset_bg(screen)

    please_enter = create_txt_obj("Please enter the new text and then press on the Enter button", 22, (0, 0, 0))
    screen.blit(please_enter, (32, 120))

    _max = create_txt_obj("(Max length: 40 characters)", 20, (0, 0, 0))
    screen.blit(_max, (190, 210))

    cur = create_txt_obj("Current text:", 20, (0, 0, 0))
    screen.blit(cur, (32, 350))

    cur = create_txt_obj(text, 20, (160, 0, 0))
    screen.blit(cur, (32, 380))


    # screen, width, height, left_loc, top_loc, txt="", txt_size = 2, txt_x=0, txt_y=0, bg_color=(160,160,160), txt_color =(0,0,0)
    writer = Button(screen, 640, 40, 30, 160, "", 20, txt_x=2, txt_y=10, txt_color=(160, 0, 0), bg_color=(160,160,160))
    writer.draw_button(no_bg=False)

    back = Button(screen, 70, 40, 600, 480, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    back.draw_button()

    return writer, back

def dc_from_manager(screen):
    reset_bg(screen)

    please_enter = create_txt_obj("Seems to be disconnected from manager", 30, (0, 0, 0))
    screen.blit(please_enter, (50, 120))

    please_enter = create_txt_obj("Please reconnect and restart", 30, (0, 0, 0))
    screen.blit(please_enter, (140, 170))

    please_enter = create_txt_obj("Type ot press anything to exit", 22, (160, 0, 0))
    screen.blit(please_enter, (200, 510))

def no_database(screen):
    reset_bg(screen)

    please_enter = create_txt_obj("No active connection with database", 30, (0, 0, 0))
    screen.blit(please_enter, (95, 120))

    #please_enter = create_txt_obj("Type ot press anything to exit", 22, (160, 0, 0))
    #screen.blit(please_enter, (200, 510))

    back = Button(screen, 70, 40, 600, 480, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    back.draw_button()

    return back

def mid_video_camera_dc(screen):
    reset_bg(screen)

    please_enter = create_txt_obj("The camera seems to be disconnected", 30, (0, 0, 0))
    screen.blit(please_enter, (70, 120))

    #please_enter = create_txt_obj("Type ot press anything to exit", 22, (160, 0, 0))
    #screen.blit(please_enter, (200, 510))

    back = Button(screen, 70, 40, 600, 480, "Back", 20, txt_x=11, txt_y=10, txt_color=(0, 0, 0))
    back.draw_button()

    return back

