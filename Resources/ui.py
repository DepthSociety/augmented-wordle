import pygame
from utils import get_font, left_mouse_click
from config import BUTTON_MOUSE, BUTTON_NO_MOUSE

class Box:

    """
    Lớp Box tạo một ô hình chữ nhật chứa văn bản trong pygame bao gồm nền của ô, khung của ô, và văn bản (nếu có). Trong đó:
        center_x, center_y (int): Tọa độ trung tâm của Box lần lượt theo chiều x và chiều y
        width, height (int): Chiều rộng và chiều dài của Box
        text (str): Văn bản nằm trong Box, mặc định là ""
        align_text (str): Trục căn chỉnh của text, nếu align_text = "left" thì văn bản căn lề trái, "mid" thì văn bản căn lề giữa (mặc định align_text = "mid")
        left, top, right, bottom (int): Lần lượt là tận cùng bên trái, bên trên, bên phải, bên dưới của Box

        surf (pygame.Surface): pygame.Surface tương ứng của Box, là nơi để vẽ Box
        rect (pygame.Rect): pygame.Rect tương ứng của Box
        color (str): Màu nền của Box
        frame_color (str): Màu khung của Box

        font: phông chữ của Box
        text_color: màu của văn bản của Box
        text_surf: pygame.Surface tương ứng của text, là nơi để vẽ text

    """

    def __init__(self, center_x = 0, center_y = 0, width = 0, height = 0, text = "", align_text = "mid", curve = False):
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

        self.curve = curve

        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect(center = (center_x, center_y))
        self.color = "white"
        self.frame_color = "black"
        
        self.font = get_font(min(self.width, self.height) * 2 // 3)
        self.text_color = "black"
        self.text_surf = self.font.render(self.text, True, self.text_color)

        font_size = min(self.width, self.height) * 2 // 3 # Kích thước của văn bản trong Box phải bằng 2 / 3 của min(self.width, self.height)

        # Sửa kích thước văn bản để vừa với Box
        if self.text_surf.get_rect(topleft = (0, 0)).width > self.width:
            while self.text_surf.get_rect(topleft = (0, 0)).width * 3 > 2 * self.width:
                font_size -= 1
                self.font = get_font(font_size)
                self.text_surf = self.font.render(self.text, True, self.text_color)

        self.text_rect = None
        # Canh lề văn bản
        if (self.align_text == "left"):
            self.text_rect = self.text_surf.get_rect(midleft = (self.left + 7, self.center_y))
        else:
            self.text_rect = self.text_surf.get_rect(center = (center_x, center_y))

        self.draw_frame = True # Nếu True thì vẽ khung, False thì không vẽ khung
        self.draw_back = True # Nếu True thì vẽ nền (back), False thì không

    def update_text(self, text = "", color = "black"):

        """
        Hàm cập nhật văn bản chứa trong Box về nội dung văn bản và màu của chữ.
        Tham số:
            text (str): văn bản mới, mặc định là ""
            color (str): màu mới của chữ, mặc định là "black"
        """

        self.text = text
        self.text_color = color
        self.text_surf = self.font.render(self.text, True, self.text_color).convert_alpha()
        self.text_rect = None
        if (self.align_text == "left"):
            self.text_rect = self.text_surf.get_rect(midleft = (self.left + 7, self.center_y))
        else:
            self.text_rect = self.text_surf.get_rect(center = (self.center_x, self.center_y))

    def mouse_collides(self):

        """
        Hàm kiểm tra xem vị trí của chuột có nằm trên Box không.
        Cụ thể, kiểm tra xem pygame.Rect của Box có giao với tọa độ của chuột (pygame.mouse.get_pos()) không
        """

        if (self.rect.collidepoint(pygame.mouse.get_pos())):
            return True
        return False

    def draw(self, screen):

        """
        Hàm vẽ Box lên màn hình screen
        """

        if (self.draw_back): # Thực hiện vẽ nền (nếu có)
            pygame.draw.rect(screen, self.color, self.rect, 0, border_radius = 5 if self.curve else 0)

        if (self.draw_frame): # Thực hiện vẽ khung (nếu có)
            pygame.draw.rect(screen, self.frame_color, self.rect, 2)
        
        # Vẽ văn bản lên screen
        screen.blit(self.text_surf, self.text_rect)

class TextBox:

    """
    Lớp TextBox tạo ra một hình chữ nhật chứa văn bản, kích thước dựa vào độ dài và độ lớn của văn bản (khác với Box khi được căn chỉnh trước)
    Gồm các thông tin:
        text (str): Nội dung văn bản của TextBox, mặc định là "Text"
        size (int): Kích thước chữ, mặc định là 40
        color (str): màu của chữ, mặc định là "black"
        back_color (str): màu của nền của TextBox, mặc định là BUTTON_NO_MOUSE
        center_x, center_y (int): tọa độ trung tâm của TextBox, mặc định là 0 và 0
        left, right: tọa độ biên trái và biên phải của TextBox, mặc định là -1 và -1

        curve (bool): nếu curve = True thì bo tròn bốn góc của TextBox, ngược lại thì không bo tròn

        font, font_surf, font_rect: phông chữ và các cấu trúc cần thiết để vẽ phông chữ trong Pygame

        back_surf, back_rect: cấu trúc dùng để vẽ nền của TextBox trong Pygame
    """

    def __init__(self, text = "Text", size = 40, color = 'black', back_color = BUTTON_NO_MOUSE, center_x = -1, center_y = 0, left = -1, right = -1, curve = True):
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

        # print(center_x, self.center_x)

        # Tính lại self.center_x, self.left và self.right tùy vào cách khởi tạo
        if self.center_x != -1:
            self.left = self.center_x - self.font_rect.width // 2
            self.right = self.center_x + self.font_rect.width // 2
            # print("CENTER")
        elif (self.left != -1):
            self.center_x = self.left + self.font_rect.width // 2
            self.right = self.left + self.font_rect.width
            self.font_rect = self.font_surf.get_rect(center = (self.center_x, self.center_y))
        elif (self.right != -1):
            self.center_x = self.right - self.font_rect.width // 2
            self.left = self.right - self.font_rect.width
            self.font_rect = self.font_surf.get_rect(center = (self.center_x, self.center_y))

        self.back_surf = pygame.Surface((self.font_rect.w + self.font_rect.h // 2, 3 * self.font_rect.h // 2))
        self.back_rect = self.back_surf.get_rect(center = (self.center_x, self.center_y))

        self.width = self.back_rect.w
        self.height = self.back_rect.h

    def draw(self, screen): # Vẽ TextBox lên màn hình screen
        pygame.draw.rect(screen, self.back_color, self.back_rect, 0, 5 if self.curve else 0)
        screen.blit(self.font_surf, self.font_rect)

    def update_text(self, text): # Cập nhật nội dung văn bản của TextBox
        self.__init__(text, self.size, self.color, self.back_color, self.center_x, self.center_y, self.left, self.right, self.curve)

    def change_color(self, color, back_color): # Đổi màu của TextBox: màu chữ thành color, màu nền thành back_color
        self.__init__(self.text, self.size, color, back_color, self.center_x, self.center_y, self.left, self.right, self.curve)

    def mouse_collides(self): # Kiểm tra xem chuột có nằm ở trên TextBox không
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
        self.box.draw_frame = False

    def draw(self, screen):
        """
        Vẽ nút BackButton lên màn hình screen.
        """

        # Nếu chuột ở trên nút thì nút có màu là BUTTON_MOUSE, nếu không thì nút có màu là BUTTON_NO_MOUSE

        if (self.box.mouse_collides() and self.active):
            self.box.color = BUTTON_MOUSE
        else:
            self.box.color = BUTTON_NO_MOUSE
        
        self.box.draw(screen)

    def mouse_collides(self): # Kiểm tra xem chuột có nằm ở trên BackButton không
        return self.box.mouse_collides()

    def is_clicked(self, event): # Kiểm tra xem sự kiện event có phải là bấm chuột trái lên BackButton không
        if left_mouse_click(event):
            return self.mouse_collides() and self.active

class Exit:
    """
    Lớp Exit tạo nút "X" thoát khỏi một hộp thông báo.
    Các thuộc tính:
        right (int): tọa độ biên phải
        top (int): tọa độ biên trên
        box (Box): Box tương ứng của Exit
    """

    def __init__(self, right, top):
        self.right = right
        self.top = top
        self.box = Box(right - 25, top + 25, 50, 50, "X") # Mặc định nút Exit có kích thước 50 x 50, do đó center_x = right - 25, center_y = top + 25
        self.box.draw_frame = False # Không vẽ khung đen của self.box

    def mouse_collides(self): # Kiểm tra xem chuột có ở trên nút Exit không
        return self.box.mouse_collides()

    def draw(self, screen): # Hàm vẽ Exit lên màn hình screen
        if (self.box.mouse_collides()):
            self.box.color = BUTTON_MOUSE
        else:
            self.box.color = "white"
        
        self.box.draw(screen)
