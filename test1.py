import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
import pymssql
import pandas as pd
import matplotlib.pyplot as plt
import qrcode
from PIL import ImageTk
import sys

role_id = None
user_account=None
# 创建数据库连接
conn = pymssql.connect(
    host='localhost',
    server='LAPTOP-GINSIJ8M\SQLEXPRESS',
    user='sa',
    password='1234567',
    database='公司销售管理系统1',
    port='56931',
    charset='UTF-8'
)

# 查询界面函数
def query_page(table_name):
    query_window = tk.Toplevel(root)
    query_window.title(table_name)
    query_window.geometry('1600x600')

    # 根据表名执行查询并获取结果
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()

    if not columns:
        messagebox.showinfo('查询结果', '没有找到数据。')
        query_window.destroy()
        return

    # 创建表格视图
    treeview = ttk.Treeview(query_window)
    treeview.pack(fill='both', expand=True)

    # 添加水平滚动条
    scrollbar_x = ttk.Scrollbar(query_window, orient='horizontal', command=treeview.xview)
    scrollbar_x.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=scrollbar_x.set)

    # 添加表头
    treeview['columns'] = columns
    treeview.heading('#0', text='Index')  # 添加索引列
    for column in columns:
        treeview.heading(column, text=column)

    # 添加数据行
    for index, row in enumerate(data, start=1):
        treeview.insert('', 'end', text=index, values=row)

    def execute_query():
        column_name = column_entry.get()
        column_value = value_entry.get()

        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = %s', (column_value,))
        query_data = cursor.fetchall()
        cursor.close()

        treeview.delete(*treeview.get_children())  # 清空表格视图

        # 添加数据行
        for index, row in enumerate(query_data, start=1):
            treeview.insert('', 'end', text=index, values=row)

        # 查询输入框和按钮

    query_frame = tk.Frame(query_window)
    query_frame.pack(pady=10)

    column_label = tk.Label(query_frame, text='列名：')
    column_label.pack(side='left')

    column_entry = tk.Entry(query_frame)
    column_entry.pack(side='left')

    value_label = tk.Label(query_frame, text='值：')
    value_label.pack(side='left')

    value_entry = tk.Entry(query_frame)
    value_entry.pack(side='left')

    query_button = tk.Button(query_frame, text='查询', command=execute_query)
    query_button.pack(side='left')
