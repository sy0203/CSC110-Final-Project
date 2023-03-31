"""This module is responsible for operating the user interface"""

# imports
import pygame
import sys
import graph_manager
import calc_helper as calc
from calc_helper import Country
import info_collection
import time, webbrowser, pyautogui


class Screen:
    """
    This is the screen class. It represents the different pages used.
    """

    def __init__(self, title: str, buttons: list, signal: str, operation: tuple):
        self.title = title
        self.buttons = buttons
        self.signal = signal
        self.operation, self.input = (0, 0)
        if len(operation) == 2:
            self.operation, self.input = operation

    def buttons_draw(self) -> None:
        """Draws the appropriate buttons for the screen"""
        for b in self.buttons:
            b.draw()

    def display_page(self) -> None:
        """This displays the page"""
        # Here the title of the window and the background are set
        pygame.display.set_caption(self.title)
        screen.fill('#b7a9d4')

        # Adding a title to the page. Since the menu is unique, there is a seperate condition for it.
        if self.title == 'Main Menu':
            self.draw_text("Covid Research", pygame.font.Font(None, 90), (22, 25, 26), screen, 60)
            self.draw_text('Selina Phadiya, Natasha Sharan, Seyoung Yoo', pygame.font.Font(None, 30),
                           (22, 25, 26), screen, 110)
        else:
            self.draw_text(self.title, pygame.font.Font(None, 90), (22, 25, 26), screen, 40)

        # This is responsible for the descriptions on the pages
        if self.operation != 0:
            self.operation(self.input)

        # Draws the buttons
        self.buttons_draw()

    def draw_text(self, text, font, color, surface, y) -> None:
        """A function that directly writes to the screen"""
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect(center=(screen.get_width() / 2, y))
        surface.blit(textobj, textrect)

    def draw_text_x(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def update_title(self, text: str) -> None:
        """This will update the title of the page"""
        self.title = text

    def update_function(self, operation: tuple) -> None:
        """This updates the description function if it is availible"""
        self.operation, self.input = (0, 0)
        if len(operation) == 2:
            self.operation, self.input = operation


class Button:
    """This class is responsible for creating buttons"""

    def __init__(self, text: str, font_size: int, width, height, y, elevation, signal: str):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = y
        self.signal = signal
        self.font_size = font_size
        pos = (self.get_x(text, width), y)

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'

        # text
        self.text = text
        self.text_surf = pygame.font.Font(None, self.font_size).render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def get_x(self, text: str, width: int) -> int:
        """This function will return the x value of text so it is in the middle"""
        if text == "Back":
            return 550
        return (screen.get_width() // 2) - (width // 2)

    def change_text(self, new_text: str) -> None:
        """This is a helper function for rendering """
        self.text_surf = pygame.font.Font(None, self.font_size).render(new_text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self) -> None:
        """This function draws the button"""
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self) -> None:
        """This function moniters how the mouse interacts with the button."""
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#d74b7c'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                self.change_text(f"{self.text}")
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed:
                    status[0] = self.signal  # this updates the status in the main loop
                    print(status)
                    self.pressed = False
                    self.change_text(self.text)
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'


def start_page(page: Screen, state: str, prev: Screen) -> None:
    """
    This will start up the page that is required.
    It has its own loop so that we can fork the path.
    """
    running = True
    vals = [page.buttons[x].signal for x in range(len(page.buttons)) if page.buttons[x].signal != 'back']

    while running:
        page.display_page()

        # checks for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # if the back button has been clicked, or a menu option
        if status[0] == 'back' or status[0] != state:
            running = False
            if prev != menu:
                if status[0] not in vals:
                    status[0] = prev.signal

        pygame.display.update()
        clock.tick(60)


def get_country_dict() -> dict[str, Country]:
    """Returns a dictionary mapping names to countries"""
    vals = info_collection.process_countries()
    return {country.name: country for country in vals}


def about_screen(_: int) -> None:
    """Descriptor function for 'about'"""
    pos = 120
    size = 33
    about.draw_text("COVID-19 crisis is not a financial or economic crisis; ",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos)
    about.draw_text("it is a health crisis which severely disrupted people’s lifestyles.",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos + size)
    about.draw_text("However, its impact on supply and demand chain has resulted in the",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos + size * 2)
    about.draw_text("pandemic turning into a large-scale financial and economical crisis.",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos + size * 3)
    about.draw_text("Recovery from economic recession during COVID-19 will be in progress",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos + size * 4)
    about.draw_text(" after restrictions are lifted. Our focus is on companies’ financial",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos + size * 5)
    about.draw_text("to their ability to continue their production of goods post-pandemic.",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos + size * 6)
    about.draw_text("Evaluating companies’ stocks is a reliable way to measure companies’",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos + size * 7)
    about.draw_text("financial stability and we are analyzing different countries’ benchmark",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos + size * 8)
    about.draw_text("index funds in this project.",
                    pygame.font.Font(None, size), (22, 25, 26), screen, pos + size * 9)
    about.draw_text('Selina Phadiya, Natasha Sharan, Seyoung Yoo', pygame.font.Font(None, size),
                    (22, 25, 26), screen, pos + size * 11)


def option_screen(_: int) -> None:
    """Descriptor function for 'the option screen'"""
    about.draw_text("Select any of the following graphs to view", pygame.font.Font(None, 30), (22, 25, 26), screen, 100)


def choro_stock_graph_description(_: int) -> None:
    """Descriptor for the choropleth map"""
    cs = list(countries_list.values())
    char_y = 250
    about.draw_text("This choropleth world map presents how many countries' index funds,",
                    pygame.font.Font(None, 30), (22, 25, 26), screen, 100)
    about.draw_text("recovered or exceeded their pre-pandemic closing price.",
                    pygame.font.Font(None, 30), (22, 25, 26), screen, 130)
    about.draw_text("Our research is focusing on the state of the following 5 countries.",
                    pygame.font.Font(None, 30), (22, 25, 26), screen, 170)
    about.draw_text("The chart below shows the the stock prices for each country at different periods.",
                    pygame.font.Font(None, 30), (22, 25, 26), screen, 200)

    about.draw_text_x('Country', pygame.font.Font(None, 30), (22, 25, 26), screen, 5, char_y)
    about.draw_text_x('Pre-Covid ', pygame.font.Font(None, 30), (22, 25, 26), screen, 163, char_y)
    about.draw_text_x('Lowest', pygame.font.Font(None, 30), (22, 25, 26), screen, 321, char_y)
    about.draw_text_x('Current', pygame.font.Font(None, 30), (22, 25, 26), screen, 479, char_y)
    about.draw_text_x('Recovery', pygame.font.Font(None, 30), (22, 25, 26), screen, 637, char_y)

    rows_y = char_y + 30
    for x in range(5):
        about.draw_text_x(cs[x].name, pygame.font.Font(None, 30), (22, 25, 26), screen, 5, rows_y + 30 * x)
        about.draw_text_x(str(cs[x].prices[0]), pygame.font.Font(None, 30), (22, 25, 26), screen, 163, rows_y + 30 * x)
        about.draw_text_x(str(min(cs[x].prices)), pygame.font.Font(None, 30), (22, 25, 26), screen, 321,
                          rows_y + 30 * x)
        about.draw_text_x(str(cs[x].prices[-1]), pygame.font.Font(None, 30), (22, 25, 26), screen, 479, rows_y + 30 * x)
        about.draw_text_x(str(cs[x].recovered), pygame.font.Font(None, 30), (22, 25, 26), screen, 637, rows_y + 30 * x)

    about.draw_text("In conclusion, all of the countries recovered or exceeded the initial stock price.",
                    pygame.font.Font(None, 30), (22, 25, 26), screen, 500)


def all_line_graphs(_: int) -> None:
    """Descriptor for the collective line graphs"""
    about.draw_text("This has a lot", pygame.font.Font(None, 30), (22, 25, 26), screen, 100)


def table_screen(_: int) -> None:
    """Descriptor for table screen"""
    about.draw_text("I am dying", pygame.font.Font(None, 30), (22, 25, 26), screen, 100)


def line_graph_single(country: Country) -> None:
    """Desctiptor for each country"""
    about.draw_text("This graph will display the change in stock prices over time.", pygame.font.Font(None, 30),
                    (22, 25, 26), screen, 100)


def sp_description(country: Country) -> None:
    """Desctiptor for each country"""
    about.draw_text("This graph will display the relation between the covid cases and the stock index funds.",
                    pygame.font.Font(None, 30),
                    (22, 25, 26), screen, 100)


# initializing pygame and other important things
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None, 30)

