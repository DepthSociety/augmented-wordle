# Các tham số kích thước/tọa độ của màn hình screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2

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
RANKBOX_GAP = 7 # Khoảng cách giữa các ô của một RankBox
RANKBOX_WIDTH = TOP_WIDTH + USER_WIDTH + SCORE_WIDTH + 2 * RANKBOX_GAP
RANKBOX_HEIGHT = 40
TOP_CENTER_X = (SCREEN_WIDTH - RANKBOX_WIDTH) // 2 + TOP_WIDTH // 2 + 20 # Tọa độ của ô Top theo trục x
USER_CENTER_X = TOP_CENTER_X + TOP_WIDTH // 2 + RANKBOX_GAP + USER_WIDTH // 2
SCORE_CENTER_X = USER_CENTER_X + USER_WIDTH // 2 + RANKBOX_GAP + SCORE_WIDTH // 2

# Các tham số kích thước/tọa độ của các ô của một RoundBar (Thanh chỉ lịch sử)
# Trong đó, các ô của RoundBar bao gồm: Order (thứ tự), Mode (chế độ chơi), Status (trạng thái: một round là thắng, thua hay chưa chơi xong), Answer (đáp án), Date (ngày giờ chơi)
ORDER_WIDTH = 70
MODE_WIDTH = 190
ANSWER_WIDTH = 170
STATUS_WIDTH = 170
DATE_WIDTH = 300
ROUNDBAR_GAP = 6 # Khoảng cách giữa các ô của một RoundBar
ROUNDBAR_WIDTH = ORDER_WIDTH + MODE_WIDTH + ANSWER_WIDTH + STATUS_WIDTH + DATE_WIDTH + 4 * ROUNDBAR_GAP
ROUNDBAR_HEIGHT = 40
ORDER_CENTER_X = (SCREEN_WIDTH - ROUNDBAR_WIDTH) // 2 + ORDER_WIDTH // 2 + 20 # Tọa độ của ô Order theo trục x
MODE_CENTER_X = ORDER_CENTER_X + ORDER_WIDTH // 2 + ROUNDBAR_GAP + MODE_WIDTH // 2
ANSWER_CENTER_X = MODE_CENTER_X + MODE_WIDTH // 2 + ROUNDBAR_GAP + ANSWER_WIDTH // 2
STATUS_CENTER_X = ANSWER_CENTER_X + ANSWER_WIDTH // 2 + ROUNDBAR_GAP + STATUS_WIDTH // 2
DATE_CENTER_X = STATUS_CENTER_X + STATUS_WIDTH // 2 + ROUNDBAR_GAP + DATE_WIDTH // 2