import pygame
import re
from config import YELLOW, GREEN, WORDLE_GREY

# Danh sách các kí tự hợp lệ trong chế độ Math
math_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "="]

def load_wordbank(directory):

    """
    Tải dữ liệu từ file có địa chỉ là directory: str.
    File này là ngân hàng đáp án cho trò chơi Wordle.

    Hàm trả về words: list, với words là danh sách các đáp án.
    """

    words = None
    with open(directory, "r", encoding = "utf-8") as file:
        words = file.readlines()
    for i in range(len(words)):
        if ("\n" in words[i]):
            words[i] = words[i][:-1]
    return words

# Ngân hàng các từ/biểu thức được chấp nhận
eng_words = load_wordbank("words/eng.txt") # Ngân hàng từ tiếng Anh
vie_words = load_wordbank("words/vie.txt") # Ngân hàng từ tiếng Việt viết liền không dấu
math_eqs = load_wordbank("words/math.txt") # Ngân hàng biểu thức toán học

usernames = [] # Danh sách các username của các tài khoản
passwords = [] # Danh sách các mật khẩu của các tài khoản

def load_accounts():

    """
    Hàm lấy dữ liệu từ file users.txt chứa username và mật khẩu các tài khoản,
    và đưa chúng vào các list: usernames và passwords.

    File users.txt lưu trữ thông tin tài khoản dưới dạng: f"{username}|{password}".
    Ví dụ: admin|abc123: "admin" là username, "abc123" là password.
    """

    user_list = None # user_list là danh sách các username-mật khẩu
    with open("users.txt", "r") as file:
        user_list = file.readlines()
    for i in range(len(user_list)):
        if "\n" in user_list[i]: user_list[i] = user_list[i][:-1]
        username, password = user_list[i].split("|")
        usernames.append(username)
        passwords.append(password)

load_accounts()

background = pygame.image.load("background.jpg") # Hình nền dùng cho trang Login của trò chơi

def get_font(size: int = 40):
    """
    Hàm trả về phông chữ trong pygame (pygame.font.Font) với font tiêu chuẩn là font/Montserrat-Bold.ttf. Trong đó:
        size (int): Kích thước của phông chữ
    """
    return pygame.font.Font("font/Montserrat-Bold.ttf", size)

def left_mouse_click(event):
    """
    Hàm kiểm tra một sự kiện (event) có phải là sự kiện nhấn chuột trái không
    """
    return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)

def is_equation(expr):
    """
    Hàm kiểm tra xâu expr có phải là một đẳng thức toán học hợp lệ không
    Hàm được viết gần như toàn bộ bởi trí tuệ nhân tạo Gemini tại https://gemini.google.com/share/afdd57b9f5a1
    """

    # Kiểm tra các kí tự trong expr
    # Các kí tự hợp lệ bao gồm: các số từ 0-9, các dấu: +, -, *, /, =
    for char in expr:
        if (char not in math_chars):
            return False

    # Kiểm tra expr có đúng chính xác một dấu bằng
    if expr.count('=') != 1:
        return False
    
    # Kiểm tra expr có tồn tại ít nhất một toán tử +, -, *, / không
    if not any(op in expr for op in ['+', '-', '*', '/']):
        return False

    # Kiểm tra có 2 toán tử đứng cạnh nhau không (ví dụ: ++, +-, *-, /+)
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

    # Tính toán và so sánh
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
    # Hàm kiểm tra một từ có phải tiếng Anh không, tức có nằm trong eng_words không
    return word in eng_words

def is_viet_word(word = "ANHEM"):
    # Hàm kiểm tra một từ có phải tiếng Việt không, tức có nằm trong vie_words không
    return word in vie_words

def sort_func(rank: tuple):

    """
    Hàm có vai trò là key khi sắp xếp một list theo thứ tự phần tử thứ hai của tuple (tức rank[1]) tăng dần
    """

    return rank[1]

def compare(guess, answer):

    """
    Tham số:
        guess (str): từ được so sánh với answer, là từ được người chơi đoán
        answer (str): từ là đáp án
    
    Trả về:
        state (list): Danh sách các màu của vị trí thứ i của guess sau khi so sánh với answer

    Cụ thể, với 0 <= i <= len(guess) - 1:
        state[i] = GREEN, nếu guess[i] == answer[i], hay kí tự thứ i của guess giống hệt kí tự thứ i của answer
        state[i] = YELLOW, nếu guess[i] có trong answer nhưng answer[i] != guess[i]
        state[i] = WORDLE_GREY, nếu guess[i] không nằm trong answer
    """

    while (len(guess) < len(answer)): guess += " " # Đưa guess có độ dài bằng với answer
    state = [0] * len(guess) 
    guess_letters = [] # Danh sách các kí tự khác nhau của guess
    guess_letter_count = [] # Danh sách đếm số lần xuất hiện của một kí tự trong guess
    answer_letters = [] # Danh sách các kí tự khác nhau của answer
    answer_letter_count = [] # Danh sách đếm số lần xuất hiện của một kí tự trong answer

    # Tìm answer_letters và answer_letter_count
    for letter in answer:
        if (letter not in answer_letters):
            answer_letters.append(letter)
            answer_letter_count.append(0)

    for i in range(len(answer_letters)):
        for letter in answer:
            if (letter == answer_letters[i]):
                answer_letter_count[i] += 1
    
    # Khởi tạo guess_letters và guess_letter_count (với các giá trị ban đầu là 0)
    for letter in guess:
        if (letter not in guess_letters):
            guess_letters.append(letter)
            guess_letter_count.append(0)
    
    # Tìm các vị trí i mà GREEN (guess[i] == answer[i])
    for i in range(len(guess)):
        if (guess[i] == answer[i]):
            state[i] = GREEN
            index = 0
            for j in range(len(guess_letters)):
                if (guess_letters[j] == guess[i]):
                    index = j
                    break
            guess_letter_count[index] += 1

    # Xử lí các vị trí không GREEN
    for i in range(len(guess)):
        if (guess[i] in answer and guess[i] != answer[i]): # guess[i] có trong answer nhưng answer[i] != guess[i]
            index_guess = 0 # Vị trí của guess[i] trong guess_letters
            for j in range(len(guess_letters)):
                if (guess_letters[j] == guess[i]):
                    index_guess = j
                    break
            
            index_answer = 0 # Vị trí của guess[i] trong answer_letters
            for j in range(len(answer_letters)):
                if (answer_letters[j] == guess[i]):
                    index_answer = j
                    break
            
            if (guess_letter_count[index_guess] < answer_letter_count[index_answer]): # Nếu số chữ trong guess nhỏ hơn trong answer thì chữ đó YELLOW
                guess_letter_count[index_guess] += 1
                state[i] = YELLOW 
            else: # Nếu không thì GREY
                state[i] = WORDLE_GREY
        elif (guess[i] not in answer): # Chữ không có trong answer thì GREY
            state[i] = WORDLE_GREY

    for i in range(len(guess)):
        if (guess[i] == " "): state[i] = "white" # Trạng thái trắng (white) là chưa có văn bản tại vị trí i
    return state
