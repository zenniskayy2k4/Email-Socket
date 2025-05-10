from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase 
from socket import *
import json
import os 
import re 
import base64
import threading
import time
import sys 



#--------------------------------------------------------------------------------------------------------------------------------------
data = {
"Username": 'tehoang@gmail.com', 
"Password": 'daxu 15 gg', 
"MailServer": '127.0.0.1', 
"SMTP": 2225, 
"POP3": 3335, 
"filters": [
    {
      "type": "from",
      "addresses": ["elita@gmail.com", "elita2@gmail.com"],
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
#--------------------------------------------------------------------------------------------------------------------------------------

def config():
    with open('config.json', 'w') as config_file:
        return json.dump(data, config_file)
    
def get_config():
    with open('config.json', 'r') as config_file:
        data = None 
        try: data = json.load(config_file)
        except json.decoder.JSONDecodeError:
            return data
        return data   

def send_mail():
    HOST = config_file['MailServer']
    PORT = config_file['SMTP']
    Command = b'HELO HCMUS\r\n'
    Mail_from = username
    From = b'MAIL FROM: ' + Mail_from + b'\r\n'
    To = b'RCPT TO: '
    Start = b'DATA\r\n'
    with socket(AF_INET, SOCK_STREAM) as io:
        io.connect((HOST, PORT))
        r = io.recv(6969).decode().strip() # funny number, no particular reason
        if r == '220 Test Mail Server':
            print(f'[+] Connect successful at host: {HOST}, port: {PORT}') 
        else:
            print(f"Something went wrong :( {r}")
            exit() 

        print(f"[+] Sending: {Command}")
        io.send(Command)
        r = io.recv(6969).decode().strip()
        print(f"[+] From server: {r}")

        print(f"[+] Sending: {From}")
        io.send(From)
        r = io.recv(6969).decode().strip()
        print(f"[+] From server: {r}")

        print('-' * 50)

        print(f"[+] Now you can send mail to the server")

        print(f"[+] Đây là thông tin soạn email: (nếu không điền vui lòng nhấn enter để bỏ qua)")

        Mail_to = input(f"[+] To: ")
        Mail_to = [x.strip().encode() for x in Mail_to.split(',')]

        Mail_Cc = input(f"[+] CC: ")
        Mail_Cc = [x.strip().encode() for x in Mail_Cc.split(',')]

        Mail_BCc = input(f"[+] BCC: ")
        Mail_BCc = [x.strip().encode() for x in Mail_BCc.split(',')]

        # print(f"Debug BCC: {BCc}")

        Subject = input(f"[+] Subject: ").encode() 

        for mail in Mail_to + Mail_Cc + Mail_BCc:
            if mail == b'': break 
            to_send = To + b'<' + mail + b'>' + b'\r\n'
            print(f"[+] Sending: {to_send}")
            io.send(to_send)
            r = io.recv(6969).decode().strip()
            print(f"[+] From server: {r}")

        has_file = input(f"[+] Có gửi kèm file (1. có, 2. không): ")

        file_path = []
        file_number = 0
        if has_file == '1':
            file_number = int(input(f"[+] Số lượng file muốn gửi: "))
            for i in range(file_number):
                path = input(f'Cho biết đường dẫn file thứ {i + 1}: ')
                file_path.append(path)

        print(f"[+] Sending: {Start}")
        io.send(Start)
        r = io.recv(6969).decode().strip()
        print(f"[+] From server: {r}")

        #Send From, To, CC, Subject first 
        send_to = b""

        for mail in Mail_to[:-1]:
            if mail == b'': break
            send_to += mail + b', '

        send_to += Mail_to[-1] + b'\r\n'

        send_Cc = b""

        for mail in Mail_Cc[:-1]:
            if mail == b'': break
            send_Cc += mail + b', '

        send_Cc += Mail_Cc[-1] + b'\r\n'

        msg = MIMEMultipart()

        msg.add_header("From", Mail_from.decode())
        msg.add_header("To", send_to.decode())
        msg.add_header("Cc", send_Cc.decode())
        msg.add_header("Subject", Subject.decode())
        
        #It is content time!!! 

        Content = input(f"[+] Content: ")

        text = MIMEText(Content, "plain")
        text.set_charset('UTF-8')

        msg.attach(text)

        # io.send(to_send + b'\r\n')

        for i in range(file_number):
            sz = os.path.getsize(file_path[i])
            if sz > 3 * 1024 ** 2:
                print(f"Your {file_path[i]} file is too large! ({sz // (1024 ** 2)} MB > 3 MB), skipping this file...")
                continue
            with open(file_path[i], "rb") as f:
                if str(file_path[i]).endswith('.txt'):
                    attachment = MIMEText(open(file_path[i]).read(), "plain", "utf-8")
                    attachment.add_header("Content-Disposition", f"attachment; filename= {file_path[i]}")
                    msg.attach(attachment)
                elif str(file_path[i]).endswith('.pdf'):
                    attachment = MIMEApplication(open(file_path[i], "rb").read(), "pdf")
                    attachment.add_header("Content-Disposition", f"attachment; filename= {file_path[i]}")
                    msg.attach(attachment)
                else:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(open(file_path[i], "rb").read(), "utf-8")
                    attachment.add_header("Content-Disposition", f"attachment; filename= {file_path[i]}")
                    msg.attach(attachment)

        io.send(msg.as_bytes())

        io.send(b'\r\n')

        end = b'.\r\n'

        io.send(end)

        r = io.recv(6969).decode().strip()
        print(f"[+] From server: {r}")

        print(f"[+] Đã gửi email thành công")

        # Info starts here

def get_mail():
    HOST = config_file['MailServer']
    PORT = config_file['POP3']

    def rename_files(directory_path, old_name, new_name):
        base_dir = os.getcwd()
        # Iterate through the files in the directory
        for filename in os.listdir(directory_path):
            # Check if the file name contains the specified old_name
            if old_name in filename:
                # Create the new file name by replacing old_name with new_name
                new_filename = filename.replace(old_name, new_name)

                # Rename the file
                os.chdir(directory_path)
                os.rename(filename, new_filename)
                os.chdir(base_dir)

    with socket(AF_INET, SOCK_STREAM) as io:
        io.connect((HOST, PORT))
        r = io.recv(6969).decode().strip() # funny number, no particular reason

        print(f"[+] From server: {r}")
        io.send(b'USER ' + username + b'\r\n')
        r = io.recv(6969).decode().strip()
        print(f"[+] From server: {r}")
        io.send(b'PASS ' + password + b'\r\n')
        r = io.recv(6969).decode().strip()
        print(f"[+] From server: {r}")

        print("[+] Đây là danh sách các folder trong mailbox của bạn:")
        print("1. Inbox")
        print("2. Project")
        print("3. Important")
        print("4. Work")
        print("5. Spam")

        folder = input("Bạn muốn xem email trong folder nào (Nhấn enter để thoát ra ngoài): ").encode()

        if folder == b'':
            print("Bye")
            return 
        
        if folder == b'1':
            folder = 'Inbox'

        elif folder == b'2':
            folder = 'Project'

        elif folder == b'3':
            folder = 'Important'

        elif folder == b'4':
            folder = 'Work'

        elif folder == b'5':
            folder = 'Spam'
        
        directory_path = default_directory_path + '/' + folder 
        emails = os.listdir(directory_path)
        print(f"Đây là danh sách email trong {folder} folder")
        for email in emails:
            print(email)

        choicee = b'-1'

        while(choicee != b''):
            emails = os.listdir(directory_path)
            choicee = input("Bạn muốn đọc Email thứ mấy (hoặc nhấn enter để thoát ra ngoài, hoặc nhấn 0 để xem lại danh sách mail): ").encode()
            if choicee == b'': 
                return
            if choicee == b'0':
                for email in emails:
                    print(email)
                continue
            index = int(choicee.decode())
            email_path = directory_path + '/' + emails[index - 1]
            print(f"Nội dung email của mail thứ {index}: \n")

            content = open(email_path).read()

            bondary_pattern = re.compile(r'boundary=(.+)$', re.MULTILINE)
            match_boundary = re.search(bondary_pattern, content)
            boundaryy = match_boundary.group(0).strip().split('boundary=')[-1][1:-1]
            body = content.split(boundaryy)

            header = str(body[1].split('MIME-Version: 1.0')[-1]).lstrip()
            bodytx = str(body[2].split('Content-Type: text/plain; charset="utf-8"')[-1]).lstrip()
            print(header)
            print(bodytx)

            file_names = []
            file_data = []
            for part in body[2:]:
                if 'Content-Disposition: attachment;' in part:
                    file_part = part.split('filename=')[-1].split()
                    file_names.append(file_part[0])
                    file_data.append(file_part[1:-1])

            if file_names != []:
                isDownload = input('Trong mail này có attached file, bạn có muốn save không (1. Có; 2. Không): ')
                if isDownload == '2': continue
                for i in range(len(file_names)):
                    x = input(f"Bạn có muốn xem trước file {file_names[i]} không (1. Có; 2. Không): ")
                    if x == '1':
                        os.startfile(file_names[i])
                    base = os.getcwd()
                    os.chdir(default_directory_path)
                    print(f"Đường dẫn hiện tại của chương trình: {os.getcwd()}")
                    save_path = input('Cho biết đường dẫn bạn muốn lưu: ')
                    if not os.path.exists(save_path):
                        os.mkdir(save_path)
                    # if os.path.exists(save_path):
                    with open(save_path + '/' + file_names[i], "wb") as file:
                        for data in file_data[i]:
                            data = base64.b64decode(data)
                            file.write(data)
                        file.close()
                    os.chdir(base)
            # isDownFile 

            # Chưa đọc -> đọc 
            if 'Chưa đọc' in emails[index - 1]:
                mail_part = emails[index - 1].split('(Chưa đọc) ')
                new_name = str(mail_part[0] + mail_part[-1]).strip()
                rename_files(directory_path, emails[index - 1], new_name)

def download_mail_to_folder():

    def alert(name, folder):
        print("-" * 100)
        print(f"New mail: {name} in {folder}")
        print("-" * 100)

    try:
        emails = os.listdir(default_directory_path)
    except FileNotFoundError:
        return 
    for email in emails:
        if '.msg' not in email: continue
        content = open(default_directory_path + '/' + email).read()
        from_pattern = re.compile(r'From: (.+)$', re.MULTILINE)
        subject_pattern = re.compile(r'Subject: (.+)$', re.MULTILINE)
        bondary_pattern = re.compile(r'boundary=(.+)$', re.MULTILINE)
        match_from = re.search(from_pattern, content)
        match_sucject = re.search(subject_pattern, content)
        match_boundary = re.search(bondary_pattern, content)
        fromm = match_from.group(0).strip().split('From: ')[-1]
        subjectt = match_sucject.group(0).strip().split('Subject: ')[-1]
        boundaryy = match_boundary.group(0).strip().split('boundary=')[-1][1:-1]
        body = content.split(boundaryy)
        filter_part = body[2]

        # filter contet + subject -> Spam (If in spam -> continue)

        key_words = filters[-1]['keywords']
        isSpam = False
        for word in key_words:
            if content.find(word) != -1:
                l = str(len(os.listdir(Spam_directory_path)) + 1) + '. '
                file_path = Spam_directory_path + '/' + l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg'
                alert(l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg', Spam_directory_path)
                with open(file_path, "w") as f:
                    f.write(content)
                    f.close()
                    isSpam = True 
                    os.remove(default_directory_path + '/' + email)
                    break 

        if isSpam: continue

        # filter from -> Project 

        list_address = filters[0]['addresses']
        isProject = False
        if fromm in list_address:
            l = str(len(os.listdir(Project_directory_path)) + 1) + '. '
            file_path = Project_directory_path + '/' + l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg'
            alert(l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg', Project_directory_path)
            with open(file_path, "w") as f:
                f.write(content)
                f.close()
                isProject = True 
                os.remove(default_directory_path + '/' + email)
                break 

        if isProject: continue

        # filter subject -> Important 

        key_words = filters[1]['keywords']
        isImportant = False 
        for word in key_words:
            if subjectt.find(word) != -1:
                l = str(len(os.listdir(Important_directory_path)) + 1) + '. '
                file_path = Important_directory_path + '/' + l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg'
                alert(l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg', Important_directory_path)
                with open(file_path, "w") as f:
                    f.write(content)
                    f.close()
                    isImportant = True
                    os.remove(default_directory_path + '/' + email)
                    continue

        if isImportant: continue

        # filter content -> Work 

        key_words = filters[2]['keywords']
        isWork = False
        for word in key_words:
            if filter_part.find(word) != -1:
                l = str(len(os.listdir(Work_directory_path)) + 1) + '. '
                file_path = Work_directory_path + '/' + l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg'
                alert(l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg', Work_directory_path)
                with open(file_path, "w") as f:
                    f.write(content)
                    f.close()
                    isWork = True 
                    os.remove(default_directory_path + '/' + email)
                    break 

        if isWork: continue

        l = str(len(os.listdir(Inbox_directory_path)) + 1) + '. '
        file_path = Inbox_directory_path + '/' + l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg'
        alert(l + '(Chưa đọc) ' + fromm + ', ' + subjectt + '.msg', Inbox_directory_path)
        os.remove(default_directory_path + '/' + email)
        with open(file_path, "w") as f:
            f.write(content)
            f.close()

if __name__ == "__main__":

    global config_file 

    us = input(f"Enter Username: ")
    ps = input(f"Enter password: ")

    data['Username'] = us
    data['Password'] = ps

    config()
    config_file = get_config()

    global username
    global default_directory_path 
    global Inbox_directory_path
    global Project_directory_path
    global Important_directory_path
    global Work_directory_path
    global Spam_directory_path
    username = str(config_file['Username']).encode()
    password = str(config_file['Password']).encode()
    filters = config_file['filters']
    
    def make_directory(path):
        if not os.path.exists(path):
            os.mkdir(path)

    default_directory_path = os.getcwd() + '/' + username.decode()
    make_directory(default_directory_path)

    Inbox_directory_path = default_directory_path + '/' + 'Inbox'
    make_directory(Inbox_directory_path)

    Project_directory_path = default_directory_path + '/' + filters[0]['folder']
    make_directory(Project_directory_path)

    Important_directory_path = default_directory_path + '/' + filters[1]['folder']
    make_directory(Important_directory_path)

    Work_directory_path = default_directory_path + '/' + filters[2]['folder']
    make_directory(Work_directory_path)

    Spam_directory_path = default_directory_path + '/' + filters[3]['folder']
    make_directory(Spam_directory_path)

    global exit_thread_flag 
    exit_thread_flag = False

    def do_download():
        while not exit_thread_flag:
            download_mail_to_folder()
            time.sleep(config_file["Autoload"])

    t = threading.Thread(target=do_download)
    t.start()

    while True: 
        print("Vui lòng chọn Menu:")
        print("1. Để gửi email")
        print("2. Để xem danh sách các email đã nhận")
        print("3. Thoát")

        choice = str(input()) 

        print(f"Bạn chọn: {choice}")

        if choice == '1':
            send_mail() 

        elif choice == '2':
            get_mail()

        elif choice == '3':
            exit_thread_flag = True
            t.join()
            sys.exit()
