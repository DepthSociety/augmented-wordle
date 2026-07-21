import pygame
pygame.init()

import random
from datetime import datetime
import re

# Các tham số kích thước/tọa độ của màn hình screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Màu sắc được sử dụng
FRAME_NOT_CLICKED = "#a7a7a7" # Màu của khung của ô chữ Wordle khi chưa được chọn và chưa có chữ ở trong
GREEN = "#538d4e"
YELLOW = "#b59f3b"
WORDLE_GREY = "#3a3a3c" # Màu xám dùng để tô ô chữ Wordle khi chữ của ô không có trong đáp án
BUTTON_NO_MOUSE = "#d3d6da" # Màu của các nút (Button) khi chưa di chuột vào nút
BUTTON_MOUSE = "#a6a8ad" # Màu của các nút (Button) khi di chuột vào nút

# Các tham số kích thước/tọa độ của các ô của một Rank (Xếp hạng)
# Trong đó, các ô của Rank bao gồm: Top (thứ hạng), User (tên người dùng), Score (điểm cao nhất của người dùng)
TOP_WIDTH = 60
USER_WIDTH = 700
SCORE_WIDTH = 150
RANKBOX_GAP = 7
RANKBOX_WIDTH = TOP_WIDTH + USER_WIDTH + SCORE_WIDTH + 2 * RANKBOX_GAP
RANKBOX_HEIGHT = 40
TOP_CENTER_X = (SCREEN_WIDTH - RANKBOX_WIDTH) // 2 + TOP_WIDTH // 2 + 20
USER_CENTER_X = TOP_CENTER_X + TOP_WIDTH // 2 + RANKBOX_GAP + USER_WIDTH // 2
SCORE_CENTER_X = USER_CENTER_X + USER_WIDTH // 2 + RANKBOX_GAP + SCORE_WIDTH // 2

# Các tham số kích thước/tọa độ của các ô của một RoundBar (Thanh chỉ lịch sử)
# Trong đó, các ô của RoundBar bao gồm: Top (thứ tự), Mode (chế độ chơi), Answer (đáp án), Date (ngày giờ chơi)
ORDER_WIDTH = 70
MODE_WIDTH = 190
ANSWER_WIDTH = 170
STATUS_WIDTH = 170
DATE_WIDTH = 300
ROUNDBAR_GAP = 6
ROUNDBAR_WIDTH = ORDER_WIDTH + MODE_WIDTH + ANSWER_WIDTH + STATUS_WIDTH + DATE_WIDTH + 4 * ROUNDBAR_GAP
ROUNDBAR_HEIGHT = 40
ORDER_CENTER_X = (SCREEN_WIDTH - ROUNDBAR_WIDTH) // 2 + ORDER_WIDTH // 2 + 20
MODE_CENTER_X = ORDER_CENTER_X + ORDER_WIDTH // 2 + ROUNDBAR_GAP + MODE_WIDTH // 2
ANSWER_CENTER_X = MODE_CENTER_X + MODE_WIDTH // 2 + ROUNDBAR_GAP + ANSWER_WIDTH // 2
STATUS_CENTER_X = ANSWER_CENTER_X + ANSWER_WIDTH // 2 + ROUNDBAR_GAP + STATUS_WIDTH // 2
DATE_CENTER_X = STATUS_CENTER_X + STATUS_WIDTH // 2 + ROUNDBAR_GAP + DATE_WIDTH // 2

# Danh sách của các loại kí tự được chấp nhận, gồm: chữ số, chữ cái và một số kí tự đặc biệt


# Ngân hàng các từ/biểu thức được chấp nhận

def load_wordbank(directory):
    words = None
    with open(directory, "r", encoding = "utf-8") as file:
        words = file.readlines()
    for i in range(len(words)):
        if ("\n" in words[i]):
            words[i] = words[i][:-1]
            # eng_words[i] = eng_words[i].upper()
    return words

eng_words = load_wordbank("words/eng.txt")
vie_words = load_wordbank("words/vie.txt")
vie_org = load_wordbank("words/vie_org.txt")
math_eqs = load_wordbank("words/math.txt")

math_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "="]

usernames = []
passwords = []

def load_accounts():
    user_list = None
    with open("users.txt", "r") as file:
        user_list = file.readlines()
    for i in range(len(user_list)):
        if "\n" in user_list[i]: user_list[i] = user_list[i][:-1]
        username, password = user_list[i].split("|")
        usernames.append(username)
        passwords.append(password)
    user_list[i] = (username, password)

user_list = load_accounts()

background = pygame.image.load("background.jpg")

def get_font(size: int = 40):
    """
    Hàm trả về phông chữ trong pygame (pygame.font.Font) với font tiêu chuẩn là font/Montserrat-Bold.ttf. Trong đó:
        size (int): Kích thước của phông chữ
    """
    return pygame.font.Font("font/Montserrat-Bold.ttf", size)

def left_mouse_click(event):
    return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)

def is_equation(expr):
    # 1. Kiểm tra ký tự lạ và dấu ngoặc
    # Chỉ cho phép: 0-9, +, -, *, /, =
    # Nếu chứa ( hoặc ) lập tức trả về False
    for char in expr:
        if (char not in math_chars):
            return False

    # 2. Kiểm tra dấu bằng (=)
    # Bắt buộc phải có đúng 1 dấu bằng
    if expr.count('=') != 1:
        return False
    
    # 3. Kiểm tra sự tồn tại của toán tử
    # Phải có ít nhất một trong 4 dấu + - * /
    if not any(op in expr for op in ['+', '-', '*', '/']):
        return False

    # 4. Kiểm tra toán tử liên tiếp và vị trí toán tử
    # Không cho phép 2 toán tử đứng cạnh nhau (vd: ++, +-, *-, /+)
    if re.search(r"[+\-*/]{2,}", expr):
        return False
    
    # Tách vế trái và vế phải
    parts = expr.split('=')
    lhs = parts[0] # Vế trái
    rhs = parts[1] # Vế phải

    # Kiểm tra vế rỗng (trường hợp "=5" hoặc "5=")
    if not lhs or not rhs:
        return False

    # Kiểm tra toán tử ở đầu hoặc cuối mỗi vế (vd: *5=... hoặc ...= /5)
    # Regex này kiểm tra nếu ký tự đầu hoặc cuối của chuỗi là toán tử
    if lhs[0] in "+-*/" or lhs[-1] in "+-*/" or rhs[0] in "+-*/" or rhs[-1] in "+-*/":
        return False

    # 5. Tính toán và so sánh
    try:
        val_lhs = eval(lhs)
        val_rhs = eval(rhs)
        
        # Kiểm tra tính đúng đắn toán học (Vế trái == Vế phải)
        # Lưu ý: eval có thể trả về float (vd: 5/2 = 2.5). 
        # So sánh sai số nhỏ để đảm bảo chính xác với số thực.
        return abs(val_lhs - val_rhs) < 1e-9
        
    except ZeroDivisionError:
        return False # Loại bỏ trường hợp chia cho 0
    except Exception:
        return False
    
def is_english_word(word = "HELLO"):
    return word in eng_words

def is_viet_word(word = "ANHEM"):
    return word in vie_words

def sort_func(rank: tuple):
    return rank[1]

def compare(guess, answer):
    while (len(guess) < len(answer)): guess += " "
    state = [0] * len(guess)
    guess_letters = []
    guess_letter_count = []
    answer_letters = []
    answer_letter_count = []

    for letter in answer:
        if (letter not in answer_letters):
            answer_letters.append(letter)
            answer_letter_count.append(0)

    for i in range(len(answer_letters)):
        for letter in answer:
            if (letter == answer_letters[i]):
                answer_letter_count[i] += 1
    
    for letter in guess:
        if (letter not in guess_letters):
            guess_letters.append(letter)
            guess_letter_count.append(0)
    # print(guess, answer)
    for i in range(len(guess)):
        if (guess[i] == answer[i]):
            state[i] = GREEN
            index = 0
            for j in range(len(guess_letters)):
                if (guess_letters[j] == guess[i]):
                    index = j
                    break
            guess_letter_count[index] += 1
            # print(state[i])

    for i in range(len(guess)):
        if (guess[i] in answer and guess[i] != answer[i]):
            index_guess = 0
            for j in range(len(guess_letters)):
                if (guess_letters[j] == guess[i]):
                    index_guess = j
                    break
            
            index_answer = 0
            for j in range(len(answer_letters)):
                if (answer_letters[j] == guess[i]):
                    index_answer = j
                    break
            
            if (guess_letter_count[index_guess] < answer_letter_count[index_answer]):
                guess_letter_count[index_guess] += 1
                state[i] = YELLOW
            else:
                state[i] = WORDLE_GREY
        elif (guess[i] not in answer):
            state[i] = WORDLE_GREY
        # print(state)
    for i in range(len(guess)):
        if (guess[i] == " "): state[i] = "white"
    return state


