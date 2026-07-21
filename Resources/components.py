import pygame
from config import FRAME_NOT_CLICKED, GREEN, YELLOW, WORDLE_GREY, BUTTON_MOUSE, BUTTON_NO_MOUSE
from ui import Box
from utils import compare

class WordleLine:

    """
    Lớp WordleLine tương ứng với một hàng của một Grid (lưới ô vuông) trong trò chơi Wordle.
    Các thuộc tính:
        center_x, center_y (int): tọa độ trung tâm
        size (int): số lượng ô của hàng, hay số lượng chữ của đáp án
        word (str): từ được chứa trong hàng
        answer (str): đáp án của hàng
        width (int): kích thước của một ô vuông trong hàng, mặc định là 60

        cur (int): con trỏ chỉ ô hiện tại đang xét, là ô mà chữ được điền vào
        entered (bool): chỉ việc hàng đã được Enter chưa, tức đã "chốt" đáp án chưa
        active (bool): chỉ việc hàng đã được xét chưa, hoặc chỉ việc hàng có được phép hoạt động không (True là có, False là không)

        boxes (list): danh sách chứa các Box (các ô) của hàng
    """

    def __init__(self, center_x, center_y, word = "", answer = "", width = 60):
        self.center_x = center_x
        self.center_y = center_y
        self.size = len(answer)
        self.word = word
        self.answer = answer
        self.cur = 0
        self.entered = False
        self.active = False

        # Khởi tạo danh sách ô self.boxes
        self.boxes = []
        for i in range(self.size):
            # Dựa vào tính chẵn lẻ của số ô (self.size) mà tọa độ của các ô được tính khác nhau, với công thức như ở dưới
            if (self.size & 1): # Nếu có số ô là số lẻ
                self.boxes.append(Box(self.center_x + (i - self.size // 2) * (width + 6), self.center_y, width, width))
                # 6 mặc định là khoảng cách giữa hai ô giáp nhau trong cùng 1 hàng
            else:
                if (i < self.size // 2):
                    self.boxes.append(Box(self.center_x - (6 // 2 + width // 2) + (i - self.size // 2 + 1) * (width + 6), self.center_y, width, width))
                else:
                    self.boxes.append(Box(self.center_x + (6 // 2 + width // 2) + (i - self.size // 2) * (width + 6), self.center_y, width, width))
    
    def mouse_collides(self):
        """
        Kiểm tra xem chuột có nằm ở trên bất cứ ô nào của hàng hay không
        """
        for box in self.boxes:
            if box.mouse_collides():
                return True
        return False
    
    def update_line(self, word, entered = True):

        """
        Hàm cập nhật từ được chứa trong hàng WordleLine thành word, với trạng thái entered.
        Trong đó:
            entered = True là hàng đã được tính và xét tính đúng sai
            entered = False là hàng chưa được tính, và vẫn chỉnh sửa được
        """

        self.word = word
        self.entered = entered
        for i in range(self.size):
            # Cập nhật văn bản trong ô thứ i (self.boxes[i])
            if (i >= len(self.word) or len(self.word) == 0):
                # i vượt ngoài độ dài của self.word hay self.word rỗng thì ô thứ i là ô rỗng
                self.boxes[i].update_text(text = "")
            else:
                self.boxes[i].update_text(text = word[i])

        self.cur = len(word) # Đưa con trỏ của hàng đến ô thứ len(word) - độ dài của word

    def add_char(self, char):
        """
        Hàm bổ sung chữ cho hàng WordleLine.
        Hàng được thêm chữ vào vị trí trái nhất chưa có chữ, là ô thứ self.cur
        """

        if (not self.entered) and self.active: # Nếu hàng vẫn còn thực hiện thao tác thêm/bớt chữ được 
            if (self.cur < self.size):
                self.word += char
                self.boxes[self.cur].update_text(text = char)
                self.cur += 1
    
    def backspace(self):
        """
        Hàm mô phỏng thao tác Backspace, tức xóa kí tự cuối cùng của từ chứa trong WordleLine
        """
        if (not self.entered) and self.active: # Nếu hàng vẫn còn thực hiện thao tác thêm/bớt chữ được 
            if (self.cur > 0):
                self.cur -= 1
                self.boxes[self.cur].update_text(text = "")
                self.word = self.word[:-1]

    def draw(self, screen):
        """
        Hàm vẽ WordleLine lên màn hình screen
        """
        if (self.entered): # Nếu hàng đã được "chốt"
            # Khi đó, ta đổi màu các ô của WordleLine tương ứng với trạng thái của từng chữ
            colors = compare(self.word, self.answer) # Lấy danh sách các màu sau khi so sánh self.word và self.answer
            for i in range(self.size):
                # Đổi màu và vẽ ô thứ i
                self.boxes[i].update_text(text = self.boxes[i].text, color = "white")
                self.boxes[i].color = colors[i]
                self.boxes[i].frame_color = "black"
                self.boxes[i].draw(screen)
        else: # Hàng chưa được "chốt"
            for i in range(self.size):
                # Đổi màu và vẽ ô thứ i
                self.boxes[i].update_text(text = self.boxes[i].text, color = "black")
                self.boxes[i].color = "white"
                if (i >= self.cur):
                    self.boxes[i].frame_color = FRAME_NOT_CLICKED # Vẽ mờ viền ô khi con trỏ chưa tới ô (i >= self.cur)
                else:
                    # Vẽ đen viền ô nếu hàng đã được xét và ô đã có chữ, ngược lại thì vẽ viền mờ
                    self.boxes[i].frame_color = "black" if self.active else FRAME_NOT_CLICKED 
                self.boxes[i].draw(screen)

class Grid:

    """
    Lớp Grid tương ứng với lưới ô vuông trong trò chơi Wordle.
    Các thuộc tính:
        num_lines = 6: Số hàng của Grid, mặc định là 6
        center_x, center_y (int): tọa độ trung tâm
        answer (str): từ đáp án của Grid
        cur_line (int): con trỏ trỏ tới hàng đang được xét trong Grid
        lines (list): danh sách các hàng của Grid
    """

    def __init__(self, center_x, center_y, answer, width = 60): # width là kích thước của một ô vuông
        self.num_lines = 6
        self.center_x = center_x
        self.center_y = center_y
        self.answer = answer
        self.cur_line = 0
        self.lines = []

        # Khởi tạo self.lines
        # Quá trình tương tự với khởi tạo WordleLine.boxes, khi tọa độ của một WordleLine phụ thuộc vào i
        for i in range(self.num_lines):
            if i < self.num_lines // 2:
                self.lines.append(WordleLine(self.center_x, self.center_y - (10 // 2 + width // 2) + (i - self.num_lines // 2 + 1) * (width + 10), "", answer, width))
            else:
                self.lines.append(WordleLine(self.center_x, self.center_y + (10 // 2 + width // 2) + (i - self.num_lines // 2) * (width + 10), "", answer, width)) 
    
    def mouse_collides(self):
        # Kiểm tra xem chuột có nằm trên một ô của Grid không
        for i in range(self.num_lines):
            if (self.lines[i].mouse_collides()): # Nếu có một hàng có chuột ở trên
                return True
        return False

    def draw(self, screen):
        # Vẽ Grid lên màn hình screen
        for i in range(self.num_lines): # Vẽ từng hàng trong Grid
            self.lines[i].draw(screen)
