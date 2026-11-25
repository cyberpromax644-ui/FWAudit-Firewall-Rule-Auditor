import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from parser import parse_rules
from checks import audit_rules
from report import generate_report


class FWAuditApp:

    def __init__(self, root):
        self.root = root
        self.root.title("FWAudit | Firewall Rule Auditor")
        self.root.geometry("1150x720")
        self.root.minsize(950, 600)
        self.root.configure(bg="#101827")

        self.total_rules = 0
        self.total_audits = 0
        self.last_audit_time = "Not available"
        self.last_findings = []
        self.current_report = None
        self.audit_completed = False
        self.reports_dir = os.path.join(BASE_DIR, "reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        self.report_history = []
        self.load_report_history()

        self.setup_style()
        self.create_layout()
        self.show_dashboard()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1e293b",
            foreground="white",
            fieldbackground="#1e293b",
            rowheight=35,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#263449",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#2563eb")]
        )

    def create_layout(self):

        self.sidebar = tk.Frame(
            self.root,
            bg="#0b1220",
            width=220
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="FWAudit",
            bg="#0b1220",
            fg="#38bdf8",
            font=("Arial", 24, "bold")
        ).pack(pady=(35, 5))

        tk.Label(
            self.sidebar,
            text="FIREWALL RULE AUDITOR",
            bg="#0b1220",
            fg="#94a3b8",
            font=("Arial", 8, "bold")
        ).pack(pady=(0, 35))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("New Audit", self.show_audit),
            ("Reports", self.show_reports),
            ("About", self.show_about)
        ]

        for name, command in buttons:
            tk.Button(
                self.sidebar,
                text="   " + name,
                command=command,
                bg="#0b1220",
                fg="white",
                activebackground="#1e293b",
                activeforeground="#38bdf8",
                relief="flat",
                anchor="w",
                font=("Arial", 12),
                padx=20,
                pady=14,
                cursor="hand2"
            ).pack(fill="x", padx=10, pady=3)

        self.main = tk.Frame(
            self.root,
            bg="#101827"
        )
        self.main.pack(
            side="right",
            fill="both",
            expand=True
        )

    def clear_page(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def heading(self, title, subtitle):

        tk.Label(
            self.main,
            text=title,
            bg="#101827",
            fg="white",
            font=("Arial", 25, "bold")
        ).pack(anchor="w", padx=35, pady=(30, 5))

        tk.Label(
            self.main,
            text=subtitle,
            bg="#101827",
            fg="#94a3b8",
            font=("Arial", 11)
        ).pack(anchor="w", padx=35, pady=(0, 25))

    def create_card(self, parent, title, value):

        card = tk.Frame(
            parent,
            bg="#1e293b",
            padx=25,
            pady=25
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )

        tk.Label(
            card,
            text=title,
            bg="#1e293b",
            fg="#94a3b8",
            font=("Arial", 11)
        ).pack(anchor="w")

        label = tk.Label(
            card,
            text=str(value),
            bg="#1e293b",
            fg="#38bdf8",
            font=("Arial", 27, "bold")
        )

        label.pack(anchor="w", pady=(12, 0))

        return label

    def show_dashboard(self):

        self.clear_page()

        self.heading(
            "Dashboard",
            "Firewall security audit overview"
        )

        cards = tk.Frame(self.main, bg="#101827")
        cards.pack(fill="x", padx=20)

        self.audits_card = self.create_card(
            cards, "Total Audits", self.total_audits
        )

        self.reports_card = self.create_card(
            cards, "Reports Saved", len(self.report_history)
        )

        self.rules_card = self.create_card(
            cards, "Total Rules", self.total_rules
        )

        self.findings_card = self.create_card(
            cards, "Total Findings", len(self.last_findings)
        )

        high = sum(1 for x in self.last_findings if x["severity"] == "HIGH")
        medium = sum(1 for x in self.last_findings if x["severity"] == "MEDIUM")
        low = sum(1 for x in self.last_findings if x["severity"] == "LOW")

        self.high_card = self.create_card(
            cards, "High Severity", high
        )

        tk.Label(
            self.main,
            text=f"Risk Summary     HIGH: {high}     MEDIUM: {medium}     LOW: {low}",
            bg="#1e293b",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=18
        ).pack(fill="x", padx=35, pady=(25, 5))

        tk.Label(
            self.main,
            text=f"Last Audit: {self.last_audit_time}",
            bg="#101827",
            fg="#38bdf8",
            font=("Arial", 11)
        ).pack(anchor="w", padx=35, pady=12)

        tk.Label(
            self.main,
            text="Recent Audit Status",
            bg="#101827",
            fg="white",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=35, pady=(45, 15))

        status = "No audit performed yet"

        if self.audit_completed:
            status = (
                f"Last audit completed successfully | "
                f"{self.total_rules} rules analyzed | "
                f"{len(self.last_findings)} findings detected"
            )

        tk.Label(
            self.main,
            text=status,
            bg="#1e293b",
            fg="#38bdf8",
            font=("Arial", 11),
            padx=20,
            pady=20
        ).pack(fill="x", padx=35)

        tk.Label(
            self.main,
            text="FWAudit analyzes firewall CSV exports in read-only mode.",
            bg="#101827",
            fg="#94a3b8",
            font=("Arial", 10)
        ).pack(anchor="w", padx=35, pady=25)

    def show_audit(self):

        self.clear_page()

        self.heading(
            "New Audit",
            "Import a firewall CSV file and analyze its rules"
        )

        tk.Button(
            self.main,
            text="Select Firewall CSV",
            command=self.select_file,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            relief="flat",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12,
            cursor="hand2"
        ).pack(anchor="w", padx=35)

        self.file_label = tk.Label(
            self.main,
            text="No file selected",
            bg="#101827",
            fg="#94a3b8",
            font=("Arial", 10)
        )

        self.file_label.pack(anchor="w", padx=35, pady=15)

        tk.Label(
            self.main,
            text="Audit Findings",
            bg="#101827",
            fg="white",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=35, pady=(15, 12))

        columns = (
            "rule", "severity", "issue", "evidence"
        )

        self.results = ttk.Treeview(
            self.main,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "rule": "Rule ID",
            "severity": "Severity",
            "issue": "Security Issue",
            "evidence": "Evidence"
        }

        widths = {
            "rule": 80,
            "severity": 100,
            "issue": 210,
            "evidence": 420
        }

        for column in columns:
            self.results.heading(
                column,
                text=headings[column]
            )
            self.results.column(
                column,
                width=widths[column]
            )

        self.results.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        tk.Button(
            self.main,
            text="Save Audit Report",
            command=self.save_report,
            bg="#059669",
            fg="white",
            relief="flat",
            font=("Arial", 10, "bold"),
            padx=18,
            pady=10
        ).pack(anchor="e", padx=35, pady=15)

    def select_file(self):

        filename = filedialog.askopenfilename(
            title="Select Firewall CSV",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not filename:
            return

        try:

            rules = parse_rules(filename)
            findings = audit_rules(rules)

            self.total_rules = len(rules)
            self.last_findings = findings
            self.audit_completed = True
            self.total_audits += 1
            self.last_audit_time = datetime.now().strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )

            self.file_label.config(
                text=os.path.basename(filename)
            )

            for item in self.results.get_children():
                self.results.delete(item)

            for finding in findings:
                self.results.insert(
                    "",
                    "end",
                    values=(
                        finding["rule"],
                        finding["severity"],
                        finding["issue"],
                        finding["evidence"]
                    )
                )

            messagebox.showinfo(
                "Audit Completed",
                f"Rules analyzed: {len(rules)}\n"
                f"Findings detected: {len(findings)}"
            )

        except (OSError, ValueError, KeyError) as error:

            messagebox.showerror(
                "Audit Error",
                str(error)
            )

    def load_report_history(self):
        self.report_history = []

        for name in sorted(os.listdir(self.reports_dir), reverse=True):
            path = os.path.join(self.reports_dir, name)

            if os.path.isfile(path) and name.lower().endswith(".txt"):
                self.report_history.append(path)

    def save_report(self):

        if not self.audit_completed:
            messagebox.showwarning(
                "No Audit",
                "Please perform an audit first."
            )
            return

        output = filedialog.asksaveasfilename(
            title="Save Audit Report",
            initialdir=self.reports_dir,
            defaultextension=".txt",
            filetypes=[("Text Report", "*.txt")]
        )

        if not output:
            return

        try:

            generate_report(
                self.last_findings,
                self.total_rules,
                output
            )

            self.current_report = output
            self.load_report_history()

            messagebox.showinfo(
                "Report Saved",
                f"Report saved successfully:\n{output}"
            )

        except OSError as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )

    def show_reports(self):

        self.load_report_history()
        self.clear_page()

        self.heading(
            "Reports",
            "View previously saved audit reports"
        )

        if not self.report_history:

            tk.Label(
                self.main,
                text="No reports saved yet.",
                bg="#101827",
                fg="#94a3b8",
                font=("Arial", 12)
            ).pack(anchor="w", padx=35, pady=20)

            return

        folder_button = tk.Button(
            self.main,
            text="Open Reports Folder",
            command=self.open_reports_folder,
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        )
        folder_button.pack(anchor="e", padx=35, pady=10)

        for path in self.report_history:

            row = tk.Frame(self.main, bg="#1e293b")
            row.pack(fill="x", padx=35, pady=5)

            tk.Label(
                row,
                text=os.path.basename(path),
                bg="#1e293b",
                fg="#38bdf8",
                font=("Arial", 11),
                padx=20,
                pady=15
            ).pack(side="left", fill="x", expand=True)

            tk.Button(
                row,
                text="View Report",
                command=lambda p=path: self.view_report(p),
                bg="#0f766e",
                fg="white",
                relief="flat",
                padx=12,
                pady=7
            ).pack(side="right", padx=15, pady=8)

            tk.Button(
                row,
                text="Delete",
                command=lambda p=path: self.delete_report(p),
                bg="#991b1b",
                fg="white",
                relief="flat",
                padx=12,
                pady=7
            ).pack(side="right", padx=5, pady=8)

    def delete_report(self, path):
        confirm = messagebox.askyesno(
            "Delete Report",
            f"Are you sure you want to delete {os.path.basename(path)}?"
        )

        if not confirm:
            return

        try:
            os.remove(path)
            self.load_report_history()
            self.show_reports()
            messagebox.showinfo("Deleted", "Report deleted successfully.")

        except OSError as error:
            messagebox.showerror("Delete Error", str(error))

    def view_report(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            window = tk.Toplevel(self.root)
            window.title("FWAudit | Report Viewer")
            window.geometry("800x600")
            window.configure(bg="#101827")

            text_box = tk.Text(
                window,
                bg="#1e293b",
                fg="white",
                font=("Courier New", 10),
                wrap="word"
            )
            text_box.pack(fill="both", expand=True, padx=15, pady=15)
            text_box.insert("1.0", content)
            text_box.config(state="disabled")

        except OSError as error:
            messagebox.showerror("Report Error", str(error))

    def open_reports_folder(self):
        try:
            subprocess.Popen(["xdg-open", self.reports_dir])
        except OSError as error:
            messagebox.showerror("Folder Error", str(error))

    def show_about(self):

        self.clear_page()

        self.heading(
            "About FWAudit",
            "Firewall Rule Auditor"
        )

        description = (
            "FWAudit is a defensive firewall rule auditing tool.\n\n"
            "It analyzes firewall CSV exports in read-only mode.\n\n"
            "Security Checks:\n\n"
            "1. Any-to-Any Allow Rules\n"
            "2. Management Port Exposure\n"
            "3. Potential Shadowed Rules\n"
            "4. Deny Rules with Logging Disabled\n\n"
            "Technology: Python and Tkinter\n"
            "Interface: Graphical User Interface (GUI)\n"
            "Purpose: Network Defense and Security Auditing"
        )

        tk.Label(
            self.main,
            text=description,
            bg="#1e293b",
            fg="white",
            justify="left",
            font=("Arial", 12),
            padx=30,
            pady=30
        ).pack(anchor="w", padx=35)


if __name__ == "__main__":

    root = tk.Tk()
    app = FWAuditApp(root)
    root.mainloop()