#更新界面函数
def update_data_page(table_name):

    def show_table_data():
        # 查询表格数据
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        cursor.close()

        # 创建数据窗口
        data_window = tk.Toplevel(root)
        data_window.title(table_name)
        data_window.geometry('1600x600')

        # 创建表格视图
        treeview = ttk.Treeview(data_window)
        treeview.pack(fill='both', expand=True)
        # 添加水平滚动条
        scrollbar_x = ttk.Scrollbar(data_window, orient='horizontal', command=treeview.xview)
        scrollbar_x.pack(side='bottom', fill='x')
        treeview.configure(xscrollcommand=scrollbar_x.set)
        # 添加表头
        treeview['columns'] = columns
        treeview.heading('#0', text='索引')  # 添加索引列
        for column in columns:
            treeview.heading(column, text=column)

        # 添加数据行
        for index, row in enumerate(data, start=1):
            treeview.insert('', 'end', text=index, values=row)

        def add_data():
            # 创建添加数据窗口
            add_window = tk.Toplevel(data_window)
            add_window.title('添加数据')

            # 创建滚动条
            scrollbar = tk.Scrollbar(add_window)
            scrollbar.pack(side='right', fill='y')

            # 创建文本框
            text = tk.Text(add_window, yscrollcommand=scrollbar.set)
            text.pack(side='left', fill='both', expand=True)

            # 关联滚动条和文本框
            scrollbar.config(command=text.yview)

            entry_values = []
            for col in columns:
                label = tk.Label(text, text=col)
                label.pack(anchor='w')
                entry = tk.Entry(text)
                entry.pack(anchor='w')
                entry_values.append(entry)

            def save_data():
                # 获取输入数据
                values = []
                for entry in entry_values:
                    value = entry.get()
                    if value == "":
                        value = None
                    values.append(value)

                # 执行插入操作
                cursor = conn.cursor()
                cursor.execute(f'INSERT INTO {table_name} VALUES ({", ".join(["%s"] * len(values))})', tuple(values))
                conn.commit()
                cursor.close()

                messagebox.showinfo('添加成功', '数据添加成功！')

                # 刷新数据
                show_table_data()

                # 关闭添加数据窗口
                add_window.destroy()

            # 创建保存按钮
            save_button = tk.Button(add_window, text='保存', command=save_data)
            save_button.pack()

        def delete_data():
            # 创建删除数据窗口
            delete_window = tk.Toplevel(data_window)
            delete_window.title('删除数据')

            # 创建滚动条
            scrollbar = tk.Scrollbar(delete_window)
            scrollbar.pack(side='right', fill='y')

            # 创建文本框
            text = tk.Text(delete_window, yscrollcommand=scrollbar.set)
            text.pack(side='left', fill='both', expand=True)

            # 关联滚动条和文本框
            scrollbar.config(command=text.yview)

            label = tk.Label(text, text=columns[0])
            label.pack(anchor='w')
            entry = tk.Entry(text)
            entry.pack(anchor='w')

            def delete_rows():
                # 获取输入数据
                delete_value = entry.get().replace('(', '').replace(')', '')

                # 生成删除条件
                delete_query = f'DELETE FROM {table_name} WHERE {columns[0]} = %s'

                cursor = conn.cursor()
                cursor.execute(delete_query, (delete_value,))
                conn.commit()
                cursor.close()

                messagebox.showinfo('删除成功', '数据删除成功！')

                # 刷新数据
                show_table_data()

                # 关闭删除数据窗口
                delete_window.destroy()

            # 创建删除按钮
            delete_button = tk.Button(delete_window, text='删除', command=delete_rows)
            delete_button.pack()

        def modify_data():
            # 创建修改数据窗口
            modify_window = tk.Toplevel(data_window)
            modify_window.title('修改数据')

            # 创建标签和文本框用于输入要修改的列名、对应的值和修改后的值
            label_column = tk.Label(modify_window, text='列名:')
            label_column.pack(anchor='w')
            entry_column = tk.Entry(modify_window)
            entry_column.pack(anchor='w')

            label_old_value = tk.Label(modify_window, text='原始值:')
            label_old_value.pack(anchor='w')
            entry_old_value = tk.Entry(modify_window)
            entry_old_value.pack(anchor='w')

            label_new_value = tk.Label(modify_window, text='修改后的值:')
            label_new_value.pack(anchor='w')
            entry_new_value = tk.Entry(modify_window)
            entry_new_value.pack(anchor='w')

            def modify_row():
                # 获取输入的列名、原始值和修改后的值
                column = entry_column.get()
                old_value = entry_old_value.get()
                new_value = entry_new_value.get()
                # 生成更新语句
                update_query = f'UPDATE {table_name} SET {column} = %s WHERE {column} = %s'

                cursor = conn.cursor()
                cursor.execute(update_query,(new_value, old_value))
                conn.commit()
                cursor.close()
                messagebox.showinfo('修改成功', '数据修改成功！')

                # 刷新数据
                show_table_data()

                # 关闭修改数据窗口
                modify_window.destroy()

                # 创建修改按钮

            modify_button = tk.Button(modify_window, text='修改', command=modify_row)
            modify_button.pack()

        button_frame = tk.Frame(data_window)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text='添加', command=add_data)
        add_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(button_frame, text='删除', command=delete_data)
        delete_button.grid(row=0, column=1, padx=5)

        update_button = tk.Button(button_frame, text='修改', command=modify_data)
        update_button.grid(row=0, column=2, padx=5)

    show_table_data()
#人事档案
def query_renshi_page(table_name):
    query_renshi_window = tk.Toplevel(root)
    query_renshi_window.title(table_name)
    query_renshi_window.geometry('1600x600')

    # 根据表名执行查询并获取结果
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()

    if not columns:
        messagebox.showinfo('查询结果', '没有找到数据。')
        query_renshi_window.destroy()
        return

    # 创建表格视图
    treeview = ttk.Treeview(query_renshi_window)
    treeview.pack(fill='both', expand=True)

    # 添加水平滚动条
    scrollbar_x = ttk.Scrollbar(query_renshi_window, orient='horizontal', command=treeview.xview)
    scrollbar_x.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=scrollbar_x.set)

    # 添加表头
    treeview['columns'] = columns
    treeview.heading('#0', text='Index')  # 添加索引列
    for column in columns:
        treeview.heading(column, text=column)

     # 添加数据行
    for index, row in enumerate(data, start=1):
        treeview.insert('', 'end', text=index, values=row)

    def execute_query():
        column_name = column_entry.get()
        column_value = value_entry.get()

        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = %s', (column_value,))
        query_data = cursor.fetchall()
        cursor.close()

        treeview.delete(*treeview.get_children())  # 清空表格视图

        # 添加数据行
        for index, row in enumerate(query_data, start=1):
            treeview.insert('', 'end', text=index, values=row)

        # 生成统计报表
        df = pd.DataFrame(query_data, columns=columns)
        statistics = df.groupby(column_name).size().reset_index(name='Count')

        statistics_window = tk.Toplevel(query_renshi_window)
        statistics_window.title('统计报表')
        statistics_window.geometry('600x400')

        statistics_text = tk.Text(statistics_window)
        statistics_text.pack(fill='both', expand=True)

        statistics_text.insert(tk.END, '统计报表:\n\n')
        statistics_text.insert(tk.END, statistics.to_string(index=False))

    # 查询输入框和按钮
    query_frame = tk.Frame(query_renshi_window)
    query_frame.pack(pady=10)

    column_label = tk.Label(query_frame, text='列名：')
    column_label.pack(side='left')

    column_entry = tk.Entry(query_frame)
    column_entry.pack(side='left')

    value_label = tk.Label(query_frame, text='值：')
    value_label.pack(side='left')

    value_entry = tk.Entry(query_frame)
    value_entry.pack(side='left')

    query_button = tk.Button(query_frame, text='查询', command=execute_query)
    query_button.pack(side='left')
