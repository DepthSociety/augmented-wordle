import pygame
import random
from datetime import datetime
from config import *
from ui import *
from utils import *
from components import *

class GameScene:
    """
    Lớp GameScene tạo và quản lí màn hình trò chơi.

    Các lớp dưới GameScene đa phần là các nút chức năng mà có thể được bấm vào/được nhập dữ liệu vào.
    Khi Game Scene ở trạng thái xác nhận lưu - tương đương với việc tạm dừng, tất cả các nút phải không được hoạt động
    Do đó, đa phần các lớp ở dưới sẽ có thuộc tính self.active để chỉ là có được phép hoạt động không/đang hoạt động hay không
    """
    class Key:
        """
        Lớp Key tương ứng với một phím của bàn phím ảo.
        """
        def __init__(self, x, y, width, height, text):
            """
            Các tham số:
                x, y (int): tọa độ góc trên bên trái (topleft)
                width: chiều rộng của phím (độ dài theo chiều ngang)
                height: chiều cao của phím (độ dài theo chiều dọc)
                text: kí tự chứa trong phím
            """

            # Box nhận tọa độ tâm (center_x, center_y) nên cần tính toán lại từ x, y (topleft)
            center_x = x + width // 2
            center_y = y + height // 2
            self.text = text
            # Tạo Box với màu nền mặc định là BUTTON_NO_MOUSE
            self.box = Box(center_x, center_y, width, height, text, curve = True)
            self.box.color = BUTTON_NO_MOUSE 
            self.box.draw_frame = False # Viền trắng cho nút
            
            # Thứ tự ưu tiên màu sắc: GREEN > YELLOW > WORDLE_GREY > WHITE (Defaul)
            self.state_priority = 0 # 0: Default, 1: Grey, 2: Yellow, 3: Green

        def update_state(self, color):
            """
            Hàm cập nhật trạng thái màu sắc của phím thành color
            """
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
            # Hàm vẽ phím lên màn hình screen
            if self.state_priority == 0: # Chỉ hover (đổi màu khi di chuột) khi chưa có màu kết quả
                if self.box.mouse_collides():
                    self.box.color = BUTTON_MOUSE
                else:
                    self.box.color = BUTTON_NO_MOUSE
            
            self.box.draw(screen)

        def click(self):
            # Trả về True nếu chuột ở trên phím, False nếu ngược lại
            return self.box.mouse_collides()

        def reset(self):
            # Reset màu của phím
            self.state_priority = 0
            self.box.color = BUTTON_NO_MOUSE
            self.box.update_text(self.text, "black")
            self.box.frame_color = "white"

    class VirtualKeyboard:

        """
        Lớp tương ứng với bàn phím ảo của trò chơi
        Các thuộc tính:
            keys (list): Danh sách các phím của bàn phím
            mode (str): Chế độ trò chơi
        """

        def __init__(self, mode, start_y): # start_y là biên trên của bàn phím
            self.keys = []
            self.mode = mode
            
            key_w, key_h, gap = 43, 60, 6 # Chiều rộng, chiều cao của một phím và khoảng cách giữa hai phím giáp nhau

            rows = []
            if mode == "Math":
                # Danh sách phím cho chế độ Toán
                rows = [
                    "12345",
                    "67890",
                    "+-*/="
                ]
            else:
                # Danh sách phím cho chế độ tiếng Anh/tiếng Việt
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

            else: # Chế độ tiếng Anh/tiếng Việt
                row3_len = len(rows[2])
                row3_width = row3_len * (key_w + gap) - gap
                start_x_row3 = (SCREEN_WIDTH - row3_width) // 2
                
                # Enter bên trái
                self.keys.append(GameScene.Key(start_x_row3 - gap - 65, last_y, 65, key_h, "ENTER"))
                # Backspace bên phải
                self.keys.append(GameScene.Key(start_x_row3 + row3_width + gap, last_y, 65, key_h, "<"))

        def draw(self, screen):
            # Hàm vẽ bàn phím lên màn hình screen
            for key in self.keys:
                key.draw(screen)

        def handle_event(self, event):
            # Hàm xử lí các sự kiện từ người chơi
            if left_mouse_click(event): 
                # Tìm nút được nhấn khi người chơi nhấn chuột trái
                for key in self.keys:
                    if key.click():
                        return key.text
            return None

        def update_colors(self, guess_word, colors):
            # Hàm đồng bộ màu từ Grid xuống bàn phím
            for i in range(len(guess_word)):
                char = guess_word[i]
                color = colors[i]
                for key in self.keys:
                    if key.text == char:
                        key.update_state(color)

        def reset(self):
            # Reset lại bàn phím
            for key in self.keys:
                key.reset()

    class SaveConfirm:
        """
        Lớp tương ứng với hộp thoại xác nhận người chơi có lưu lại ván chơi hay không
        Các thuộc tính:
            frame (Box): khung của hộp thoại, là hình chữ nhật nền màu trắng được dùng để các bộ phận khác xuất hiện ở trên
            line (TextBox): tiêu đề hộp thoại, mặc định ghi "Do you want to save this game?"
            yes_button (Box): nút Yes - lưu ván chơi
            no_button (Box): nút No - không lưu ván chơi
            exit (Exit): nút thoát hộp thoại
        """
        def __init__(self):
            self.frame = Box(SCREEN_CENTER_X, SCREEN_CENTER_Y, 550, 250)
            self.frame.draw_frame = False # Không vẽ viền của khung hộp thoại
            self.line = TextBox("Do you want to save this game?", 30, back_color = "white", center_x = SCREEN_CENTER_X, center_y = SCREEN_CENTER_Y - 30)

            self.yes_button = Box(SCREEN_CENTER_X - 5 - 120 // 2, SCREEN_CENTER_Y + 40, 100, 38, "Yes")
            self.yes_button.color = BUTTON_NO_MOUSE # Mặc định màu nút khi không có chuột là BUTTON_NO_MOUSE

            self.no_button = Box(SCREEN_CENTER_X + 5 + 120 // 2, SCREEN_CENTER_Y + 40, 100, 38, "No")
            self.no_button.color = BUTTON_NO_MOUSE # Mặc định màu nút khi không có chuột là BUTTON_NO_MOUSE

            self.exit = Exit(self.frame.right, self.frame.top)

        def draw(self, screen):
            # Hàm vẽ SaveConfirm lên màn hình screen
            self.frame.draw(screen)
            self.line.draw(screen)
            
            self.yes_button.color = BUTTON_MOUSE if self.yes_button.mouse_collides() else BUTTON_NO_MOUSE # Khi có chuột ở trên thì nút có màu là BUTTON_MOUSE
            self.no_button.color = BUTTON_MOUSE if self.no_button.mouse_collides() else BUTTON_NO_MOUSE

            self.yes_button.draw(screen)
            self.no_button.draw(screen)
            
            self.exit.draw(screen)

    class Button:
        """
        Lớp Button tương ứng với nút chức năng trên màn hình Game Scene.
        Các thuộc tính:
            box (Box): Box tương ứng của Button
            active (bool): True nếu nút được phép hoạt động (hoặc nút được "bật"), False nếu ngược lại
        """
        def __init__(self, text = "Text", size = 30, center_x = -1, center_y = 0, left = -1, right = -1):
            self.box = TextBox(text, size, center_x = center_x, center_y = center_y, left = left, right = right)
            self.active = True
        
        def draw(self, screen):
            # Vẽ Button lên screen
            self.box.back_color = BUTTON_MOUSE if (self.box.mouse_collides() and self.active) else BUTTON_NO_MOUSE
            self.box.draw(screen)

        def mouse_collides(self):
            # Kiểm tra xem chuột có ở trên Button hay không
            return self.box.mouse_collides()
        
        def clicked(self):
            # Kiểm tra xem chuột có ở trên Button khi Button được phép hoạt động hay không
            # Hàm được dùng khi kiểm tra xem Button đã được nhấn vào hay chưa
            return self.mouse_collides() and self.active

    class ModeBar:
        """
        Lớp ModeBar tương ứng với thanh chứa chế độ trong Game Scene
        Thanh ModeBar sẽ bao gồm ba nút GameScene.Button tương ứng với ba chế độ của trò chơi (English, Vietnamese, Math).
        Thanh ModeBar sẽ hiển thị hoặc tắt khi nút Mode Button của Game Scene được nhấn vào.
        """
        def __init__(self):
            # Ba nút của thanh ModeBar
            self.english = GameScene.Button("English", size = 20, left = 120, center_y = 140 - (100 - 45))
            self.vnese = GameScene.Button("Vietnamese", size = 20, left = 120, center_y = 180 - (100 - 45))
            self.math = GameScene.Button("Math", size = 20, left = 120, center_y = 220 - (100 - 45))

        def draw(self, screen):
            # Vẽ ModeBar lên screen
            self.english.draw(screen)
            self.vnese.draw(screen)
            self.math.draw(screen)

        def active(self):
            # Kiểm tra xem thanh có được phép hoạt động không
            # Thanh được phép hoạt động đồng nghĩa với cả ba nút được phép
            if self.english.active and self.vnese.active and self.math.active:
                return True
            return False

        def deactivate(self):
            # Hàm tắt tính hoạt động của ModeBar
            self.english.active = self.vnese.active = self.math.active = False
        
        def activate(self):
            # Hàm bật tính hoạt động của ModeBar
            self.english.active = self.vnese.active = self.math.active = True

        def mode_clicked(self):
            # Hàm tìm chế độ đã được chọn trong ModeBar
            # Hàm chỉ được gọi khi có event là nhấn chuột trái
            if self.english.box.mouse_collides() and self.english.active:
                return "English"
            elif self.vnese.box.mouse_collides() and self.vnese.active:
                return "Vietnamese"
            elif self.math.box.mouse_collides() and self.math.active:
                return "Math"
            return None

    class TimeBox:
        """
        Lớp TimeBox tương ứng với một hình chữ nhật vẽ thời gian đã trải qua tính từ khi người chơi bắt đầu chơi.
        Các thuộc tính:
            time_str (str): xâu chỉ thời gian đã trải qua
            box (Box): Box tương ứng của TimeBox
            start_ticks (int): thời điểm bắt đầu tính thời gian khi khởi tạo
            pause_start (int): thời điểm bắt đầu tạm dừng
            paused_time (int): tổng thời gian dùng để tạm dừng
            elapsed_time (int): tổng thời gian đã chơi (không tính thời gian tạm dừng)
        """
        def __init__(self, width, height):
            self.time_str = "00:00"
            self.box = Box(1000, 240, width, height, self.time_str) # Mặc định Box có tọa độ trung tâm là (1000, 240)
            self.start_ticks = pygame.time.get_ticks()
            self.pause_start = 0
            self.paused_time = 0
            self.elapsed_time = 0

        def update_time(self):
            # Hàm cập nhật thời gian
            # Tính thời gian chơi: (thời điểm hiện tại - thời điểm bắt đầu) - thời giam tạm dừng
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
            # Vẽ TimeBox lên screen
            self.box.draw(screen)
    """
    GameScene bao gồm các thuộc tính:
        manager: Manager của trò chơi và của GameScene
        username: username của người chơi hiện tại, là kết quả của việc đăng nhập
        mode: chế độ chơi
        bank: ngân hàng đáp án để lấy đáp án
        answer: đáp án của ván
        grid: lưới ô vuông của trò chơi
        done: True nếu ván chơi đã xong, False nếu chưa xong
        is_valid: hàm kiểm tra một từ được nhập vào phải từ hợp lệ không
        notif: hộp thông báo, có thể thông báo lỗi hoặc thông báo đáp án, hoặc chúc mừng người chơi

        Các Button cho: New Game, BackButton, Mode, Redo, Undo, Keyboard Control

        save: hộp thoại lựa chọn việc lưu trò chơi hay không
        draw_save: chỉ trạng thái có đang vẽ SaveConfirm không
        game_saved: ván chơi đã lưu chưa

        modebar: thanh chế độ
        keyboard: bàn phím ảo

        stack1: list mô phỏng một stack, dùng để lưu lịch sử chơi của người chơi
        stack2: list mô phỏng một stack, dùng để lưu các lượt chơi đã bị undo

        Cả stack1 và stack2 đều sẽ lưu dữ liệu gồm các cặp WORD, STATE liên tiếp. Trong đó:
            WORD: là văn bản đã được người dùng nhập vào
            STATE: trạng thái là từ đó đã được chốt chưa: "1" là rồi, "0" là chưa
    """
    def __init__(self, manager, mode = "English", valid_func = is_english_word, bank = eng_words):
        self.manager = manager
        self.username = self.manager.login.user_box.text
        self.mode = mode
        self.bank = bank
        self.answer = self.bank[random.randint(0, len(self.bank) - 1)]
        self.grid = Grid((80 + SCREEN_CENTER_X) // 2 + 40, SCREEN_CENTER_Y - 80, self.answer)

        self.done = False

        self.is_valid = valid_func

        self.notif = TextBox("", size = 23, back_color = "white", center_x = self.grid.center_x, center_y = self.grid.center_y)
        self.draw_notif = False

        self.newgame_button = self.Button("NEW GAME", 35, 1000, 320)
        self.backbutton = BackButton()
        self.mode_button = self.Button("Mode: " + self.mode, 20, center_y = 45, left = 120)
        self.redo_button = self.Button("Redo", 20, center_y = 45, right = SCREEN_CENTER_X + 40)
        self.undo_button = self.Button("Undo", 20, center_y = 45, right = self.redo_button.box.left - 20)
        self.kbcontrol_button = self.Button("Hide Keyboard", 20, center_y = 600, left = 120)

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
        # Hàm lấy thông báo chỉ là từ/biểu thức là không hợp lệ
        if (self.mode == "Math"):
            return "Not a valid expression"
        else:
            return "Word does not exist"
        
    def handle_enter(self, line):
        # Hàm xử lí tình huống người dùng chốt - tức nhấn phím Enter
        if (len(line.word) < len(line.answer)): # line.word chưa đủ kí tự
            self.notif.update_text("Not enough characters")
            self.draw_notif = True
        elif (self.is_valid(line.word) == False): # line.word không phải từ hợp lệ
            notification = self.get_invalid_notif()
            self.notif.update_text(notification)
            self.draw_notif = True
        else:
            line.entered = True
            colors = compare(line.word, self.answer)
            self.keyboard.update_colors(line.word, colors) # cập nhật màu bàn phím

            # Đẩy từ cũ khỏi stack1
            self.stack1.pop()
            self.stack1.pop()
            # Thêm từ mới vào stack1
            self.stack1.append(line.word)
            self.stack1.append("1")

            if (line.word == self.answer): # nếu từ trùng với đáp án
                self.done = True
                self.notif.update_text("You won!")
                self.draw_notif = True
                # continue
                return
            self.grid.cur_line += 1
            if (self.grid.cur_line == 6): # nếu hết ván mà vẫn chưa ra được từ
                self.notif.update_text(f"Correct answer: {self.answer}")
                self.draw_notif = True
                self.done = True
    
    def process_input(self, key_text):
        """
        Hàm xử lý input chung cho cả phím ảo và phím thật
        """
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
                    line.add_char(key_text.upper()) # in hoa

        if (len(self.stack1) // 2 - 1 == self.grid.cur_line): # Nếu từ đã từng gõ chữ thì xóa từ đó để thay bằng từ mới
            if (self.stack1):
                self.stack1.pop()
                self.stack1.pop()
        self.stack1.append(line.word)
        self.stack1.append("1" if line.entered else "0")

    def deactivate(self): # Hàm vô hiệu hóa tất cả các nút trong Scene
        if (self.grid.cur_line < 6):
            self.grid.lines[self.grid.cur_line].active = True
        self.newgame_button.active = False
        self.backbutton.active = False
        self.mode_button.active = False
        self.undo_button.active = False
        self.redo_button.active = False
        self.modebar.deactivate()
        self.kbcontrol_button.active = False

    def activate(self): # Hàm kích hoạt tất cả các nút trong Scene
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
        # Hàm xử lí tình huống hiển thị hộp thoại lưu SaveConfirm
        if left_mouse_click(event):
            if (self.save.yes_button.mouse_collides()): # Nếu chọn Yes thì lưu
                if (self.game_saved == False):
                    self.savegame()
                self.draw_save = False
                self.manager.state = "start"
            elif (self.save.no_button.mouse_collides()): # Nếu chọn No thì thoát
                self.draw_save = False
                self.manager.state = "start"
                self.manager.game.restart()
            elif (self.save.exit.mouse_collides()): # Nếu exit thì tiếp tục chơi
                self.draw_save = False
                self.timer.paused_time += pygame.time.get_ticks() - self.timer.pause_start
    
    def draw(self, screen):
        # Vẽ lưới ô vuông Grid và bàn phím Keyboard
        self.grid.draw(screen)

        if (self.draw_kb):
            self.keyboard.draw(screen)

        # Vẽ các nút chức năng
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
            if (pos == self.grid.cur_line): # Con trỏ cùng vị trí với hàng bị undo
                line = self.grid.lines[self.grid.cur_line]
                # Thêm vào stack2
                self.stack2.append(word)
                self.stack2.append(self.stack1[-1])
                # xóa khỏi stack1
                self.stack1.pop()
                self.stack1.pop()
                line.update_line("", False)
            else: # Con trỏ khác vị trí (ở dưới) hàng bị undo
                self.grid.cur_line -= 1
                line = self.grid.lines[self.grid.cur_line]
                self.stack2.append(word)
                self.stack2.append(self.stack1[-1])
                self.stack1.pop()
                self.stack1.pop()
                line.update_line("", False)

            self.sync_keyboard()

    def redo(self):
        if (self.stack2):
            state = self.stack2[-1]
            self.stack2.pop()

            word = self.stack2[-1]
            self.stack2.pop()

            line = self.grid.lines[self.grid.cur_line]
            if (state == "1"): # đã enter thì tham số entered = True trong update_line()
                line.update_line(word, True)
                self.grid.cur_line += 1
            else:
                line.update_line(word, False)
            
            self.stack1.append(word)
            self.stack1.append(state)
            self.sync_keyboard()

    def handle_kbcontrol(self):
        # Hàm xử lí nút kbcontrol và kiểm soát việc có hiển thị bàn phím ảo không
        if (self.draw_kb):
            self.draw_kb = False
            self.kbcontrol_button.box.update_text("Show Keyboard")
        else:
            self.draw_kb = True
            self.kbcontrol_button.box.update_text("Hide Keyboard")

    def handle_buttons(self, event):
        
        # Hàm xử lí các event liên quan đến các nút trong Scene

        if left_mouse_click(event):
            if self.newgame_button.clicked():
                self.restart() # Chọn New Game thì Restart Game

            if self.mode_button.clicked(): 
                self.draw_modebar = True if self.draw_modebar == False else False # Bật nút Mode khi chưa được bật, tắt nếu đã được bật

            if self.backbutton.is_clicked(event):
                # Chọn BackButton thì ván chơi tạm dừng, và hiện hộp thoại SaveConfirm
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
        # Hàm xử lí tình huống để tắt notif
        if (event.type == pygame.KEYDOWN):
            if (self.draw_notif): self.draw_notif = False
        
        if left_mouse_click(event):
            if (not self.notif.mouse_collides()):
                self.draw_notif = False

    def restart(self): # Tạo GameScene mới
        self.__init__(self.manager, self.mode, self.is_valid, self.bank)

    def change_mode(self, mode):
        # Hàm thay đổi chế độ chơi
        # Khi thay đổi chế độ, một ván mới sẽ bắt đầu và GameScene được khởi tạo lại
        if (self.mode != mode):
            if (mode == 'English'):
                self.__init__(self.manager, mode, valid_func = is_english_word)
            elif (mode == "Math"):
                self.__init__(self.manager, mode, valid_func = is_equation, bank = math_eqs)
            elif (mode == "Vietnamese"):
                self.__init__(self.manager, mode, valid_func = is_viet_word, bank = vie_words)
        else:
            # Nếu mode được thay đổi giống ban đầu thì chỉ tắt ModeBar là xong
            self.draw_modebar = False

    def savegame(self): # Lưu lại dữ liệu của ván
        # data có dạng: username|mode|answer|stack1|elapsed_time|status|date
        # Trong đó, status là Win/Lose/NotDone tùy vào trạng thái của ván
        data = f"{self.manager.username}|{self.mode}|{self.answer}|"
        data += ",".join(self.stack1)
        data += "|"
        data += f"{self.timer.elapsed_time}|"
        data += "Win|" if self.done and self.stack1[-2] == self.answer else "Lose|" if self.done else "NotDone|"

        time_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # Lấy ngày giờ lưu
        data += time_date

        with open("round.txt", "a") as round_file:
            round_file.write(data + "\n") # ghi data vào file round.txt

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

        return True

    def run(self, screen, events):
        screen.fill('white')
        if self.done: # Nếu ván đã xong
            if self.game_saved == False: # Nếu chưa lưu thì lưu
                self.savegame()
                self.game_saved = True # Không lưu nữa
        if (self.grid.cur_line < 6):
            self.grid.lines[self.grid.cur_line].active = True # Luôn bật hoạt động cho Grid

        if (self.draw_save): # nếu vẽ hộp thoại SaveConfirm
            self.deactivate()
            for event in events:
                self.handle_save_scene(event)
        else:
            if (not self.done):
                self.timer.update_time() # Chưa xong ván thì liên tục cập nhật thời gian chơi
            self.activate()
            for event in events:
                # Xử lí các nút trên màn hình chơi thường
                self.handle_buttons(event)
                self.handle_notif(event)
                if self.done:
                    pass
                else:
                    # Tìm nút ảo đã nhấn
                    virtual_key = None
                    if self.draw_kb:
                        virtual_key = self.keyboard.handle_event(event)

                    if virtual_key: # Nếu có nút ảo thì xử lí nút ảo
                        if self.draw_notif: self.draw_notif = False
                        self.process_input(virtual_key)
                    if (event.type == pygame.KEYDOWN): # Nếu có nhấn phím
                        if (self.draw_notif):
                            self.draw_notif = False # Bỏ notif
                        if (event.key == pygame.K_ESCAPE):
                            self.draw_save = True # Nếu nhấn Esc thì vẽ hộp thoại SaveConfirm
                        elif (event.key == pygame.K_BACKSPACE):
                            self.process_input("<") # Nếu Backspace thì xử lí Backspace
                        elif (event.key == pygame.K_RETURN):
                            self.process_input("ENTER")
                        else:
                            if (self.mode == "Math"):
                                if (event.unicode and event.unicode.isprintable() and event.unicode in math_chars):
                                    # Bổ sung kí tự mới vào Grid
                                    self.process_input(event.unicode)
                                    self.stack2.clear() # hiển nhiên phải xóa stack redo
                            else:
                                if ('a' <= event.unicode <= 'z' or 'A' <= event.unicode <= 'Z') and event.unicode.isprintable():
                                    self.process_input(event.unicode.upper())
                                    self.stack2.clear()

        self.draw(screen)
