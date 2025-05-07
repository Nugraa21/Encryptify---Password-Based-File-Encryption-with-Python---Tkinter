import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet, InvalidToken
import os
import hashlib
import base64
import json

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption App")
        self.root.geometry("900x600")
        self.root.configure(bg="#0d1117")

        self.encrypted_folder = "encrypted_files"
        self.decrypted_folder = "decrypted_files"
        self.keys_folder = "keys"
        self.keys_file = os.path.join(self.keys_folder, "keys.json")

        for folder in [self.encrypted_folder, self.decrypted_folder, self.keys_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)
        if not os.path.exists(self.keys_file):
            with open(self.keys_file, 'w') as f:
                json.dump({}, f)

        self.setup_styles()
        self.setup_sidebar()
        self.setup_main_area()
        self.refresh_file_list()
        self.load_keys()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Helvetica", 12), background="#238636", foreground="#ffffff")
        self.style.configure("TLabel", background="#0d1117", foreground="#c9d1d9", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))

    def setup_sidebar(self):
        self.sidebar_frame = tk.Frame(self.root, bg="#161b22", width=200)
        self.sidebar_frame.pack(side="left", fill="y")

        self.toggle_button = tk.Button(self.sidebar_frame, text="☰", bg="#161b22", fg="#c9d1d9", relief="flat", command=self.toggle_sidebar)
        self.toggle_button.pack(pady=10, padx=10, anchor="w")

        self.nav_buttons = []
        for text, command in [
            ("Enkripsi File", self.encrypt_file),
            ("Dekripsi File", self.decrypt_file),
            ("Pengaturan", self.show_settings)
        ]:
            btn = tk.Button(self.sidebar_frame, text=text, bg="#161b22", fg="#c9d1d9", relief="flat", anchor="w", command=command)
            btn.pack(fill="x", padx=10, pady=5)
            self.nav_buttons.append(btn)

    def setup_main_area(self):
        self.main_frame = tk.Frame(self.root, bg="#0d1117")
        self.main_frame.pack(fill="both", expand=True)

        self.label = tk.Label(self.main_frame, text="Masukan data yang akan di enkripsi", font=("Helvetica", 20, "bold"), bg="#0d1117", fg="#58a6ff")
        self.label.pack(pady=20)

        self.key_entry = ttk.Entry(self.main_frame, width=50, show="*")
        self.key_entry.pack(pady=10)

        self.file_listbox = tk.Listbox(self.main_frame, width=80, height=15, bg="#161b22", fg="#c9d1d9", selectbackground="#238636")
        self.file_listbox.pack(pady=10)

    def toggle_sidebar(self):
        if self.sidebar_frame.winfo_width() > 50:
            self.sidebar_frame.config(width=50)
            for btn in self.nav_buttons:
                btn.pack_forget()
        else:
            self.sidebar_frame.config(width=200)
            for btn in self.nav_buttons:
                btn.pack(fill="x", padx=10, pady=5)

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file in os.listdir(self.encrypted_folder):
            self.file_listbox.insert(tk.END, f"[Encrypted] {file}")
        for file in os.listdir(self.decrypted_folder):
            self.file_listbox.insert(tk.END, f"[Decrypted] {file}")

    def load_keys(self):
        with open(self.keys_file, 'r') as f:
            self.keys_data = json.load(f)

    def save_keys(self):
        with open(self.keys_file, 'w') as f:
            json.dump(self.keys_data, f, indent=4)

    def generate_key(self, password):
        hashed = hashlib.sha256(password.encode()).digest()
        key = base64.urlsafe_b64encode(hashed[:32])
        return key

    def encrypt_file(self):
        password = self.key_entry.get()
        if not password:
            messagebox.showwarning("Peringatan", "Masukkan kunci terlebih dahulu!")
            return

        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                key = self.generate_key(password)
                fernet = Fernet(key)

                with open(file_path, "rb") as f:
                    file_data = f.read()

                encrypted_data = fernet.encrypt(file_data)
                file_name = os.path.basename(file_path)
                encrypted_file_path = os.path.join(self.encrypted_folder, file_name)

                with open(encrypted_file_path, "wb") as f:
                    f.write(encrypted_data)

                self.keys_data[file_name] = key.decode()
                self.save_keys()
                self.refresh_file_list()
                messagebox.showinfo("Sukses", f"File {file_name} berhasil dienkripsi!")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengenkripsi: {str(e)}")

    def decrypt_file(self):
        password = self.key_entry.get()
        if not password:
            messagebox.showwarning("Peringatan", "Masukkan kunci terlebih dahulu!")
            return

        selected_file = self.file_listbox.get(tk.ACTIVE)
        if not selected_file or not selected_file.startswith("[Encrypted] "):
            messagebox.showwarning("Peringatan", "Pilih file terenkripsi terlebih dahulu!")
            return

        file_name = selected_file.replace("[Encrypted] ", "")
        encrypted_file_path = os.path.join(self.encrypted_folder, file_name)
        try:
            key = self.generate_key(password)
            fernet = Fernet(key)

            with open(encrypted_file_path, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            decrypted_file_path = os.path.join(self.decrypted_folder, file_name)
            with open(decrypted_file_path, "wb") as f:
                f.write(decrypted_data)

            self.refresh_file_list()
            messagebox.showinfo("Sukses", f"File {file_name} berhasil didekripsi!")
        except InvalidToken:
            messagebox.showerror("Error", "Kunci salah! File tidak dapat didekripsi.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mendekripsi: {str(e)}")

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Pengaturan")
        settings_window.geometry("500x400")
        settings_window.configure(bg="#0d1117")

        label = tk.Label(settings_window, text="Daftar Key Tersimpan", font=("Helvetica", 14, "bold"), bg="#0d1117", fg="#58a6ff")
        label.pack(pady=10)

        tree = ttk.Treeview(settings_window, columns=("File", "Key"), show="headings")
        tree.heading("File", text="Nama File")
        tree.heading("Key", text="Key")
        tree.column("File", width=200)
        tree.column("Key", width=280)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for file, key in self.keys_data.items():
            tree.insert("", "end", values=(file, key))

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