#考勤
def query_kaoqin_page(table_name):
    query_kaoqin_window = tk.Toplevel(root)
    query_kaoqin_window.title(table_name)
    query_kaoqin_window.geometry('1600x600')

    # 根据表名执行查询并获取结果
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()

    if not columns:
        messagebox.showinfo('查询结果', '没有找到数据。')
        query_renshi_window.destroy()
        return

    # 创建表格视图
    treeview = ttk.Treeview(query_kaoqin_window)
    treeview.pack(fill='both', expand=True)

    # 添加水平滚动条
    scrollbar_x = ttk.Scrollbar(query_kaoqin_window, orient='horizontal', command=treeview.xview)
    scrollbar_x.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=scrollbar_x.set)

    # 添加表头
    treeview['columns'] = columns
    treeview.heading('#0', text='Index')  # 添加索引列
    for column in columns:
        treeview.heading(column, text=column)

     # 添加数据行
    for index, row in enumerate(data, start=1):
        treeview.insert('', 'end', text=index, values=row)

    def execute_query():
        column_name = column_entry.get()
        column_value = value_entry.get()

        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = %s', (column_value,))
        query_data = cursor.fetchall()
        cursor.close()

        treeview.delete(*treeview.get_children())  # 清空表格视图

        # 添加数据行
        for index, row in enumerate(query_data, start=1):
            treeview.insert('', 'end', text=index, values=row)

        # 获取出勤次数、加班次数、出差次数的列索引
        attendance_index = columns.index('出勤次数')
        overtime_index = columns.index('加班次数')
        business_trip_index = columns.index('出差次数')

        # 提取出勤次数、加班次数、出差次数的数据
        attendance_data = [row[attendance_index] for row in query_data]
        overtime_data = [row[overtime_index] for row in query_data]
        business_trip_data = [row[business_trip_index] for row in query_data]

        # 生成柱状图
        plt.figure(figsize=(8, 6))
        plt.bar(range(len(attendance_data)), attendance_data, label='出勤次数')
        plt.bar(range(len(overtime_data)), overtime_data, label='加班次数')
        plt.bar(range(len(business_trip_data)), business_trip_data, label='出差次数')
        plt.xlabel('Index')
        plt.ylabel('Count')
        plt.title('Kaoqin Data')
        plt.legend()
        plt.show()

    # 查询输入框和按钮
    query_frame = tk.Frame(query_kaoqin_window)
    query_frame.pack(pady=10)

    column_label = tk.Label(query_frame, text='列名：')
    column_label.pack(side='left')

    column_entry = tk.Entry(query_frame)
    column_entry.pack(side='left')

    value_label = tk.Label(query_frame, text='值：')
    value_label.pack(side='left')

    value_entry = tk.Entry(query_frame)
    value_entry.pack(side='left')

    query_button = tk.Button(query_frame, text='查询', command=execute_query)
    query_button.pack(side='left')
# 辅料查询
def query_fuliao_page(table_name):
    query_fuliao_window = tk.Toplevel(root)
    query_fuliao_window.title(table_name)
    query_fuliao_window.geometry('1600x600')

    # 根据表名执行查询并获取结果
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()

    if not columns:
        messagebox.showinfo('查询结果', '没有找到数据。')
        query_fuliao_window.destroy()
        return

    # 创建表格视图
    treeview = ttk.Treeview(query_fuliao_window)
    treeview.pack(fill='both', expand=True)

    # 添加水平滚动条
    scrollbar_x = ttk.Scrollbar(query_fuliao_window, orient='horizontal', command=treeview.xview)
    scrollbar_x.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=scrollbar_x.set)

    # 添加表头
    treeview['columns'] = columns
    treeview.heading('#0', text='Index')  # 添加索引列
    for column in columns:
        treeview.heading(column, text=column)

     # 添加数据行
    for index, row in enumerate(data, start=1):
        treeview.insert('', 'end', text=index, values=row)

    def execute_query():
        column_name = column_entry.get()
        column_value = value_entry.get()

        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = %s', (column_value,))
        query_data = cursor.fetchall()
        cursor.close()

        treeview.delete(*treeview.get_children())  # 清空表格视图

        # 添加数据行
        for index, row in enumerate(query_data, start=1):
            treeview.insert('', 'end', text=index, values=row)

    # 查询输入框和按钮
    query_frame = tk.Frame(query_fuliao_window)
    query_frame.pack(pady=10)

    column_label = tk.Label(query_frame, text='列名：')
    column_label.pack(side='left')

    column_entry = tk.Entry(query_frame)
    column_entry.pack(side='left')

    value_label = tk.Label(query_frame, text='值：')
    value_label.pack(side='left')

    value_entry = tk.Entry(query_frame)
    value_entry.pack(side='left')

    query_button = tk.Button(query_frame, text='查询', command=execute_query)
    query_button.pack(side='left')
