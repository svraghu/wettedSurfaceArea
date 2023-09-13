import tkinter as tk
from tkinter import ttk, messagebox
import math
from sympy import sympify, SympifyError

class Shape:
    def __init__(self, name, dimensions):
        self.name = name
        self.dimensions = dimensions
    def surface_area(self, *args):
        raise NotImplementedError
    def volume(self, *args):
        raise NotImplementedError
    
class ConicalFrustrum(Shape):
    def __init__(self):
        super().__init__('Conical Frustrum',['Small Diameter', 'Large Diameter', 'Length'])
    def surface_area(self, sdiameter, ldiameter, length):
        r1 = sdiameter / 2
        r2 = ldiameter / 2
        sa = math.pi * ((r1+r2)*((((r1-r2)**2)+length**2)**0.5))
        return sa
    def volume(self, sdiameter, ldiameter, length):
        r1 = sdiameter / 2
        r2 = ldiameter / 2
        vol = ((r1**2 + r2**2 + (r1*r2)) * math.pi * length) / 3 #V = (1/3) * π * h * (r1^2 + r2^2 + (r1 * r2)) 
        return vol

class Tube(Shape):
    def __init__(self):
        super().__init__('Tube',['Diameter', 'Length'])
    def surface_area(self, diameter, length):
        sa = math.pi * diameter * length
        return sa
    def volume(self, diameter, length):
        vol = math.pi * (diameter/2)**2 * length
        return vol

class TwoDBag(Shape):
    def __init__(self):
        super().__init__('2D Bag',['Length', 'Height'])
    def surface_area(self, length, width):
        sa = 2 * length * width
        return sa
    def volume(self, length, width):
        vol = math.pi * (width/2)**2 * length 
        return vol

class ThreeDBiocontainer(Shape):
    def __init__(self):
        super().__init__('3D Rectangular Biocontainer',['Length', 'Width', 'Height'])
    def surface_area(self, length, width, height):
        sa = 2 * (length * width + width * height + length * height)
        return sa
    def volume(self, length, width, height):
        vol = length * width * height
        return vol
    
class Tee(Shape):
    def __init__(self):
        super().__init__('Tee',['Horizontal ID', 'Vertical ID', 'Length', 'Height', 'Flange OD'])
    def surface_area(self, id_1, id_2, length, height, flange):
        trunk_height = height - ((flange - id_1)/2) - id_1
        area_tube_1 = math.pi * id_1 * length
        area_tube_2 = math.pi * id_2 * trunk_height
        sa = area_tube_1 + area_tube_2
        return sa
    def volume(self, id_1, id_2, length, height, flange):
        r1 = id_1 / 2
        r2 = id_2 / 2
        trunk_height = height - ((flange - id_1)/2) - id_1
        vol = ( math.pi * length * r1**2 ) + ( math.pi * trunk_height * r2**2)
        return vol

class Elbow(Shape):
    def __init__(self):
        super().__init__('Elbow',['Horizontal ID', 'Vertical ID', 'Length', 'Height'])
    def surface_area(self, id_1, id_2, length, height):
        arc_length = math.radians(90)
        area_tube_1 = math.pi * id_1 * length
        area_tube_2 = math.pi * id_2 * height
        area_curve = math.pi * id_2 * arc_length
        sa = area_tube_1 + area_tube_2 + area_curve
        return sa
    def volume(sself, id_1, id_2, length, height):
        r1 = id_1 / 2
        r2 = id_2 / 2
        arc_length = math.radians(90)
        vol = ( math.pi * length * r1**2 ) + ( math.pi * height * r2**2) + (math.pi * arc_length * r2**2)
        return vol

class Cross(Shape):
    def __init__(self):
        super().__init__('Cross',['Horizontal ID', 'Vertical ID', 'Length', 'Height'])
    def surface_area(self, id_1, id_2, length, height):
        area_tube_1 = math.pi * id_1 * length
        area_tube_2 = math.pi * id_2 * height
        intersection_area = math.pi * (id_2/2)**2
        sa = area_tube_1 + area_tube_2 - intersection_area
        return sa
    def volume(self, id_1, id_2, length, height):
        r1 = id_1 / 2
        r2 = id_2 / 2
        vol = ( math.pi * length * r1**2 ) + ( math.pi * height * r2**2) - (math.pi * r2**2)
        return vol
    
class Wye(Shape):
    def __init__(self):
        super().__init__('Wye',['Tusk ID', 'Trunk ID', 'Length', 'Height'])#arc length can be a variable, but currently estimated as 30*
    def surface_area(self, id_1, id_2, length, height):
        tusk_height = (height - (2 * math.cos(math.radians(30))*(id_1/2)))/2
        tusk_length = tusk_height / math.sin(math.radians(30))
        tusk_area = 2 * math.pi * id_1 * tusk_length
        trunk_length = (length - (math.cos(math.radians(30)) * tusk_length)) - ((id_1/2)*math.sin(math.radians(30)))
        trunk_area = math.pi * id_2 * trunk_length
        sa_curve = math.radians(30) * id_2
        intersection_area = math.pi * (id_2/2)**2  # Assuming a full circle intersection
        sa = tusk_area + trunk_area + sa_curve - intersection_area
        return sa
    def volume(self, id_1, id_2, length, height):
        tusk_height = (height - (2 * math.cos(math.radians(30))*(id_1/2)))/2
        tusk_length = tusk_height / math.sin(math.radians(30))
        trunk_length = (length - (math.cos(math.radians(30)) * tusk_length)) - ((id_1/2)*math.sin(math.radians(30)))
        vol_tusk = 2 * ( math.pi * tusk_length * (id_1 / 2)**2 )
        vol_trunk = ( math.pi * trunk_length * (id_2 / 2)**2 )
        arc_length = math.radians(30) * id_2
        vol_curve = (arc_length * (id_2 / 2)**2 * math.pi) / 3
        vol = vol_tusk + vol_trunk + vol_curve
        return vol

