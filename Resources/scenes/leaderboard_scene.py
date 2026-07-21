import pygame
from ui import Box, TextBox, BackButton
from utils import left_mouse_click, sort_func
from config import *

class LeaderboardScene:
    """
    Lớp LeaderboardScene quản lí và hiển thị màn hình bảng xếp hạng (Leaderboard Scene)
    """
    class Button:
        """
        Lớp Button tương ứng với nút chọn chế độ để hiện bảng xếp hạng của chế độ tương ứng
        """
        def __init__(self, text = "Text", size = 30, center_x = -1, center_y = 0, left = -1, right = -1):
            self.box = TextBox(text, size, center_x = center_x, center_y = center_y, left = left, right = right, curve = False)
            self.is_clicked = False # Kiểm tra xem nút được nhấn/được chọn hay chưa

        def draw(self, screen):
            # Vẽ lên screen
            if self.is_clicked:
                self.box.change_color("white", GREEN) # Khi được nhấn thì nền green, chữ trắng
            else:
                if self.box.mouse_collides():
                    self.box.change_color("black", BUTTON_MOUSE) # Khi có chuột ở trên thì nền xám, chữ đen
                else:
                    self.box.change_color("black", "white") # nền trắng, chữ đen
            self.box.draw(screen)

    class Leaderboard:
        """
        Lớp tương ứng với một bảng xếp hạng của một chế độ
        """
        class Rank:

            """
            Lớp tương ứng với một hạng của bảng xếp hạng
            Một Rank sẽ bao gồm: top (thứ hạng), user (tên người dùng), score (điểm số), và các box tương ứng ba thông tin trên.
            """

            def __init__(self, top, user, score, center_y):
                self.top = top
                self.user = user
                self.score = score

                # Tạo các box tương ứng với ba thuộc tính trên để vẽ
                self.top_box = Box(TOP_CENTER_X, center_y, TOP_WIDTH, RANKBOX_HEIGHT, str(self.top))
                self.user_box = Box(USER_CENTER_X, center_y, USER_WIDTH, RANKBOX_HEIGHT, self.user)
                self.score_box = Box(SCORE_CENTER_X, center_y, SCORE_WIDTH, RANKBOX_HEIGHT, f"{self.score:.2f}s")

            def draw(self, screen): # Vẽ Rank lên screen
                # Nếu chuột ở trên Rank thì đổi màu: nền xanh lá, chữ trắng
                if (self.top_box.mouse_collides() or self.user_box.mouse_collides() or self.score_box.mouse_collides()):
                    self.top_box.color = self.user_box.color = self.score_box.color = GREEN
                    self.top_box.update_text(self.top_box.text, "white")
                    self.user_box.update_text(self.user_box.text, "white")
                    self.score_box.update_text(self.score_box.text, "white")
                else: # Nếu không thì hiện như mặc định là nền trắng, chữ đen
                    self.top_box.color = self.user_box.color = self.score_box.color = "white"
                    self.top_box.update_text(self.top_box.text, "black")
                    self.user_box.update_text(self.user_box.text, "black")
                    self.score_box.update_text(self.score_box.text, "black")

                self.top_box.draw(screen)
                self.user_box.draw(screen)
                self.score_box.draw(screen)

        def __init__(self, mode):
            """
            Một Leaderboard gồm:
            frame: Khung viền của Leaderboard
            title: Tiêu đề của Leaderboard, sẽ ghi "Leaderboard"
            mode: Chế độ của Leaderboard
            ranks: Danh sách các Rank của Leaderboard
            """
            self.frame = Box(SCREEN_CENTER_X + 20, SCREEN_CENTER_Y, 1080, 630)
            self.title = Box(SCREEN_CENTER_X, 130, 1080, 70, "LEADERBOARD")
            # Box của Title không vẽ nền lẫn viền
            self.title.draw_frame = False
            self.title.draw_back = False
            
            self.mode = mode
            self.ranks = []
            self.to_load_ranks = True # chỉ việc cần tải các Rank từ file lưu trữ hay không (True là cần)
            self.to_draw = False # chỉ việc có vẽ Leaderboard hay không, tức Leaderboard này có được chọn hay không

        def load_ranks(self): # Tải dữ liệu rank từ file lưu trữ "round.txt"
            # Hàm sẽ tổng kết các round đã thắng của tất cả người chơi
            # Và tính điểm của từng người chơi là: "Tổng thời gian chơi các ván thắng" / "Số ván thắng"
            # Sau đó, các Rank sẽ được tạo thành và được sắp xếp theo điểm tăng dần
            self.ranks.clear() # Luôn xóa ranks để tránh trường hợp chồng lặp
            
            # Danh sách các người dùng có ván thắng, tổng thời gian chơi các ván thắng, số ván thắng
            users = []
            scores = []
            count = []

            with open("round.txt", "r") as round_file:
                while True:
                    round = round_file.readline()
                    if not round: # round là xâu rỗng thì dừng đọc file
                        break
                    round = round[:-1].split("|")
                    mode = round[1]
                    if (mode != self.mode): # Khác chế độ được chọn thì không xét round này
                        continue
                    user = round[0]
                    round_win = round[5]
                    score = int(round[4])
                    if round_win == "Win":
                        # Bổ sung các round mà thắng
                        if user not in users:
                            users.append(user)
                            scores.append(score)
                            count.append(1)
                        else:
                            index = users.index(user)
                            scores[index] += score
                            count[index] += 1

            temp = [] # temp là danh sách tạm, dùng để sắp xếp các Rank theo điểm tăng dần
            for i in range(len(users)):
                temp.append((users[i], scores[i] / float(count[i])))
            temp.sort(key = sort_func) # Sắp xếp lại temp theo điểm tăng dần

            # Thêm các Rank vào self.ranks
            for i in range(len(temp)): 
                self.ranks.append(self.Rank(i + 1, temp[i][0], temp[i][1] / 1000, 200 + i * (RANKBOX_HEIGHT + RANKBOX_GAP)))

            # Tạo Rank rỗng khi chưa đủ 10 Rank
            while (len(self.ranks) < 10):
                self.ranks.append(self.Rank(len(self.ranks) + 1, "", 0, 200 + len(self.ranks) * (RANKBOX_HEIGHT + RANKBOX_GAP)))

        def draw(self, screen): # vẽ lên screen
            if self.to_load_ranks:
                self.load_ranks()
                self.to_load_ranks = False
            self.frame.draw(screen)
            self.title.draw(screen)

            for i in range(min(10, len(self.ranks))): # Chỉ vẽ tối đa 10 Rank
                self.ranks[i].draw(screen)     

    def __init__(self, manager):
        self.manager = manager # Manager của Scene
        
        # Các nút và bảng xếp hạng tương ứng của từng chế độ
        self.english_button = self.Button("English", size = 20, left = 126, center_y = 45)
        self.english_lb = self.Leaderboard("English") # Leaderboard của chế độ English
        self.english_button.is_clicked = True # Mặc định mới vào thì sẽ hiện bảng tiếng Anh
        
        self.vnese_button = self.Button("Vietnamese", size = 20, left = self.english_button.box.back_rect.right + 5, center_y = 45)
        self.vnese_lb = self.Leaderboard("Vietnamese")

        self.math_button = self.Button("Math", size = 20, left = self.vnese_button.box.back_rect.right + 5, center_y = 45)
        self.math_lb = self.Leaderboard("Math")

        self.backbutton = BackButton() # Nút thoát khỏi màn hình và về Start Scene

    def run(self, screen, events):
        # Hàm chạy Scene, nhận tham số là màn hình screen và events - các event diễn ra trong quá trình chơi

        screen.fill('white')
        self.backbutton.draw(screen)

        for event in events:
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE): # Nếu bấm nút Esc thì thoát về Start Scene
                self.manager.state = "start"
            if left_mouse_click(event):
                if (self.backbutton.box.mouse_collides()): # Nếu bấm nút BackButton thì thoát về Start Scene
                    self.manager.state = "start"
                elif (self.english_button.box.mouse_collides()): # Nếu chọn chế độ tiếng Anh thì chỉ hiện Leaderboard tiếng Anh
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

        # Tải dữ liệu và vẽ bảng xếp hạng tương ứng với chế độ
        if self.english_button.is_clicked: # Nếu chọn chế độ tiếng Anh
            self.english_lb.to_load_ranks = True # Tải dữ liệu tiếng Anh
            self.english_lb.draw(screen) # Vẽ Leaderboard tiếng Anh
        elif self.vnese_button.is_clicked:
            self.vnese_lb.to_load_ranks = True
            self.vnese_lb.draw(screen)
        elif self.math_button.is_clicked:
            self.math_lb.to_load_ranks = True
            self.math_lb.draw(screen)
        
        # Vẽ các nút chế độ
        self.english_button.draw(screen)
        self.vnese_button.draw(screen)
        self.math_button.draw(screen)
  