#订购查询
def query_chaxun_page(table_name):
    query_chaxun_window = tk.Toplevel(root)
    query_chaxun_window.title(table_name)
    query_chaxun_window.geometry('1600x600')

    # 根据表名执行查询并获取结果
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()

    if not columns:
        messagebox.showinfo('查询结果', '没有找到数据。')
        query_chaxun_window.destroy()
        return

    # 创建表格视图
    treeview = ttk.Treeview(query_chaxun_window)
    treeview.pack(fill='both', expand=True)

    # 添加水平滚动条
    scrollbar_x = ttk.Scrollbar(query_chaxun_window, orient='horizontal', command=treeview.xview)
    scrollbar_x.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=scrollbar_x.set)

    # 添加表头
    treeview['columns'] = columns
    treeview.heading('#0', text='Index')  # 添加索引列
    for column in columns:
        treeview.heading(column, text=column)

     # 添加数据行
    for index, row in enumerate(data, start=1):
        treeview.insert('', 'end', text=index, values=row)

    def execute_query():
        column_name = column_entry.get()
        column_value = value_entry.get()

        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = %s', (column_value,))
        query_data = cursor.fetchall()
        cursor.close()

        treeview.delete(*treeview.get_children())  # 清空表格视图

        # 添加数据行
        for index, row in enumerate(query_data, start=1):
            treeview.insert('', 'end', text=index, values=row)

    # 查询输入框和按钮
    query_frame = tk.Frame(query_chaxun_window)
    query_frame.pack(pady=10)

    column_label = tk.Label(query_frame, text='列名：')
    column_label.pack(side='left')

    column_entry = tk.Entry(query_frame)
    column_entry.pack(side='left')

    value_label = tk.Label(query_frame, text='值：')
    value_label.pack(side='left')

    value_entry = tk.Entry(query_frame)
    value_entry.pack(side='left')

    query_button = tk.Button(query_frame, text='查询', command=execute_query)
    query_button.pack(side='left')

