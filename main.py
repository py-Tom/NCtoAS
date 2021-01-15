import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from db_operations import select, insert, select_name, select_table, update, remove, update_previous
from translator import translate

bg_col = '#CDD4DB'
hh_col = '#EFF6FD'
hl_col = '#A2B4C3'
hl_size = 4
fnt_col = '#0B212F'


class PathFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.nc_path = tk.StringVar()
        self.nc_label = tk.Label(self, text='NC: ', bg=bg_col, fg=fnt_col)
        self.nc_entry = tk.Entry(self, textvariable=self.nc_path, width=52, bg=hh_col, fg=fnt_col)
        self.nc_browse = tk.Button(self, text='Browse', command=lambda: self.nc_path.set(set_path('open')), bg=bg_col,
                                   fg=fnt_col)

        self.as_path = tk.StringVar()
        self.as_label = tk.Label(self, text='AS: ', bg=bg_col, fg=fnt_col)
        self.as_entry = tk.Entry(self, textvariable=self.as_path, width=52, bg=hh_col, fg=fnt_col)
        self.as_browse = tk.Button(self, text='Browse', command=lambda: self.as_path.set(set_path('save')), bg=bg_col,
                                   fg=fnt_col)

        self.nc_label.grid(column=0, row=0)
        self.nc_entry.grid(column=1, row=0)
        self.nc_browse.grid(column=2, row=0)

        self.as_label.grid(column=0, row=1)
        self.as_entry.grid(column=1, row=1)
        self.as_browse.grid(column=2, row=1)


class CoordFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.base_coord = tk.StringVar()
        self.base_label = tk.Label(self, text='BASE: ', bg=bg_col, fg=fnt_col)
        self.base_entry = tk.Entry(self, textvariable=self.base_coord, width=36, bg=hh_col, fg=fnt_col)
        self.base_chosen = tk.StringVar()
        self.base_values = ttk.Combobox(self, textvariable=self.base_chosen)
        self.base_values['values'] = select_name('base') + ['-- Change --']
        self.base_values.bind('<<ComboboxSelected>>', lambda _: self.callback(table='base'))

        self.tool_coord = tk.StringVar()
        self.tool_label = tk.Label(self, text='TOOL: ', bg=bg_col, fg=fnt_col)
        self.tool_entry = tk.Entry(self, textvariable=self.tool_coord, width=36, bg=hh_col, fg=fnt_col)
        self.tool_chosen = tk.StringVar()
        self.tool_values = ttk.Combobox(self, textvariable=self.tool_chosen)
        self.tool_values['values'] = select_name('tool') + ['-- Change --']
        self.tool_values.bind('<<ComboboxSelected>>', lambda _: self.callback(table='tool'))

        self.base_label.grid(column=0, row=0, sticky='nsew')
        self.base_entry.grid(column=1, row=0, sticky='nsew')
        self.base_values.grid(column=2, row=0, sticky='nsew')

        self.tool_label.grid(column=0, row=1, sticky='nsew')
        self.tool_entry.grid(column=1, row=1, sticky='nsew')
        self.tool_values.grid(column=2, row=1, sticky='nsew')

    def callback(self, event=None, table=None):
        if table == 'base':
            name = self.base_chosen.get()
            if name == '-- Change --':
                new_window = InsertWindow(root, table)
            else:
                self.base_coord.set(select(table, name, 'coord'))
        elif table == 'tool':
            name = self.tool_chosen.get()
            if name == '-- Change --':
                new_window = InsertWindow(root, table)
            else:
                self.tool_coord.set(select(table, name, 'coord'))
        else:
            raise ValueError
        return None