class ThreeDRdBottle(Shape):
    def __init__(self):
        super().__init__('3D Round Bottle',['ID', 'Height'])
    def surface_area(self, id_1, height):
        sa = ( 2 * math.pi * ( (id_1 / 2) **2 )) + ( math.pi * id_1 * height )
        return sa
    def volume(self, id_1, height):
        vol = math.pi * height * (id_1 / 2)**2
        return vol

class Cap(Shape):
    def __init__(self):
        super().__init__('Cap',['ID'])
    def surface_area(self, id_1):
        sa =  math.pi * ( (id_1 / 2) **2 )
        return sa
    def volume(self, id_1):
        vol = 0.0
        return vol

class Flask(Shape):
    def __init__(self):
        super().__init__('Flask',['Small Diameter', 'Large Diameter', 'Height'])
    def surface_area(self, sdiameter, ldiameter, height):
        r1 = sdiameter / 2
        r2 = ldiameter / 2
        sa = math.pi * ((r1+r2)*((((r1-r2)**2)+height**2)**0.5))+(r2**2)
        return sa
    def volume(self, sdiameter, ldiameter, height):
        r1 = sdiameter / 2
        r2 = ldiameter / 2
        vol = ((r1**2 + r2**2 + (r1*r2)) * math.pi * height) / 3 #V = (1/3) * π * h * (r1^2 + r2^2 + (r1 * r2)) 
        return vol

class Plug(Shape):
    def __init__(self):
        super().__init__('Plug',['Diameter', 'Length'])
    def surface_area(self, diameter, length):
        sa = (math.pi * (diameter/2)**2) + (math.pi * diameter * length)
        return sa
    def volume(self, diameter, length):
        vol = 0.0
        return vol

SHAPES = [Tube(), TwoDBag(), ThreeDBiocontainer(),  ThreeDRdBottle(), Flask(), ConicalFrustrum(), Tee(), Elbow(), Cross(), Wye(), Cap(), Plug()]
compute_after_id = None
def compute_values(event=None):
    global compute_after_id
    if compute_after_id:
        app.after_cancel(compute_after_id)
    compute_after_id = app.after(100, computing_values)
def computing_values():
    selected_shape_name = shape_combobox.get()
    shape_class = SHAPE_CLASSES[selected_shape_name]
    shape_instance = shape_class()
    try:
        values = [float(sympify(entry.get())) if entry.get() else 0 for entry in shape_entries]
        sa = shape_instance.surface_area(*values)
        vol = shape_instance.volume(*values)
        sa_var.set(f"Surface Area: {sa:,.2f} cm\u00B2")
        volume_var.set(f"Volume: {vol:,.2f} cm\u00B3")
    except (ValueError, SympifyError):
        messagebox.showerror("Error", "Please enter valid numbers or calculations for dimensions.")
def on_shape_change(event):
    shape_entries.clear()
    sa_var.set("")
    volume_var.set("")
    
    for widget in dynamic_widgets:
        widget.grid_remove()
    dynamic_widgets.clear()
    
    selected_shape_name = shape_combobox.get()
    for idx, dimension in enumerate(SHAPE_CLASSES[selected_shape_name]().dimensions, start=1):
        label = ttk.Label(app, text=f"{dimension}:")
        entry = ttk.Entry(app)
        label.grid(row=idx, column=0, sticky="e", pady=5)
        entry.grid(row=idx, column=1, pady=5)
        dynamic_widgets.extend([label, entry])
        shape_entries.append(entry)

    sa_label.grid(row=len(dynamic_widgets)//2 + 1, column=0, columnspan=2, pady=5)
    volume_label.grid(row=len(dynamic_widgets)//2 + 2, column=0, columnspan=2, pady=5)
    compute_button.grid(row=len(dynamic_widgets)//2 + 3, column=0, pady=20)
    quit_button.grid(row=len(dynamic_widgets)//2 + 3, column=1, pady=20)

app = tk.Tk()
app.title("Shape Calculator")
app.columnconfigure(0, weight=1, uniform="col1")
app.columnconfigure(1, weight=1, uniform="col1")
shape_label = ttk.Label(app, text="Choose a shape:")
shape_label.grid(row=0, column=0, sticky="e", pady=5)
shape_combobox = ttk.Combobox(app, values=[shape.name for shape in SHAPES], state="readonly")
shape_combobox.grid(row=0, column=1, pady=5)
shape_combobox.bind("<<ComboboxSelected>>", on_shape_change)
dynamic_widgets = []
shape_entries = []
sa_var = tk.StringVar()
volume_var = tk.StringVar()
sa_label = ttk.Label(app, textvariable=sa_var)
volume_label = ttk.Label(app, textvariable=volume_var)
SHAPE_CLASSES = {shape.name: type(shape) for shape in SHAPES}

#Compute & Quit
compute_button = ttk.Button(app, text="Compute", command=compute_values)
quit_button = ttk.Button(app, text="Quit", command=app.destroy)
app.mainloop()
