import pygame
from config import *
from utils import *

class StartScene:
    """
    Lớp StartScene quản lí và hiển thị màn hình chính của trò chơi
    """
    class Button:
        """
        Lớp Button tương ứng với một nút trên Start Scene
        Các thuộc tính:
            center_x, center_y (int): tọa độ trung tâm của nút
            text (str): văn bản của nút
            
            font, text_surf, text_rect: các thành phần cần thiết để vẽ văn bản
            width, height, left, top (int): chiều rộng, chiều cao, biên trái, biên trên của nút
            active (bool): nút có hoạt động hay không
        """
        def __init__(self, center_x, center_y, text = "", size = 40):
            self.center_x = center_x
            self.center_y = center_y

            self.text = text
            self.font = get_font(size)
            self.text_surf = self.font.render(self.text, True, "black")
            self.text_rect = self.text_surf.get_rect(center = (center_x, center_y))
            
            self.rect = pygame.Rect(self.text_rect.x - 5, self.text_rect.y, self.text_rect.w + 10, self.text_rect.h) # Hình chữ nhật pygame.Rect tương ứng của nút
            self.width = self.rect.w
            self.height = self.rect.h
            self.left = self.rect.x
            self.top = self.rect.y
            self.active = True
            # self.mouse_here = False

        def draw(self, screen):
            # Vẽ nút lên screen
            if (self.active): # Nếu nút được hoạt động
                mouse_here = self.rect.collidepoint(pygame.mouse.get_pos()) # Chuột có ở trên nút hay không
                rect_color = "white"
                text_color = "black"
                if (mouse_here):
                    # Chuột ở trên nút thì đổi màu từ trắng - đen sang GREEN - trắng
                    rect_color, text_color = "#538d4e", "white"
            else:
                # Làm mờ nút
                rect_color = "white"
                text_color = WORDLE_GREY

            self.text_surf = self.font.render(self.text, True, text_color)
            self.text_rect = self.text_surf.get_rect(center = (self.center_x, self.center_y))

            # Vẽ nút lên màn hình screen
            pygame.draw.rect(screen, rect_color, self.rect)
            screen.blit(self.text_surf, self.text_rect)


    def __init__(self, manager):
        self.manager = manager # Manager quản lí trò chơi

        # Các nút của Start Scene
        self.new_game = self.Button(SCREEN_WIDTH // 2, 200, "NEW GAME")
        self.resume = self.Button(SCREEN_WIDTH // 2, self.new_game.center_y + self.new_game.height // 2 + 60, "RESUME")
        self.ranking = self.Button(SCREEN_WIDTH // 2, self.resume.center_y + self.resume.height // 2 + 60, "LEADERBOARD")
        self.history = self.Button(SCREEN_WIDTH // 2, self.ranking.center_y + self.ranking.height // 2 + 60, "HISTORY")
        self.log_out = self.Button(SCREEN_WIDTH // 2, self.history.center_y + self.history.height // 2 + 60, "LOG OUT")

    def check_resume(self):
        """
        Kiểm tra người dùng đã từng chơi round nào hay chưa,
        với biến has_save chỉ kết quả kiểm tra: True là đã có round, False là không có

        has_save sẽ được gán vào thuộc tính self.resume.active
        """
        has_save = False
        try:
            with open("round.txt", "r", encoding = "utf-8") as file:
                rounds = file.readlines()
                # Duyệt ngược để tìm round mới nhất
                for round in reversed(rounds):
                    data = round.strip().split("|")
                    # Kiểm tra đúng định dạng và tên người dùng
                    if len(data) >= 7 and data[0] == self.manager.username:
                        has_save = True
                        break
        except FileNotFoundError:
            has_save = False
        
        # Cập nhật trạng thái cho nút Resume
        self.resume.active = has_save

    def draw(self, screen): # Vẽ lên screen
        self.new_game.draw(screen)
        self.resume.draw(screen)
        self.ranking.draw(screen)
        self.history.draw(screen)
        self.log_out.draw(screen)

    def run(self, screen, events):
        self.check_resume() # Luôn kiểm tra xem resume đã được hoạt động chưa
        screen.fill("white")

        for event in events:
            if left_mouse_click(event):
                if self.new_game.rect.collidepoint(event.pos): # Nhấn chuột trái lên nút NEW GAME
                    # Tạo Game Scene mới và chuyển sang Game Scene
                    self.manager.game.restart()
                    self.manager.state = "game"
                elif self.resume.rect.collidepoint(event.pos):
                    # Nếu resume được thì chuyển sang màn Game Scene
                    if self.manager.game.resume():
                        self.manager.state = "game"
                    else:
                        self.resume.active = False
                elif self.ranking.rect.collidepoint(event.pos):
                    # Chuyển sang màn hình Leaderboard Scene
                    self.manager.state = "leaderboard"
                elif self.history.rect.collidepoint(event.pos):
                    # Chuyển sang màn hình History Scene
                    self.manager.history.loaded = False
                    self.manager.state = "history"
                elif self.log_out.rect.collidepoint(event.pos):
                    # Chuyển sang màn hình Login Scene
                    self.manager.login.restart()
                    self.manager.state = "login"

        self.draw(screen)
