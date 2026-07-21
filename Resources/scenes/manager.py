from scenes.login_scene import LoginScene
from scenes.game_scene import GameScene
from scenes.start_scene import StartScene
from scenes.history_scene import HistoryScene
from scenes.leaderboard_scene import LeaderboardScene

class Manager:
    """
    Lớp Manager có vai trò quản lí và điều phối các màn hình của trò chơi.
    Lớp quyết định là trò chơi sẽ ở màn hình nào thông qua thuộc tính state.
    Ngoài ra, Manager sẽ bao gồm các thuộc tính là các màn hình của trò chơi
    """
    def __init__(self):
        self.state = "login" # Luôn khởi tạo là bắt đầu bằng màn hình đăng nhập
        self.username = "" # Tên người dùng của manager
        self.login = LoginScene(self)
        self.start = StartScene(self)
        self.game = GameScene(self)
        self.history = HistoryScene(self)
        self.leaderboard = LeaderboardScene(self)
        
    
    def run(self, screen, events):
        # Hàm chạy trò chơi
        # State là gì thì chạy màn đó
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
