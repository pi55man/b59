import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageDraw
import numpy as np

class PhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Editor")
        self.root.geometry("1920x1080")
        self.root.config(bg="#323434")

        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.zoom_scale = 1.0
        self.applied_adjustment = None
        self.applied_filter = None
        self.applied_fun_filter = None
        self.crop_rectangle = None
        self.temp_image = None
        self.current_angle = 0

        self.setup_gui()

    def setup_gui(self):
        toolbar = tk.Frame(self.root, bg="#323434")
        toolbar.pack(side=tk.TOP, fill="x")

        load_btn = ttk.Button(toolbar, text="Load Image", command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=5, pady=5)

        save_btn = ttk.Button(toolbar, text="Save Image", command=self.save_image)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        sidebar = tk.Frame(self.root, bg="#323434", width=150)
        sidebar.pack(side=tk.LEFT, fill="y")

        tk.Label(sidebar, text="Adjustments", bg="#323434", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        self.create_adjustment_slider(sidebar, "Brightness", self.adjust_brightness)
        self.create_adjustment_slider(sidebar, "Contrast", self.adjust_contrast)
        self.create_adjustment_slider(sidebar, "Saturation", self.adjust_saturation)
        self.create_adjustment_slider(sidebar, "Sharpness", self.adjust_sharpness)
        
        remove_adjustments_btn = ttk.Button(sidebar, text="Remove Adjustments", command=self.remove_adjustments)
        remove_adjustments_btn.pack(fill="x", padx=10, pady=5)
        

        tk.Label(sidebar, text="Filters", bg="#323434", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        self.create_filter_button(sidebar, "HDR", self.apply_hdr)
        self.create_filter_button(sidebar, "Vintage", self.apply_vintage)
        self.create_filter_button(sidebar, "B&W", self.apply_black_white)
        self.create_filter_button(sidebar, "Vivid", self.apply_vivid)
        self.create_filter_button(sidebar, "Cool", self.apply_cool)
        self.create_filter_button(sidebar, "Blur", self.apply_blur)

        remove_filters_btn = ttk.Button(sidebar, text="Remove Regular Filters", command=self.remove_regular_filters)
        remove_filters_btn.pack(fill="x", padx=10, pady=5)
        
        tk.Label(sidebar, text="Miscellaneous", bg="#323434", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        self.create_filter_button(sidebar, "Wave", self.apply_wave)
        self.create_filter_button(sidebar, "Pixelate", self.apply_pixelate)
        remove_fun_filters_btn = ttk.Button(sidebar, text="Remove Fun Filters", command=self.remove_fun_filters)
        remove_fun_filters_btn.pack(fill="x", padx=10, pady=5)


        crop_btn = ttk.Button(sidebar, text="Crop", command=self.enable_crop)
        crop_btn.pack(fill="x", padx=10, pady=5)

        zoom_in_btn = ttk.Button(sidebar, text="Zoom In", command=self.zoom_in)
        zoom_in_btn.pack(fill="x", padx=10, pady=5)
        zoom_out_btn = ttk.Button(sidebar, text="Zoom Out", command=self.zoom_out)
        zoom_out_btn.pack(fill="x", padx=10, pady=5)

        #TODO LATER
        # rotate_left_btn = ttk.Button(sidebar, text="Rotate Left", command=lambda: self.rotate_image(90))
        # rotate_left_btn.pack(fill="x", padx=10, pady=5)
    
        # rotate_right_btn = ttk.Button(sidebar, text="Rotate Right", command=lambda: self.rotate_image(-90))
        # rotate_right_btn.pack(fill="x", padx=10, pady=5)

        remove_filters_btn = ttk.Button(sidebar, text="Remove All Filters", command=self.remove_all_filters)
        remove_filters_btn.pack(fill="x", padx=10, pady=5)
        
        self.image_label = tk.Label(self.root, bg="#000000")
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)

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
            self.processed_image = self.original_image.copy()
            self.display_image(self.original_image)

    def save_image(self):
        if self.processed_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg")])
            if save_path:
                self.processed_image.save(save_path)
                messagebox.showinfo("Image Saved", "Your image has been saved successfully!")

    def display_image(self, img):
        img = img.resize((int(img.width * self.zoom_scale), int(img.height * self.zoom_scale)), Image.LANCZOS)
        imgtk = ImageTk.PhotoImage(img)
        self.image_label.config(image=imgtk)
        self.image_label.image = imgtk  

    def adjust_brightness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Brightness(self.original_image)
            img = enhancer.enhance(float(value))
            self.applied_adjustment = lambda img: ImageEnhance.Brightness(img).enhance(float(value))
            self.apply_filters()

    def adjust_contrast(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Contrast(self.original_image)
            img = enhancer.enhance(float(value))
            self.applied_adjustment = lambda img: ImageEnhance.Contrast(img).enhance(float(value))
            self.apply_filters()

    def adjust_saturation(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Color(self.original_image)
            img = enhancer.enhance(float(value))
            self.applied_adjustment = lambda img: ImageEnhance.Color(img).enhance(float(value))
            self.apply_filters()

    def adjust_sharpness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Sharpness(self.original_image)
            img = enhancer.enhance(float(value))
            self.applied_adjustment = lambda img: ImageEnhance.Sharpness(img).enhance(float(value))
            self.apply_filters()

    def apply_hdr(self):
        if self.original_image:
            img = self.original_image.filter(ImageFilter.DETAIL)
            self.applied_filter = lambda img: img.filter(ImageFilter.DETAIL)
            self.apply_filters()

    def apply_vintage(self):
        if self.original_image:
            sepia = ImageEnhance.Color(self.original_image).enhance(0.3)
            self.applied_filter = lambda img: ImageEnhance.Color(img).enhance(0.3)
            self.apply_filters()

    def apply_black_white(self):
        if self.original_image:
            bw_image = self.original_image.convert("L")
            self.applied_filter = lambda img: img.convert("L")
            self.apply_filters()

    def apply_vivid(self):
        if self.original_image:
            vivid_image = ImageEnhance.Color(self.original_image).enhance(1.5)
            self.applied_filter = lambda img: ImageEnhance.Color(img).enhance(1.5)
            self.apply_filters()

    def apply_cool(self):
        if self.original_image:
            cool_image = self.original_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            self.applied_filter = lambda img: img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            self.apply_filters()

    def apply_blur(self):
        if self.original_image:
            blurred_image = self.original_image.filter(ImageFilter.BLUR)
            self.applied_filter = lambda img: img.filter(ImageFilter.BLUR)
            self.apply_filters()

    def rotate_image(self, direction):
        if self.original_image:
            self.current_angle = (self.current_angle + direction) % 360
            rotated_image = self.original_image.rotate(self.current_angle, expand=True)
            
            self.processed_image = rotated_image
            self.display_image(rotated_image)
            self.apply_filters()  
    
    def apply_wave(self):
        if self.original_image:
            self.applied_fun_filter = lambda img: self.wave_filter(img)
            self.apply_filters()

    def apply_pixelate(self):
        if self.original_image:
            self.applied_fun_filter = lambda img: self.pixelate_filter(img)
            self.apply_filters()

    def wave_filter(self, img):
        img = np.array(img)
        height, width = img.shape[:2]
        amplitude = 10
        frequency = 20

        for y in range(height):
            offset = int(amplitude * np.sin(2 * np.pi * y / frequency))
            img[y] = np.roll(img[y], offset, axis=0)
        return Image.fromarray(img)

    def pixelate_filter(self, img):
        pixel_size = 10
        img = img.resize(
            (img.width // pixel_size, img.height // pixel_size),
            Image.NEAREST
        )
        img = img.resize(
            (img.width * pixel_size, img.height * pixel_size),
            Image.NEAREST
        )
        return img

    def apply_filters(self):
        img = self.original_image
        if self.applied_adjustment:
            img = self.applied_adjustment(img)
        if self.applied_filter:
            img = self.applied_filter(img)
        if self.applied_fun_filter:
            img = self.applied_fun_filter(img)
        self.processed_image = img
        self.display_image(img)

    def remove_all_filters(self):
        self.applied_adjustment = None
        self.applied_filter = None
        self.applied_fun_filter = None
        self.processed_image = self.original_image.copy()
        self.display_image(self.processed_image)
    
    def remove_adjustments(self):
        self.applied_adjustment = None
        self.apply_filters()

    def remove_regular_filters(self):
        self.applied_filter = None
        self.apply_filters()

    def remove_fun_filters(self):
        self.applied_fun_filter = None
        self.apply_filters()

    
    def enable_crop(self):
        self.crop_rectangle = None
        self.temp_image = self.processed_image.copy()  
        self.image_label.bind("<ButtonPress-1>", self.start_crop)
        self.image_label.bind("<B1-Motion>", self.update_crop)
        self.image_label.bind("<ButtonRelease-1>", self.finish_crop)

    def start_crop(self, event):
        x = int(event.x / self.zoom_scale)
        y = int(event.y / self.zoom_scale)
        self.crop_rectangle = [x, y, x, y]  

    def update_crop(self, event):
        if self.crop_rectangle:
            self.crop_rectangle[2] = int(event.x / self.zoom_scale)
            self.crop_rectangle[3] = int(event.y / self.zoom_scale)
            self.display_crop_rectangle() 

    def finish_crop(self, event):
        if self.crop_rectangle and self.processed_image:
            x1, y1, x2, y2 = self.crop_rectangle
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            
            if x2 > x1 and y2 > y1:
                cropped_image = self.processed_image.crop((x1, y1, x2, y2))
                self.processed_image = cropped_image
                self.display_image(cropped_image)
            
            self.image_label.unbind("<ButtonPress-1>")
            self.image_label.unbind("<B1-Motion>")
            self.image_label.unbind("<ButtonRelease-1>")
            self.crop_rectangle = None

    def display_crop_rectangle(self):
        
        if self.crop_rectangle and self.temp_image:
            img_copy = self.temp_image.copy()
            draw = ImageDraw.Draw(img_copy)
            x1, y1, x2, y2 = self.crop_rectangle
            draw.rectangle([x1 * self.zoom_scale, y1 * self.zoom_scale, x2 * self.zoom_scale, y2 * self.zoom_scale], outline="red", width=2)
            self.display_image(img_copy)  

    def zoom_in(self):
        self.zoom_scale *= 1.2
        self.display_image(self.processed_image)

    def zoom_out(self):
        self.zoom_scale /= 1.2
        self.display_image(self.processed_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoEditor(root)
    root.state('zoomed')
    root.mainloop()
