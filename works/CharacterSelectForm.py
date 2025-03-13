"""
Created on Thu Mar  10 22:44:18 2023

@author: LUCAS
"""
import tkinter as tk

class CharacterSelectForm(tk.Toplevel):
    def __init__(self, master, character_list, team_size):
        super().__init__(master)
        self.title("Sélection des personnages")

        self.character_list = character_list
        self.team_size = team_size
        
        self.team_1 = []
        self.team_2 = []

        self._create_widgets()

    def _create_widgets(self):
        self.character_frame = tk.Frame(self)
        self.character_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.team_1_frame = tk.Frame(self)
        self.team_1_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.team_2_frame = tk.Frame(self)
        self.team_2_frame.pack(side=tk.LEFT, padx=10, pady=10)

        for i, character_name in enumerate(self.character_list):
            character_button = tk.Button(self.character_frame, text=character_name, command=lambda name=character_name: self._add_character(name))
            character_button.pack(fill=tk.X)

        self.team_1_label = tk.Label(self.team_1_frame, text="Équipe 1")
        self.team_1_label.pack()

        self.team_1_listbox = tk.Listbox(self.team_1_frame, height=self.team_size)
        self.team_1_listbox.pack(fill=tk.BOTH)

        self.team_1_remove_button = tk.Button(self.team_1_frame, text="Retirer", command=self._remove_character_1)
        self.team_1_remove_button.pack()

        self.team_2_label = tk.Label(self.team_2_frame, text="Équipe 2")
        self.team_2_label.pack()

        self.team_2_listbox = tk.Listbox(self.team_2_frame, height=self.team_size)
        self.team_2_listbox.pack(fill=tk.BOTH)

        self.team_2_remove_button = tk.Button(self.team_2_frame, text="Retirer", command=self._remove_character_2)
        self.team_2_remove_button.pack()

        self.validate_button = tk.Button(self, text="Valider", command=self.destroy)
        self.validate_button.pack(pady=10)
        self._update_validate()
        
    def _add_character(self, name):
        if len(self.team_1) < self.team_size:
            self.team_1.append(name)
            self.team_1_listbox.insert(tk.END, name)
        elif len(self.team_2) < self.team_size:
            self.team_2.append(name)
            self.team_2_listbox.insert(tk.END, name)
        self._update_validate()    

    def _remove_character_1(self):
        index = self.team_1_listbox.curselection()
        if index:
            name = self.team_1_listbox.get(index)
            self.team_1.remove(name)
            self.team_1_listbox.delete(index)
            self._update_validate()
            
    def _remove_character_2(self):
        index = self.team_2_listbox.curselection()
        if index:
            name = self.team_2_listbox.get(index)
            self.team_2.remove(name)
            self.team_2_listbox.delete(index)
            self._update_validate()

    def _update_validate(self):
        if len(self.team_2) >= self.team_size and len(self.team_1) >= self.team_size:
            self.validate_button.config(state=tk.NORMAL)
        else:
            self.validate_button.config(state=tk.DISABLED)
            
    def run(self):
        self.grab_set()
        self.wait_window()
        return self

