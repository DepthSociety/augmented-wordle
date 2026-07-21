import pygame
from ui import Box
from config import *
from utils import *


class LoginScene:
    """
    Lớp LoginScene tương ứng với màn hình đăng nhập của trò chơi
    """
    class UserBox:
        """
        Lớp UserBox tương ứng với một "thành phần" đóng vai trò xử lí việc nhập tên người dùng từ người chơi.
        Các thuộc tính:
            type_box (ui.Box): Box chứa và hiện tiêu đề của UserBox, mặc định tiêu đề là "Username".
            imp_box (ui.Box): Box dùng để nhận và hiện đầu vào từ người chơi là tên người dùng được nhập vào.
            warning (ui.Box): Box dùng để chứa và hiện các cảnh báo liên quan tới tên người dùng, gòm: quá 20 kí tự, kí tự không hợp lệ
            text (str): Văn bản chứa trong UserBox, tức tên người dùng được nhập vào
            active (bool): Kiểm tra xem UserBox đã được chọn hay chưa để nhận đầu vào (active = True là đã được chọn) 
        """
        def __init__(self, center_y):
            # Tất cả các ô đều sẽ vẽ ở trung tâm màn hình theo chiều x
            self.type_box = Box(SCREEN_CENTER_X, center_y, 415, 30, "Username", align_text = "left") # Mặc định type_box có kích thước 415 x 30
            self.type_box.draw_frame = False # Box chứa tiêu đề "Username" không vẽ viền

            self.inp_box = Box(SCREEN_CENTER_X, center_y + self.type_box.height // 2 + 15, 400, 30, align_text = "left") # Mặc định inp_box có kích thước 415 x 30

            self.warning = Box(SCREEN_CENTER_X, self.inp_box.center_y + self.inp_box.height // 2 + 10, 415, 20, align_text = "left") 
            self.warning.draw_frame = False # Không vẽ viền
            self.warning.update_text(self.warning.text, color = "red") # Warning thì chữ màu đỏ

            self.text = ""
            self.active = False

        def empty(self):
            # Kiểm tra xem tên người dùng có trống không
            return len(self.inp_box.text) == 0

        def update_warning(self):
            # Hàm cập nhật nội dung waring
            new_warning = ""
            if (len(self.text) > 20):
                new_warning = "Username must not have more than 20 characters"
            else:
                # Tìm xem có ít nhất một kí tự không hợp lệ hay không
                for char in self.text:
                    if (char.isalpha() == False) and (char.isnumeric() == False): # Nếu char không phải chữ và không phải số
                        new_warning = "Username must only have numbers and/or English letters"
                        break
            
            # Cập nhật nội dung
            if (new_warning != self.warning.text):
                self.warning.update_text(new_warning, color = "red")

        def draw(self, screen):
            # Hàm vẽ UserBox lên màn hình screen
            self.update_warning()
            
            # Hộp inp_box đổi màu khi được người dùng nhấn chuột vào (nếu trước đó chưa được nhấn vào)
            if (self.active):
                self.inp_box.frame_color = "black"
            else:
                self.inp_box.frame_color = FRAME_NOT_CLICKED

            self.type_box.draw(screen)
            self.inp_box.draw(screen)
            self.warning.draw(screen)
        
        def handle_event(self, event):
            # Hàm xử lí các sự kiện event trong quá trình chơi, gồm: nhấn chuột và nhấn phím
            self.update_warning() # Luốn cập nhật warning
            if left_mouse_click(event):
                if self.inp_box.rect.collidepoint(event.pos): # Nếu người dùng nhấn chuột trái vào inp_box
                    self.active = True # Nếu nhấn chuột vào thì UserBox được bật, cho phép nhận đầu vào
                else:
                    self.active = False
            if (event.type == pygame.KEYDOWN): # Nếu event là nhấn phím xuống
                if (self.active):
                    if (event.unicode and event.unicode.isprintable()): # Nếu phím được nhấn là kí tự hợp lệ và in được
                        # Thêm kí tự event.unicode vào UserBox
                        self.inp_box.text += event.unicode
                        self.text += event.unicode
                        self.inp_box.update_text(self.inp_box.text) # Cập nhật lại inp_box
                    elif (event.key == pygame.K_BACKSPACE): # Nếu phím được nhấn là nút Backspace
                        # Xóa kí tự cuối cùng trong UserBox
                        self.inp_box.text = self.inp_box.text[:-1]
                        self.text = self.text[:-1]
                        self.inp_box.update_text(self.inp_box.text)

    class PassBox:
        """
        Lớp PassBox tương ứng với một "thành phần" đóng vai trò xử lí việc nhập tên người dùng từ người chơi.
        Tuy nhiên, khác với UserBox, xâu được hiển thị lên màn hình chỉ chứa dấu sao "*".

        Các thuộc tính:
            type_box (ui.Box): Box chứa và hiện tiêu đề của UserBox, mặc định tiêu đề là "Username".
            imp_box (ui.Box): Box dùng để nhận và hiện đầu vào từ người chơi là tên người dùng được nhập vào.
            warning (ui.Box): Box dùng để chứa và hiện các cảnh báo liên quan tới tên người dùng, gòm: quá 20 kí tự, kí tự không hợp lệ
            text (str): Văn bản chứa trong UserBox, tức tên người dùng được nhập vào
            active (bool): Kiểm tra xem UserBox đã được chọn hay chưa để nhận đầu vào (active = True là đã được chọn) 
        """
        def __init__(self, center_y):
            self.type_box = Box(SCREEN_WIDTH // 2, center_y, 415, 30, "Password", align_text = "left")
            self.type_box.draw_frame = False

            self.inp_box = Box(SCREEN_WIDTH // 2, center_y + self.type_box.height // 2 + 15, 400, 30, align_text = "left")

            self.warning = Box(SCREEN_CENTER_X, self.inp_box.center_y + self.inp_box.height // 2 + 10, 415, 20, align_text = "left")
            self.warning.draw_frame = False
            self.warning.update_text(self.warning.text, color = "red")

            self.text = ""
            self.active = False

        # Các hàm phương thức ở dưới cách hoạt động tương tự UserBox

        def empty(self): # Kiểm tra mật khẩu có rỗng không
            return len(self.inp_box.text) == 0

        def update_warning(self): # Cập nhật cảnh báo
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

        def draw(self, screen): # Vẽ lên screen
            self.update_warning()
            if (self.active):
                self.inp_box.frame_color = "black"
            else:
                self.inp_box.frame_color = FRAME_NOT_CLICKED

            self.type_box.draw(screen)
            self.inp_box.draw(screen)
            self.warning.draw(screen)
        
        def handle_event(self, event):
            # Hàm xử lí các sự kiện event trong quá trình chơi, gồm: nhấn chuột và nhấn phím
            if left_mouse_click(event): # Nếu event là nhấn chuột trái
                if self.inp_box.rect.collidepoint(event.pos): # Nếu người dùng nhấn chuột trái vào inp_box
                    self.active = True # Nếu nhấn vào thì "Bật"
                else:
                    self.active = False
            if (event.type == pygame.KEYDOWN): # Nếu event là nhấn phím
                if (self.active): # Chỉ khi PassBox được "chọn" thì mới xử lí đầu vào
                    if (event.unicode and event.unicode.isprintable()): # Nếu phím nhập vào là kí tự in được
                        # Thêm kí tự event.unicode vào PassBox, nhưng hiển thị trên màn hình là thêm dấu *
                        self.inp_box.text += "*"
                        self.text += event.unicode
                        self.inp_box.update_text(self.inp_box.text)
                    elif (event.key == pygame.K_BACKSPACE):
                        # Xóa kí tự cuối cùng trong PassBox
                        self.inp_box.text = self.inp_box.text[:-1]
                        self.text = self.text[:-1]
                        self.inp_box.update_text(self.inp_box.text)
    """
    Các thuộc tính của LoginScene:
        manager (Manager): class quản lí của trò chơi
        frame (Box): khung vẽ giao diện đăng kí/đăng nhập của Login Scene
        user_box (UserBox): hộp xử lí nhập tên người dùng
        pass_box (PassBox): hộp xử lí nhập mật khẩu
        login (Box): nút đăng nhập - Login
        register (Box): nút đăng kí - Register
        error (Box): Box biểu diễn lỗi khi đăng nhập/đăng kí (nếu có) hoặc thông báo đăng kí thành công
    """
    def __init__(self, manager):
        self.manager = manager
        self.frame = Box(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 550, 350)
        
        self.user_box = self.UserBox(270)
        self.pass_box = self.PassBox(270 + 100)

        self.login = Box(SCREEN_CENTER_X - 10 - 190 // 2, SCREEN_CENTER_Y + 120, 190, 30, "Login")
        self.login.color = BUTTON_NO_MOUSE

        self.register = Box(SCREEN_CENTER_X + 10 + 190 // 2, SCREEN_CENTER_Y + 120, 190, 30, "Register")
        self.register.color = BUTTON_NO_MOUSE

        self.error = Box(SCREEN_CENTER_X, SCREEN_CENTER_Y + 85, 500, 25)
        self.error.draw_frame = False
        self.error.text_color = "red"

    def restart(self):
        # Khởi động lại màn hình đăng nhập
        # Được dùng mỗi khi một người chơi đăng xuất
        self.__init__(self.manager)

    def draw(self, screen):
        # Vẽ lên screen
        self.frame.draw(screen)
        self.user_box.draw(screen)
        self.pass_box.draw(screen)

        self.login.color = BUTTON_MOUSE if self.login.mouse_collides() else BUTTON_NO_MOUSE
        self.register.color = BUTTON_MOUSE if self.register.mouse_collides() else BUTTON_NO_MOUSE

        self.login.draw(screen)
        self.register.draw(screen)
        self.error.draw(screen)
    
    def handle_register(self):
        # Hàm xử lí quá trình đăng kí
        username = self.user_box.text # Lấy username
        password = self.pass_box.text # Lấy password

        if not username: # Thiếu username
            self.error.update_text("Username is missing", color = "red")
        elif not password: # Thiếu password
            self.error.update_text("Password is missing", color = "red")
        else:
            if username not in usernames: # username chưa được dùng để tạo tài khoản
                if self.pass_box.warning.text == "" and self.user_box.warning.text == "": # Nếu không có warning ở cả user_box và pass_box
                    # Thêm vào danh sách usernames và passwords
                    usernames.append(username)
                    passwords.append(password)
                    with open("users.txt", "a") as file:
                        file.write(f"{username}|{password}\n") # Lưu trữ username và password vào file
                    self.error.update_text("Registration succeed", color = GREEN) # Thông báo đăng kí thành công
                elif self.user_box.warning.text: # user_box có warning thì username không hợp lệ
                    self.error.update_text("Invalid username", color = "red")
                else: # pass_box có warning thì password không hợp lệ
                    self.error.update_text("Invalid password", color = "red")
            else:
                # username đã được dùng để tạo tài khoản
                self.error.update_text("Username already exists", color = "red")

    def handle_login(self):
        # Hàm xử lí quá trình đăng nhập
        username = self.user_box.text
        password = self.pass_box.text

        if not username: # Thiếu username
            self.error.update_text("Username is missing", color = "red")
        elif not password: # Thiếu password
            self.error.update_text("Password is missing", color = "red")
        else:
            if username not in usernames: # Không có tài khoản có tên người dùng là username
                self.error.update_text("Account does not exist", color = "red")
            else:
                # Tìm mật khẩu tương ứng của username
                index = usernames.index(username)
                if (password != passwords[index]): # Không khớp thì sai mật khẩu
                    self.error.update_text("Wrong password", color = "red")
                else: # Khớp thì chuyển sang màn hình bắt đầu Start Scene
                    self.manager.state = "start"
                    self.manager.username = username
                    self.__init__(self.manager)

    def run(self, screen, events):
        # Hàm chạy màn hình
        screen.blit(background, background.get_rect(center = (SCREEN_CENTER_X, SCREEN_CENTER_Y))) # Vẽ tệp ảnh background làm nền

        for event in events:
            self.user_box.handle_event(event) # Xử lí event trên user_box
            self.pass_box.handle_event(event) # Xử lí event trên pass_box

            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_RETURN): # Nếu enter thì tương đương với đăng nhập
                    self.handle_login()

            if left_mouse_click(event):
                if (self.login.mouse_collides()): # Nếu nhấn nút Login thì đăng nhập
                    self.handle_login()
                elif (self.register.mouse_collides()): # Nếu nhấn nút Register thì đăng kí
                    self.handle_register()

        self.draw(screen) # Luôn vẽ LoginScene lên màn hình screen
