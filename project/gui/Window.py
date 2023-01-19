import urllib.error

import numpy as np
import tkinter as tk

from project.src.GetSkin import GetSkin
from project.src.LCUAccess import LCUAccess
from project.utils.utils import *


def required_legal_statement():
    window = tk.Tk()
    window.title("Legal statement")
    window.geometry("{}x{}".format(450, 150))

    statement = u"SkinSelector isn't endorsed by Riot Games and doesn't reflect the views or\n" \
                u"opinions of Riot Games or anyone officially involved in producing or\n" \
                u" managing Riot Games properties. Riot Games, and all associated properties are\n" \
                u"trademarks or registered trademarks of Riot Games, Inc."
    tk.Label(window, text=statement).place(relx=0.5,
                                           rely=0.35,
                                           anchor=tk.CENTER)
    tk.Button(window, text="Ok", command=window.destroy).place(relx=0.5,
                                                               rely=0.75,
                                                               anchor=tk.CENTER)
    window.mainloop()


def exit_confirmation(root):
    def close_program(confirmation_window, root_window):
        confirmation_window.destroy()
        root_window.destroy()

    exit_confirmation_window = tk.Tk()
    exit_confirmation_window.title("Confirmation")
    exit_confirmation_window.geometry("{}x{}".format(250, 100))
    tk.Label(exit_confirmation_window, text="Do you wish to close the Skin Selector?").place(relx=0.5,
                                                                                             rely=0.35,
                                                                                             anchor=tk.CENTER)
    tk.Button(exit_confirmation_window, text="Yes",
              command=lambda: close_program(exit_confirmation_window, root)).place(relx=0.25,
                                                                                   rely=0.75,
                                                                                   relwidth=0.3,
                                                                                   anchor=tk.CENTER)
    tk.Button(exit_confirmation_window, text="No", command=exit_confirmation_window.destroy).place(relx=0.75,
                                                                                                   rely=0.75,
                                                                                                   relwidth=0.3,
                                                                                                   anchor=tk.CENTER)

    exit_confirmation_window.mainloop()


