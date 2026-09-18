<div align="center">

# 公司销售管理系统

### 基于 Python + Tkinter + SQL Server 的桌面端公司销售管理系统

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-2022-red.svg)](https://www.microsoft.com/sql-server)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010-lightgrey.svg)](https://www.microsoft.com/windows)

</div>

---

## 📖 项目简介

本项目是一个基于 **Python** 与 **Tkinter** 图形界面库，并使用 **SQL Server Management Studio (SSMS)** 作为数据库管理系统的公司销售管理系统。系统旨在简化和自动化公司的销售管理流程，减少繁琐的手动操作和纸质记录，提高销售人员和管理人员的工作效率。

所有销售相关数据集中存储于 SQL Server 数据库中，保证数据的完整性和一致性；系统通过**多级用户权限机制**为不同角色提供差异化服务，满足使用者多方面的需求。

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🔐 **用户注册 / 登录** | 用户可注册账号并登录系统，四种角色对应不同操作权限 |
| 🔍 **信息查询** | 支持 18 张业务表的全表浏览，可按列名 + 值进行条件查询 |
| ✏️ **数据更新** | 对各业务表进行添加、删除、修改操作（需相应权限） |
| 👥 **人员管理** | 查看人事档案、统计人事报表、考勤统计可视化 |
| 🛒 **订购辅料** | 查询辅料、添加订购项、自动计算金额、扫码支付、提交订单 |
| 🗑️ **删除用户** | 管理员可删除用户账号，收回其登录权限 |
| 🚪 **退出系统** | 安全退出销售管理系统 |

---

## 🔑 权限设计

系统采用 **RBAC（基于角色的访问控制）** 模型，共四级权限：

| role_id | 角色 | 权限说明 |
|:-------:|------|----------|
| 1 | 普通用户 | 查询数据、订购辅料 |
| 2 | 业务经理 | 查询数据、订购辅料 |
| 3 | 销售经理 | 查询、订购、**更新数据** |
| 4 | 管理员 | 全部功能 + 人员管理 + 删除用户 |

新注册账号默认为**普通用户**。无权限操作时会弹出提示框拦截。

---

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 开发语言 | Python 3.x |
| 图形界面 | Tkinter（Canvas 画布 + 背景图 + ttk.Treeview 表格） |
| 数据库 | SQL Server 2022 Express（SSMS 管理） |
| 数据库连接 | pymssql |
| 数据统计 | pandas（groupby 分组统计报表） |
| 数据可视化 | matplotlib（考勤柱状图） |
| 支付功能 | qrcode + Pillow（生成支付二维码） |

---

## 🗄️ 数据库设计

### E-R 模型核心关系
<div align="center">
<img width="1300" height="770" alt="image" src="https://github.com/user-attachments/assets/ea1ee303-37f6-49f3-9a96-5f001964f77a" />

  </div>
<div align="center">
<img width="1277" height="842" alt="image" src="https://github.com/user-attachments/assets/ec703519-9b06-4ac0-9266-8b1f95673d2c" />
  </div>

<div align="center">
<img width="1295" height="1214" alt="image" src="https://github.com/user-attachments/assets/5b7e2483-09af-4681-8e5d-0811deca690e" />
  </div>

### 主要数据表

**权限相关（RBAC）：**

- `User`（id, username, password, role_id）
- `Role`（id, role_name）
- `Permission`（id, permission_name）
- `User_Permission`（role_id, permission_id）

**业务数据表（18 张）：**

- 药用辅料产品规格编码表
- 外贸部客户档案表 / 外贸部台账总表
- 研部客户流水表 / 研部客户对接表
- 研发客户档案 / 研发_客户信息 / 研发_赠样记录 / 研发_销售数据
- 授权书总表 / 已有制剂的供应商变更 / 新品研发项目
- 产品问题反馈表 / 内贸部台账总表
- 员工信息表 / 人事档案 / 考勤表 / 订购表

> 📌 `订购表` 用于记录用户订购记录（用户账号、订购辅料、订购重量、金额）；`客户信息`、`赠样记录`、`销售数据`、`电话销售拜访记录` 通过外键关联至研发服务部客户档案。

---

## 🖥️ 系统界面一览

| 界面 | 功能说明 |
|------|----------|
| **登录界面** | 输入用户名密码登录，支持跳转注册 |

<div align="center">
<img width="1203" height="843" alt="image" src="https://github.com/user-attachments/assets/f6f924ba-c5c1-4371-a661-7fb95ba298fe" />

  </div>
  
| **注册界面** | 注册新账号，默认普通用户权限 |
<div align="center">
<img width="508" height="451" alt="image" src="https://github.com/user-attachments/assets/0098f613-a951-425c-a54f-20c0f35ea166" />

  </div>
  
| **主界面** | 六大功能按钮入口，按权限展示 |
<div align="center">
<img width="1209" height="841" alt="image" src="https://github.com/user-attachments/assets/71aa5c82-aa96-46ff-917e-d9eda768e9ed" />

  </div>
  
| **信息查询** | 18 张表的按钮矩阵，点击进入对应表格 |
<div align="center">
<img width="799" height="1075" alt="image" src="https://github.com/user-attachments/assets/5e20b3c0-4d78-4a1d-bde8-cc71dba27c52" />

  </div>
  
| **表查询界面** | Treeview 全表展示 + 条件查询，支持横向滚动 |
<div align="center">
<img width="1605" height="639" alt="image" src="https://github.com/user-attachments/assets/ebc0bd59-ce22-41a0-b8e8-c8d972dfb513" />

  </div>
  
| **更新数据** | 添加 / 删除 / 修改三按钮，弹窗表单操作 |
<div align="center">
<img width="800" height="1075" alt="image" src="https://github.com/user-attachments/assets/468e0b90-a829-419a-a8fe-83ad565923ed" />
<img width="282" height="397" alt="image" src="https://github.com/user-attachments/assets/cd904adb-0000-4eb1-81e8-48d469f030c0" />

  </div>
  
| **人员管理** | 人事档案（含统计报表）+ 考勤统计（柱状图可视化） |
<div align="center">
<img width="802" height="640" alt="image" src="https://github.com/user-attachments/assets/58d7df83-7df3-43fd-8299-4d812e510d08" />
<img width="999" height="828" alt="image" src="https://github.com/user-attachments/assets/00302df6-1c0b-4ab4-bbd4-b0f8d340a32b" />

  </div>
  
| **客户订购** | 查询辅料 → 订购 → 金额计算 → 二维码支付 → 提交订单 |
<div align="center">
<img width="804" height="637" alt="image" src="https://github.com/user-attachments/assets/435dc1da-9b1b-4151-8ba5-42a9b0fc4ce6" />
  <img width="804" height="636" alt="image" src="https://github.com/user-attachments/assets/aaad7aa0-3f1c-4e5b-b797-f0ddb4d7a41b" />

<img width="801" height="637" alt="image" src="https://github.com/user-attachments/assets/f54d0c83-0079-4870-9811-eb0dcfffb82b" />

  </div>
  
| **删除用户** | 管理员输入账号即可删除用户 |
<div align="center">
<img width="506" height="446" alt="image" src="https://github.com/user-attachments/assets/8907659d-590b-471a-b63d-121ccaa8d7e1" />

  </div>

---

## 📊 功能亮点

- **统计报表**：使用 pandas 对查询结果 `groupby` 分组计数，在独立窗口以表格形式呈现（如统计“户口=城市”的人数）；
- **考勤可视化**：matplotlib 绘制出勤 / 加班 / 出差次数柱状图，支持按条件筛选后作图；
- **扫码支付**：`qrcode` 库根据订单总金额实时生成支付二维码；
- **界面美化**：Canvas 画布 + 自定义背景图，按钮分色区分功能、relief 样式差异化。

---

## 🧪 测试与维护

系统经过多轮测试，验证了登录注册、查询、客户订购等核心功能的正确性；通过模拟用户操作流程评估了界面易用性，优化了布局、输入验证和错误提示。后续将持续调试，定期备份数据库与代码。

---

## 📚 参考文献

[1] 王志刚，肖骏，方晓宇. 《SQL Server 从入门到精通》. 清华大学出版社， 2012
[2] 张良均，王路，谭立云，苏剑林. 《Python 数据分析与挖掘实战》. 机械工业出版社
[3] 钱雪忠. 《数据库原理及应用实验指导》. 北京邮电大学出版社， 2005
[4] 钱雪忠. 《数据原理及应用》. 北京邮电大学出版社， 2015

---

<div align="center">

**⭐ 如果本项目对你有帮助，欢迎 Star 支持！**

</div>
