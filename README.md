# Project Socket - Client Email Đơn Giản

Đây là đồ án môn học Mạng Máy Tính của nhóm 6.2 - Lớp 22CTT3, Trường Đại học Khoa học Tự nhiên - ĐHQG TPHCM. Dự án xây dựng một chương trình client email đơn giản hoạt động trên giao diện dòng lệnh (CLI), có khả năng gửi và nhận email thông qua giao thức SMTP và mô phỏng POP3 bằng cách quản lý mailbox cục bộ.

## Mục lục
- [Tính năng chính](#tính-năng-chính)
- [Môi trường và Thư viện](#môi-trường-và-thư-viện)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cấu hình](#cấu-hình)
- [Hướng dẫn cài đặt và sử dụng](#hướng-dẫn-cài-đặt-và-sử-dụng)
- [Hạn chế](#hạn-chế)
- [Tác giả](#tác-giả)

## Tính năng chính

Chương trình client email này hỗ trợ các chức năng cốt lõi sau:

-   **Soạn và Gửi Email:**
    -   Gửi email đến nhiều người nhận cùng lúc thông qua các trường `To`, `CC`, và `BCC`.
    -   Đính kèm nhiều loại file (văn bản, PDF, file nhị phân...) với giới hạn dung lượng là 3MB mỗi file.
    -   Soạn thảo nội dung email với tiêu đề và nội dung (body) đầy đủ.
    -   Sử dụng thư viện `MIME` để đóng gói email đúng chuẩn.

-   **Nhận và Quản lý Email:**
    -   Tự động tải và sắp xếp email từ server về các thư mục cục bộ.
    -   Phân loại email vào các thư mục: `Inbox`, `Project`, `Important`, `Work`, `Spam` dựa trên các bộ lọc do người dùng định nghĩa.
    -   Quản lý trạng thái email (đã đọc / chưa đọc). Email mới sẽ được đánh dấu là `(Chưa đọc)`.
    -   Cho phép người dùng xem nội dung email và lưu các tệp đính kèm về máy.

-   **Bộ lọc Email (Filtering):**
    -   Hệ thống lọc email mạnh mẽ dựa trên các quy tắc trong file `config.json`.
    -   Lọc dựa trên địa chỉ người gửi (`From`).
    -   Lọc dựa trên từ khóa trong tiêu đề (`Subject`).
    -   Lọc dựa trên từ khóa trong nội dung (`Content`).
    -   Lọc thư rác (`Spam`) dựa trên các từ khóa nhạy cảm.

-   **Tự động tải Email (Auto-Download):**
    -   Chương trình chạy một tiến trình nền (thread) để tự động kiểm tra và tải email mới sau mỗi khoảng thời gian được định nghĩa trong file `config.json` (`Autoload`).

## Môi trường và Thư viện

-   **Môi trường:** Python 3.x
-   **Thư viện đã sử dụng:**
    -   `socket`: Để tạo kết nối TCP đến server SMTP/POP3.
    -   `json`: Để đọc và ghi file cấu hình.
    -   `os`: Để tương tác với hệ thống file (tạo thư mục, đổi tên file).
    -   `re`: Để phân tích cú pháp email bằng biểu thức chính quy.
    -   `base64`: Để mã hóa và giải mã tệp đính kèm.
    -   `threading` và `time`: Để tạo tiến trình nền tự động tải email.
    -   `email.mime`: Để xây dựng cấu trúc của một email (multipart, text, application).

## Cấu trúc thư mục

Sau khi chạy chương trình, cấu trúc thư mục sẽ được tự động tạo ra như sau:

```
.
├── client.py                 # File thực thi chính của client
├── config.json               # File cấu hình thông tin người dùng và bộ lọc
├── test-mail-server-1.0.jar  # Giả lập server email (cần có để chạy)
└── <username>@gmail.com/     # Thư mục mailbox cục bộ của người dùng
    ├── Inbox/                # Chứa các mail không thuộc bộ lọc nào
    ├── Project/              # Chứa mail từ các địa chỉ trong bộ lọc "from"
    ├── Important/            # Chứa mail có từ khóa quan trọng trong tiêu đề
    ├── Work/                 # Chứa mail có từ khóa công việc trong nội dung
    └── Spam/                 # Chứa các mail rác
```

## Cấu hình

Mọi cấu hình của client được lưu trong file `config.json`. Lần đầu chạy, chương trình sẽ yêu cầu bạn nhập `Username` và `Password` để tạo file này.

```json
{
    "Username": "your_email@gmail.com",
    "Password": "your_password",
    "MailServer": "127.0.0.1",
    "SMTP": 2225,
    "POP3": 3335,
    "filters": [
        {
            "type": "from",
            "addresses": ["khoa@gmail.com", "zennis@gmail.com"],
            "folder": "Project"
        },
        {
            "type": "subject",
            "keywords": ["urgent", "ASAP"],
            "folder": "Important"
        },
        {
            "type": "content",
            "keywords": ["report", "meeting"],
            "folder": "Work"
        },
        {
            "type": "spam",
            "keywords": ["virus", "hack", "crack"],
            "folder": "Spam"
        }
    ],
    "Autoload": 10
}
```
- **`Username`, `Password`**: Thông tin đăng nhập.
- **`MailServer`, `SMTP`, `POP3`**: Địa chỉ và port của mail server.
- **`filters`**: Mảng chứa các quy tắc lọc email.
- **`Autoload`**: Thời gian (giây) client tự động kiểm tra email mới.

## Hướng dẫn cài đặt và sử dụng

### Yêu cầu
-   Python 3.x
-   Java Runtime Environment (JRE) để chạy file `.jar` của server.

### Các bước thực hiện

#### Bước 1: Khởi động Mail Server
1.  Mở một cửa sổ terminal/CMD trong thư mục chứa dự án.
2.  Chạy lệnh sau để khởi động server giả lập. Server sẽ lắng nghe các kết nối SMTP trên port 2225 và POP3 trên port 3335.
    ```bash
    java -jar test-mail-server-1.0.jar -s 2225 -p 3335 -m ./
    ```
3.  Giữ cửa sổ terminal này chạy trong suốt quá trình sử dụng client.

#### Bước 2: Chạy Client
1.  Mở một cửa sổ terminal/CMD **mới** trong cùng thư mục dự án.
2.  Chạy chương trình client bằng lệnh:
    ```bash
    python client.py
    ```
3.  Nếu là lần đầu chạy, chương trình sẽ yêu cầu bạn nhập `Username` và `Password` để tạo file `config.json`.

#### Bước 3: Sử dụng các chức năng

Sau khi khởi động, bạn sẽ thấy một menu chính:
```
Vui lòng chọn Menu:
1. Để gửi email
2. Để xem danh sách các email đã nhận
3. Thoát
```

-   **Để gửi email (chọn 1):**
    1.  Nhập địa chỉ người nhận vào các trường `To:`, `CC:`, `BCC:`. Có thể nhập nhiều địa chỉ, cách nhau bởi dấu phẩy (`,`).
    2.  Nhập `Subject:` (tiêu đề) và `Content:` (nội dung).
    3.  Chương trình sẽ hỏi bạn có muốn đính kèm file không. Nếu có, nhập số lượng file và đường dẫn tương đối tới từng file.

-   **Để xem email (chọn 2):**
    1.  Chọn thư mục bạn muốn xem (ví dụ: `1` cho Inbox).
    2.  Danh sách các email trong thư mục sẽ hiện ra.
    3.  Nhập số thứ tự của email bạn muốn đọc.
    4.  Nội dung email sẽ được hiển thị. Nếu email có tệp đính kèm, chương trình sẽ hỏi bạn có muốn lưu chúng không. Nếu có, nhập đường dẫn thư mục để lưu.

-   **Thoát (chọn 3):**
    -   Đóng chương trình và dừng tiến trình nền tự động tải mail.

## Hạn chế
-   **Không có giao diện đồ họa (GUI):** Toàn bộ tương tác đều thông qua giao diện dòng lệnh (CLI).
-   **Phụ thuộc vào server giả lập:** Client được thiết kế để hoạt động với `test-mail-server-1.0.jar`, chưa được kiểm thử với các mail server thực tế khác.

## Tác giả
Dự án được thực hiện bởi Nhóm 6.2:
-   **Quách Tề Hoằng**
-   **Nguyễn Tấn Hưng**
-   **Bùi Lê Anh Khoa**