# 公司销售管理系统窗口
def main_window():
    def inquire_page():
        inquire_window = tk.Toplevel(root)
        inquire_window.title('信息查询')
        inquire_window.geometry('800x1600')

        # 创建画布
        canvas = tk.Canvas(inquire_window, width=800, height=1600)
        canvas.pack()

        # 添加背景图像
        bg_image = tk.PhotoImage(file='E:/sqlpython/sql/cha.gif')  # 请将'inquire.gif'替换为您的背景图像文件路径
        canvas.create_image(0, 0, anchor='nw', image=bg_image)

        # 设置标题
        title_label = tk.Label(inquire_window, text='信息查询', font=('Arial', 18), bg='white')
        title_label_window = canvas.create_window(400, 50, anchor='center', window=title_label)

        # 设置按钮样式
        button_width = 20
        button_height = 3
        button_font = ('Arial', 12)
        button_bg = 'lightblue'
        button_fg = 'black'
        button_relief = 'raised'
        button_padding = 10

        # 设置按钮位置
        button_x = 250
        button_y = 150
        button_spacing_x = 300
        button_spacing_y = 100

        query_buttons = [
            ('药用辅料产品规格编码表', '药用辅料产品规格编码表'),
            ('外贸部客户档案表', '外贸部客户档案表'),
            ('研部客户流水表', '研部客户流水表'),
            ('研部客户对接表', '研部客户对接表'),
            ('研发客户档案', '研发客户档案'),
            ('研发_客户信息', '研发_客户信息'),
            ('研发_赠样记录', '研发_赠样记录'),
            ('研发_销售数据', '研发_销售数据'),
            ('授权书总表', '授权书总表'),
            ('已有制剂的供应商变更', '已有制剂的供应商变更'),
            ('新品研发项目', '新品研发项目'),
            ('产品问题反馈表', '产品问题反馈表'),
            ('内贸部台账总表', '内贸部台账总表'),
            ('外贸部台账总表', '外贸部台账总表'),
            ('员工信息表', '员工信息表'),
            ('人事档案', '人事档案'),
            ('考勤表', '考勤表'),
            ('订购表', '订购表'),
        ]

        # 创建按钮
        for i, (text, table_name) in enumerate(query_buttons):
            col = i % 2
            row = i // 2
            button_x_pos = button_x + col * button_spacing_x
            button_y_pos = button_y + row * button_spacing_y

            button = tk.Button(inquire_window, text=text, command=lambda name=table_name: query_page(name),
                                width=button_width, height=button_height, font=button_font, bg=button_bg,
                                fg=button_fg, relief=button_relief)
            button_window = canvas.create_window(button_x_pos, button_y_pos, anchor='center', window=button)
        inquire_window.mainloop()

    def updata_page():
        if (role_id == 1 or role_id==2):
            messagebox.showerror('提示', '您没有更新数据的权限')
            return
        update_window = tk.Toplevel(root)
        update_window.title('更新数据')
        update_window.geometry('800x1600')

        # 创建画布
        canvas = tk.Canvas(update_window, width=800, height=1600)
        canvas.pack()

        # 添加背景图像
        bg_image = tk.PhotoImage(file='E:/sqlpython/sql/gai.gif')  # 请将'inquire.gif'替换为您的背景图像文件路径
        canvas.create_image(0, 0, anchor='nw', image=bg_image)

        # 设置标题
        title_label = tk.Label(update_window, text='更新数据', font=('Arial', 18), bg='white')
        title_label_window = canvas.create_window(400, 50, anchor='center', window=title_label)

        # 设置按钮样式
        button_width = 20
        button_height = 3
        button_font = ('Arial', 12)
        button_bg = 'lightgreen'
        button_fg = 'black'
        button_relief = 'raised'
        button_padding = 10

        # 设置按钮位置
        button_x = 250
        button_y = 150
        button_spacing_x = 300
        button_spacing_y = 100

        updata_buttons = [
            ('药用辅料产品规格编码表', '药用辅料产品规格编码表'),
            ('外贸部客户档案表', '外贸部客户档案表'),
            ('研部客户流水表', '研部客户流水表'),
            ('研部客户对接表', '研部客户对接表'),
            ('研发客户档案', '研发客户档案'),
            ('研发_客户信息', '研发_客户信息'),
            ('研发_赠样记录', '研发_赠样记录'),
            ('研发_销售数据', '研发_销售数据'),
            ('授权书总表', '授权书总表'),
            ('已有制剂的供应商变更', '已有制剂的供应商变更'),
            ('新品研发项目', '新品研发项目'),
            ('产品问题反馈表', '产品问题反馈表'),
            ('内贸部台账总表', '内贸部台账总表'),
            ('外贸部台账总表', '外贸部台账总表'),
            ('员工信息表', '员工信息表'),
            ('人事档案', '人事档案'),
            ('考勤表', '考勤表'),
            ('订购表', '订购表'),
        ]
        # 创建按钮
        for i, (text, table_name) in enumerate(updata_buttons):
            col = i % 2
            row = i // 2
            button_x_pos = button_x + col * button_spacing_x
            button_y_pos = button_y + row * button_spacing_y

            button = tk.Button(update_window, text=text, command=lambda name=table_name: update_data_page(name),
                               width=button_width, height=button_height, font=button_font, bg=button_bg,
                               fg=button_fg, relief=button_relief)
            button_window = canvas.create_window(button_x_pos, button_y_pos, anchor='center', window=button)
        update_window.mainloop()

    def delete_user_page():
        if role_id != 4:
            messagebox.showerror('提示', '您没有删除用户的权限')
            return
        delete_window = tk.Toplevel(root)
        delete_window.title('删除用户')
        delete_window.geometry('500x400')

        # 创建画布
        canvas = tk.Canvas(delete_window, width=500, height=400)
        canvas.pack()

        # 添加背景图像
        bg_image = tk.PhotoImage(file='E:/sqlpython/sql/3.gif')  # 替换为您的背景图像文件路径
        canvas.create_image(0, 0, anchor='nw', image=bg_image)

        # 设置标题
        title_label = tk.Label(delete_window, text='删除用户', font=('Arial', 18), bg='white')
        title_label_window = canvas.create_window(250, 30, anchor='center', window=title_label)

        # 设置标签和输入框
        username_label = tk.Label(delete_window, text='要删除的用户账号：', bg='white')
        username_label_window = canvas.create_window(250, 150, anchor='center', window=username_label)

        username_entry = tk.Entry(delete_window)
        username_entry_window = canvas.create_window(250, 180, anchor='center', window=username_entry)

        # 设置按钮样式
        button_width = 15
        button_height = 2
        button_font = ('Arial', 12)
        button_bg = 'lightpink'
        button_fg = 'black'
        button_relief = 'raised'

        def delete_user():
            username = username_entry.get()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM "User" WHERE username = %s', (username,))
            conn.commit()
            cursor.close()
            messagebox.showinfo('删除用户', '用户删除成功！')

        delete_button = tk.Button(delete_window, text='删除用户', command=delete_user,
                                  width=button_width, height=button_height, font=button_font,
                                  bg=button_bg, fg=button_fg, relief=button_relief)
        delete_button_window = canvas.create_window(250, 300, anchor='center', window=delete_button)
        delete_window.mainloop()

    def renyuan_page():
        if role_id != 4:
            messagebox.showerror('提示', '您没有人员管理的权限')
            return
        def show_all_data():
            query_renshi_page('人事档案')

        def show_all_data1():
            query_kaoqin_page('考勤表')

        renyuan_window = tk.Toplevel(root)
        renyuan_window.title('人员管理')
        renyuan_window.geometry('800x600')

        # 创建画布
        canvas = tk.Canvas(renyuan_window, width=800, height=600)
        canvas.pack()

        # 添加背景图像
        bg_image = tk.PhotoImage(file='E:/sqlpython/sql/1.gif')  # 替换为您的背景图像文件路径
        canvas.create_image(0, 0, anchor='nw', image=bg_image)

        # 设置标题
        title_label = tk.Label(renyuan_window, text='人员管理', font=('Arial', 18), bg='white')
        title_label_window = canvas.create_window(400, 50, anchor='center', window=title_label)

        # 设置按钮样式
        button_width = 20
        button_height = 3
        button_font = ('Arial', 12)
        button_bg = 'lightyellow'
        button_fg = 'black'
        button_relief = 'raised'
        button_padding = 10

        # 人事档案按钮
        show_data_button = tk.Button(renyuan_window, text='人事档案', command=show_all_data,
                                     width=button_width, height=button_height, font=button_font,
                                     bg=button_bg, fg=button_fg, relief=button_relief)
        show_data_button_window = canvas.create_window(400, 200, anchor='center', window=show_data_button)

        # 考勤统计按钮
        show_data_button1 = tk.Button(renyuan_window, text='考勤统计', command=show_all_data1,
                                      width=button_width, height=button_height, font=button_font,
                                      bg=button_bg, fg=button_fg, relief=button_relief)
        show_data_button1_window = canvas.create_window(400, 350, anchor='center', window=show_data_button1)

        renyuan_window.mainloop()

    def dinggou_page():

        def show_all_data2():
            query_fuliao_page('药用辅料产品规格编码表')
        def show_all_data3():
            query_chaxun_page('订购表')

        def submit_order():
            # 创建订购页面
            order_window = tk.Toplevel(dinggou_window)
            order_window.title('订购')
            order_window.geometry('800x600')

            # 输入框列表
            input_fields = []

            def add_input_fields():
                # 创建新的输入框
                input_frame = tk.Frame(order_window)
                input_frame.pack(pady=10)

                fuliao_label = tk.Label(input_frame, text='辅料销售编码：')
                fuliao_label.pack(side='left')

                fuliao_entry = tk.Entry(input_frame)
                fuliao_entry.pack(side='left')

                weight_label = tk.Label(input_frame, text='重量：')
                weight_label.pack(side='left')

                weight_entry = tk.Entry(input_frame)
                weight_entry.pack(side='left')

                # 将输入框添加到列表
                input_fields.append((fuliao_entry, weight_entry))

            # 添加辅料和重量按钮
            add_button = tk.Button(order_window, text='添加辅料和重量', command=add_input_fields)
            add_button.pack()

            def calculate_amount():
                total_amount = 0

                # 遍历输入框列表，计算每个输入框中的金额
                for fuliao_entry, weight_entry in input_fields:
                    fuliao = fuliao_entry.get()
                    weight = float(weight_entry.get())

                    # 查询药用辅料产品规格编码表获取对应的值
                    cursor = conn.cursor()
                    cursor.execute("SELECT 标签右上角体现 FROM 药用辅料产品规格编码表 WHERE 销售部编码 = %s", (fuliao,))
                    result = cursor.fetchone()
                    cursor.close()

                    if result:
                        value = float(result[0])
                        amount = weight * value
                        total_amount += amount

                # 创建结算界面
                payment_window = tk.Toplevel(order_window)
                payment_window.title('结算')
                payment_window.geometry('800x600')

                # 显示所需金额
                amount_label = tk.Label(payment_window, text=f'所需金额：{total_amount}')
                amount_label.pack()

                qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=10,
                                        border=4)
                qr_code.add_data(total_amount)
                qr_code.make(fit=True)
                qr_image = qr_code.make_image(fill_color="black", back_color="white")
                qr_photo = ImageTk.PhotoImage(qr_image)
                qr_label = tk.Label(payment_window, image=qr_photo)
                qr_label.image = qr_photo
                qr_label.pack()

                def process_payment():
                    # 处理付款完成的代码
                    messagebox.showinfo('付款成功', '付款已完成。')

                # 付款按钮
                payment_button = tk.Button(payment_window, text='付款', command=process_payment)
                payment_button.pack()

            # 计算金额按钮
            calculate_button = tk.Button(order_window, text='计算金额', command=calculate_amount)
            calculate_button.pack()

            def submit_form():
                # 提交表单并添加到订购表中
                for fuliao_entry, weight_entry in input_fields:
                    fuliao = fuliao_entry.get()
                    weight = float(weight_entry.get())

                    # 查询药用辅料产品规格编码表获取对应的值
                    cursor = conn.cursor()
                    cursor.execute("SELECT 标签右上角体现 FROM 药用辅料产品规格编码表 WHERE 销售部编码 = %s", (fuliao,))
                    result = cursor.fetchone()
                    cursor.close()

                    if result:
                        value = float(result[0])
                        amount = weight * value
                        # 添加到订购表
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO 订购表 (用户账号, 订购辅料, 订购重量, 金额) VALUES (%s, %s, %s, %s)",
                                       (user_account, fuliao, weight, amount))
                        conn.commit()
                        cursor.close()

                    messagebox.showinfo('提交成功', '表单提交成功。')

            # 提交表单按钮
            submit_button = tk.Button(order_window, text='提交表单', command=submit_form)
            submit_button.pack()

        dinggou_window = tk.Toplevel(root)
        dinggou_window.title('客户订购')
        dinggou_window.geometry('800x600')
        # 创建画布
        canvas = tk.Canvas(dinggou_window, width=800, height=600)
        canvas.pack()

        # 添加背景图像
        bg_image = tk.PhotoImage(file='E:/sqlpython/sql/2.gif')  # 替换为您的背景图像文件路径
        canvas.create_image(0, 0, anchor='nw', image=bg_image)

        # 设置标题
        title_label = tk.Label(dinggou_window, text='客户订购', font=('Arial', 18), bg='white')
        title_label_window = canvas.create_window(400, 50, anchor='center', window=title_label)

        # 设置按钮样式
        button_width = 20
        button_height = 3
        button_font = ('Arial', 12)
        button_bg = 'lightyellow'
        button_fg = 'black'
        button_relief = 'raised'
        button_padding = 10

        # 查询辅料按钮
        show_data_button = tk.Button(dinggou_window, text='查询辅料', command=show_all_data2,
                                     width=button_width, height=button_height, font=button_font,
                                     bg=button_bg, fg=button_fg, relief=button_relief)
        show_data_button_window = canvas.create_window(400, 180, anchor='center', window=show_data_button)

        # 订购按钮
        order_button = tk.Button(dinggou_window, text='订购', command=submit_order,
                                 width=button_width, height=button_height, font=button_font,
                                 bg=button_bg, fg=button_fg, relief=button_relief)
        order_button_window = canvas.create_window(400, 330, anchor='center', window=order_button)

        # 订购查询按钮
        show_data_button = tk.Button(dinggou_window, text='订购查询', command=show_all_data3,
                                     width=button_width, height=button_height, font=button_font,
                                     bg=button_bg, fg=button_fg, relief=button_relief)
        show_data_button_window = canvas.create_window(400, 480, anchor='center', window=show_data_button)

        dinggou_window.mainloop()

    root.withdraw()  # 隐藏根窗口

    main_window = tk.Toplevel(root)
    main_window.title('公司销售管理系统')
    main_window.geometry('1200x800')

    def on_close():
        root.destroy()
        sys.exit()

    main_window.protocol('WM_DELETE_WINDOW', on_close)  # 绑定关闭事件
    # 创建画布
    canvas = tk.Canvas(main_window, width=1200, height=800)
    canvas.pack()

    # 添加背景图像
    bg_image = tk.PhotoImage(file='E:/sqlpython/sql/main.gif')  # 请将'background.png'替换为你的背景图像文件路径
    canvas.create_image(0, 0, anchor='nw', image=bg_image)

    # 显示欢迎信息
    welcome_label = tk.Label(main_window, text='欢迎使用公司销售系统', font=('Arial', 18), bg='white')
    welcome_label_window = canvas.create_window(600, 100, anchor='center', window=welcome_label)

    # 查询按钮
    query_button = tk.Button(main_window, text='查询', command=lambda: inquire_page(), width=15, height=3,
                             font=('Arial', 12), bg='lightblue', fg='black', relief='raised')
    query_button_window = canvas.create_window(300, 250, anchor='center', window=query_button)

    # 更新数据按钮
    update_button = tk.Button(main_window, text='更新数据', command=lambda: updata_page(), width=15, height=3,
                              font=('Arial', 12), bg='lightgreen', fg='black', relief='sunken')
    update_button_window = canvas.create_window(900, 250, anchor='center', window=update_button)

    # 人员管理按钮
    renyuan_button = tk.Button(main_window, text='人员管理', command=lambda: renyuan_page(), width=15, height=3,
                               font=('Arial', 12), bg='lightyellow', fg='black', relief='ridge')
    renyuan_button_window = canvas.create_window(300, 450, anchor='center', window=renyuan_button)

    # 订购辅料按钮
    dinggou_button = tk.Button(main_window, text='订购辅料', command=lambda: dinggou_page(), width=15, height=3,
                               font=('Arial', 12), bg='orange', fg='black', relief='flat')
    dinggou_button_window = canvas.create_window(900, 450, anchor='center', window=dinggou_button)

    # 删除用户按钮
    delete_button = tk.Button(main_window, text='删除用户', command=lambda: delete_user_page(), width=15, height=3,
                              font=('Arial', 12), bg='pink', fg='black', relief='groove')
    delete_button_window = canvas.create_window(300, 650, anchor='center', window=delete_button)

    # 退出按钮
    exit_button = tk.Button(main_window,text='退出', command=on_close, width=15, height=3,
                            font=('Arial', 12), bg='gray', fg='black', relief='groove')
    exit_button_window = canvas.create_window(900, 650, anchor='center', window=exit_button)
    main_window.mainloop()

