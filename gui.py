"""
    PAF GUI
    Paf application -> linux compatibility
"""

import customtkinter

from paf_core import weather as wht


class Paf(customtkinter.CTk):
    """application GUI class"""
    def __init__(self):
        super().__init__()

        self.title('my app')
        self.geometry('600x300')
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.temp_act = wht.TemActual()
        self.temp_act.dat('Madrid')
        data_dict = self.temp_act.temp()

        self.temp_box = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.temp_box.grid(row=0, column=0, sticky='nsew', )
        self.temp_box.insert('0.0', f'La temperatura actual es de: {data_dict["temp"]}ºC')

        self.humi_box = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.humi_box.grid(row=1, column=0, sticky='nsew', )
        self.humi_box.insert('0.0', f'La humedad actual es de: {data_dict["humi"]}%')

        self.vient_box = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.vient_box.grid(row=2, column=0, sticky='nsew', )
        self.vient_box.insert('0.0', f'La velocidad del viento es de: {data_dict["vient"]}m/s')

        self.des_box = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.des_box.grid(row=3, column=0, sticky='nsew', )
        self.des_box.insert('0.0', data_dict['des'])

        self.button = customtkinter.CTkButton(self, text='Actualiza!', command=self.button_callback)
        self.button.grid(row=0, column=1, sticky='nsew', rowspan=4)

    def button_callback(self):
        """Update button"""

        self.temp_act.dat('Madrid')
        data_dict = self.temp_act.temp()

        self.temp_box.destroy()
        self.temp_box = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.temp_box.grid(row=0, column=0, sticky='nsew', )
        self.temp_box.insert('0.0', f'{data_dict["temp"]} ºC')

        self.humi_box.destroy()
        self.humi_box = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.humi_box.grid(row=1, column=0, sticky='nsew', )
        self.humi_box.insert('0.0', f'La humedad actual es de: {data_dict["humi"]}%')

        self.vient_box.destroy()
        self.vient_box = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.vient_box.grid(row=2, column=0, sticky='nsew', )
        self.vient_box.insert('0.0', f'La velocidad del viento es de: {data_dict["vient"]}m/s')

        self.des_box.destroy()
        self.des_box = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.des_box.grid(row=3, column=0, sticky='nsew', )
        self.des_box.insert('0.0', data_dict['des'])

        print('button pressed')

paf = Paf()
paf.mainloop()