class InsertWindow(tk.Frame):
    def __init__(self, parent, label, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.window = tk.Toplevel(self.parent)
        self.window.resizable(width=False, height=False)
        self.frame = tk.Frame(self.window, highlightbackground=bg_col, highlightcolor=bg_col,
                              highlightthickness=hl_size, bg=bg_col)
        self.frame.pack()

        self.title = tk.Label(self.frame, text='change ' + label + ' values', bg=bg_col, fg=fnt_col)
        self.title.pack()

        self.operation_chosen = tk.StringVar()
        self.operation_values = ttk.Combobox(self.frame, textvariable=self.operation_chosen)
        self.operation_values['values'] = ['New', 'Update', 'Delete']
        self.operation_values.bind('<<ComboboxSelected>>', lambda _: self.operation(label))
        self.operation_values.pack()

        self.new_name_value = tk.StringVar()
        self.label_name = tk.Label(self.frame, text='NAME:', bg=bg_col, fg=fnt_col)
        self.new_name = tk.Entry(self.frame, textvariable=self.new_name_value, width=22, bg=hh_col, fg=fnt_col)

        self.new_coord_value = tk.StringVar()
        self.label_coord = tk.Label(self.frame, text='COORD:', bg=bg_col, fg=fnt_col)
        self.new_coord = tk.Entry(self.frame, textvariable=self.new_coord_value, width=22, bg=hh_col, fg=fnt_col)

        self.old_chosen = tk.StringVar()
        self.old_values = ttk.Combobox(self.frame, textvariable=self.old_chosen)
        self.old_values['values'] = select_name(label)

        self.accept_button = tk.Button(self.frame, text='OK', command=lambda: self.window.destroy(), bg=bg_col,
                                       fg=fnt_col)
        self.accept_button.pack()

    def operation(self, table):
        operation_chosen = self.operation_chosen.get()
        if operation_chosen == 'New':
            self.forget_all()
            self.label_name.pack()
            self.new_name.pack()
            self.label_coord.pack()
            self.new_coord.pack()
            self.accept_button.pack()
            self.accept_button.configure(
                command=lambda: [insert(table, self.new_name_value.get(), self.new_coord_value.get()),
                                 self.update_values(table), self.window.destroy()])
        elif operation_chosen == 'Update':
            self.forget_all()
            self.label_name.pack()
            self.old_values.pack()
            self.label_coord.pack()
            self.new_coord.pack()
            self.accept_button.pack()
            self.accept_button.configure(
                command=lambda: [update(table, self.old_chosen.get(), self.new_coord_value.get()),
                                 self.update_values(table), self.window.destroy()])
        elif operation_chosen == 'Delete':
            self.forget_all()
            self.label_name.pack()
            self.old_values.pack()
            self.accept_button.pack()
            self.accept_button.configure(
                command=lambda: [remove(table, self.old_chosen.get()), self.update_values(table),
                                 self.window.destroy()])
        else:
            raise ValueError
        return None

    def forget_all(self):
        self.label_name.pack_forget()
        self.new_name.pack_forget()
        self.label_coord.pack_forget()
        self.new_coord.pack_forget()
        self.old_values.pack_forget()
        self.accept_button.pack_forget()

    def update_values(self, table):
        if table == 'base':
            app.coord_frame.base_values['values'] = select_name('base') + ['-- Change --']
        elif table == 'tool':
            app.coord_frame.tool_values['values'] = select_name('tool') + ['-- Change --']
        else:
            raise ValueError
        return None


class MoveFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.speed_label = tk.Label(self, text='SPEED', bg=bg_col, fg=fnt_col)
        self.accuracy_label = tk.Label(self, text='ACCURACY', bg=bg_col, fg=fnt_col)

        self.rapid_speed = tk.IntVar()
        self.rapid_label = tk.Label(self, text='RAPID', bg=bg_col, fg=fnt_col)
        self.rapid_s = tk.Entry(self, textvariable=self.rapid_speed, width=6, bg=hh_col, fg=fnt_col)
        self.rapid_accuracy = tk.IntVar()
        self.rapid_a = tk.Entry(self, textvariable=self.rapid_accuracy, width=6, bg=hh_col, fg=fnt_col)

        self.line_speed = tk.IntVar()
        self.line_label = tk.Label(self, text='LINEAR', bg=bg_col, fg=fnt_col)
        self.line_s = tk.Entry(self, textvariable=self.line_speed, width=6, bg=hh_col, fg=fnt_col)
        self.line_accuracy = tk.IntVar()
        self.line_a = tk.Entry(self, textvariable=self.line_accuracy, width=6, bg=hh_col, fg=fnt_col)

        self.circular_speed = tk.IntVar()
        self.circular_label = tk.Label(self, text='CIRCULAR', bg=bg_col, fg=fnt_col)
        self.circular_s = tk.Entry(self, textvariable=self.circular_speed, width=6, bg=hh_col, fg=fnt_col)
        self.circular_accuracy = tk.IntVar()
        self.circular_a = tk.Entry(self, textvariable=self.circular_accuracy, width=6, bg=hh_col, fg=fnt_col)

        self.speed_label.grid(column=1, row=0)
        self.accuracy_label.grid(column=2, row=0, padx=8)

        self.rapid_label.grid(column=0, row=1, sticky='e')
        self.rapid_s.grid(column=1, row=1)
        self.rapid_a.grid(column=2, row=1)

        self.line_label.grid(column=0, row=2, sticky='e')
        self.line_s.grid(column=1, row=2)
        self.line_a.grid(column=2, row=2)

        self.circular_label.grid(column=0, row=3, sticky='e')
        self.circular_s.grid(column=1, row=3)
        self.circular_a.grid(column=2, row=3)


class OptionFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.option_label = tk.Label(self, text='', bg=bg_col, fg=fnt_col)
        self.option_speed = tk.IntVar()
        self.option1 = tk.Checkbutton(self, text='G-code speed', variable=self.option_speed,
                                      command=lambda: self.state_speed(), bg=bg_col,
                                      fg=fnt_col, selectcolor=hh_col, activebackground=bg_col, activeforeground=fnt_col)
        self.option_speed.set(1)
        self.option_base = tk.IntVar()
        self.option2 = tk.Checkbutton(self, text='Set robot base', variable=self.option_base, state='disabled',
                                      bg=bg_col,
                                      fg=fnt_col, selectcolor=bg_col, activebackground=bg_col, activeforeground=fnt_col)
        self.run_button = tk.Button(self, text='TRANSLATE', command=lambda: [self.update_values()],
                                    bg=bg_col, fg=fnt_col)
        self.last_button = tk.Button(self, text='\u21BA', command=lambda: [self.previous_values(), self.state_speed()],
                                     bg=bg_col, fg=fnt_col)

        self.option_label.grid(column=0, row=0, sticky='nsew', columnspan=2)
        self.option1.grid(column=0, row=1, sticky='nw')
        self.option2.grid(column=0, row=2, sticky='nw')
        self.last_button.grid(column=1, row=1, rowspan=1)
        self.run_button.grid(column=1, row=2, rowspan=1, sticky='nsew', pady=6, padx=8)

    def state_speed(self):
        val = self.option_speed.get()
        new_state = 'disabled' if val == 1 else 'normal'
        app.move_frame.rapid_s.configure(state=new_state)
        app.move_frame.line_s.configure(state=new_state)
        app.move_frame.circular_s.configure(state=new_state)

    def previous_values(self):
        values = select_table('previous')
        app.path_frame.nc_path.set(values[0])
        app.path_frame.as_path.set(values[1])
        app.coord_frame.base_coord.set(values[2])
        app.coord_frame.tool_coord.set(values[3])
        app.move_frame.rapid_speed.set(values[4])
        app.move_frame.rapid_accuracy.set(values[5])
        app.move_frame.line_speed.set(values[6])
        app.move_frame.line_accuracy.set(values[7])
        app.move_frame.circular_speed.set(values[8])
        app.move_frame.circular_accuracy.set(values[9])
        app.option_frame.option_speed.set(values[10])
        app.option_frame.option_base.set(values[11])
        return None

    def update_values(self):
        v0 = app.path_frame.nc_path.get()
        v1 = app.path_frame.as_path.get()
        v2 = app.coord_frame.base_coord.get()
        v3 = app.coord_frame.tool_coord.get()
        v4 = app.move_frame.rapid_speed.get()
        v5 = app.move_frame.rapid_accuracy.get()
        v6 = app.move_frame.line_speed.get()
        v7 = app.move_frame.line_accuracy.get()
        v8 = app.move_frame.circular_speed.get()
        v9 = app.move_frame.circular_accuracy.get()
        v10 = app.option_frame.option_speed.get()
        v11 = app.option_frame.option_base.get()
        update_previous(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)
        translate(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)
        return None


class FooterFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # self.readme = tk.Label(self, text='READ ME', bg=bg_col, fg=fnt_col)
        self.email = tk.Label(self, text='tomaszpierog@hotmail.com', bg=bg_col, fg=fnt_col)

        # self.readme.grid(column=0, row=0, sticky='sw')
        self.email.pack(anchor='e')


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.path_frame = PathFrame(self, highlightbackground=hl_col, highlightcolor=hl_col,
                                    highlightthickness=hl_size, bg=bg_col)
        self.coord_frame = CoordFrame(self, highlightbackground=hl_col, highlightcolor=hl_col,
                                      highlightthickness=hl_size, bg=bg_col)
        self.move_frame = MoveFrame(self, highlightbackground=hl_col, highlightcolor=hl_col,
                                    highlightthickness=hl_size, bg=bg_col)
        self.option_frame = OptionFrame(self, highlightbackground=hl_col, highlightcolor=hl_col,
                                        highlightthickness=hl_size, bg=bg_col)
        self.footer_frame = FooterFrame(self, highlightbackground=hl_col, highlightcolor=hl_col,
                                        highlightthickness=hl_size, bg=bg_col)

        self.path_frame.grid(column=0, row=0, sticky='nsew', columnspan=2)
        self.coord_frame.grid(column=0, row=1, sticky='nsew', columnspan=2)
        self.move_frame.grid(column=0, row=2, sticky='nsew')
        self.option_frame.grid(column=1, row=2, sticky='nsew')
        self.footer_frame.grid(column=0, row=3, sticky='nsew', columnspan=2)


def set_path(mode):
    if mode == 'open':
        root.filename = filedialog.askopenfilename(title='Select NC File',
                                                   filetypes=(('NC programs', '*.NC'), ('pg programs', '*.pg'),
                                                              ('all files', '*.*')))
    elif mode == 'save':
        root.filename = filedialog.asksaveasfilename(title='Select AS File', initialfile='.pg',
                                                     filetypes=(('AS programs', '*.pg'), ('NC programs', '*.NC'),
                                                                ('all files', '*.*')))
    else:
        root.filename = None

    file_path = root.filename
    return file_path


# window and widgets creation
root = tk.Tk()
root.title('NCtoAS')

stl = ttk.Style()
stl.theme_create('combostyle', parent='alt',
                 settings={'TCombobox':
                               {'configure':
                                    {'selectbackground': bg_col,
                                     'selectforeground': fnt_col,
                                     'fieldbackground': hh_col,
                                     'background': bg_col,
                                     'foreground': fnt_col
                                     }
                                }
                           }
                 )
stl.theme_use('combostyle')

app = Main(root)
app.pack()
app.option_frame.state_speed()
root.resizable(width=False, height=False)
root.mainloop()
