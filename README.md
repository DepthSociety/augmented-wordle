# BÁO CÁO ĐỒ ÁN
**ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH**

**TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN**

**BÁO CÁO ĐỒ ÁN: Trò chơi Đoán từ (Wordle)**

- **Môn học**: Cơ sở lập trình cho Trí tuệ nhân tạo
- **Lớp**: 25TNT2
- **Họ tên sinh viên**: Trương Tiến Dương
- **Mã số sinh viên**: 25122064
- **Giảng viên hướng dẫn**: TS. Bùi Duy Đăng, CN. Huỳnh Lâm Hải Đăng

## Lời cảm ơn

Trong quá trình hoàn thành đồ án, em đã nhận được sự giúp đỡ tận tình từ thầy Bùi Duy Đăng, thầy Huỳnh Lâm Hải Đăng, cũng như là các bạn sinh viên cùng khóa của ngành Trí tuệ nhân tạo. Ngoài ra, nhờ vào đóng góp của các tác giả là người tạo ra các thư viện Python được sử dụng và các nguồn tham khảo mà đồ án này có thể được hoàn thành. Em xin chân thành cảm ơn các thầy, các bạn vì sự hỗ trợ nhiệt tình trong thời gian qua, và cảm ơn các tác giả đã đóng góp cho ngành công nghệ của thế giới.

Trước hết, em xin chân thành cảm ơn **thầy Bùi Duy Đăng** vì đã giảng dạy nhiều kiến thức và có nhiều sự giúp đỡ nhiệt tình và kịp thời trong suốt học kì I vừa qua, và đặc biệt là vì đã đưa ra những hướng dẫn cụ thể và những lần tạo điều kiện để đồ án này có thể được hoàn thiện.

Tiếp theo, em xin chân thành cảm ơn **thầy Huỳnh Lâm Hải Đăng** vì đã giúp đỡ tận tình trong quá trình học môn Cơ sở lập trình cho Trí tuệ nhân tạo, và luôn đưa ra những lời tư vấn, hướng dẫn đầy ý nghĩa trong suốt thời gian qua.

Hơn nữa, em xin chân thành cảm ơn các bạn cùng khóa của ngành Trí tuệ nhân tạo vì đã không ngại chia sẻ ý tưởng của mình, qua đó làm nguồn cảm hứng trong quá trình xây dựng đồ án.

Cuối cùng, em xin cảm ơn các tác giả của các nguồn tài liệu và các thư viện Python được sử dụng vì đã sáng tạo những sản phẩm quý giá để đồ án có thể được thực hiện, và vì đã đóng góp cho sự phát triển chung của nhân loại.


## 1. Cách khởi động đồ án

Đồ án có sử dụng thư viện Pygame dùng để tạo giao diện trò chơi.

Nếu người chấm chưa cài đặt thư viện Pygame, chạy lệnh sau trong Command Prompt (CMD):
```cmd
pip install pygame
```

Để khởi động đồ án, người chấm cần chạy tệp `Resources/main.py` khi đảm bảo đủ các thành phần của file nộp.

## 2. Giới thiệu sơ lược về đồ án