# creating buttons
menu_b1 = Button('Begin', 50, 300, 70, 200, 5, 'begin')  # menu buttons
menu_b2 = Button('About', 50, 300, 70, 310, 5, 'about')
menu_b3 = Button('Quit', 50, 300, 70, 420, 5, 'exit')

chlo_in_graphs = Button('Choropleth Index Graph', 50, 500, 50, 150, 5, 'choro ig')  # graph buttons
index_vs_time_graph = Button('Line Graph (All Countries): Stock vs Time', 50, 700, 50, 220, 5, 'index/time')
line_graph = Button('Line Graph: Stock vs Time', 50, 500, 50, 290, 5, 'countries lg')
scatterplot = Button('Scatterplot: Cases vs Stock', 50, 600, 50, 360, 5, 'countries sp')
table = Button('Table of Recovery', 50, 400, 50, 430, 5, 'table')

us = Button('United States', 50, 300, 50, 150, 5, 'us')  # country buttons
france = Button('France', 50, 300, 50, 220, 5, 'france')
india = Button('India', 50, 300, 50, 290, 5, 'india')
japan = Button('Japan', 50, 300, 50, 360, 5, 'japan')
brazil = Button('Brazil', 50, 300, 50, 430, 5, 'brazil')

general_b = Button('Back', 50, 200, 40, 530, 5, 'back')  # return button

