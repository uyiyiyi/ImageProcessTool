import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageDraw

# 创建主窗口
root = tk.Tk()
root.title("图片处理工具")

# 全局变量保存当前处理的图像
current_image = None
original_image = None

# 打开文件函数
def open_file():
    global current_image, original_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        current_image = Image.open(file_path)
        original_image = current_image.copy()
        display_image(current_image)

# 显示图像函数
def display_image(image):
    img = ImageTk.PhotoImage(image)
    panel.config(image=img)
    panel.image = img

# 保存文件函数
def save_file():
    if current_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            current_image.save(file_path)

# 图像缩放和裁剪
def resize_image(value):
    global current_image
    if current_image:
        scale_factor = float(value) / 100
        width, height = original_image.size
        new_size = (int(width * scale_factor), int(height * scale_factor))
        current_image = original_image.resize(new_size)
        display_image(current_image)

# 色彩调整
def adjust_color(value):
    global current_image
    if current_image:
        enhancer = ImageEnhance.Color(original_image)
        current_image = enhancer.enhance(float(value))
        display_image(current_image)

# 滤镜效果
def apply_filter(filter_type):
    global current_image
    if current_image:
        if filter_type == "模糊":
            current_image = original_image.filter(ImageFilter.BLUR)
        elif filter_type == "锐化":
            current_image = original_image.filter(ImageFilter.SHARPEN)
        elif filter_type == "边缘增强":
            current_image = original_image.filter(ImageFilter.EDGE_ENHANCE)
        display_image(current_image)

# 旋转和翻转
def rotate_flip(action):
    global current_image
    if current_image:
        if action == "水平翻转":
            current_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)
        elif action == "垂直翻转":
            current_image = original_image.transpose(Image.FLIP_TOP_BOTTOM)
        display_image(current_image)

def rotate_image(value):
    global current_image
    if current_image:
        current_image = original_image.rotate(float(value))
        display_image(current_image)

# 添加文本和标注
def add_text():
    global current_image
    if current_image:
        text = text_entry.get()
        if text:
            x = int(x_entry.get())
            y = int(y_entry.get())
            if x is not None and y is not None:
                image_editable = ImageDraw.Draw(current_image)
                image_editable.text((x, y), text, (255, 255, 255))
                display_image(current_image)

# 去噪和增强
def denoise_enhance(action):
    global current_image
    if current_image:
        if action == "去噪":
            current_image = original_image.filter(ImageFilter.MedianFilter(size=3))
        elif action == "增强细节":
            enhancer = ImageEnhance.Detail(original_image)
            current_image = enhancer.enhance(2.0)
        display_image(current_image)

# 形状识别和分割
def shape_recognition():
    global current_image
    if current_image:
        messagebox.showinfo("提示", "此功能尚未实现")

# 图像融合和混合
def image_blending():
    global current_image
    if current_image:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            image_to_blend = Image.open(file_path)
            image_to_blend = image_to_blend.resize(current_image.size)
            alpha = alpha_scale.get()
            if alpha:
                current_image = Image.blend(original_image, image_to_blend, alpha)
                display_image(current_image)

# 创建按钮
buttons = [
    ("选择图片", open_file),
    ("保存图片", save_file),
    ("形状识别和分割", shape_recognition),
    ("图像融合和混合", image_blending)
]

for text, command in buttons:
    button = tk.Button(root, text=text, command=command)
    button.pack(pady=5)

# 创建图像显示区域
panel = tk.Label(root)
panel.pack()

# 创建滑动条和功能
sliders = [
    ("缩放和裁剪", resize_image, 10, 200),
    ("色彩调整", adjust_color, 0.0, 2.0),
    ("旋转", rotate_image, 0, 360)
]

for label, command, from_, to_ in sliders:
    frame = tk.Frame(root)
    frame.pack(pady=5)
    tk.Label(frame, text=label).pack(side="left")
    scale = tk.Scale(frame, from_=from_, to=to_, orient="horizontal", resolution=0.01 if isinstance(from_, float) else 1, command=command)
    scale.pack(side="right")

# 滤镜效果按钮
filter_buttons = [
    ("模糊", lambda: apply_filter("模糊")),
    ("锐化", lambda: apply_filter("锐化")),
    ("边缘增强", lambda: apply_filter("边缘增强"))
]

for text, command in filter_buttons:
    button = tk.Button(root, text=text, command=command)
    button.pack(pady=5)

# 旋转和翻转按钮
rotate_flip_buttons = [
    ("水平翻转", lambda: rotate_flip("水平翻转")),
    ("垂直翻转", lambda: rotate_flip("垂直翻转"))
]

for text, command in rotate_flip_buttons:
    button = tk.Button(root, text=text, command=command)
    button.pack(pady=5)

# 添加文本输入框和按钮
text_frame = tk.Frame(root)
text_frame.pack(pady=5)
tk.Label(text_frame, text="文本:").pack(side="left")
text_entry = tk.Entry(text_frame)
text_entry.pack(side="left")
tk.Label(text_frame, text="X:").pack(side="left")
x_entry = tk.Entry(text_frame, width=5)
x_entry.pack(side="left")
tk.Label(text_frame, text="Y:").pack(side="left")
y_entry = tk.Entry(text_frame, width=5)
y_entry.pack(side="left")
add_text_button = tk.Button(text_frame, text="添加文本", command=add_text)
add_text_button.pack(side="left")

# 去噪和增强按钮
denoise_enhance_buttons = [
    ("去噪", lambda: denoise_enhance("去噪")),
    ("增强细节", lambda: denoise_enhance("增强细节"))
]

for text, command in denoise_enhance_buttons:
    button = tk.Button(root, text=text, command=command)
    button.pack(pady=5)

# 图像融合和混合滑动条
blend_frame = tk.Frame(root)
blend_frame.pack(pady=5)
tk.Label(blend_frame, text="图像融合因子:").pack(side="left")
alpha_scale = tk.Scale(blend_frame, from_=0.0, to=1.0, orient="horizontal", resolution=0.01)
alpha_scale.pack(side="right")

# 运行主循环
root.mainloop()
