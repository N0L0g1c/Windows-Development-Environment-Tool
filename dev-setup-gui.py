#!/usr/bin/env python3
"""
Windows Dev Environment Setup GUI
Beautiful GUI for setting up your Windows development environment
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import subprocess
import threading
import sys
from pathlib import Path
import webbrowser
from datetime import datetime

class DevSetupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Dev Environment Setup")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        # State variables
        self.is_installing = False
        self.installation_log = []
        self.config = {}
        self.package_managers = {}
        self.available_stacks = {}
        
        # Load configuration
        self.load_config()
        
        # Configure styles
        self.configure_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Auto-detect package managers
        self.auto_detect_package_managers()
        
        # Load available stacks
        self.load_available_stacks()
    
    def configure_styles(self):
        """Configure the modern dark theme"""
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3c3c3c',
            'accent': '#0078d4',
            'accent_hover': '#106ebe',
            'success': '#00d084',
            'warning': '#ff8c00',
            'error': '#d13438',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'text_muted': '#999999',
            'border': '#404040'
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title style
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_primary'])
        
        # Header style
        style.configure('Header.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.colors['accent'],
                       background=self.colors['bg_primary'])
        
        # Custom button styles
        style.configure('Custom.TButton',
                       font=('Segoe UI', 10),
                       padding=(10, 5))
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground='white',
                       background=self.colors['success'])
        
        style.configure('Warning.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground='white',
                       background=self.colors['warning'])
        
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground='white',
                       background=self.colors['accent'])
        
        # Status label style
        style.configure('Status.TLabel',
                       font=('Segoe UI', 10),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_primary'])
        
        # Custom frame style
        style.configure('Custom.TFrame',
                       background=self.colors['bg_primary'])
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Configure root window
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title section
        self.create_title_section(main_frame)
        
        # Content notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create tabs
        self.create_setup_tab()
        self.create_stacks_tab()
        self.create_tools_tab()
        self.create_settings_tab()
        self.create_log_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_title_section(self, parent):
        """Create the title section with logo and status"""
        title_frame = ttk.Frame(parent, style='Custom.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(title_frame, 
                               text="🚀 Windows Dev Environment Setup",
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        self.status_label = ttk.Label(title_frame,
                                     text="⚪ Ready",
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.RIGHT)
        
        # Progress bar
        self.progress = ttk.Progressbar(title_frame, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, padx=(0, 10))
        self.progress.pack_forget()  # Hide initially
    
    def create_setup_tab(self):
        """Create the main setup tab"""
        setup_frame = ttk.Frame(self.notebook)
        self.notebook.add(setup_frame, text="🏗️ Quick Setup")
        
        # Package manager selection
        pm_frame = ttk.LabelFrame(setup_frame, text="Package Manager", padding=10)
        pm_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.pm_var = tk.StringVar(value="auto")
        ttk.Radiobutton(pm_frame, text="Auto-detect (Recommended)", 
                       variable=self.pm_var, value="auto").pack(anchor=tk.W)
        ttk.Radiobutton(pm_frame, text="Chocolatey", 
                       variable=self.pm_var, value="choco").pack(anchor=tk.W)
        ttk.Radiobutton(pm_frame, text="Scoop", 
                       variable=self.pm_var, value="scoop").pack(anchor=tk.W)
        ttk.Radiobutton(pm_frame, text="Winget", 
                       variable=self.pm_var, value="winget").pack(anchor=tk.W)
        
        # Quick setup buttons
        quick_frame = ttk.LabelFrame(setup_frame, text="Quick Setup", padding=10)
        quick_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Web Development
        web_btn = ttk.Button(quick_frame, text="🌐 Web Development Stack",
                           command=lambda: self.setup_stack("web-dev"),
                           style='Primary.TButton')
        web_btn.pack(fill=tk.X, pady=2)
        
        # Data Science
        data_btn = ttk.Button(quick_frame, text="📊 Data Science Stack",
                             command=lambda: self.setup_stack("data-science"),
                             style='Primary.TButton')
        data_btn.pack(fill=tk.X, pady=2)
        
        # .NET Development
        dotnet_btn = ttk.Button(quick_frame, text="🔷 .NET Development Stack",
                              command=lambda: self.setup_stack("dotnet"),
                              style='Primary.TButton')
        dotnet_btn.pack(fill=tk.X, pady=2)
        
        # Mobile Development
        mobile_btn = ttk.Button(quick_frame, text="📱 Mobile Development Stack",
                              command=lambda: self.setup_stack("mobile-dev"),
                              style='Primary.TButton')
        mobile_btn.pack(fill=tk.X, pady=2)
        
        # DevOps
        devops_btn = ttk.Button(quick_frame, text="⚙️ DevOps Stack",
                              command=lambda: self.setup_stack("devops"),
                              style='Primary.TButton')
        devops_btn.pack(fill=tk.X, pady=2)
        
        # Custom setup
        custom_btn = ttk.Button(quick_frame, text="🛠️ Custom Setup",
                              command=self.show_custom_setup,
                              style='Warning.TButton')
        custom_btn.pack(fill=tk.X, pady=2)
        
        # Action buttons
        action_frame = ttk.Frame(setup_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.install_btn = ttk.Button(action_frame, text="🚀 Start Installation",
                                    command=self.start_installation,
                                    style='Success.TButton')
        self.install_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.dry_run_btn = ttk.Button(action_frame, text="🔍 Dry Run",
                                   command=self.dry_run,
                                   style='Warning.TButton')
        self.dry_run_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.reset_btn = ttk.Button(action_frame, text="🔄 Reset",
                                  command=self.reset_setup,
                                  style='Custom.TButton')
        self.reset_btn.pack(side=tk.LEFT)
    
    def create_stacks_tab(self):
        """Create the stacks configuration tab"""
        stacks_frame = ttk.Frame(self.notebook)
        self.notebook.add(stacks_frame, text="📦 Development Stacks")
        
        # Stack selection
        stack_frame = ttk.LabelFrame(stacks_frame, text="Available Stacks", padding=10)
        stack_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Stack listbox with scrollbar
        list_frame = ttk.Frame(stack_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.stack_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE,
                                      bg=self.colors['bg_secondary'],
                                      fg=self.colors['text_primary'],
                                      selectbackground=self.colors['accent'])
        self.stack_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.stack_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stack_listbox.config(yscrollcommand=scrollbar.set)
        
        # Stack details
        details_frame = ttk.LabelFrame(stacks_frame, text="Stack Details", padding=10)
        details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stack_details = scrolledtext.ScrolledText(details_frame, height=8,
                                                      bg=self.colors['bg_secondary'],
                                                      fg=self.colors['text_primary'])
        self.stack_details.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.stack_listbox.bind('<<ListboxSelect>>', self.on_stack_select)
    
    def create_tools_tab(self):
        """Create the individual tools tab"""
        tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(tools_frame, text="🛠️ Individual Tools")
        
        # Tools categories
        categories = {
            "Code Editors": ["vscode", "cursor", "sublime-text", "atom"],
            "Version Control": ["git", "github-desktop", "sourcetree"],
            "Languages": ["python", "nodejs", "java", "go", "rust"],
            "Databases": ["mysql", "postgresql", "mongodb", "redis"],
            "Containers": ["docker-desktop", "kubernetes-cli"],
            "Cloud Tools": ["azure-cli", "aws-cli", "terraform"],
            "Utilities": ["7zip", "winscp", "putty", "wireshark"]
        }
        
        # Create category frames
        for category, tools in categories.items():
            cat_frame = ttk.LabelFrame(tools_frame, text=category, padding=10)
            cat_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Create checkboxes for tools
            for tool in tools:
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(cat_frame, text=tool, variable=var)
                cb.pack(anchor=tk.W)
                setattr(self, f"{tool.replace('-', '_')}_var", var)
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # General settings
        general_frame = ttk.LabelFrame(settings_frame, text="General Settings", padding=10)
        general_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Auto-detect existing installations
        self.auto_detect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(general_frame, text="Auto-detect existing installations",
                       variable=self.auto_detect_var).pack(anchor=tk.W)
        
        # Skip if already installed
        self.skip_installed_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(general_frame, text="Skip if already installed",
                       variable=self.skip_installed_var).pack(anchor=tk.W)
        
        # Create desktop shortcuts
        self.desktop_shortcuts_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(general_frame, text="Create desktop shortcuts",
                       variable=self.desktop_shortcuts_var).pack(anchor=tk.W)
        
        # Environment settings
        env_frame = ttk.LabelFrame(settings_frame, text="Environment Setup", padding=10)
        env_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.setup_path_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(env_frame, text="Setup PATH environment variables",
                       variable=self.setup_path_var).pack(anchor=tk.W)
        
        self.setup_git_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(env_frame, text="Configure Git editor",
                       variable=self.setup_git_var).pack(anchor=tk.W)
        
        # Logging settings
        log_frame = ttk.LabelFrame(settings_frame, text="Logging", padding=10)
        log_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.logging_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(log_frame, text="Enable detailed logging",
                       variable=self.logging_var).pack(anchor=tk.W)
        
        # Debug mode
        self.debug_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(log_frame, text="Debug mode",
                       variable=self.debug_var).pack(anchor=tk.W)
    
    def create_log_tab(self):
        """Create the log viewer tab"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="📋 Installation Log")
        
        # Log controls
        controls_frame = ttk.Frame(log_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls_frame, text="🔄 Refresh",
                  command=self.refresh_log).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="💾 Save Log",
                  command=self.save_log).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="🗑️ Clear Log",
                  command=self.clear_log).pack(side=tk.LEFT)
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                 bg=self.colors['bg_secondary'],
                                                 fg=self.colors['text_primary'],
                                                 font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = ttk.Frame(parent, style='Custom.TFrame')
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status text
        self.status_text = ttk.Label(status_frame, text="Ready to setup your development environment",
                                   style='Status.TLabel')
        self.status_text.pack(side=tk.LEFT)
        
        # Package manager status
        self.pm_status = ttk.Label(status_frame, text="",
                                  style='Status.TLabel')
        self.pm_status.pack(side=tk.RIGHT)
    
    def load_config(self):
        """Load configuration from file"""
        config_path = Path("config.json")
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                self.log_message(f"Error loading config: {e}")
                self.config = {}
        else:
            self.config = {}
    
    def auto_detect_package_managers(self):
        """Auto-detect available package managers"""
        self.package_managers = {}
        
        # Check Chocolatey
        try:
            result = subprocess.run(['choco', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.package_managers['choco'] = result.stdout.strip()
        except:
            pass
        
        # Check Scoop
        try:
            result = subprocess.run(['scoop', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.package_managers['scoop'] = result.stdout.strip()
        except:
            pass
        
        # Check Winget
        try:
            result = subprocess.run(['winget', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.package_managers['winget'] = result.stdout.strip()
        except:
            pass
        
        # Update status
        pm_text = " | ".join([f"{pm}: {ver}" for pm, ver in self.package_managers.items()])
        self.pm_status.config(text=pm_text if pm_text else "No package managers detected")
    
    def load_available_stacks(self):
        """Load available development stacks"""
        if 'stacks' in self.config:
            self.available_stacks = self.config['stacks']
            
            # Populate stack listbox
            for stack_name, stack_config in self.available_stacks.items():
                if stack_config.get('enabled', True):
                    self.stack_listbox.insert(tk.END, stack_name)
    
    def setup_stack(self, stack_name):
        """Setup a specific development stack"""
        self.log_message(f"Setting up {stack_name} stack...")
        # Implementation for stack setup
        pass
    
    def show_custom_setup(self):
        """Show custom setup dialog"""
        messagebox.showinfo("Custom Setup", "Custom setup dialog would open here")
    
    def start_installation(self):
        """Start the installation process"""
        if self.is_installing:
            return
        
        self.is_installing = True
        self.install_btn.config(state='disabled')
        self.progress.pack(side=tk.RIGHT, padx=(0, 10))
        self.progress.start()
        
        # Run installation in separate thread
        thread = threading.Thread(target=self.run_installation)
        thread.daemon = True
        thread.start()
    
    def run_installation(self):
        """Run the actual installation process"""
        try:
            self.log_message("Starting installation...")
            self.update_status("Installing packages...")
            
            # Get selected package manager
            pm = self.pm_var.get()
            if pm == "auto":
                pm = self.detect_best_package_manager()
            
            # Run PowerShell script
            cmd = [
                'powershell', '-ExecutionPolicy', 'Bypass', '-File', 'setup.ps1',
                '-PackageManager', pm
            ]
            
            if self.debug_var.get():
                cmd.append('-Debug')
            
            if self.logging_var.get():
                cmd.append('-Verbose')
            
            # Execute command
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, text=True)
            
            for line in process.stdout:
                self.log_message(line.strip())
                self.root.update_idletasks()
            
            process.wait()
            
            if process.returncode == 0:
                self.log_message("Installation completed successfully!")
                self.update_status("Installation completed")
            else:
                self.log_message(f"Installation failed with code {process.returncode}")
                self.update_status("Installation failed")
                
        except Exception as e:
            self.log_message(f"Error during installation: {e}")
            self.update_status("Installation error")
        finally:
            self.is_installing = False
            self.install_btn.config(state='normal')
            self.progress.stop()
            self.progress.pack_forget()
    
    def detect_best_package_manager(self):
        """Detect the best available package manager"""
        if 'choco' in self.package_managers:
            return 'choco'
        elif 'winget' in self.package_managers:
            return 'winget'
        elif 'scoop' in self.package_managers:
            return 'scoop'
        else:
            return 'winget'  # Default to winget
    
    def dry_run(self):
        """Perform a dry run of the installation"""
        self.log_message("Performing dry run...")
        # Implementation for dry run
        pass
    
    def reset_setup(self):
        """Reset the setup configuration"""
        if messagebox.askyesno("Reset Setup", "Are you sure you want to reset the setup?"):
            self.log_message("Setup reset")
            # Reset implementation
    
    def on_stack_select(self, event):
        """Handle stack selection"""
        selection = self.stack_listbox.curselection()
        if selection:
            stack_name = self.stack_listbox.get(selection[0])
            if stack_name in self.available_stacks:
                stack_config = self.available_stacks[stack_name]
                self.show_stack_details(stack_name, stack_config)
    
    def show_stack_details(self, stack_name, stack_config):
        """Show details for selected stack"""
        details = f"Stack: {stack_name}\n\n"
        details += f"Packages: {', '.join(stack_config.get('packages', []))}\n\n"
        
        if 'pythonPackages' in stack_config:
            details += f"Python Packages: {', '.join(stack_config['pythonPackages'])}\n\n"
        
        if 'vscodeExtensions' in stack_config:
            details += f"VS Code Extensions: {', '.join(stack_config['vscodeExtensions'])}\n\n"
        
        self.stack_details.delete(1.0, tk.END)
        self.stack_details.insert(1.0, details)
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.installation_log.append(log_entry)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, status):
        """Update status display"""
        self.status_text.config(text=status)
        self.status_label.config(text="🟡 Working" if self.is_installing else "⚪ Ready")
    
    def refresh_log(self):
        """Refresh the log display"""
        self.log_text.delete(1.0, tk.END)
        for entry in self.installation_log:
            self.log_text.insert(tk.END, entry)
    
    def save_log(self):
        """Save log to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.writelines(self.installation_log)
            self.log_message(f"Log saved to {filename}")
    
    def clear_log(self):
        """Clear the log"""
        if messagebox.askyesno("Clear Log", "Are you sure you want to clear the log?"):
            self.installation_log.clear()
            self.log_text.delete(1.0, tk.END)
            self.log_message("Log cleared")

def main():
    """Main function"""
    root = tk.Tk()
    app = DevSetupGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