# creating lists for readability
menu_buttons = [menu_b1, menu_b2, menu_b3]
graph_buttons = [chlo_in_graphs, index_vs_time_graph, line_graph, scatterplot, table, general_b]
countries = [us, france, india, japan, brazil, general_b]
status = ['']

# creating the screens
menu = Screen('Main Menu', menu_buttons, "menu", ())
about = Screen('About', [general_b], 'about', (about_screen, 0))
graphs = Screen('Options', graph_buttons, 'begin', (option_screen, 0))
general_graphs = Screen('Graph', [general_b], 'general graphs', ())
country_graphs_line = Screen('Countries', countries, 'countries lg', ())
country_graphs_scatter = Screen('Country', countries, 'countries sp', ())
country_page = Screen('Country', [general_b], 'country', ())

# relevant dictionaries for quick search
graph_funcs = {
    'choro ig': (choro_stock_graph_description, 0),
    'index/time': (all_line_graphs, 0),
    'table': (table_screen, 0),
    'countries lg': (),
    'countries sp': ()
}

stats_titles = {
    'us': 'United States',
    'india': 'India',
    'japan': 'Japan',
    'france': 'France',
    'brazil': 'Brazil'
}

countries_list = get_country_dict()
print(countries_list)

# main loop
while True:
    menu.display_page()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if status[0] == 'begin':
        while status[0] != 'back':
            start_page(graphs, 'begin', menu)

            if status[0] in graph_funcs:
                general_graphs.update_function(graph_funcs[status[0]])

            if status[0] == 'choro ig':
                webbrowser.open(graph_manager.choropleth_graph(list(countries_list.values())))
                start_page(general_graphs, 'choro ig', graphs)

            elif status[0] == 'index/time':
                graph_manager.line_graph_all_vs_time(list(countries_list.values()))
                start_page(general_graphs, 'index/time', graphs)

            elif status[0] == 'table':
                graph_manager.recovery_table(list(countries_list.values()))
                start_page(general_graphs, 'table', graphs)

            elif status[0] == 'countries lg':
                while status[0] != 'back' and status[0] != 'begin':
                    start_page(country_graphs_line, 'countries lg', graphs)

                    if status[0] in stats_titles:
                        country_page.update_title((stats_titles[status[0]]) + ' Statistics')
                        graph_manager.line_graph(countries_list[stats_titles[status[0]]])
                        country_page.update_function((line_graph_single, countries_list[stats_titles[status[0]]]))
                        state = status[0]
                        start_page(country_page, state, country_graphs_line)

                    """if status[0] == 'us':
                        graph_manager.line_graph(countries_list[stats_titles[status[0]]])
                        start_page(country_page, 'us', country_graphs_line)

                    elif status[0] == 'france':
                        graph_manager.line_graph(countries_list[stats_titles[status[0]]])
                        start_page(country_page, 'france', country_graphs_line)

                    elif status[0] == 'india':
                        graph_manager.line_graph(countries_list[stats_titles[status[0]]])
                        start_page(country_page, 'india', country_graphs_line)

                    elif status[0] == 'japan':
                        graph_manager.line_graph(countries_list[stats_titles[status[0]]])
                        start_page(country_page, 'japan', country_graphs_line)

                    elif status[0] == 'brazil':
                        graph_manager.line_graph(countries_list[stats_titles[status[0]]])
                        start_page(country_page, 'brazil', country_graphs_line)"""

            elif status[0] == 'countries sp':
                while status[0] != 'back' and status[0] != 'begin':
                    start_page(country_graphs_scatter, 'countries sp', graphs)
                    country_page.update_title("Covid Cases vs Stock")
                    if status[0] in stats_titles:
                        graph_manager.scatter_plot(countries_list[stats_titles[status[0]]])
                        state = status[0]
                        start_page(country_page, state, country_graphs_line)

                    """if status[0] == 'us':
                        print('us')
                        start_page(country_page, 'us', country_graphs_scatter)

                    elif status[0] == 'france':
                        print('france')
                        start_page(country_page, 'france', country_graphs_scatter)

                    elif status[0] == 'india':
                        print('india')
                        start_page(country_page, 'india', country_graphs_scatter)

                    elif status[0] == 'japan':
                        print('japan')
                        start_page(country_page, 'japan', country_graphs_scatter)

                    elif status[0] == 'brazil':
                        print('brazil')
                        start_page(country_page, 'brazil', country_graphs_scatter)"""

    elif status[0] == 'about':
        start_page(about, 'about', menu)

    elif status[0] == 'exit':
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(60)
