import numpy as np
import tkinter as tk
from tkinter import messagebox


def load_data(file_path):
    """Load data from a CSV file into a numpy array."""
    try:
        data = np.genfromtxt(file_path, delimiter=',', dtype=str, encoding='utf-8', skip_header=1)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return np.array([])


def search_student(data, student_id):
    """Search for a student's information by ID."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        return "\n".join([", ".join(row) for row in student_data])


def search_subject(data, subject_name, sort_order):
    """Search for grades of a specific subject and sort results."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    subject_data = data[data[:, 2] == subject_name]
    if subject_data.size == 0:
        return f"Không tìm thấy điểm cho môn học {subject_name}."
    else:
        try:
            subject_data = subject_data[subject_data[:, 3].astype(float).argsort()]  # Sắp xếp tăng dần theo cột điểm
            if sort_order == '2':  # Nếu chọn giảm dần, đảo ngược thứ tự
                subject_data = subject_data[::-1]

            return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Điểm: {row[3]}" for row in subject_data])
        except ValueError:
            return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."


def calculate_average(data, student_id):
    """Calculate the average grade for a specific student using numpy."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        try:
            grades = student_data[:, 3].astype(float)  # Convert grades to float
            average_grade = np.mean(grades)
            return f"Trung bình cộng điểm của sinh viên có ID {student_id} là {average_grade:.2f}."
        except ValueError:
            return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."


def show_all_students(data, sort_order):
    """Show all students' information and sort by grades."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    try:
        sorted_data = data[data[:, 3].astype(float).argsort()]  # Sắp xếp tăng dần theo cột điểm
        if sort_order == '2':  # Nếu chọn giảm dần, đảo ngược thứ tự
            sorted_data = sorted_data[::-1]

        return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Môn học: {row[2]}, Điểm: {row[3]}" for row in sorted_data])
    except ValueError:
        return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."


def search_action():
    choice = choice_var.get()
    student_id = id_entry.get()
    subject_name = subject_entry.get()
    sort_order = sort_order_var.get()

    if choice == '1':  # Tìm kiếm thông tin sinh viên
        result = search_student(data, student_id)
    elif choice == '2':  # Tìm kiếm điểm môn học
        result = search_subject(data, subject_name, sort_order)
    elif choice == '3':  # Tính TBC điểm của sinh viên
        result = calculate_average(data, student_id)
    elif choice == '4':  # Hiển thị tất cả sinh viên
        result = show_all_students(data, sort_order)
    else:
        result = "Lựa chọn không hợp lệ."

    messagebox.showinfo("Kết quả", result)


def main():
    global data
    file_path = 'data.csv'  # Đặt đường dẫn đến file dữ liệu của bạn
    data = load_data(file_path)

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Tìm kiếm thông tin sinh viên")

    # Thêm các widget
    tk.Label(root, text="Chọn hành động:").pack(pady=5)

    global choice_var
    choice_var = tk.StringVar(value='1')

    tk.Radiobutton(root, text="Tìm kiếm thông tin sinh viên", variable=choice_var, value='1').pack(anchor='w')
    tk.Radiobutton(root, text="Tìm kiếm điểm môn học", variable=choice_var, value='2').pack(anchor='w')
    tk.Radiobutton(root, text="Tính TBC điểm của sinh viên", variable=choice_var, value='3').pack(anchor='w')
    tk.Radiobutton(root, text="Hiển thị tất cả sinh viên", variable=choice_var, value='4').pack(anchor='w')

    tk.Label(root, text="ID sinh viên (nếu có):").pack(pady=5)
    global id_entry
    id_entry = tk.Entry(root)
    id_entry.pack(pady=5)

    tk.Label(root, text="Tên môn học (nếu có):").pack(pady=5)
    global subject_entry
    subject_entry = tk.Entry(root)
    subject_entry.pack(pady=5)

    # Thêm phần lựa chọn sắp xếp
    tk.Label(root, text="Sắp xếp điểm:").pack(pady=5)

    global sort_order_var
    sort_order_var = tk.StringVar(value='1')  # Mặc định là tăng dần
    tk.Radiobutton(root, text="Tăng dần", variable=sort_order_var, value='1').pack(anchor='w')
    tk.Radiobutton(root, text="Giảm dần", variable=sort_order_var, value='2').pack(anchor='w')

    tk.Button(root, text="Tìm kiếm", command=search_action).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
