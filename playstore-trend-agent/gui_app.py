import threading
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess
from datetime import datetime

from main import run_pipeline


# ---------- HELPERS ----------

def is_valid_url(url: str) -> bool:
    return url.startswith("https://play.google.com/store/apps/details?id=")


def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def open_csv_file(path):
    abs_path = os.path.abspath(path)
    if sys.platform.startswith("win"):
        os.startfile(abs_path)
    elif sys.platform == "darwin":
        subprocess.call(["open", abs_path])
    else:
        subprocess.call(["xdg-open", abs_path])


# ---------- BACKGROUND TASK ----------

def start_processing(app_url, target_date, status_label, progress, button):
    def task():
        try:
            status_label.config(text="⏳ Generating report… Please wait")
            progress.start(12)

            output_file = run_pipeline(app_url, target_date)

            progress.stop()
            status_label.config(text="✅ Report generated successfully")

            if os.path.isfile(output_file):
                messagebox.showinfo(
                    "Success",
                    f"Trend analysis report generated!\n\n{output_file}"
                )
                open_csv_file(output_file)
            else:
                messagebox.showwarning(
                    "File Not Found",
                    "Report generated but file could not be opened.\n"
                    "Please check the output folder manually."
                )

        except Exception as e:
            progress.stop()
            messagebox.showerror("Error", str(e))
        finally:
            button.config(state=tk.NORMAL)

    threading.Thread(target=task, daemon=True).start()


# ---------- GUI ----------

def launch_gui():
    root = tk.Tk()
    root.title("AI Trend Analysis")
    root.geometry("520x360")
    root.resizable(False, False)

    # Dark mode colors
    bg = "#1e1e1e"
    fg = "#ffffff"
    accent = "#4CAF50"

    root.configure(bg=bg)

    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "TProgressbar",
        troughcolor="#2b2b2b",
        background=accent
    )

    tk.Label(
        root,
        text="Google Play Review Trend Analysis",
        font=("Segoe UI", 14, "bold"),
        bg=bg,
        fg=fg
    ).pack(pady=14)

    # App URL
    tk.Label(root, text="App Store URL", bg=bg, fg=fg).pack(anchor="w", padx=25)
    app_url_entry = tk.Entry(root, width=62)
    app_url_entry.pack(padx=25)
    app_url_entry.insert(
        0,
        "https://play.google.com/store/apps/details?id=in.swiggy.android"
    )

    # Target Date
    tk.Label(root, text="Target Date (YYYY-MM-DD)", bg=bg, fg=fg)\
        .pack(anchor="w", padx=25, pady=(10, 0))
    date_entry = tk.Entry(root, width=62)
    date_entry.pack(padx=25)
    date_entry.insert(0, "2024-07-15")

    status_label = tk.Label(root, text="", bg=bg, fg="lightblue")
    status_label.pack(pady=10)

    progress = ttk.Progressbar(
        root,
        orient="horizontal",
        length=400,
        mode="indeterminate"
    )
    progress.pack(pady=6)

    def on_submit():
        app_url = app_url_entry.get().strip()
        target_date = date_entry.get().strip()

        if not is_valid_url(app_url):
            messagebox.showwarning(
                "Invalid URL",
                "Please enter a valid Google Play Store app URL."
            )
            return

        if not is_valid_date(target_date):
            messagebox.showwarning(
                "Invalid Date",
                "Date must be in YYYY-MM-DD format."
            )
            return

        generate_btn.config(state=tk.DISABLED)
        start_processing(app_url, target_date, status_label, progress, generate_btn)

    generate_btn = tk.Button(
        root,
        text="Generate Report",
        command=on_submit,
        width=24,
        bg=accent,
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold")
    )
    generate_btn.pack(pady=14)

    root.mainloop()


if __name__ == "__main__":
    launch_gui()