# 用户登录函数
def login():
    global role_id  # 声明使用全局变量
    global user_account  # 声明使用全局变量
    username = username_entry.get()
    password = password_entry.get()

    cursor = conn.cursor()
    cursor.execute('SELECT id, role_id FROM "User" WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        user_id, role_id = user
        messagebox.showinfo('登录成功', '登录成功！')
        user_account=username
        # 在这里添加根据权限进行相应操作的逻辑
        if role_id == 1:
            # 普通用户
            pass
        elif role_id == 2:
            # 业务经理
            pass
        elif role_id == 3:
            # 销售经理
            print('销售经理登录')
            pass
        elif role_id == 4:
            # 管理员
            print('管理员登录')
            pass

        main_window()
    else:
        messagebox.showerror('登录失败', '用户名或密码错误')

# 注册界面函数
def register():
    def register_user():
        username = username_entry.get()
        password = password_entry.get()

        cursor = conn.cursor()
        cursor.execute('INSERT INTO "User" (username, password, role_id) VALUES (%s, %s, %s)', (username, password, 1))
        conn.commit()
        cursor.close()

        messagebox.showinfo('注册成功', '注册成功！')

        register_window.destroy()

    register_window = tk.Toplevel(root)
    register_window.title('注册')
    register_window.geometry('500x400')

    # 创建画布
    canvas = tk.Canvas(register_window, width=500, height=400)
    canvas.pack()

    # 添加背景图像
    bg_image = tk.PhotoImage(file='E:/sqlpython/sql/3.gif')  # 替换为您的背景图像文件路径
    canvas.create_image(0, 0, anchor='nw', image=bg_image)

    # 设置标题
    title_label = tk.Label(register_window, text='注册', font=('Arial', 18), bg='white')
    title_label_window = canvas.create_window(250, 30, anchor='center', window=title_label)

    # 设置标签和输入框
    username_label = tk.Label(register_window, text='用户名:', bg='white')
    username_label_window = canvas.create_window(150, 150, anchor='center', window=username_label)

    username_entry = tk.Entry(register_window)
    username_entry_window = canvas.create_window(280, 150, anchor='center', window=username_entry)

    password_label = tk.Label(register_window, text='密码:', bg='white')
    password_label_window = canvas.create_window(150, 200, anchor='center', window=password_label)

    password_entry = tk.Entry(register_window, show='*')
    password_entry_window = canvas.create_window(280, 200, anchor='center', window=password_entry)

    # 设置按钮样式
    button_width = 15
    button_height = 2
    button_font = ('Arial', 12)
    button_bg = 'lightyellow'
    button_fg = 'black'
    button_relief = 'raised'

    # 注册按钮
    register_button = tk.Button(register_window, text='注册', command=register_user,
                                width=button_width, height=button_height, font=button_font,
                                bg=button_bg, fg=button_fg, relief=button_relief)
    register_button_window = canvas.create_window(250, 300, anchor='center', window=register_button)

    register_window.mainloop()

# 创建开始界面
root = tk.Tk()
root.title('开始界面')
root.geometry('1200x800')

# 创建画布
canvas = tk.Canvas(root, width=1200, height=800)
canvas.pack()

# 导入背景图像
bg_image = tk.PhotoImage(file='E:/sqlpython/sql/be.gif')  # 替换为您的背景图像文件路径
canvas.create_image(0, 0, anchor='nw', image=bg_image)

# 显示"公司销售系统"文本
title_label = tk.Label(canvas, text='公司销售系统', font=('Arial', 24), bg='white')
title_label.place(x=600, y=100, anchor='center')

# 设置用户名输入框样式
username_label = tk.Label(canvas, text='用户名:', font=('Arial', 14), bg='white')
username_label.place(x=150, y=200)
username_entry = tk.Entry(canvas, font=('Arial', 14))
username_entry.place(x=250, y=200)

# 设置密码输入框样式
password_label = tk.Label(canvas, text='密码:', font=('Arial', 14), bg='white')
password_label.place(x=170, y=250)
password_entry = tk.Entry(canvas, show='*', font=('Arial', 14))
password_entry.place(x=250, y=250)

# 设置登录按钮样式
login_button = tk.Button(canvas, text='登录', command=login, width=10, height=2, font=('Arial', 14), bg='lightgreen', fg='black')
login_button.place(x=200, y=300)

# 设置注册按钮样式
register_button = tk.Button(canvas, text='注册', command=register, width=10, height=2, font=('Arial', 14), bg='lightyellow', fg='black')
register_button.place(x=350, y=300)

root.mainloop()
# 关闭数据库连接
conn.close()