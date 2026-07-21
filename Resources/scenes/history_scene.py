import pygame
from config import *
from ui import Box, Exit, BackButton
from components import Grid
from utils import left_mouse_click

class HistoryScene:
    """
    Lớp quản lí và hiển thị màn hình lịch sử chơi History Scene
    """
    class Round:
        """
        Lớp tương ứng với một ván chơi, bao gồm:
            mode (str): chế độ chơi
            answer (str): đáp án ván chơi
            history (str): lịch sử chơi, tức các từ đã điền vào
            time (int): thời gian chơi
            status (str): trạng thái ván, có thể là: Win, Lose, NotDone
            date (str): thời điểm ngày giờ chơi
        """
        def __init__(self, mode, answer, history, time, status, date):
            self.mode = mode
            self.answer = answer
            self.history = history
            self.time = time
            self.status = status
            self.date = date

    class RoundBar:
        """
        Thanh RoundBar tương ứng với một Round, sẽ là một hàng gồm các thông tin quan trọng của Round
        Bao gồm: mode, answer, status, date
        """
        def __init__(self, order, round, center_y, align_text = "left", draw_frame = True):
            self.order = order
            self.mode = round.mode
            self.answer = round.answer
            self.status = round.status
            self.date = round.date

            # Các box chứa các thông tin trên
            self.order_box = Box(ORDER_CENTER_X, center_y, ORDER_WIDTH, ROUNDBAR_HEIGHT, str(self.order))
            self.mode_box = Box(MODE_CENTER_X, center_y, MODE_WIDTH, ROUNDBAR_HEIGHT, self.mode, align_text = align_text)
            self.answer_box = Box(ANSWER_CENTER_X, center_y, ANSWER_WIDTH, ROUNDBAR_HEIGHT, self.answer, align_text = align_text)
            self.status_box = Box(STATUS_CENTER_X, center_y, STATUS_WIDTH, ROUNDBAR_HEIGHT, self.status, align_text = align_text)
            self.date_box = Box(DATE_CENTER_X, center_y, DATE_WIDTH, ROUNDBAR_HEIGHT, self.date, align_text = align_text)
            
            # Vẽ viền cho tất cả nếu draw_frame = True, không vẽ tất cả nếu draw_frame = False
            self.order_box.draw_frame = self.mode_box.draw_frame = self.answer_box.draw_frame\
                = self.status_box.draw_frame = self.date_box.draw_frame = draw_frame 

            self.active = True # hàng có hoạt động không (không hoạt động khi mở hộp thoại RoundBar)
            self.chosen = False # hàng có được người chơi chọn không

        def mouse_collides(self):
            # Kiểm tra chuột có ở trên hàng không
            if not self.active: 
                return False

            # Một box có chuột thì cả RoundBar có chuột
            return self.order_box.mouse_collides() or self.mode_box.mouse_collides() or self.answer_box.mouse_collides() or self.status_box.mouse_collides() or self.date_box.mouse_collides()

        def change_color(self, box_color, text_color):
            # Hàm đổi màu: màu nền của các box thành box_color, màu chữ thành text_color
            self.order_box.color = self.mode_box.color = self.answer_box.color = self.status_box.color = self.date_box.color = box_color
            self.order_box.update_text(self.order_box.text, text_color)
            self.mode_box.update_text(self.mode_box.text, text_color)
            self.answer_box.update_text(self.answer_box.text, text_color)
            self.status_box.update_text(self.status_box.text, text_color)
            self.date_box.update_text(self.date_box.text, text_color)

        def draw(self, screen): # Vẽ lên screen
            if self.active: # Nếu hàng hoạt động
                if self.chosen: # Được chọn thì nền xanh lá, chữ trắng
                    self.change_color(GREEN, "white")
                elif self.mouse_collides(): # có chuột ở trên thì nền xám, chữ đen
                    self.change_color(BUTTON_MOUSE, "black")
                else: # không có chuột thì nền trắng chữ đen
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
        """
        RoundBox là hộp thoại hiện các thông tin của Round, bao gồm:
            mode, answer, time, history
            grid: các từ người chơi đã điền và tính đúng sai của các kí tự trong các từ
        """
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
            self.to_draw = False # Nếu True thì vẽ RoundBox, False thì không vẽ

        def handle_event(self, event):
            if left_mouse_click(event):
                if self.exit.mouse_collides():
                    self.to_draw = False # Nếu nhấn chuột trái vào RoundBox thì kết thúc vẽ

        def draw(self, screen): # Vẽ lên screen
            if self.to_draw:
                self.frame.draw(screen)
                self.grid.draw(screen)
                self.exit.draw(screen)
                self.mode_box.draw(screen)
                self.answer_box.draw(screen)
                self.time_box.draw(screen)

    def __init__(self, manager):
        self.manager = manager # Manager của trò chơi, cũng là Manager của Scene

        self.frame = Box(SCREEN_CENTER_X + 20, SCREEN_CENTER_Y, 1080, 630) # Khung viền
        self.title = Box(SCREEN_CENTER_X + 20, 110, 1080, 70, "TEN LATEST ROUNDS") # Tiêu đề
        # Box tiêu đề không vẽ nền lẫn viền
        self.title.draw_frame = False 
        self.title.draw_back = False
        self.backbutton = BackButton() # Nút trở về

        # Thanh "chỉ loại" - là thanh đầu tiên trong Scene chỉ thông tin của các cột
        # typebar sẽ hiện: TOP, MODE, ANSWER, WIN/LOSE, TIME AND DATE
        self.typebar = self.RoundBar(
            "Top",
            self.Round("Mode", "Answer", None, None, "Win/Lose", "Time and Date"),
            center_y = 120 + (ROUNDBAR_HEIGHT + ROUNDBAR_GAP),
            align_text = "mid",
            draw_frame = False
        )
        # Danh sách các round, roundbar, roundbox của Scene
        self.rounds = []
        self.roundbars = []
        self.roundboxes = []
        self.loaded = False # loaded = True nếu đã tải dữ liệu round lên, False nếu ngược lại
        self.draw_roundbox = False # chỉ việc có RoundBox đang được vẽ hay chưa

    def up_rounds(self):
        # Hàm tải dữ liệu các round của người chơi lên để hiện lên History Scene
        # Một round được lưu trữ dạng: username|mode|answer|history|time|status|date
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

                if (status != "NotDone"):
                    round = self.Round(mode, answer, history, time, status, date)
                    self.rounds.append(round)

        self.rounds.reverse() # Đảo ngược để lấy round gần đây nhất trước
        for i in range(min(10, len(self.rounds))):
            self.roundbars.append(self.RoundBar(i + 1, self.rounds[i], 120 + (i + 2) * (ROUNDBAR_HEIGHT + ROUNDBAR_GAP)))
            self.roundboxes.append(self.RoundBox(self.rounds[i]))

    def get_clicked_round(self):
        # Tìm round đã được nhấn vào
        for i in range(len(self.roundbars)):
            if self.roundbars[i].mouse_collides():
                return i
        return None

    def get_chosen_round(self):
        # Tìm round đã được chọn
        for i in range(len(self.roundbars)):
            if self.roundbars[i].chosen:
                return i
        return None

    def draw(self, screen): # Vẽ lên screen
        self.frame.draw(screen)
        self.title.draw(screen)
        self.backbutton.draw(screen)

        for roundbar in self.roundbars:
            roundbar.draw(screen)

        self.typebar.draw(screen)

        if self.draw_roundbox:
            # Khi vẽ RoundBox thì màn hình ngoài RoundBox phải mờ đen
            dark_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            dark_surf.fill("black")
            dark_surf.set_alpha(200)
            screen.blit(dark_surf, (0, 0))
            
            round = self.get_chosen_round()
            self.roundboxes[round].draw(screen)

    def handle_backbutton(self, event): # Xử lí khi nhấn nút BackButton
        if self.backbutton.is_clicked(event):
            self.manager.state = "start"

    def deactivate(self): # Vô hiệu hóa tính hoạt động của tất cả nút/round trong Scene
        self.backbutton.active = False
        self.typebar.active = False
        for i in range(len(self.roundbars)):
            self.roundbars[i].active = False
        
    def activate(self): # Bật tính hoạt động của tất cả nút/round trong Scene
        self.backbutton.active = True
        self.typebar.active = False
        for i in range(len(self.roundbars)):
            self.roundbars[i].active = True

    def run(self, screen, events): # Chạy scene

        # Nếu chưa tải dữ liệu thì tải
        if self.loaded == False:
            self.up_rounds()
            self.loaded = True # Tải rồi thì không tải nữa

        screen.fill('white')
        
        for event in events:
            if self.draw_roundbox: # Nếu đang hiện RoundBox
                self.deactivate() # vô hiệu hóa các nút/round
                round = self.get_chosen_round()
                roundbar = self.roundbars[round]
                roundbox = self.roundboxes[round]

                # Nếu chuột trái vào nút Exit hoặc vào vị trí ngoài RoundBox thì tắt RoundBox
                if left_mouse_click(event):
                    if roundbox.exit.mouse_collides() or roundbox.frame.mouse_collides() == False:
                        self.draw_roundbox = False
                        roundbox.to_draw = False
                        roundbar.chosen = False
            else:
                self.activate() # kích hoạt các nút/round
                self.handle_backbutton(event) # xử lí tình huống nhấn vào BackButton
                if left_mouse_click(event):
                    round_clicked = self.get_clicked_round() # Tìm round đã được chọn
                    if round_clicked is not None:
                        # Nếu có round được chọn thì vẽ RoundBox tương ứng
                        self.draw_roundbox = True
                        self.roundbars[round_clicked].chosen = True
                        self.roundboxes[round_clicked].to_draw = True

        self.draw(screen)
