import tkinter as tk
from tkinter import scrolledtext, messagebox
from text_blind_watermark import TextBlindWatermark

class TextWatermarkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("文本盲水印工具")
        self.root.geometry("800x600")
        
        # 初始化水印工具（稍后用）
        self.twm = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # 0. 加载文本（简化，直接用输入框）
        title0 = tk.Label(self.root, text="文本", font=("Arial", 12, "bold"))
        title0.pack(pady=5)
        
        # 1. 嵌入水印
        frame1 = tk.LabelFrame(self.root, text="1. 嵌入密文（加密）", font=("Arial", 12, "bold"))
        frame1.pack(fill="both", expand=True, padx=0, pady=5)
        
        # 原文部分
        tk.Label(frame1, text="密码:", width=6,anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.pwd_embed = tk.Entry(frame1, width=20, show="*")
        self.pwd_embed.grid(row=0, column=0, sticky="w", padx=50, pady=5)

# 水印部分（类似）
        tk.Label(frame1, text="密文:", width=6).grid(row=0, column=2, sticky="w", padx=(0, 5), pady=5)  # 左侧 10 像素分隔上一组
        self.wm_embed = tk.Entry(frame1, width=20)
        self.wm_embed.insert(0, "隐藏的密文")
        self.wm_embed.grid(row=0, column=2, sticky="w", padx=50, pady=5)

# 列配置（在按钮后添加）
        frame1.grid_columnconfigure(0, weight=0)  # 密码标签
        frame1.grid_columnconfigure(1, weight=1)  # 密码输入
        frame1.grid_columnconfigure(2, weight=0)  # 水印标签
        frame1.grid_columnconfigure(3, weight=1)  # 水印输入
        
        # 输入文本
        tk.Label(frame1, text="输入原文:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.input_text_embed = scrolledtext.ScrolledText(frame1, width=40, height=8)
        self.input_text_embed.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # 输出文本
        tk.Label(frame1, text="输出明文:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.output_text_embed = scrolledtext.ScrolledText(frame1, width=40, height=8)
        self.output_text_embed.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Embed 按钮
        self.embed_btn = tk.Button(frame1, text="加密 ->", command=self.embed_watermark, bg="lightblue")
        self.embed_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_columnconfigure(2, weight=1)
        frame1.grid_rowconfigure(2, weight=1)
        
        # 2. 提取水印
        frame2 = tk.LabelFrame(self.root, text="2. 提取密文（解密）", font=("Arial", 12, "bold"))
        frame2.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 输入文本（水印文本）
        tk.Label(frame2, text="输入明文:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.input_text_extract = scrolledtext.ScrolledText(frame2, width=60, height=6)
        self.input_text_extract.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # 密码
        tk.Label(frame2, text="密码: ").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.pwd_extract = tk.Entry(frame2, width=20, show="*")
        self.pwd_extract.grid(row=2, column=1, padx=5, pady=5)
        
        # Extract 按钮
        self.extract_btn = tk.Button(frame2, text="解密 ->", command=self.extract_watermark, bg="lightgreen")
        self.extract_btn.grid(row=4, column=1, pady=10)
        
        frame2.grid_columnconfigure(1, weight=1)
        frame2.grid_rowconfigure(1, weight=1)
        
        # 提取结果
        tk.Label(frame2, text="密文:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.output_extract = tk.Entry(frame2, width=50)
        self.output_extract.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
    def embed_watermark(self):
        pwd = self.pwd_embed.get()
        if not pwd:
            messagebox.showerror("错误", "密码不能为空！")
            return
        wm = self.wm_embed.get()
        text = self.input_text_embed.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("错误", "请输入文本！")
            return
        
        try:
            self.twm = TextBlindWatermark(pwd=pwd.encode())
            text_with_wm = self.twm.add_wm_rnd(text=text, wm=wm.encode())
            self.output_text_embed.delete("1.0", tk.END)
            self.output_text_embed.insert("1.0", text_with_wm)
            messagebox.showinfo("成功", "水印嵌入完成！")
        except Exception as e:
            messagebox.showerror("错误", f"嵌入失败: {str(e)}")
    
    def extract_watermark(self):
        pwd = self.pwd_extract.get()
        if not pwd:
            messagebox.showerror("错误", "密码不能为空！")
            return
        text_with_wm = self.input_text_extract.get("1.0", tk.END).strip()
        if not text_with_wm:
            messagebox.showerror("错误", "请输入水印文本！")
            return
        
        try:
            self.twm = TextBlindWatermark(pwd=pwd.encode())
            watermark_extract = self.twm.extract(text_with_wm)
            self.output_extract.delete(0, tk.END)
            self.output_extract.insert(0, watermark_extract.decode())
            messagebox.showinfo("成功", "水印提取完成！")
        except Exception as e:
            messagebox.showerror("错误", f"密码错误: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextWatermarkGUI(root)
    root.mainloop()