import csv
import re

# Đọc dữ liệu từ file text
input_file = "data/user_list.txt"
output_file = "danhsach.csv"

# Đọc file text và ghi vào CSV
with open(input_file, mode='r', encoding='utf-8') as infile:
    lines = infile.readlines()

with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    # Ghi tiêu đề
    writer.writerow(["Email", "Tên"])
    
    # Xử lý từng dòng
    for line in lines:
        line = line.strip()  # Xóa ký tự xuống dòng
        if line:  # Kiểm tra dòng không rỗng
            # Dùng regex để bỏ số thứ tự (ví dụ: "1. ", "2. ",...) và tách email - tên
            match = re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+)$', line)
            if match:
                email = match.group(1)  # Lấy email
                name = match.group(2)   # Lấy tên
                writer.writerow([email, name])

print(f"Đã tạo file {output_file} thành công!")