class GUI:
    def __init__(self):
        self._width = 1280
        self._height = 720
        self._borders_width_ratio = 0.03

        self._lcu_access = LCUAccess()

        self._root = tk.Tk()
        self._root.configure(bg='light gray')
        self._root.resizable(width=False, height=False)

        self._opening_screen()

        self._rows_height = np.array([0.1, 0.7, 0.15, 0.05])
        self._columns_width = np.array([0.25, 0.75])
        np.testing.assert_approx_equal(np.sum(self._rows_height), 1.0)
        np.testing.assert_approx_equal(np.sum(self._columns_width), 1.0)

        self._canvas_borders_width = max(self._width, self._height) * self._borders_width_ratio
        self._canvas_size = (self._width-self._canvas_borders_width,
                             self._height-self._canvas_borders_width)

        if self._canvas_size[0] > self._canvas_size[1]:
            self._chosen_skin_image_new_size = tuple([int(self._canvas_size[0] * self._rows_height[1]),
                                                      int(self._canvas_size[1] * self._rows_height[1])])
        else:
            self._chosen_skin_image_new_size = tuple([int(self._canvas_size[0] * self._columns_width[1]),
                                                      int(self._canvas_size[1] * self._columns_width[1])])

        self._root.mainloop()

    # for debugging
    def _get_rest_request_header(self):
        self._lcu_access.build_header()

    def _draw_chosen_skin_image(self, url, new_size):
        chosen_skin = load_image_from_web(url)

        chosen_skin = resize_image_from_web(chosen_skin[1],
                                            new_size=new_size)
        self._chosen_skin_image = tk.Label(self._canvas,
                                           image=chosen_skin,
                                           bg='light gray')
        self._chosen_skin_image.image = chosen_skin
        self._chosen_skin_image.place(relheight=self._rows_height[1],
                                      relwidth=self._columns_width[1],
                                      relx=self._columns_width[0],
                                      rely=self._rows_height[0])

    def _choose_skin(self):
        res = self._get_skin.get_available_skins_and_chromas()
        if res['res']:
            # Chosen skin. Loads image and name
            # Loads skin splash art
            selected_skin = res['output'][0]
            champion = selected_skin[0].replace(" ", "").replace(".", "").replace("'", "")
            skin_id = selected_skin[2]
            try:
                url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + champion + '_' + str(skin_id) + '.jpg'
                print(url)
                self._draw_chosen_skin_image(url, self._chosen_skin_image_new_size)
            except urllib.error.HTTPError:
                champion = champion.lower().capitalize()
                url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + champion + '_' + str(skin_id) + '.jpg'
                self._draw_chosen_skin_image(url, self._chosen_skin_image_new_size)

            # Writes skin name and chroma if applicable
            selected_skin_name = selected_skin[1].upper()
            if selected_skin_name == champion.upper():
                selected_skin_name = "CLASSIC " + selected_skin_name
            elif selected_skin[3]:
                selected_skin_name += " - " + selected_skin[3]
            self._chosen_skin_name.configure(text=selected_skin_name,
                                             font=("Helvetica", 20))

            # loads every other skin and respective number of chromas available
            every_option = {}
            for skin in res['output'][1]:
                if skin[1] not in every_option:
                    every_option[skin[1]] = 0
                else:
                    every_option[skin[1]] += 1
    
            list_skins_chromas = ""
            for skin, chromas in every_option.items():
                if not chromas:
                    list_skins_chromas += skin.upper() + "\n\n"
                else:
                    list_skins_chromas += skin.upper() + "\n+ " + str(chromas) + " chromas\n\n"
            self._available_skins_list.config(state=tk.NORMAL)
            self._available_skins_list.delete('1.0', tk.END)
            self._available_skins_list.insert(tk.END, list_skins_chromas)
            self._available_skins_list.config(state=tk.DISABLED)

    def _opening_screen(self):
        self._root.title("Skin Selector")

        def is_lol_running():
            if self._lcu_access.is_lol_running:
                self._main_screen()
            else:
                message_error = tk.Tk()
                message_error.geometry("{}x{}".format(250, 100))
                tk.Label(message_error,
                         text="League of Legends is not running").place(relx=0.5,
                                                                        rely=0.3,
                                                                        anchor=tk.CENTER)
                tk.Button(message_error,
                          text="Ok",
                          command=message_error.destroy).place(relx=0.5,
                                                               rely=0.7,
                                                               anchor=tk.CENTER)

        # os = opening screen
        os_width = 200
        os_height = 200

        background_image_url = 'http://ddragon.leagueoflegends.com/cdn/13.1.1/img/mission/newPlayerExperience/Pupil_Becomes_The_Master.png'
        background_image = load_image_from_web(background_image_url)
        background_image = resize_image_from_web(background_image[1], new_size=(200, 200))

        background = tk.Label(self._root, image=background_image)
        background.image = background_image
        background.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Button(self._root, text="Start", command=is_lol_running).place(relx=0.5,
                                                                          rely=0.75,
                                                                          anchor=tk.CENTER)
        tk.Button(self._root, text="Exit", command=self._root.destroy).place(relx=0.5,
                                                                             rely=0.9,
                                                                             anchor=tk.CENTER)

        self._root.geometry("{}x{}".format(os_width, os_height))

    def _main_screen(self):
        self._root.geometry("{}x{}".format(self._width, self._height))
        self._get_skin = GetSkin(self._lcu_access)

        self._canvas = tk.Canvas(self._root,
                                 width=self._canvas_size[0],
                                 height=self._canvas_size[1])
        self._canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Headers - Top row
        tk.Label(self._canvas,
                 text="AVAILABLE SKINS",
                 font=("Helvetica", 15),
                 bg='light gray').place(relheight=self._rows_height[0],
                                        relwidth=self._columns_width[0])
        tk.Label(self._canvas,
                 text="CHOSEN SKIN",
                 font=("Helvetica", 15),
                 bg='light gray').place(relheight=self._rows_height[0],
                                        relwidth=self._columns_width[1],
                                        relx=self._columns_width[0])

        # Skins - Middle row
        # List of available skins for that champion
        scroll_bar_width = 0.01
        scroll_bar = tk.Scrollbar(self._canvas, bg='black', width=10)
        self._available_skins_list = tk.Text(self._canvas,
                                             relief=tk.FLAT,
                                             bg='light gray',
                                             yscrollcommand=scroll_bar.set,
                                             font=("Helvetica", 13)
                                             )
        self._available_skins_list.place(relheight=self._rows_height[1],
                                         relwidth=self._columns_width[0]-scroll_bar_width,
                                         rely=self._rows_height[0])
        scroll_bar.config(command=self._available_skins_list.yview)
        scroll_bar.place(relheight=self._rows_height[1],
                         relwidth=scroll_bar_width,
                         relx=self._columns_width[0]-scroll_bar_width,
                         rely=self._rows_height[0])
        self._available_skins_list.config(state=tk.DISABLED)

        # Draw placeholder while skin is not chosen
        url = 'http://ddragon.leagueoflegends.com/cdn/13.1.1/img/mission/eog/rewards/leveling/features/Feature_FWoTD.png'
        placeholder_size = (int(self._canvas_size[1] * self._rows_height[1]),
                            int(self._canvas_size[1] * self._rows_height[1]))
        self._draw_chosen_skin_image(url, placeholder_size)

        # Buttons and skin name - Bottom row
        # Buttons
        tk.Button(self._canvas,
                  text="CHOOSE SKIN",
                  font=("Helvetica", 15),
                  bg='green',
                  command=self._choose_skin).place(relheight=self._rows_height[2],
                                                   relwidth=self._columns_width[0],
                                                   rely=float(np.sum(self._rows_height[:2])))

        tk.Button(self._canvas,
                  text="EXIT",
                  font=("Helvetica", 15),
                  command=lambda: exit_confirmation(self._root),
                  bg='red').place(relheight=self._rows_height[3],
                                  relwidth=self._columns_width[0],
                                  rely=float(np.sum(self._rows_height[:3])))

        # Chosen skin name
        self._chosen_skin_name = tk.Label(self._canvas, bg='light gray')
        self._chosen_skin_name.place(relheight=float(np.sum(self._rows_height[2:])),
                                     relwidth=self._columns_width[1],
                                     relx=self._columns_width[0],
                                     rely=float(np.sum(self._rows_height[:2])))

        # Required legal statement button
        rlgs_button_width = self._width*0.02
        tk.Button(self._root,
                  text="i",
                  font=("Helvetica", 15),
                  command=required_legal_statement).place(width=int(rlgs_button_width),
                                                          height=int(rlgs_button_width),
                                                          x=self._width,
                                                          anchor=tk.NE)