class Box:

    """
    Lớp Box tạo một ô hình chữ nhật chứa văn bản trong pygame bao gồm nền của ô, khung của ô, và văn bản (nếu có). Trong đó:
        center_x, center_y (int): Tọa độ trung tâm của Box lần lượt theo chiều x và chiều y
        width, height (int): Chiều rộng và chiều dài của Box
        text (str): Văn bản nằm trong Box, mặc định là ""
        align_text (str): Trục căn chỉnh của text, nếu align_text = "left" thì văn bản căn lề trái, "mid" thì văn bản căn lề giữa (mặc định align_text = "mid")
        left, top, right, bottom (int): Lần lượt là tận cùng bên trái, bên trên, bên phải, bên dưới của Box

        surf (pygame.Surface): pygame.Surface tương ứng của Box
        rect (pygame.Rect): pygame.Rect tương ứng của Box
        color (str): Màu nền của Box
        frame_color (str): Màu khung của Box
    """

    def __init__(self, center_x = 0, center_y = 0, width = 0, height = 0, text = "", align_text = "mid"):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.align_text = align_text
        self.left = center_x - width // 2
        self.top = center_y - height // 2
        self.right = center_x + width // 2
        self.bottom = center_y + height // 2

        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect(center = (center_x, center_y))
        self.color = "white"
        self.frame_color = "black"
        
        self.font = get_font(min(self.width, self.height) * 2 // 3)
        self.text_color = "black"
        self.text_surf = self.font.render(self.text, True, self.text_color)

        font_size = min(self.width, self.height) * 2 // 3
        if self.text_surf.get_rect(topleft = (0, 0)).width > self.width:
            while self.text_surf.get_rect(topleft = (0, 0)).width * 3 > 2 * self.width:
                font_size -= 1
                self.font = get_font(font_size)
                self.text_surf = self.font.render(self.text, True, self.text_color)

        self.text_rect = None
        if (self.align_text == "left"):
            self.text_rect = self.text_surf.get_rect(midleft = (self.left + 7, self.center_y))
        else:
            self.text_rect = self.text_surf.get_rect(center = (center_x, center_y))

        self.draw_frame = True
        self.draw_back = True

    def update_text(self, text = "", color = "black"):
        self.text = text
        self.text_color = color
        self.text_surf = self.font.render(self.text, True, self.text_color).convert_alpha()
        self.text_rect = None
        if (self.align_text == "left"):
            self.text_rect = self.text_surf.get_rect(midleft = (self.left + 7, self.center_y))
        else:
            self.text_rect = self.text_surf.get_rect(center = (self.center_x, self.center_y))

    def mouse_collides(self):
        if (self.rect.collidepoint(pygame.mouse.get_pos())):
            return True
        return False

    def draw(self, screen):
        if (self.draw_back):
            pygame.draw.rect(screen, self.color, self.rect)

        if (self.draw_frame):
            pygame.draw.rect(screen, self.frame_color, self.rect, 2)
        
        screen.blit(self.text_surf, self.text_rect)

class TextBox:
    def __init__(self, text = "Text", size = 40, color = 'black', back_color = BUTTON_NO_MOUSE, center_x = 0, center_y = 0, left = -1, right = -1, curve = True):
        self.text = text
        self.size = size
        self.color = color
        self.back_color = back_color
        self.center_x = center_x
        self.center_y = center_y
        self.left = left
        self.right = right

        self.font = get_font(self.size)
        self.font_surf = self.font.render(text, True, color).convert_alpha()
        self.font_rect = self.font_surf.get_rect(center = (center_x, center_y))

        self.curve = curve

        if (self.left != -1):
            self.center_x = self.left + self.font_rect.width // 2
            self.font_rect = self.font_surf.get_rect(center = (self.center_x, self.center_y))
        elif (self.right != -1):
            self.center_x = self.right - self.font_rect.width // 2
            self.font_rect = self.font_surf.get_rect(center = (self.center_x, self.center_y))
        
        self.left = self.center_x - self.font_rect.width // 2
        self.right = self.center_x + self.font_rect.width // 2

        self.back_surf = pygame.Surface((self.font_rect.w + self.font_rect.h // 2, 3 * self.font_rect.h // 2))
        self.back_rect = self.back_surf.get_rect(center = (self.center_x, self.center_y))

        self.width = self.back_rect.w
        self.height = self.back_rect.h

    def draw(self, screen):
        pygame.draw.rect(screen, self.back_color, self.back_rect, 0, 5 if self.curve else 0)
        screen.blit(self.font_surf, self.font_rect)

    def update_text(self, text):
        self.__init__(text, self.size, self.color, self.back_color, self.center_x, self.center_y, self.left, self.right, self.curve)

    def change_color(self, color, back_color):
        self.__init__(self.text, self.size, color, back_color, self.center_x, self.center_y, self.left, self.right, self.curve)

    def mouse_collides(self):
        return self.back_rect.collidepoint(pygame.mouse.get_pos())

class BackButton:

    """
    Lớp BackButton tạo nút quay về màn hình trước đó của màn hình hiện tại. Trong đó:
        box (Box): Box tương ứng của BackButton (một ô hình chữ nhật có nền, khung, và văn bản)
    """

    def __init__(self):
        """
        Khởi tạo lớp, mặc định lớp có tọa độ trung tâm là (80, 45), kích thước là 45 x 45
        """
        self.box = Box(80, 45, 45, 45, "<")
        self.active = True

    def draw(self, screen):
        """
        Vẽ nút BackButton lên màn hình screen.
        """
        if (self.box.mouse_collides() and self.active):
            self.box.color = BUTTON_MOUSE
        else:
            self.box.color = BUTTON_NO_MOUSE
        
        self.box.draw(screen)

    def mouse_collides(self):
        return self.box.mouse_collides()

    def is_clicked(self, event):
        if left_mouse_click(event):
            return self.mouse_collides() and self.active

class Exit:
    def __init__(self, right, top):
        self.right = right
        self.top = top
        self.box = Box(right - 25, top + 25, 50, 50, "X")
        self.box.draw_frame = False

    def draw(self, screen):
        if (self.box.mouse_collides()):
            self.box.color = BUTTON_MOUSE
        else:
            self.box.color = "white"
        
        self.box.draw(screen)

    def mouse_collides(self):
        return self.box.mouse_collides()

class WordleLine:
    def __init__(self, center_x, center_y, word = "", answer = "", width = 60):
        self.center_x = center_x
        self.center_y = center_y
        self.size = len(answer)
        self.word = word
        self.answer = answer
        self.cur = 0
        self.entered = False
        self.active = False

        self.boxes = []
        for i in range(self.size):
            if (self.size & 1):
                self.boxes.append(Box(self.center_x + (i - self.size // 2) * (width + 6), self.center_y, width, width))
            else:
                if (i < self.size // 2):
                    self.boxes.append(Box(self.center_x - (6 // 2 + width // 2) + (i - self.size // 2 + 1) * (width + 6), self.center_y, width, width)) # box.center_x = center_x - (gap // 2 + w // 2) + (i - ) * (gap + w)
                    # print(self.center_x - (6 // 2 + width // 2) + (i - self.size // 2 + 1) * (width + 6), self.center_y)
                else:
                    self.boxes.append(Box(self.center_x + (6 // 2 + width // 2) + (i - self.size // 2) * (width + 6), self.center_y, width, width))
                    # print(self.center_x + (6 // 2 + width // 2) + (i - self.size // 2) * (width + 6))
    
    def mouse_collides(self):
        for i in range(self.size):
            if (self.boxes[i].mouse_collides()):
                return True
        return False
    
    # def update_box(self, )
    
    def update_line(self, word, entered = True):
        self.word = word
        # for i in range(self.size):
            # self.boxes[i].update_text()
        self.entered = entered
        for i in range(self.size):
            if (i >= len(self.word) or len(self.word) == 0):
                self.boxes[i].update_text(text = "")
            else:
                self.boxes[i].update_text(text = word[i])
        self.cur = len(word)

    def add_char(self, char):
        if (not self.entered) and self.active:
            if (self.cur < self.size):
                self.word += char
                self.boxes[self.cur].update_text(text = char)
                self.cur += 1
                # print(self.boxes[self.cur - 1].text)
        # print(self.word)
                # for i in range(self.size):
                    # print(self.boxes[i].text)

    # def state(self):
        # if len(self.word) < len(self.answer):
            # return "short"
        # elif 
    
    def backspace(self):
        if (not self.entered) and self.active:
            if (self.cur > 0):
                self.cur -= 1
                self.boxes[self.cur].update_text(text = "")
                self.word = self.word[:-1]

    def draw(self, screen):
        if (self.entered):
            # print("ENTERED")
            colors = compare(self.word, self.answer)
            # print(colors)
            for i in range(self.size):
                self.boxes[i].update_text(text = self.boxes[i].text, color = "white")
                self.boxes[i].color = colors[i]
                self.boxes[i].frame_color = "black"
                self.boxes[i].draw(screen)
        else:
            for i in range(self.size):
                self.boxes[i].update_text(text = self.boxes[i].text, color = "black")
                self.boxes[i].color = "white"
                if (i >= self.cur):
                    self.boxes[i].frame_color = FRAME_NOT_CLICKED
                else:
                    self.boxes[i].frame_color = "black" if self.active else FRAME_NOT_CLICKED
                self.boxes[i].draw(screen)

class Grid:
    def __init__(self, center_x, center_y, answer, width = 60):
        self.num_lines = 6
        self.center_x = center_x
        self.center_y = center_y
        self.answer = answer
        self.cur_line = 0
        self.lines = []

        for i in range(self.num_lines):
            if i < self.num_lines // 2:
                self.lines.append(WordleLine(self.center_x, self.center_y - (10 // 2 + width // 2) + (i - self.num_lines // 2 + 1) * (width + 10), "", answer, width))
                # print(self.center_x, self.center_y - (10 // 2 + width // 2) + (i - self.num_lines // 2 + 1) * (width + 10))
            else:
                self.lines.append(WordleLine(self.center_x, self.center_y + (10 // 2 + width // 2) + (i - self.num_lines // 2) * (width + 10), "", answer, width)) 
                # print(self.center_x, self.center_y - (10 // 2 + width // 2) + (i - self.num_lines // 2) * (width + 10))
    
    def mouse_collides(self):
        for i in range(self.num_lines):
            if (self.lines[i].mouse_collides()):
                return True
        return False

    def draw(self, screen):
        for i in range(self.num_lines):
            self.lines[i].draw(screen)

class Manager:
    def __init__(self):
        self.state = "login"
        self.username = ""
        self.login = LoginScene(self)
        self.start = StartScene(self)
        self.game = GameScene(self)
        self.history = HistoryScene(self)
        self.leaderboard = LeaderboardScene(self)
        
    
    def run(self, screen, events):
        if (self.state == "login"):
            self.login.run(screen, events)
        elif (self.state == "start"):
            self.start.run(screen, events)
        elif (self.state == "game"):
            self.game.run(screen, events)
        elif (self.state == "leaderboard"):
            self.leaderboard.run(screen, events)
        elif (self.state == "history"):
            self.history.run(screen, events)

class LoginScene:

    class UserBox:
        def __init__(self, center_y):
            self.type_box = Box(SCREEN_WIDTH // 2, center_y, 415, 30, "Username", align_text = "left")
            self.type_box.draw_frame = False

            self.inp_box = Box(SCREEN_WIDTH // 2, center_y + self.type_box.height // 2 + 15, 400, 30, align_text = "left")

            self.warning = Box(SCREEN_CENTER_X, self.inp_box.center_y + self.inp_box.height // 2 + 10, 415, 20, align_text = "left")
            self.warning.draw_frame = False
            self.warning.update_text(self.warning.text, color = "red")

            self.text = ""
            self.active = False

        def empty(self):
            return len(self.inp_box.text) == 0

        def update_warning(self):
            new_warning = ""
            if (len(self.text) > 20):
                new_warning = "Username must not have more than 20 characters"
            else:
                for char in self.text:
                    # print(char, char.isalpha, )
                    if (char.isalpha() == False) and (char.isnumeric() == False):
                        # print(char)
                        new_warning = "Username must only have numbers and/or English letters"
                        break
            
            if (new_warning != self.warning.text):
                self.warning.update_text(new_warning, color = "red")

        def draw(self, screen):
            self.update_warning()
            # print(self.warning.text)
            if (self.active):
                self.inp_box.frame_color = "black"
            else:
                self.inp_box.frame_color = FRAME_NOT_CLICKED

            self.type_box.draw(screen)
            self.inp_box.draw(screen)
            self.warning.draw(screen)
        
        def handle_event(self, event):
            # print(self.text)
            self.update_warning()
            # active = self.is_clicked(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.inp_box.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if (event.type == pygame.KEYDOWN):
                if (self.active):
                    if (event.unicode and event.unicode.isprintable()):
                        self.inp_box.text += event.unicode
                        self.text += event.unicode
                        self.inp_box.update_text(self.inp_box.text)
                    elif (event.key == pygame.K_BACKSPACE):
                        self.inp_box.text = self.inp_box.text[:-1]
                        self.text = self.text[:-1]
                        self.inp_box.update_text(self.inp_box.text)

    class PassBox:
        def __init__(self, center_y):
            self.type_box = Box(SCREEN_WIDTH // 2, center_y, 415, 30, "Password", align_text = "left")
            self.type_box.draw_frame = False

            self.inp_box = Box(SCREEN_WIDTH // 2, center_y + self.type_box.height // 2 + 15, 400, 30, align_text = "left")

            self.warning = Box(SCREEN_CENTER_X, self.inp_box.center_y + self.inp_box.height // 2 + 10, 415, 20, align_text = "left")
            self.warning.draw_frame = False
            self.warning.update_text(self.warning.text, color = "red")

            self.text = ""
            self.active = False

        def empty(self):
            return len(self.inp_box.text) == 0

        def update_warning(self):
            new_warning = ""
            if (len(self.text) > 20):
                new_warning = "Password must not have more than 20 characters"
            else:
                for char in self.text:
                    if char.isalpha() == False and char.isnumeric() == False:
                        new_warning = "Password must only have numbers and/or English letters"
                        break
            
            if (new_warning != self.warning.text):
                self.warning.update_text(new_warning, color = "red")

        def draw(self, screen):
            self.update_warning()
            if (self.active):
                self.inp_box.frame_color = "black"
            else:
                self.inp_box.frame_color = FRAME_NOT_CLICKED

            self.type_box.draw(screen)
            self.inp_box.draw(screen)
            self.warning.draw(screen)
        
        def handle_event(self, event):
            # active = self.is_clicked(event)
            # print(self.text)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.inp_box.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if (event.type == pygame.KEYDOWN):
                if (self.active):
                    if (event.unicode and event.unicode.isprintable()):
                        self.inp_box.text += "*"
                        self.text += event.unicode
                        self.inp_box.update_text(self.inp_box.text)
                    elif (event.key == pygame.K_BACKSPACE):
                        self.inp_box.text = self.inp_box.text[:-1]
                        self.text = self.text[:-1]
                        self.inp_box.update_text(self.inp_box.text)

    def __init__(self, manager):
        self.manager = manager
        self.frame = Box(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 550, 350)
        
        self.user_box = self.UserBox(270)
        self.pass_box = self.PassBox(270 + 100)

        self.login = Box(SCREEN_CENTER_X - 10 - 190 // 2, SCREEN_CENTER_Y + 120, 190, 30, "Login")
        self.login.color = BUTTON_NO_MOUSE

        self.register = Box(SCREEN_CENTER_X + 10 + 190 // 2, SCREEN_CENTER_Y + 120, 190, 30, "Register")
        self.register.color = BUTTON_NO_MOUSE
        # self.exit = self.Exit()

        self.error = Box(SCREEN_CENTER_X, SCREEN_CENTER_Y + 85, 500, 25)
        self.error.draw_frame = False
        self.error.text_color = "red"

        # self.username_text = Box()

    def draw(self, screen):
        self.frame.draw(screen)
        self.user_box.draw(screen)
        self.pass_box.draw(screen)

        self.login.color = BUTTON_MOUSE if self.login.mouse_collides() else BUTTON_NO_MOUSE
        self.register.color = BUTTON_MOUSE if self.register.mouse_collides() else BUTTON_NO_MOUSE

        self.login.draw(screen)
        self.register.draw(screen)
        self.error.draw(screen)
    
    def handle_register(self):
        username = self.user_box.text
        password = self.pass_box.text

        if not username:
            self.error.update_text("Username is missing", color = "red")
        elif not password:
            self.error.update_text("Password is missing", color = "red")
        else:
            if username not in usernames:
                if self.pass_box.warning.text == "" and self.user_box.warning.text == "":
                    usernames.append(username)
                    passwords.append(password)
                    with open("users.txt", "a") as file:
                        file.write(f"{username}|{password}\n")
                    self.error.update_text("Registration succeed", color = GREEN)
                elif self.user_box.warning.text:
                    self.error.update_text("Invalid username", color = "red")
                else:
                    self.error.update_text("Invalid password", color = "red")
            else:
                print(username)
                self.error.update_text("Username already exists", color = "red")

    def handle_login(self):
        username = self.user_box.text
        password = self.pass_box.text

        if not username:
            self.error.update_text("Username is missing", color = "red")
        elif not password:
            self.error.update_text("Password is missing", color = "red")
        else:
            if username not in usernames:
                self.error.update_text("Account does not exist", color = "red")
            else:
                index = usernames.index(username)
                if (password != passwords[index]):
                    self.error.update_text("Wrong password", color = "red")
                else:
                    self.manager.state = "start"
                    self.manager.username = username
                    print(f"username: {username}")
                    self.__init__(self.manager)

    def run(self, screen, events):
        # screen.fill("white")
        screen.blit(background, background.get_rect(center = (SCREEN_CENTER_X, SCREEN_CENTER_Y)))

        for event in events:
            self.user_box.handle_event(event)
            self.pass_box.handle_event(event)

            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_RETURN):
                    self.handle_login()

            if left_mouse_click(event):
                if (self.login.mouse_collides()):
                    self.handle_login()
                elif (self.register.mouse_collides()):
                    self.handle_register()

        self.draw(screen)

class StartScene:

    class Button:
        def __init__(self, center_x, center_y, text = "", size = 40):
            self.center_x = center_x
            self.center_y = center_y

            self.text = text
            self.font = get_font(size)
            self.text_surf = self.font.render(self.text, True, "black")
            self.text_rect = self.text_surf.get_rect(center = (center_x, center_y))
            
            self.rect = pygame.Rect(self.text_rect.x - 5, self.text_rect.y, self.text_rect.w + 10, self.text_rect.h)
            self.width = self.rect.w
            self.height = self.rect.h
            self.left = self.rect.x
            self.top = self.rect.y
            self.active = True
            # self.mouse_here = False

        def draw(self, screen):
            if (self.active):
                mouse_here = self.rect.collidepoint(pygame.mouse.get_pos())
                rect_color = "white"
                text_color = "black"
                if (mouse_here):
                    rect_color, text_color = "#538d4e", "white"
            else:
                rect_color = "white"
                text_color = WORDLE_GREY

            self.text_surf = self.font.render(self.text, True, text_color)
            self.text_rect = self.text_surf.get_rect(center = (self.center_x, self.center_y))

            pygame.draw.rect(screen, rect_color, self.rect)
            screen.blit(self.text_surf, self.text_rect)


    def __init__(self, manager):
        self.manager = manager

        self.new_game = self.Button(SCREEN_WIDTH // 2, 200, "NEW GAME")
        self.resume = self.Button(SCREEN_WIDTH // 2, self.new_game.center_y + self.new_game.height // 2 + 60, "RESUME")
        self.ranking = self.Button(SCREEN_WIDTH // 2, self.resume.center_y + self.resume.height // 2 + 60, "LEADERBOARD")
        self.history = self.Button(SCREEN_WIDTH // 2, self.ranking.center_y + self.ranking.height // 2 + 60, "HISTORY")
        self.log_out = self.Button(SCREEN_WIDTH // 2, self.history.center_y + self.history.height // 2 + 60, "LOG OUT")

    def check_resume(self):
        """Kiểm tra xem user hiện tại có game nào để resume không"""
        has_save = False
        try:
            with open("round.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                # Duyệt ngược để tìm game mới nhất
                for line in reversed(lines):
                    data = line.strip().split("|")
                    # Kiểm tra đúng username và định dạng
                    if len(data) >= 7 and data[0] == self.manager.username:
                        # [TÙY CHỌN] Nếu bạn CHỈ muốn resume game chưa xong thì thêm:
                        # if data[5] == "NotDone":
                        has_save = True
                        break
        except FileNotFoundError:
            has_save = False
        
        # Cập nhật trạng thái cho nút Resume
        self.resume.active = has_save

    def run(self, screen, events):
        self.check_resume()
        screen.fill("white")
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.new_game.rect.collidepoint(event.pos):
                    self.manager.game.restart()
                    self.manager.state = "game"
                elif self.resume.rect.collidepoint(event.pos):
                    #RESUME
                    if self.manager.game.resume():
                        self.manager.state = "game"
                    else:
                        self.resume.active = False
                elif self.ranking.rect.collidepoint(event.pos):
                    self.manager.state = "leaderboard"
                elif self.history.rect.collidepoint(event.pos):
                    self.manager.history.load_rounds = True
                    self.manager.state = "history"
                elif self.log_out.rect.collidepoint(event.pos):
                    self.manager.state = "login"

        self.new_game.draw(screen)
        self.resume.draw(screen)
        self.ranking.draw(screen)
        self.history.draw(screen)
        self.log_out.draw(screen)

class HistoryScene:

    class Round:
        def __init__(self, mode, answer, history, time, status, date):
            self.mode = mode
            self.answer = answer
            self.history = history
            self.time = time
            self.status = status
            self.date = date

    class RoundBar:
        def __init__(self, order, round, center_y, align_text = "left", draw_frame = True):
            self.order = order
            # print(round)
            self.mode = round.mode
            self.answer = round.answer
            self.status = round.status
            self.date = round.date

            self.order_box = Box(ORDER_CENTER_X, center_y, ORDER_WIDTH, ROUNDBAR_HEIGHT, str(self.order))
            self.mode_box = Box(MODE_CENTER_X, center_y, MODE_WIDTH, ROUNDBAR_HEIGHT, self.mode, align_text = align_text)
            self.answer_box = Box(ANSWER_CENTER_X, center_y, ANSWER_WIDTH, ROUNDBAR_HEIGHT, self.answer, align_text = align_text)
            self.status_box = Box(STATUS_CENTER_X, center_y, STATUS_WIDTH, ROUNDBAR_HEIGHT, self.status, align_text = align_text)
            self.date_box = Box(DATE_CENTER_X, center_y, DATE_WIDTH, ROUNDBAR_HEIGHT, self.date, align_text = align_text)

            self.order_box.draw_frame = self.mode_box.draw_frame = self.answer_box.draw_frame\
                = self.status_box.draw_frame = self.date_box.draw_frame = draw_frame

            self.active = True
            self.chosen = False

        def mouse_collides(self):
            if not self.active:
                return False

            return self.order_box.mouse_collides() or self.mode_box.mouse_collides() or self.answer_box.mouse_collides() or self.status_box.mouse_collides() or self.date_box.mouse_collides()

        def change_color(self, box_color, text_color):
            self.order_box.color = self.mode_box.color = self.answer_box.color = self.status_box.color = self.date_box.color = box_color
            self.order_box.update_text(self.order_box.text, text_color)
            self.mode_box.update_text(self.mode_box.text, text_color)
            self.answer_box.update_text(self.answer_box.text, text_color)
            self.status_box.update_text(self.status_box.text, text_color)
            self.date_box.update_text(self.date_box.text, text_color)

        def draw(self, screen):
            if self.active:
                if self.chosen:
                    self.change_color(GREEN, "white")
                elif self.mouse_collides():
                    self.change_color(BUTTON_MOUSE, "black")
                else:
                    self.change_color("white", "black")
            else:
                if self.chosen:
                    self.change_color(GREEN, "white")
                else:
                    self.change_color("white", "black")

            self.order_box.draw(screen)
            self.mode_box.draw(screen)
            self.answer_box.draw(screen)
            self.status_box.draw(screen)
            self.date_box.draw(screen)

    class RoundBox:
        def __init__(self, round):
            self.frame = Box(SCREEN_CENTER_X, SCREEN_CENTER_Y, 560, 600)
            self.frame.draw_frame = False
            self.exit = Exit(self.frame.right, self.frame.top)

            self.mode = round.mode
            self.answer = round.answer
            self.time = round.time
            self.history = round.history

            self.grid = Grid(SCREEN_CENTER_X, SCREEN_CENTER_Y + 20, self.answer)
            for i in range(0, len(self.history), 2):
                line = self.grid.lines[self.grid.cur_line]
                word = self.history[i]
                state = self.history[i + 1]

                line.update_line(word, entered = True if state == "1" else False)
                if state == "1":
                    self.grid.cur_line += 1

            self.mode_box = Box(480, 135, 180, 35, self.mode)
            self.answer_box = Box(self.mode_box.right + 210 // 2 - 2, 135, 210, 35, self.answer)
            self.time_box = Box(self.answer_box.right + 100 // 2 - 2, 135, 130, 35, f"{(self.time / 1000):.2f}s")
            self.to_draw = False

        def handle_event(self, event):
            if left_mouse_click(event):
                if self.exit.mouse_collides():
                    self.to_draw = False

        def draw(self, screen):
            if self.to_draw:
                self.frame.draw(screen)
                self.grid.draw(screen)
                self.exit.draw(screen)
                self.mode_box.draw(screen)
                self.answer_box.draw(screen)
                self.time_box.draw(screen)

    def __init__(self, manager):
        self.manager = manager

        self.frame = Box(SCREEN_CENTER_X + 20, SCREEN_CENTER_Y, 1080, 630)
        self.title = Box(SCREEN_CENTER_X + 20, 110, 1080, 70, "TEN LATEST ROUNDS")
        self.title.draw_frame = False
        self.title.draw_back = False
        self.backbutton = BackButton()

        self.typebar = self.RoundBar("Top", self.Round("Mode", "Answer", None, None, "Win/Lose", "Time and Date"), center_y = 140 + (ROUNDBAR_HEIGHT + ROUNDBAR_GAP), align_text = "mid", draw_frame = False)
        self.rounds = []
        self.roundbars = []
        self.roundboxes = []
        self.loaded = False

        self.draw_roundbox = False

    def up_rounds(self):
        self.rounds.clear()
        self.roundbars.clear()
        self.roundboxes.clear()
        with open("round.txt", "r") as round_file:
            while True:
                round = round_file.readline()
                if not round:
                    break
                round = round[:-1].split("|")
                user = round[0]
                if (user != self.manager.username):
                    continue
                mode = round[1]
                answer = round[2]
                history = round[3].split(",")
                time = int(round[4])
                status = round[5]
                date = round[6]
                # print(order, round)
                if (status != "NotDone"):
                    round = self.Round(mode, answer, history, time, status, date)
                    self.rounds.append(round)
                    # self.roundbars.append(self.RoundBar(str(order), mode, answer, status, date, 140 + (order + 1) * (ROUNDBAR_HEIGHT + ROUNDBAR_GAP)))
                # order += 1

        self.rounds.reverse()
        for i in range(len(self.rounds)):
            self.roundbars.append(self.RoundBar(i + 1, self.rounds[i], 140 + (i + 2) * (ROUNDBAR_HEIGHT + ROUNDBAR_GAP)))
            self.roundboxes.append(self.RoundBox(self.rounds[i]))

    def get_clicked_round(self):
        for i in range(len(self.roundbars)):
            if self.roundbars[i].mouse_collides():
                return i
        return None

    def get_chosen_round(self):
        for i in range(len(self.roundbars)):
            if self.roundbars[i].chosen:
                return i
        return None

    def draw(self, screen):
        self.frame.draw(screen)
        self.title.draw(screen)
        self.backbutton.draw(screen)

        for roundbar in self.roundbars:
            roundbar.draw(screen)

        self.typebar.draw(screen)

        if self.draw_roundbox:
            dark_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            dark_surf.fill("black")
            dark_surf.set_alpha(200)
            screen.blit(dark_surf, (0, 0))
            
            round = self.get_chosen_round()
            self.roundboxes[round].draw(screen)

    def handle_backbutton(self, event):
        if self.backbutton.is_clicked(event):
            self.manager.state = "start"

    def deactivate(self):
        self.backbutton.active = False
        self.typebar.active = False
        for i in range(len(self.roundbars)):
            self.roundbars[i].active = False
        
    def activate(self):
        self.backbutton.active = True
        self.typebar.active = False
        for i in range(len(self.roundbars)):
            self.roundbars[i].active = True

    # def handle_

    def run(self, screen, events):
        if self.loaded == False:
            self.up_rounds()
            self.loaded = True
        screen.fill('white')
        
        for event in events:
            if self.draw_roundbox:
                self.deactivate()
                round = self.get_chosen_round()
                roundbar = self.roundbars[round]
                roundbox = self.roundboxes[round]
                if left_mouse_click(event):
                    if roundbox.exit.mouse_collides() or roundbox.frame.mouse_collides() == False:
                        self.draw_roundbox = False
                        roundbox.to_draw = False
                        roundbar.chosen = False
            else:
                self.activate()
                self.handle_backbutton(event)
                if left_mouse_click(event):
                    round_clicked = self.get_clicked_round()
                    if round_clicked is not None:
                        self.draw_roundbox = True
                        self.roundbars[round_clicked].chosen = True
                        self.roundboxes[round_clicked].to_draw = True

        self.draw(screen)

class LeaderboardScene:

    class Button:
        def __init__(self, text = "Text", size = 30, center_x = 0, center_y = 0, left = -1, right = -1):
            self.box = TextBox(text, size, center_x = center_x, center_y = center_y, left = left, right = right, curve = False)
            self.is_clicked = False

        def draw(self, screen):
            if self.is_clicked:
                self.box.change_color("white", GREEN)
            else:
                if self.box.mouse_collides():
                    self.box.change_color("black", BUTTON_MOUSE)
                else:
                    self.box.change_color("black", "white")
            self.box.draw(screen)

    class Leaderboard:

        class Rank:
            def __init__(self, top, user, score, center_y):
                self.top = top
                self.user = user
                self.score = score

                self.top_box = Box(TOP_CENTER_X, center_y, TOP_WIDTH, RANKBOX_HEIGHT, str(self.top))
                self.user_box = Box(USER_CENTER_X, center_y, USER_WIDTH, RANKBOX_HEIGHT, self.user)
                self.score_box = Box(SCORE_CENTER_X, center_y, SCORE_WIDTH, RANKBOX_HEIGHT, f"{self.score:.2f}s")

            def draw(self, screen):
                
                if (self.top_box.mouse_collides() or self.user_box.mouse_collides() or self.score_box.mouse_collides()):
                    self.top_box.color = self.user_box.color = self.score_box.color = GREEN
                    self.top_box.update_text(self.top_box.text, "white")
                    self.user_box.update_text(self.user_box.text, "white")
                    self.score_box.update_text(self.score_box.text, "white")
                else:
                    self.top_box.color = self.user_box.color = self.score_box.color = "white"
                    self.top_box.update_text(self.top_box.text, "black")
                    self.user_box.update_text(self.user_box.text, "black")
                    self.score_box.update_text(self.score_box.text, "black")

                self.top_box.draw(screen)
                self.user_box.draw(screen)
                self.score_box.draw(screen)

        def __init__(self, mode):
            self.frame = Box(SCREEN_CENTER_X + 20, SCREEN_CENTER_Y, 1080, 630)
            self.title = Box(SCREEN_CENTER_X, 130, 1080, 70, "LEADERBOARD")
            self.title.draw_frame = False
            self.title.draw_back = False
            
            self.mode = mode
            self.ranks = []
            self.to_load_ranks = True
            self.to_draw = False

            # self.load_ranks()

        def load_ranks(self):
            self.ranks.clear()
            users = []
            scores = []
            count = []
            with open("round.txt", "r") as round_file:
                # print(f"{mode}: {users}, {scores}")
                while True:
                    # print(f"{mode}: {users}")
                    round = round_file.readline()
                    # print(round)
                    if not round:
                        break
                    round = round[:-1].split("|")
                    mode = round[1]
                    if (mode != self.mode):
                        continue
                    user = round[0]
                    round_win = round[5]
                    score = int(round[4])
                    if round_win == "Win":
                        if user not in users:
                            users.append(user)
                            scores.append(score)
                            count.append(1)
                        else:
                            index = users.index(user)
                            scores[index] += score
                            count[index] += 1

            temp = []
            for i in range(len(users)):
                temp.append((users[i], scores[i] / float(count[i])))
            temp.sort(key = sort_func)
            # print(temp)
            for i in range(len(temp)):
                self.ranks.append(self.Rank(i + 1, temp[i][0], temp[i][1] / 1000, 200 + i * (RANKBOX_HEIGHT + RANKBOX_GAP)))

            while (len(self.ranks) < 10):
                self.ranks.append(self.Rank(len(self.ranks) + 1, "", 0, 200 + len(self.ranks) * (RANKBOX_HEIGHT + RANKBOX_GAP)))

        def draw(self, screen):
            if self.to_load_ranks:
                self.load_ranks()
                self.to_load_ranks = False
            self.frame.draw(screen)
            self.title.draw(screen)

            for i in range(min(10, len(self.ranks))):
                self.ranks[i].draw(screen)     

    def __init__(self, manager):
        self.manager = manager
        
        self.english_button = self.Button("English", size = 20, left = 126, center_y = 45)
        self.english_lb = self.Leaderboard("English")
        self.english_button.is_clicked = True
        
        self.vnese_button = self.Button("Vietnamese", size = 20, left = self.english_button.box.back_rect.right + 5, center_y = 45)
        self.vnese_lb = self.Leaderboard("Vietnamese")

        self.math_button = self.Button("Math", size = 20, left = self.vnese_button.box.back_rect.right + 5, center_y = 45)
        self.math_lb = self.Leaderboard("Math")

        self.backbutton = BackButton()

    def run(self, screen, events):
        screen.fill('white')
        self.backbutton.draw(screen)

        # self.english_lb.draw(screen)

        for event in events:
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                self.manager.state = "start"
            if left_mouse_click(event):
                if (self.backbutton.box.mouse_collides()):
                    self.manager.state = "start"
                elif (self.english_button.box.mouse_collides()):
                    self.english_button.is_clicked = True
                    self.vnese_button.is_clicked = False
                    self.math_button.is_clicked = False
                elif (self.vnese_button.box.mouse_collides()):
                    self.english_button.is_clicked = False
                    self.vnese_button.is_clicked = True
                    self.math_button.is_clicked = False
                elif (self.math_button.box.mouse_collides()):
                    self.english_button.is_clicked = False
                    self.vnese_button.is_clicked = False
                    self.math_button.is_clicked = True

        if self.english_button.is_clicked:
            self.english_lb.to_load_ranks = True
            self.english_lb.draw(screen)
        elif self.vnese_button.is_clicked:
            self.vnese_lb.to_load_ranks = True
            self.vnese_lb.draw(screen)
        elif self.math_button.is_clicked:
            self.math_lb.to_load_ranks = True
            self.math_lb.draw(screen)

        self.english_button.draw(screen)
        self.vnese_button.draw(screen)
        self.math_button.draw(screen)
        
class GameScene:

    class Key:
        def __init__(self, x, y, width, height, text):
            # Sử dụng Box để đồng bộ giao diện với newnew.py
            # Box nhận tọa độ tâm (center_x, center_y) nên cần tính toán lại từ x, y (topleft)
            center_x = x + width // 2
            center_y = y + height // 2
            self.text = text
            # Tạo Box với màu nền mặc định là BUTTON_NO_MOUSE
            self.box = Box(center_x, center_y, width, height, text)
            self.box.color = BUTTON_NO_MOUSE 
            self.box.frame_color = "white" # Viền trắng cho nút
            
            # Trạng thái màu sắc ưu tiên: Green > Yellow > Grey > Default
            self.state_priority = 0 # 0: Default, 1: Grey, 2: Yellow, 3: Green

        def update_state(self, color):
            new_priority = 0
            if color == GREEN: new_priority = 3
            elif color == YELLOW: new_priority = 2
            elif color == WORDLE_GREY: new_priority = 1
            
            # Chỉ cập nhật nếu độ ưu tiên màu mới cao hơn màu cũ
            # (Ví dụ: Đã xanh rồi thì không thể thành vàng hay xám được nữa)
            if new_priority > self.state_priority:
                self.state_priority = new_priority
                self.box.color = color
                self.box.update_text(self.text, "white") # Đổi chữ sang trắng nếu có màu
            
        def draw(self, screen):
            # Hiệu ứng hover giống try1.py nhưng dùng màu của newnew.py
            if self.state_priority == 0: # Chỉ hover khi chưa có màu kết quả
                if self.box.mouse_collides():
                    self.box.color = BUTTON_MOUSE
                else:
                    self.box.color = BUTTON_NO_MOUSE
            
            self.box.draw(screen)

        def click(self):
            return self.box.mouse_collides()

        def reset(self):
            self.state_priority = 0
            self.box.color = BUTTON_NO_MOUSE
            self.box.update_text(self.text, "black")
            self.box.frame_color = "white"

    class VirtualKeyboard:
        def __init__(self, mode, start_y):
            self.keys = []
            self.mode = mode
            
            key_w, key_h, gap = 43, 58, 6
            # Điều chỉnh kích thước nếu là chế độ Math để nút to hơn cho dễ bấm
            if mode == "Math":
                key_w, key_h = 60, 60
            
            rows = []
            if mode == "Math":
                # Layout cho chế độ Toán
                rows = [
                    "12345",
                    "67890",
                    "+-*/="
                ]
            else:
                # Layout QWERTY cho English/Vietnamese
                rows = [
                    "QWERTYUIOP",
                    "ASDFGHJKL",
                    "ZXCVBNM"
                ]

            # Tạo các hàng phím
            for r_idx, row_chars in enumerate(rows):
                # Tính toán để căn giữa hàng phím
                row_width = len(row_chars) * (key_w + gap) - gap
                start_x = (SCREEN_WIDTH - row_width) // 2
                current_y = start_y + r_idx * (key_h + gap)
                
                for i, char in enumerate(row_chars):
                    self.keys.append(GameScene.Key(start_x + i * (key_w + gap), current_y, key_w, key_h, char))

            # Thêm nút ENTER và BACKSPACE ở hàng cuối cùng
            last_y = start_y + (len(rows) - 1) * (key_h + gap)
            if mode == "Math":
                 # Với Math, đặt Enter/Back bên cạnh
                last_row_width = len(rows[-1]) * (key_w + gap) - gap
                start_x_last = (SCREEN_WIDTH - last_row_width) // 2
                
                # Nút Backspace bên trái
                self.keys.append(GameScene.Key(start_x_last - gap - 80, last_y, 80, key_h, "<"))
                # Nút Enter bên phải
                self.keys.append(GameScene.Key(start_x_last + last_row_width + gap, last_y, 80, key_h, "ENTER"))

            else:
                # Với QWERTY, đặt như try1.py
                row3_len = len(rows[2])
                row3_width = row3_len * (key_w + gap) - gap
                start_x_row3 = (SCREEN_WIDTH - row3_width) // 2
                
                # Enter bên trái
                self.keys.append(GameScene.Key(start_x_row3 - gap - 65, last_y, 65, key_h, "ENTER"))
                # Backspace bên phải
                self.keys.append(GameScene.Key(start_x_row3 + row3_width + gap, last_y, 65, key_h, "<"))

        def draw(self, screen):
            for key in self.keys:
                key.draw(screen)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for key in self.keys:
                    if key.click():
                        return key.text
            return None

        def update_colors(self, guess_word, colors):
            # Hàm này đồng bộ màu từ Grid xuống Bàn phím
            for i in range(len(guess_word)):
                char = guess_word[i]
                color = colors[i]
                for key in self.keys:
                    if key.text == char:
                        key.update_state(color)

        def reset(self):
            for key in self.keys:
                key.reset()

    class SaveConfirm:
        def __init__(self):
            self.frame = Box(SCREEN_CENTER_X, SCREEN_CENTER_Y, 550, 250)
            self.frame.draw_frame = False
            self.line = TextBox("Do you want to save this game?", 30, back_color = "white", center_x = SCREEN_CENTER_X, center_y = SCREEN_CENTER_Y - 30)

            self.yes_button = Box(SCREEN_CENTER_X - 5 - 120 // 2, SCREEN_CENTER_Y + 40, 100, 38, "Yes")
            self.yes_button.color = BUTTON_NO_MOUSE

            self.no_button = Box(SCREEN_CENTER_X + 5 + 120 // 2, SCREEN_CENTER_Y + 40, 100, 38, "No")
            self.no_button.color = BUTTON_NO_MOUSE

            self.exit = Exit(self.frame.right, self.frame.top)

        def draw(self, screen):
            self.frame.draw(screen)
            self.line.draw(screen)
            
            self.yes_button.color = BUTTON_MOUSE if self.yes_button.mouse_collides() else BUTTON_NO_MOUSE
            self.no_button.color = BUTTON_MOUSE if self.no_button.mouse_collides() else BUTTON_NO_MOUSE

            self.yes_button.draw(screen)
            self.no_button.draw(screen)
            
            self.exit.draw(screen)

    class Button:
        def __init__(self, text = "Text", size = 30, center_x = 0, center_y = 0, left = -1, right = -1):
            self.box = TextBox(text, size, center_x = center_x, center_y = center_y, left = left, right = right)
            self.active = True
        
        def draw(self, screen):
            self.box.back_color = BUTTON_MOUSE if (self.box.mouse_collides() and self.active) else BUTTON_NO_MOUSE
            self.box.draw(screen)

        def mouse_collides(self):
            return self.box.mouse_collides()
        
        def clicked(self):
            return self.mouse_collides() and self.active

    class ModeBar:
        def __init__(self):
            self.english = GameScene.Button("English", size = 20, left = 120, center_y = 140 - (100 - 45))
            self.vnese = GameScene.Button("Vietnamese", size = 20, left = 120, center_y = 180 - (100 - 45))
            self.math = GameScene.Button("Math", size = 20, left = 120, center_y = 220 - (100 - 45))

        def draw(self, screen):
            self.english.draw(screen)
            self.vnese.draw(screen)
            self.math.draw(screen)

        def active(self):
            if self.english.active and self.vnese.active and self.math.active:
                return True
            return False

        def deactivate(self):
            self.english.active = self.vnese.active = self.math.active = False
        
        def activate(self):
            self.english.active = self.vnese.active = self.math.active = True

        def mode_clicked(self):
            if self.english.box.mouse_collides() and self.english.active:
                return "English"
            elif self.vnese.box.mouse_collides() and self.vnese.active:
                return "Vietnamese"
            elif self.math.box.mouse_collides() and self.math.active:
                return "Math"
            return None

    class TimeBox:
        def __init__(self, width, height):
            self.time_str = "00:00"
            self.box = Box(1000, 320 - 80, width, height, self.time_str)
            self.start_ticks = pygame.time.get_ticks()
            self.pause_start = 0
            self.paused_time = 0
            self.elapsed_time = 0

        def update_time(self):
            self.elapsed_time = (pygame.time.get_ticks() - self.start_ticks) - self.paused_time
            minutes = str(self.elapsed_time // 1000 // 60)
            seconds = str((self.elapsed_time // 1000) % 60)
            if (len(minutes) < 2):
                minutes = "0" + minutes
            if (len(seconds) < 2):
                seconds = "0" + seconds
            self.time_str = minutes + ":" + seconds
            self.box.update_text(self.time_str)

        def draw(self, screen):
            self.box.draw(screen)

    def __init__(self, manager, mode = "English", valid_func = is_english_word, bank = eng_words):
        self.manager = manager
        self.username = self.manager.login.user_box.text
        # self.grid = self.Grid(500, 300, "NIGGA")
        self.mode = mode
        self.bank = bank
        self.answer = self.bank[random.randint(0, len(self.bank) - 1)]
        # self.answer = "NIGGA"
        self.grid = Grid((80 + SCREEN_CENTER_X) // 2 + 40, SCREEN_CENTER_Y - 80, self.answer)
        print(self.answer)

        self.done = False

        self.is_valid = valid_func

        self.notif = TextBox("", size = 23, back_color = "white", center_x = (80 + SCREEN_CENTER_X) // 2, center_y = SCREEN_CENTER_Y - 22)
        self.draw_notif = False

        self.newgame_button = self.Button("NEW GAME", 35, 1000, 320)
        self.backbutton = BackButton()
        self.mode_button = self.Button("Mode: " + self.mode, 20, center_y = 45, left = 120)
        self.redo_button = self.Button("Redo", 20, center_y = 45, right = SCREEN_CENTER_X + 40)
        self.undo_button = self.Button("Undo", 20, center_y = 45, right = self.redo_button.box.left - 20)
        self.kbcontrol_button = self.Button("Hide Keyboard", 20, center_y = 600, left = 120)
        # print(self.redo.box.left, self.redo.box.right)

        self.save = self.SaveConfirm()
        self.draw_save = False
        self.game_saved = False

        self.modebar = self.ModeBar()
        self.draw_modebar = False

        self.keyboard = self.VirtualKeyboard(self.mode, 500)
        self.draw_kb = True

        self.timer = self.TimeBox(self.newgame_button.box.width, 80)

        self.stack1 = []
        self.stack2 = []

    def sync_keyboard(self):
        # 1. Xóa sạch màu bàn phím hiện tại
        self.keyboard.reset()
        
        # 2. Duyệt qua các dòng ĐÃ NHẬP (entered) nằm trước dòng hiện tại
        # Logic: Chỉ những dòng đã enter mới tác động lên màu bàn phím
        for i in range(self.grid.cur_line):
            line = self.grid.lines[i]
            # Tính toán lại màu cho dòng đó
            colors = compare(line.word, self.answer)
            # Tô lại màu lên bàn phím
            self.keyboard.update_colors(line.word, colors)

    def get_invalid_notif(self):
        if (self.mode == "Math"):
            return "Not a valid expression"
        else:
            return "Word does not exist"
        
    def handle_enter(self, line):
        if (len(line.word) < len(line.answer)):
            self.notif.update_text("Not enough characters")
            self.draw_notif = True
        elif (self.is_valid(line.word) == False):
            notification = self.get_invalid_notif()
            self.notif.update_text(notification)
            self.draw_notif = True
        else:
            line.entered = True
            colors = compare(line.word, self.answer)
            self.keyboard.update_colors(line.word, colors)
            self.stack1.pop()
            self.stack1.pop()
            self.stack1.append(line.word)
            self.stack1.append("1")
            if (line.word == self.answer):
                self.done = True
                self.notif.update_text("You won!")
                self.draw_notif = True
                # continue
                return
            self.grid.cur_line += 1
            if (self.grid.cur_line == 6):
                self.notif.update_text(f"Correct answer: {self.answer}")
                self.draw_notif = True
                self.done = True
    
    def process_input(self, key_text):
        """Hàm xử lý input chung cho cả phím ảo và phím thật"""
        line = self.grid.lines[self.grid.cur_line]
        if key_text == "ENTER":
            self.handle_enter(line)
            return
        elif key_text == "<": # Backspace
            line.backspace()
        else:
            # Logic thêm chữ
            if self.mode == "Math":
                if key_text in math_chars:
                    line.add_char(key_text)
            else:
                if key_text.isalpha():
                    line.add_char(key_text.upper())

        if (len(self.stack1) // 2 - 1 == self.grid.cur_line):
            if (self.stack1):
                self.stack1.pop()
                self.stack1.pop()
        self.stack1.append(line.word)
        self.stack1.append("1" if line.entered else "0")

    def deactivate(self):
        if (self.grid.cur_line < 6):
            self.grid.lines[self.grid.cur_line].active = True
        self.newgame_button.active = False
        self.backbutton.active = False
        self.mode_button.active = False
        self.undo_button.active = False
        self.redo_button.active = False
        self.modebar.deactivate()
        self.kbcontrol_button.active = False

    def activate(self):
        if (self.grid.cur_line < 6):
            self.grid.lines[self.grid.cur_line].active = True
        self.newgame_button.active = True
        self.backbutton.active = True
        self.mode_button.active = True
        self.undo_button.active = True
        self.redo_button.active = True
        if (self.draw_modebar): 
            self.modebar.activate()
        else:
            self.modebar.deactivate()
        self.kbcontrol_button.active = True

    def handle_save_scene(self, event):
        if left_mouse_click(event):
            if (self.save.yes_button.mouse_collides()):
                if (self.game_saved == False):
                    self.savegame()
                self.draw_save = False
                self.manager.state = "start"
            elif (self.save.no_button.mouse_collides()):
                # self.manager.game.restart
                self.draw_save = False
                self.manager.state = "start"
                self.manager.game.restart()
            elif (self.save.exit.mouse_collides()):
                self.draw_save = False
                self.timer.paused_time += pygame.time.get_ticks() - self.timer.pause_start
    
    def draw(self, screen):
        # Vẽ lưới ô vuông Grid và bàn phím Keyboard
        self.grid.draw(screen)

        if (self.draw_kb):
            self.keyboard.draw(screen)

        # Vẽ các nút chức năng: Thông báo (Notif), New Game, Nút trở về (BackButton), Nút chế độ (Mode Button), Undo, Redo
        if (self.draw_notif): self.notif.draw(screen)
        self.newgame_button.draw(screen)
        self.backbutton.draw(screen)
        self.mode_button.draw(screen)
        self.redo_button.draw(screen)
        self.undo_button.draw(screen)
        self.kbcontrol_button.draw(screen)
        self.timer.draw(screen)

        # Vẽ thanh chế độ (Modebar) nếu được bật
        if (self.draw_modebar):
            self.modebar.draw(screen)

        # Vẽ chế độ lưu (Save) đè lên màn hình thường nếu chế độ được bật
        if (self.draw_save):
            dark_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            dark_surf.fill("black")
            dark_surf.set_alpha(200)
            screen.blit(dark_surf, (0, 0))
            self.save.draw(screen)

    def undo(self):
        if (self.stack1) and self.done == False:
            pos = len(self.stack1) // 2 - 1
            word = self.stack1[-2]
            if (pos == self.grid.cur_line):
                line = self.grid.lines[self.grid.cur_line]
                self.stack2.append(word)
                self.stack2.append(self.stack1[-1])
                self.stack1.pop()
                self.stack1.pop()
                line.update_line("", False)
                # self.keyboard.update_colors(line.word, self.answer)
                # pass
            else:
                self.grid.cur_line -= 1
                line = self.grid.lines[self.grid.cur_line]
                # self.stack2.append(word)
                self.stack2.append(word)
                self.stack2.append(self.stack1[-1])
                self.stack1.pop()
                self.stack1.pop()
                line.update_line("", False)
                # self.keyboard.update_colors(line.word, self.answer)
            self.sync_keyboard()

    def redo(self):
        if (self.stack2):
            state = self.stack2[-1]
            self.stack2.pop()

            word = self.stack2[-1]
            self.stack2.pop()

            line = self.grid.lines[self.grid.cur_line]
            if (state == "1"):
                line.update_line(word, True)
                self.grid.cur_line += 1
            else:
                line.update_line(word, False)
            
            self.stack1.append(word)
            self.stack1.append(state)
            self.sync_keyboard()

    def handle_kbcontrol(self):
        if (self.draw_kb):
            self.draw_kb = False
            self.kbcontrol_button.box.update_text("Show Keyboard")
        else:
            self.draw_kb = True
            self.kbcontrol_button.box.update_text("Hide Keyboard")

    def handle_buttons(self, event):
        if left_mouse_click(event):
            if self.newgame_button.clicked():
                self.restart() # New Game thì Restart Game

            if self.mode_button.clicked(): 
                self.draw_modebar = True if self.draw_modebar == False else False # Bật nút Mode khi chưa được bật, tắt nếu đã được bật

            if self.backbutton.is_clicked(event):
                self.draw_save = True
                self.timer.pause_start = pygame.time.get_ticks()
                
            if self.undo_button.clicked():
                self.undo()

            if self.redo_button.clicked():
                self.redo()

            if self.kbcontrol_button.clicked():
                self.handle_kbcontrol()

            mode_clicked = self.modebar.mode_clicked() # Tìm chế độ đã được bấm (trả về None nếu không bấm chế độ nào)
            if mode_clicked is not None:
                self.change_mode(mode_clicked)

    def handle_notif(self, event):
        if (event.type == pygame.KEYDOWN):
            if (self.draw_notif): self.draw_notif = False
        
        if left_mouse_click(event):
            if (not self.notif.mouse_collides()):
                self.draw_notif = False

    def restart(self):
        self.__init__(self.manager, self.mode, self.is_valid, self.bank)

    def change_mode(self, mode):
        if (self.mode != mode):
            if (mode == 'English'):
                self.__init__(self.manager, mode, valid_func = is_english_word)
            elif (mode == "Math"):
                self.__init__(self.manager, mode, valid_func = is_equation, bank = math_eqs)
            elif (mode == "Vietnamese"):
                self.__init__(self.manager, mode, valid_func = is_viet_word, bank = vie_words)
        else:
            self.draw_modebar = False

    def savegame(self):
        data = f"{self.manager.username}|{self.mode}|{self.answer}|"
        data += ",".join(self.stack1)
        data += "|"
        data += f"{self.timer.elapsed_time}|"
        data += "Win|" if self.done and self.stack1[-1] == self.answer else "Lose|" if self.done else "NotDone|"

        time_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data += time_date

        with open("round.txt", "a") as round_file:
            round_file.write(data + "\n")

    def resume(self):
        found_data = None
            
            # 1. Đọc file và tìm dòng dữ liệu cuối cùng của user hiện tại
            # Dùng reversed để tìm từ dưới lên (lấy cái mới nhất)
        with open("round.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in reversed(lines):
                data = line.strip().split("|")
                # Format: username|mode|answer|stack1|elapsed_time|status|date
                if len(data) >= 7 and data[0] == self.manager.username:
                    # Ưu tiên lấy game chưa chơi xong (NotDone), 
                    # hoặc bạn có thể bỏ điều kiện này nếu muốn load cả game đã thắng/thua để xem lại
                    found_data = data
                    break
        
        if not found_data:
            print("No saved game found for this user.")
            return False

        # 2. Parse dữ liệu
        # username = found_data[0] # Không cần dùng lại
        mode = found_data[1]
        answer = found_data[2]
        stack_str = found_data[3]
        elapsed_time = int(found_data[4])
        status = found_data[5]

        # 3. Cài đặt lại Chế độ chơi (Mode) và Từ điển (Bank)
        self.mode = mode
        if self.mode == 'English':
            self.bank = eng_words
            self.is_valid = is_english_word
        elif self.mode == "Math":
            self.bank = math_eqs
            self.is_valid = is_equation
        elif self.mode == "Vietnamese":
            self.bank = vie_words
            self.is_valid = is_viet_word
        
        # Cập nhật nút hiển thị chế độ
        self.mode_button.box.update_text("Mode: " + self.mode)

        # 4. Cài đặt lại Đáp án và Bàn phím/Lưới
        self.answer = answer
        # Tạo lại Grid với đáp án đúng của game cũ
        self.grid = Grid((80 + SCREEN_CENTER_X) // 2 + 40, SCREEN_CENTER_Y - 50, self.answer)
        # Tạo lại bàn phím (vì layout Math khác English)
        self.keyboard = self.VirtualKeyboard(self.mode, 500)

        # 5. Khôi phục các ô đã điền (Stack)
        self.stack1 = stack_str.split(",") if stack_str else []
        self.stack2 = [] # Clear Redo stack
        
        self.grid.cur_line = 0
        for i in range(0, len(self.stack1), 2):
            word = self.stack1[i]
            state = self.stack1[i + 1]

            line = self.grid.lines[self.grid.cur_line]
            entered = True if state == "1" else False
            line.update_line(word, entered)

            if entered:
                self.grid.cur_line += 1

        # 6. Đồng bộ trạng thái Game (Win/Lose/Playing)
        if status == "Win":
            self.done = True
            self.notif.update_text("You won!")
            self.draw_notif = True
        elif status == "Lose" or self.grid.cur_line >= 6:
            self.done = True
            self.notif.update_text(f"Correct answer: {self.answer}")
            self.draw_notif = True
        else:
            self.done = False

        # 7. Đồng bộ màu sắc bàn phím dựa trên các từ đã điền
        self.sync_keyboard()

        # 8. Đồng bộ Thời gian
        self.timer.elapsed_time = elapsed_time
        # Reset start_ticks để đồng hồ chạy tiếp từ thời gian cũ thay vì từ 0
        self.timer.start_ticks = pygame.time.get_ticks() - elapsed_time
        self.timer.paused_time = 0
        self.timer.update_time()

        # Đánh dấu là đã save để tránh việc tự động save chồng lên khi vừa mở
        self.game_saved = False
        
        print(f"Resumed game: {self.mode} - {elapsed_time}ms")
        return True

    def run(self, screen, events):
        print(self.stack1, self.stack2)
        screen.fill('white')
        if self.done:
            if self.game_saved == False:
                self.savegame()
                self.game_saved = True
        if (self.grid.cur_line < 6):
            self.grid.lines[self.grid.cur_line].active = True

        if (self.draw_save):
            self.deactivate()
            for event in events:
                self.handle_save_scene(event)
        else:
            if (not self.done):
                self.timer.update_time()
            self.activate()
            for event in events:
                # Xử lí các nút trên màn hình chơi thường
                self.handle_buttons(event)
                self.handle_notif(event)
                if self.done:
                    pass
                else:
                    virtual_key = self.keyboard.handle_event(event)
                    if virtual_key:
                        if self.draw_notif: self.draw_notif = False
                        self.process_input(virtual_key)
                    if (event.type == pygame.KEYDOWN):
                        if (self.draw_notif):
                            self.draw_notif = False
                        if (event.key == pygame.K_ESCAPE):
                            self.draw_save = True
                        elif (event.key == pygame.K_BACKSPACE):
                            self.process_input("<")
                        elif (event.key == pygame.K_RETURN):
                            self.process_input("ENTER")
                        else:
                            if (self.mode == "Math"):
                                if (event.unicode and event.unicode.isprintable() and event.unicode in math_chars):
                                    self.process_input(event.unicode)
                                    self.stack2.clear()
                            else:
                                if ('a' <= event.unicode <= 'z' or 'A' <= event.unicode <= 'Z') and event.unicode.isprintable():
                                    self.process_input(event.unicode.upper())
                                    self.stack2.clear()

        self.draw(screen)


def main():
    running = True
    clock = pygame.time.Clock()

    manager = Manager()

    while running:
        events = pygame.event.get()

        for event in events:
            if (event.type == pygame.QUIT):
                running = False
        
        manager.run(screen, events)
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()