import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog

from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageDraw, ImageFont

import numpy as np
import cv2
import os
import threading

class PhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Photo Editor")
        self.root.geometry("1200x700")
        self.root.config(bg="#2C3E50")

        # Initialize main variables
        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.layers = []
        self.undo_stack = []
        self.redo_stack = []
        self.draw_mode = False
        self.draw_color = "black"
        self.draw_size = 5

        # GUI setup
        self.setup_gui()

    def setup_gui(self):
        # Toolbar for essential buttons
        toolbar = tk.Frame(self.root, bg="#1C2833")
        toolbar.pack(side=tk.TOP, fill="x")
        
        load_btn = ttk.Button(toolbar, text="Load Image", command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        save_btn = ttk.Button(toolbar, text="Save Image", command=self.save_image)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        undo_btn = ttk.Button(toolbar, text="Undo", command=self.undo)
        undo_btn.pack(side=tk.LEFT, padx=5, pady=5)

        redo_btn = ttk.Button(toolbar, text="Redo", command=self.redo)
        redo_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Sidebar for adjustments
        sidebar = tk.Frame(self.root, bg="#1C2833", width=200)
        sidebar.pack(side=tk.LEFT, fill="y")

        tk.Label(sidebar, text="Adjustments", bg="#1C2833", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        self.create_adjustment_slider(sidebar, "Brightness", self.adjust_brightness)
        self.create_adjustment_slider(sidebar, "Contrast", self.adjust_contrast)
        self.create_adjustment_slider(sidebar, "Saturation", self.adjust_saturation)
        self.create_adjustment_slider(sidebar, "Sharpness", self.adjust_sharpness)

        # Filter Buttons
        tk.Label(sidebar, text="Filters", bg="#1C2833", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        self.create_filter_button(sidebar, "HDR", self.apply_hdr)
        self.create_filter_button(sidebar, "Vintage", self.apply_vintage)
        self.create_filter_button(sidebar, "B&W", self.apply_black_white)
        self.create_filter_button(sidebar, "Vivid", self.apply_vivid)
        self.create_filter_button(sidebar, "Cool", self.apply_cool)

        # Toggle Dark/Light Theme
        theme_btn = ttk.Button(sidebar, text="Toggle Theme", command=self.toggle_theme)
        theme_btn.pack(fill="x", padx=10, pady=5)

        # Display Area
        self.image_label = tk.Label(self.root, bg="#34495E")
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Drawing Mode Toggle
        self.draw_btn = ttk.Button(sidebar, text="Draw", command=self.toggle_draw)
        self.draw_btn.pack(fill="x", padx=10, pady=5)

    def create_adjustment_slider(self, frame, label, command):
        lbl = tk.Label(frame, text=label, bg="#1C2833", fg="white")
        lbl.pack(anchor="w", padx=10)
        
        slider = ttk.Scale(frame, from_=0.5, to=2.0, orient="horizontal", command=command)
        slider.set(1.0)
        slider.pack(fill="x", padx=10, pady=5)

    def create_filter_button(self, frame, text, command):
        btn = ttk.Button(frame, text=text, command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.display_image(self.original_image)

    def save_image(self):
        if self.processed_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg")])
            if save_path:
                self.processed_image.save(save_path)
                messagebox.showinfo("Image Saved", "Your image has been saved successfully!")

    def display_image(self, img):
        img.thumbnail((700, 500))
        self.processed_image = img
        imgtk = ImageTk.PhotoImage(img)
        self.image_label.config(image=imgtk)

    def add_layer(self, img):
        self.layers.append(img)
        self.undo_stack.append(img.copy())

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            if self.undo_stack:
                self.display_image(self.undo_stack[-1])

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.display_image(self.undo_stack[-1])

    def adjust_brightness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Brightness(self.original_image)
            img = enhancer.enhance(float(value))
            self.display_image(img)
            self.add_layer(img)

    def adjust_contrast(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Contrast(self.original_image)
            img = enhancer.enhance(float(value))
            self.display_image(img)
            self.add_layer(img)

    def adjust_saturation(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Color(self.original_image)
            img = enhancer.enhance(float(value))
            self.display_image(img)
            self.add_layer(img)

    def adjust_sharpness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Sharpness(self.original_image)
            img = enhancer.enhance(float(value))
            self.display_image(img)
            self.add_layer(img)

    def apply_hdr(self):
        if self.original_image:
            img = self.original_image.filter(ImageFilter.DETAIL)
            self.display_image(img)
            self.add_layer(img)

    def apply_vintage(self):
        if self.original_image:
            sepia = ImageEnhance.Color(self.original_image).enhance(0.3)
            self.display_image(sepia)
            self.add_layer(sepia)

    def apply_black_white(self):
        if self.original_image:
            bw_image = self.original_image.convert("L")
            self.display_image(bw_image)
            self.add_layer(bw_image)

    def apply_vivid(self):
        if self.original_image:
            vivid_image = ImageEnhance.Color(self.original_image).enhance(1.5)
            self.display_image(vivid_image)
            self.add_layer(vivid_image)

    def apply_cool(self):
        if self.original_image:
            cool_image = self.original_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            self.display_image(cool_image)
            self.add_layer(cool_image)

    def toggle_theme(self):
        current_bg = self.root.cget('bg')
        if current_bg == "#2C3E50":
            self.root.config(bg="#ECF0F1")
            self.image_label.config(bg="#ECF0F1")
        else:
            self.root.config(bg="#2C3E50")
            self.image_label.config(bg="#34495E")

    def toggle_draw(self):
        self.draw_mode = not self.draw_mode
        self.draw_btn.config(text="Draw" if not self.draw_mode else "Stop Drawing")
        if self.draw_mode:
            self.root.bind("<B1-Motion>", self.draw)
        else:
            self.root.unbind("<B1-Motion>")

    def draw(self, event):
        if self.draw_mode and self.processed_image:
            draw = ImageDraw.Draw(self.processed_image)
            draw.line([(event.x, event.y), (event.x + self.draw_size, event.y + self.draw_size)], fill=self.draw_color, width=self.draw_size)
            self.display_image(self.processed_image)

root = tk.Tk()
app = PhotoEditor(root)
root.mainloop()


