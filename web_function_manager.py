# /home/admin/Laborroboter/gui_app.py
#nice
from flaskr.compiler.motor_controller import MotorController
from positions_manager import PositionManager  # Importiere die neue Klasse
import threading
import time

STEPS_PER_CLICK = 500

class GUIApp:
    def __init__(self):

        self.controller = MotorController()
        self.position_manager = PositionManager()  # Instanz der PositionManager-Klasse
        self.position_labels = {}
        self.saved_position_buttons = []
        self.axiss:list[str] = ["X","Y","Z"]

        
        pos_dict = self.position_manager.load_pos_from_file("position.json")
        self.controller.set_positions(pos_dict)
        
        index = 0
        for axis in self.axiss:
            self.position_manager.save_position(index,pos_dict[axis])
            index += 1
        

    def move(self, axis, positive):
        direction = self.controller.DIR_TO_ENDSTOP if positive else self.controller.DIR_BACK
        self.controller.step_motor(axis, STEPS_PER_CLICK, direction)
        self.update_position_labels()
        self.position_manager.save_pos_in_file(self.controller.get_positions(), "position.json")

    def save_current_position(self, index):
        current_pos = self.controller.get_positions()
        self.position_manager.save_position(index, current_pos)
        self.update_saved_position_button(index)
        messagebox.showinfo("Gespeichert", f"Position {index+1} gespeichert:\n{current_pos}")

    def update_saved_position_button(self, index):
        pos = self.position_manager.get_position(index)
        if pos:
            self.saved_position_buttons[index].config(text=f"Pos {index+1}:\nX:{pos['X']} Y:{pos['Y']} Z:{pos['Z']}")
        else:
            self.saved_position_buttons[index].config(text=f"Pos {index+1}:\n-")

    def move_to_saved_position(self, index):
        pos:dict = self.position_manager.get_position(index)
        if not pos:
            messagebox.showwarning("Nicht definiert", f"Position {index+1} ist leer.")
            return

        current_pos = self.controller.get_positions()
        total_steps = sum(abs(pos[axis] - current_pos[axis]) for axis in self.axiss)
        total_steps = 0
        est_time = round(total_steps * 2 * 0.0001875, 1)

        def countdown():
            win = Toplevel()
            win.title("Bewegung läuft...")
            lbl = Label(win, text=f"Bewege zu Pos {index+1}...\n{est_time} Sekunden verbleiben", font=("Arial", 12))
            lbl.pack(padx=20, pady=20)
            for i in range(int(est_time), -1, -1):
                lbl.config(text=f"Bewege zu Pos {index+1}...\n{i} Sekunden verbleiben")
                time.sleep(1)
            win.destroy()
        
        self.position_manager.save_pos_in_file(pos, "position.json")
        threading.Thread(target=countdown, daemon=True).start()
        self.controller.move_all_axes_simultaneously(pos)
        self.update_position_labels()

    def update_position_labels(self):
        for axis in self.controller.get_positions():
            self.position_labels[axis].config(text=f"{axis}: {self.controller.get_positions()[axis]}")

    def set_axis_to_zero(self):
        messagebox.showinfo("Initialisierung", "Die Achsen werden jetzt genullt...")
        for axis in self.axiss:
            self.controller.drive_to_endstop(axis)
        self.position_manager.save_pos_in_file(self.controller.get_positions(), "position.json")    

    def start(self):
        self.root.mainloop()

