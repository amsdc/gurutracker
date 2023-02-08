import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('Treeview demo')
root.geometry('620x200')

# define columns
columns = ('first_name', 'last_name', 'email')

displaycolumns = ('first_name', 'last_name')

tree = ttk.Treeview(root, columns=columns, show='headings', selectmode=tk.BROWSE)
tree['displaycolumns'] = displaycolumns

# define headings
tree.heading('first_name', text='First Name', anchor=tk.W, command=lambda: print("ss"))
tree.heading('last_name', text='Last Name', anchor=tk.W)
tree.heading('email', text='Email')

# generate sample data
contacts = []
for n in range(1, 100):
    contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

# add data to the treeview
for contact in contacts:
    tree.insert('', tk.END, values=contact)


def item_selected(event):
    selected_item = tree.selection()[0]
    item = tree.item(selected_item)
    record = item['values']
    # show a message
    showinfo(title='Information', message=','.join(record))


tree.bind('<<TreeviewSelect>>', item_selected)

tree.grid(row=0, column=0, sticky='nsew')

# add a scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# run the app
root.mainloop()
