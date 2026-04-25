def center_toplevel(window, parent=None):
    window.update_idletasks()

    width = window.winfo_width() or window.winfo_reqwidth()
    height = window.winfo_height() or window.winfo_reqheight()

    if parent is not None:
        parent.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        x = parent_x + max((parent_width - width) // 2, 0)
        y = parent_y + max((parent_height - height) // 2, 0)
    else:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = max((screen_width - width) // 2, 0)
        y = max((screen_height - height) // 2, 0)

    window.geometry(f"{width}x{height}+{x}+{y}")