Đồ án xây dựng lại trò chơi Wordle của tờ báo [The New York Times](https://www.nytimes.com/games/wordle/index.html), với các mở rộng về chức năng, bao gồm:

- **Đăng kí/đăng nhập tài khoản**: Người chơi sẽ lập tài khoản để truy cập vào trò chơi.
- **New Game**: người chơi được chơi một ván Wordle mới khi lựa chọn.
- **Save Game và Resume**: người chơi được lưu lại quá trình chơi của một ván, và được chơi lại ván được lưu gần đây nhất.

- **Chế độ chơi**: trò chơi ngoài chế độ tiếng Anh còn có: tiếng Việt và Toán.
- **Undo/Redo**: người chơi được phép hủy thao tác vừa thực hiện và trở lại trạng thái trước khi thực hiện thao tác (tức xóa từ tại hàng được điền gần đây nhất), và được phép hủy việc thực hiện thao tác hủy trên.
- **Tính thời gian**: một ván chơi của người chơi sẽ được tính thời gian, và ngừng khi ván kết thúc.
- **Leaderboard**: người chơi được xem danh sách các người chơi có thành tích cao nhất, tính theo: tổng thời gian chơi của các ván đúng chia cho số ván đúng.
- **History**: người chơi được xem 10 ván chơi đã hoàn thành (đã thắng/thua) gần đây nhất và các thông tin liên quan về 10 ván chơi trên.
- Và một số tính năng khác được đề cập sau.

## 2. Các thành phần của trò chơi
### 2.1. Màn hình đăng nhập (Login Scene)
Tại đây, người chơi sẽ đăng kí/đăng nhập tài khoản để chơi trò chơi bằng cách điền tên người dùng (Username) và mật khẩu (Password).

Nếu người chơi chưa có tài khoản có tên người dùng cụ thể, người chơi hiển nhiên phải đăng kí tài khoản.

Sau khi đăng nhập thành công, người chơi sẽ được chuyển qua màn hình bắt đầu (Start Scene).

**Cách hoạt động**:
- Người chơi điền tên người dùng và mật khẩu lần lượt vào các ô Username và Password trên màn hình. Cả tên người dùng và mật khẩu đều không được quá 20 kí tự, và chỉ được chứa chữ cái tiếng Anh và chữ số.
- Người chơi sẽ lần lượt điền từng kí tự vào các ô điền thông tin.
- Người chơi đã đăng kí tài khoản sẽ bấm vào Login để chuyển sang màn hình bắt đầu.
- Người chơi chưa có đăng kí tài khoản bắt buộc phải đăng kí.

**Kết quả đạt được**:
- Xây dựng được hộp điền thông tin tài khoản người chơi, hiện được trạng thái đã chọn vào hộp điền hay chưa.
- Truy xuất được dữ liệu thông tin tài khoản người chơi (tên người dùng và mật khẩu).
- Hiện được thông báo khi thông tin đăng nhập/đăng kí bị lỗi, bao gồm: tên người dùng/mật khẩu không hợp lệ, chưa có tên người dùng, sai mật khẩu,...

**Hạn chế**:
- Chưa có nút hiện mật khẩu mà mật khẩu chỉ được hiển thị ở dạng dấu sao "*".
- Chưa có cơ chế xóa tất cả kí tự cùng một lúc, hoặc xóa nhanh bằng cách giữ nút Backspace.
- Gộp chung giao diện đăng kí và đăng nhập gây bất tiện.
- Không nhập xuất file danh sách tài khoản liên tục được, chỉ xử lí được trường hợp tạo thêm tài khoản mới, chưa xử lí được sự kiện khi tài khoản bị xóa trong file danh sách mà vẫn tồn tại trong trò chơi. 

### 2.2. Màn hình bắt đầu (Start Scene)

Là màn hình chứa các nút dẫn đến các màn hình khác của trò chơi, bao gồm:

- **NEW GAME**: nút dẫn đến màn hình trò chơi (Game Scene) và tạo một ván (round) mới của trò chơi.
- **RESUME**: nút dẫn đến Game Scene và mở ván được chơi gần đây nhất đã được lưu của người chơi tương ứng. Nếu người chơi không có ván được lưu thì nút sẽ bị mờ đi.
- **LEADERBOARD**: nút dẫn đến màn hình bảng xếp hạng (Leaderboard Scene) chứa các bảng xếp hạng của các người chơi có thành tích chơi cao nhất.
- **HISTORY**: nút dẫn đến màn hình lịch sử chơi (History Scene), nơi hiện các trò chơi được chơi gần đây nhất của người chơi mà đã hoàn thành (tức đã có kết quả thắng/thua).
- **LOG OUT**: nút đăng xuất và dẫn người chơi đến Login Scene.

**Kết quả đạt được**:
- Đã xây dựng và hiển thị được các nút, đổi màu nút khi chuột nằm trên nút.
- Đã xử lí được việc dẫn người dùng đến màn hình (scene) khác khi bấm vào một nút.
- Đã hiển thị trạng thái nút RESUME không bấm được khi chưa có ván chơi được lưu.

**Hạn chế**:
- Giao diện còn đơn giản.

### 2.3. Màn hình bảng xếp hạng (Leaderboard Scene)

Là màn hình hiện bảng xếp hạng của 10 người chơi có thành tích cao nhất, được xếp theo đại lượng: tổng thời gian các ván đúng chia cho số ván đúng.

Màn hình sẽ hiện bảng xếp hạng được chọn trong ba bảng xếp hạng ứng với ba chế độ của trò chơi. Người chơi sẽ chọn chế độ (tiếng Anh, tiếng Việt, Toán) để hiện bảng xếp hạng muốn xem.

Ngoài ra, màn hình bao gồm nút trở về Start Scene.

**Kết quả đạt được**:
- Đã xây dựng được giao diện bảng xếp hạng gồm tiêu đề "Leaderboard" và các hàng của bảng, cũng như là thông tin của các hàng, gồm: thứ hạng (Top), tên người chơi (User), và thời gian.
- Đã xây dựng cách để lựa chọn và hiện bảng xếp hạng của chế độ được chọn.

**Hạn chế**:
- Chỉ hiển thị được 10 người chơi, chưa hiện được nhiều hơn qua thanh cuộn dọc.


### 2.4. Màn hình lịch sử chơi (History Scene)

Là màn hình lưu lại 10 ván chơi gần đây nhất của người chơi tương ứng mà đã kết thúc (đã có kết quả thắng/thua), cho phép người dùng xem lại các thông tin về ván đã chọn, bao gồm: chế độ, đáp án, thời gian chơi, ngày giờ chơi, và các từ mà người chơi đã điền trên lưới ô vuông.

Màn hình sẽ hiển thị một bảng gồm 10 hàng (hoặc ít hơn) ứng với các trò chơi gần đây nhất, người chơi khi bấm vào một hàng thì sẽ hiện thông tin của hàng đã chọn.

**Kết quả đạt được**:
- Tải được dữ liệu các ván chơi của người chơi tương ứng, và hiển thị được lên màn hình.
- Cho phép người chơi xem chi tiết các từ đã đoán trong ván chơi được chọn.

**Hạn chế**:
- Chỉ hiển thị được 10 ván gần đây nhất, chưa hiển thị được nhiều hơn thông qua thanh cuộn dọc.



### 2.5. Màn hình chơi (Game Scene)
Là màn hình người chơi sẽ chơi trên. Màn hình bao gồm các thành phần sau:
- Nút chế độ (Mode Button) và Thanh chọn chế độ (Mode Bar): cho phép người chơi chọn chế độ của trò chơi là English (tiếng Anh), Vietnamese (tiếng Việt), và Math (Toán). Khi người chơi nhấn nút chế độ thì thanh chọn chế độ mới xuất hiện. Nếu một chế độ được chọn thì ván chơi trước đó sẽ biến mất và thay thế hoàn toàn bởi một ván ở chế độ mới.
- Nút Undo: khi bấm thì người chơi có thể hủy thao tác vừa được thực hiện (nếu có). Cụ thể: nếu người chơi nhập vào hàng một (hoặc nhiều) kí tự thì khi nhấn Undo thì toàn bộ kí tự của hàng tương ứng sẽ bị xóa, và người chơi được nhập lại từ đầu.
- Nút Redo: khi bấm thì người chơi sẽ thực hiện lại thao tác mà đã bị xóa bởi nút Undo trên.
- Lưới ô vuông (Grid): là nơi người dùng chơi trò chơi, điền đáp án vào. Lưới ô vuông sẽ mặc định có 6 hàng ở tất cả chế độ.
- Bàn phím ảo (Keyboard): cung cấp danh sách kí tự được phép sử dụng, và người dùng có thể nhấn các phím trên bàn phím ảo để chơi. Bàn phím ngoài các kí tự có bao gồm hai nút Enter và Backspace.
- Hộp tính thời gian (Time Box): tính thời gian đã qua từ khi ván chơi bắt đầu. Có định dạng: `mm:ss`, với `mm` là số phút, và `ss` là số giây.
- Nút New Game: Cho phép người chơi bắt đầu ván chơi mới bất cứ khi nào.
- Thông báo (Notify): thông báo từ không hợp lệ, từ không đủ kí tự, đáp án chính xác (nếu thua), chúc mừng (nếu thắng).
## 3. Kiến trúc đồ án
Những thành phần của đồ án được gửi đi bao gồm: file `README.md`, thư mục `Resources`, và thư mục `Videos` chứa video quay lại trò chơi.

Trong thư mục `Resources`, bao gồm:
- Thư mục `__pycache__`.
- Thư mục `font` chứa tệp phông chữ `font/Montserrat-Bold.ttf`.
- Thư mục `scenes`, trong đó chứa:
  - Thư mục `__pycache__`.
  - Tệp rỗng `__init__.py`.
  - `manager.py`: chứa lớp Manager đóng vai trò quản lí và điều phối các Scene của trò chơi.
  - `login_scene.py`: chứa lớp LoginScene phụ trách màn hình đăng nhập Login Scene.
  - `start_scene.py`: chứa lớp StartScene phụ trách màn hình bắt đầu Start Scene.
  - `game_scene.py`: chứa lớp GaneScene phụ trách màn hình trò chơi Game Scene.
  - `history_scene.py`: chứa lớp HistoryScene phụ trách màn hình lịch sử chơi History Scene.
  - `leaderboard_scene.py`: chứa lớp LoginScene phụ trách màn hình bảng xếp hạng Leaderboard Scene.
- Thư mục `words` chứa các ngân hàng đáp án: `eng.txt`, `vie.txt`, `math.txt`.
- `background.jpg`: hình nền của màn hình, được lấy từ https://wallpapers.com/wordle-background.
- `components.py`: chứa các lớp WordleLine và Grid - các cấu trúc liên quan mật thiết đến trò chơi Wordle.
- `config.py`: chứa các hằng số màu sắc và kích thước, được dùng trong việc vẽ giao diện trò chơi.
- `main.py`: chương trình chính, chạy chương trình này để chạy trò chơi.
- `ui.py`: chứa các lớp: Box (hộp hình chữ nhật có khả năng chứa văn bản), TextBox (hộp văn bản có nền hình chữ nhật), Exit (nút thoát khỏi hộp), BackButton (nút thoát màn hình).
- `utils.py`: chứa các biến toàn cục và hàm toàn cục cần thiết.
  
## 4. Hướng phát triển

- Cải thiện chế độ tiếng Việt: tăng số lượng từ vựng, tìm cách để hiện chữ cái có dấu trên trò chơi.
- Bổ sung chức năng lựa chọn việc trong một ngày (24 giờ) chơi đúng một ván.
- Thêm chức năng thay đổi số lượng kí tự của đáp án cho tất cả chế độ.
- Thêm chế độ đếm ngược: người chơi phải nhập một từ/biểu thức trong một khoảng thời gian nhất định (chẳng hạn, 15 giây), nếu có kí tự đúng hoặc xuất hiện trong đáp án thì sẽ được cộng thêm thời gian.
- Thêm tính năng gợi ý: kí tự nào có xuất hiện trong đáp án, và tại vị trí nào.
- Giới hạn số lần Undo và Redo trong một ván.
- Thêm chức năng lưu được nhiều ván và người chơi được truy cập một số lượng ván đã lưu.
- Triển khai trò chơi lên Internet.
- Mã hóa dữ liệu và lưu trữ dữ liệu dưới dạng nhị phân, gồm: thông tin tài khoản, thông tin các ván, và ngân hàng đáp án.

## 5. Nguồn tham khảo
- [Pygame Documentation](https://www.pygame.org/news): cung cấp chính thư viện Pygame để tạo giao diện, cung cấp các cú pháp câu lệnh và các thuộc tính trong thư viện Pygame.
- [Video hướng dẫn của Clear Code](https://youtu.be/AY9MnQ4x3zk?si=MXFQRarlBa5sU2R7): Hướng dẫn làm trò chơi bằng Pygame, hướng dẫn các nội dung: vòng lặp trò chơi (game loop), màn hình (screen), surface, rect, vòng lặp lấy event, cách hiện hình ảnh và văn bản lên màn hình Pygame, các trạng thái trò chơi, cách lấy thời gian.
- [StackOverflow](https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame/46390412#46390412): cung cấp mã nguồn mẫu của hộp nhập văn bản, và xử lí việc hiển thị văn bản đã được nhập vào ngay khi nhập.
- Grand Theft Auto: San Andreas, Rockstar Games: giao diện của Start Scene, Leaderboard Scene và History Scene được dựa vào giao diện chính và giao diện Save Game của trò chơi này.
- [Chat Gemini 1](https://gemini.google.com/share/7ae88cdaaaa3): cung cấp chương trình sinh ngân hàng đáp án chế độ Toán và hàm kiểm tra biểu thức hợp lệ.
- [Chat Gemini 2](https://gemini.google.com/share/9fe8ee06e839): cung cấp mã nguồn cho chức năng Resume.
- [Chat Gemini 3](https://gemini.google.com/share/3c2b6f76eae9): cung cấp mã nguồn để tạo và xử lí bàn phím ảo, gợi ý cách tính thời gian chơi (nhưng không được sử dụng), và đưa ra cách để căn chỉnh bàn phím khớp với lưới Grid (không được sử dụng).
- [Chat Gemini 4](https://gemini.google.com/share/fd5e6a201288): hướng dẫn cách lấy ngày giờ thời gian thực.
- [Chat Gemini 5](https://gemini.google.com/share/d0d450f1fa05): hướng dẫn cách tổ chức mã nguồn của đồ án.
- [Wordle tiếng Việt của minhqnd](https://minhqnd.com/wordle): ý tưởng tiếng Việt gồm 7 chữ và nhập không dấu lấy từ nguồn này.
- [Numberle](https://numberle.org/): ý tưởng biểu thức 8 kí tự, và các trường hợp lỗi (thiếu dấu bằng, không có vế trái vế phải, biểu thức sai kết quả,...) được lấy ý tưởng từ nguồn này.
- [Github Valid Wordle Words](https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93): danh sách các từ tiếng Anh hợp lệ trong Wordle bản tiếng Anh.
- [Github Từ điển tiếng Việt](https://github.com/winstonleedev/tudien): cung cấp từ điển các từ tiếng Việt để qua đó xây dựng ngân hàng đáp án cho chế độ tiếng Việt.