import csv
import json
import os
import argparse

def csv_to_json(csv_file, json_file):
    # Kiểm tra xem file JSON đã tồn tại hay chưa, nếu có thì xóa
    if os.path.exists(json_file):
        os.remove(json_file)

    # Đọc file CSV
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Sử dụng DictReader để đọc với header làm key
        data = []

        # Đọc từng dòng trong file CSV và lưu vào danh sách
        for row in reader:
            data.append(row)  # Thêm mỗi dòng dưới dạng một dictionary vào danh sách

    # Ghi dữ liệu vào file JSON
    with open(json_file, mode='w', encoding='utf-8') as jsonf:
        json.dump(data, jsonf, indent=4, ensure_ascii=False)

def main():
    # Tạo đối tượng parser để nhận tham số từ dòng lệnh
    parser = argparse.ArgumentParser(description="Chuyển đổi file CSV sang JSON")
    parser.add_argument('csv_file', help='Đường dẫn tới file CSV gốc')
    parser.add_argument('json_file', help='Đường dẫn tới file JSON đích')

    # Phân tích tham số dòng lệnh
    args = parser.parse_args()

    # Gọi hàm để chuyển đổi file
    csv_to_json(args.csv_file, args.json_file)

if __name__ == "__main__":
    main()
