from settings import *
import pygame

class Instrument:
    def __init__(self, asset_path: str, size: int, type):
        self.size = size
        self.asset = pygame.image.load(asset_path)
        self.asset = pygame.transform.scale(self.asset, (size, size))
        self.pos = (0, 0)
        self.type = type

    def draw(self, menu):
        menu.menu.blit(self.asset, self.pos)

class Menu:
    def __init__(self, screen: pygame.Surface, instruments):
        self.screen = screen
        self.w = menu_size[0]
        self.h = menu_size[1]
        self.menu = pygame.Surface((self.w, self.h))
        self.menu.fill(menu_color)

        # instruments
        self.index_of_choosing_instrument = None
        self.index_of_choosed_instrument = None

        self.instruments = instruments
        center = self.w//2, self.h//2
        size = self.instruments[0].asset.get_size()[0]
        for i in range(len(self.instruments)):
            self.instruments[i].pos = (center[0]-instrument_size//2, center[1]+i*size*1.5-instrument_size//2)
            self.instruments[i].draw(self)

    def draw(self, x: int = 0, y: int = 0):
        self.menu.fill(menu_color)

        if self.index_of_choosing_instrument != None:
            pygame.draw.rect(self.menu, choosing_color, (self.instruments[self.index_of_choosing_instrument].pos[0], self.instruments[self.index_of_choosing_instrument].pos[1], instrument_size, instrument_size), instrument_size, 3)

        if self.index_of_choosed_instrument != None:
            pygame.draw.rect(self.menu, choosing_color, (self.instruments[self.index_of_choosed_instrument].pos[0], self.instruments[self.index_of_choosed_instrument].pos[1], instrument_size, instrument_size), instrument_size, 3)
            pygame.draw.rect(self.menu, choosed_color, (self.instruments[self.index_of_choosed_instrument].pos[0], self.instruments[self.index_of_choosed_instrument].pos[1], instrument_size, instrument_size), 2, 3)

        for instrument in self.instruments:
            instrument.draw(self)

        self.screen.blit(self.menu, (x, y))

    @property
    def get_choosed(self):
        if self.index_of_choosed_instrument == None:
            return '-'
        return self.instruments[self.index_of_choosed_instrument].type

    # actions
    def mouse_on_instrument(self, xm: int, ym: int):
        self.index_of_choosing_instrument = None
        for index, instrument in enumerate(self.instruments):
            if xm > instrument.pos[0] and xm < instrument.pos[0]+instrument_size and ym > instrument.pos[1] and ym < instrument.pos[1]+instrument_size:
                self.index_of_choosing_instrument = index

    def choose_instrument(self, xm: int, ym: int):
        for index, instrument in enumerate(self.instruments):
            if xm > instrument.pos[0] and xm < instrument.pos[0]+instrument_size and ym > instrument.pos[1] and ym < instrument.pos[1]+instrument_size:
                self.index_of_choosed_instrument = index

# prebuild instruments
class Pen(Instrument):
    def __init__(self, asset_path, size, type):
        super().__init__(asset_path, size, type)
        self.positions = []

    def add_start_point(self, xm: int, ym: int):
        self.positions.append((xm, ym))

    def add(self, xm: int, ym: int):
        self.positions.append((xm, ym))
        self.positions = self.positions[-2:]

    def draw_pen(self, canvas):
        #start = time.time()
        canvas.draw_line(*self.positions[0], *self.positions[1])
        #end = time.time()
        #pygame.draw.line(canvas, 'black', self.positions[0], self.positions[1])
        #return end - start


class Fill(Instrument):
    def __init__(self, asset_path, size, type):
        super().__init__(asset_path, size, type)


    def fill(self, canvas, seed_position):
        '''queue = deque([seed_position])
        white = pygame.Color(255, 255, 255)
        black = pygame.Color(0, 0, 0)
        while queue:
            x, y = queue.popleft()
            if canvas.canvas.get_at((x, y)) != white:
                continue

            canvas.canvas.set_at((x, y), black)
            if x > 0:
                queue.append((x - 1, y))
            if x < canvas.w - 1:
                queue.append((x + 1, y))
            if y > 0:
                queue.append((x, y - 1))
            if y < canvas.h - 1:
                queue.append((x, y + 1))'''
                #start = time.time()
        #start = time.time()
        canvas.fill(seed_position)
        #end = time.time()
        canvas.canvas = pygame.surfarray.make_surface(canvas.canvas_np)
        #return end - start

class Slider:
    def __init__(self, x, y, height, min_val, max_val, initial_val, color=(100, 100, 100), handle_color=(150, 150, 150), handle_radius=5):
        self.x = x
        self.y = y
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.color = color
        self.handle_color = handle_color
        self.handle_radius = handle_radius
        self.is_dragging = False

    def _calculate_handle_position(self):
        value_range = self.max_val - self.min_val
        if value_range == 0:
            pos = self.y + self.height // 2
        else:
            value_percent = (self.value - self.min_val) / value_range
            pos = self.y + self.height - int(value_percent * self.height)
        return pos
    
    def _clamp_value(self, value):
        return max(self.min_val, min(value, self.max_val))

    def calc(self):
        if self.is_dragging:
            mouse_y = pygame.mouse.get_pos()[1]
            value_percent = 1 - (mouse_y - self.y) / self.height
            self.value = self._clamp_value(self.min_val + (self.max_val - self.min_val) * value_percent)

    def draw(self, surf: pygame.Surface):
        pygame.draw.line(surf, self.color, (self.x, self.y), (self.x, self.y+self.height), 5)
        handle_pos = self._calculate_handle_position()
        pygame.draw.circle(surf, self.handle_color, (self.x, handle_pos), self.handle_radius)

    @property
    def get_value(self):
        return self.value

class Eraser(Instrument):
    def __init__(self, asset_path, size, type, radius = 5):
        super().__init__(asset_path, size, type)
        self.slider = Slider(10+12, 375+40, 100, 5, 100, 5, choosed_color, (255, 255, 255))
        self.radius = radius

    def draw(self, menu: Menu):
        menu.menu.blit(self.asset, self.pos)
        if menu.get_choosed == 'erase': 
            self.slider.draw(menu.menu)

    def erase_field(self, screen, pos):
        self.radius = int(self.slider.get_value)
        pygame.draw.circle(screen, eraser_color, pos, self.radius, 2)

    def erase(self, canvas, pos):
        canvas.draw_circle(*pos, self.radius)
        #pygame.draw.circle(canvas.canvas, (255, 255, 255), pos, self.radius, self.radius)

pen = Pen(path_pen, instrument_size, 'pen')
fill = Fill(path_fill, instrument_size, 'fill')
eraser = Eraser(path_eraser, instrument_size, 'erase')
instruments_list = [pen, fill, eraser]