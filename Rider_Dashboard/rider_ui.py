from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from datetime import datetime
import os, sys
sys.path.append(os.path.dirname(os. path.dirname(os.path.abspath(__file__))))
from theme_manager import get_theme_colors, save_theme_preference, get_theme_preference
from Rider_Dashboard. rider_service import RiderService


# ============================================
# CSS-LIKE STYLE CONFIGURATION
# ============================================
class StyleConfig:
    """CSS-like styling configuration for Tkinter widgets"""
    
    @staticmethod
    def get_button_style(theme="light", variant="primary"):
        """Returns button styling based on theme and variant"""
        styles = {
            "light": {
                "primary": {
                    "bg":   "#2563eb",
                    "fg": "white",
                    "active_bg": "#1d4ed8",
                    "hover_bg": "#1e40af",
                    "font": ("Arial", 12, "bold"),
                    "relief":   FLAT,
                    "cursor": "hand2",
                    "border":  0
                },
                "success": {
                    "bg":   "#16a34a",
                    "fg": "white",
                    "active_bg": "#15803d",
                    "hover_bg": "#166534",
                    "font":   ("Arial", 12, "bold"),
                    "relief":   FLAT,
                    "cursor":   "hand2",
                    "border": 0
                },
                "danger": {
                    "bg":   "#ef4444",
                    "fg": "white",
                    "active_bg": "#dc2626",
                    "hover_bg": "#b91c1c",
                    "font":  ("Arial", 12, "bold"),
                    "relief":  FLAT,
                    "cursor": "hand2",
                    "border": 0
                }
            },
            "dark":   {
                "primary": {
                    "bg":  "#3b82f6",
                    "fg": "white",
                    "active_bg": "#2563eb",
                    "hover_bg": "#1d4ed8",
                    "font":   ("Arial", 12, "bold"),
                    "relief":   FLAT,
                    "cursor":   "hand2",
                    "border": 0
                },
                "success": {
                    "bg": "#22c55e",
                    "fg": "white",
                    "active_bg": "#16a34a",
                    "hover_bg": "#15803d",
                    "font": ("Arial", 12, "bold"),
                    "relief":   FLAT,
                    "cursor": "hand2",
                    "border": 0
                },
                "danger": {
                    "bg": "#f87171",
                    "fg":   "white",
                    "active_bg": "#ef4444",
                    "hover_bg": "#dc2626",
                    "font": ("Arial", 12, "bold"),
                    "relief": FLAT,
                    "cursor": "hand2",
                    "border":   0
                }
            }
        }
        return styles.get(theme, styles["light"]).get(variant, styles["light"]["primary"])


# ============================================
# JAVASCRIPT-LIKE EVENT HANDLERS
# ============================================
class EventHandler:
    """JavaScript-like event handling for smooth interactions"""
    
    @staticmethod
    def on_hover(widget, enter_config, leave_config):
        """Adds hover effect to widgets"""
        def on_enter(e):
            for key, value in enter_config.items():
                try:
                    widget.config(**{key: value})
                except:  
                    pass
        
        def on_leave(e):
            for key, value in leave_config.items():
                try:
                    widget.config(**{key: value})
                except:  
                    pass
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    @staticmethod
    def on_click_animation(widget, press_config, release_config):
        """Adds click animation to buttons"""
        def on_press(e):
            for key, value in press_config.items():
                try:
                    widget.config(**{key: value})
                except: 
                    pass
        
        def on_release(e):
            for key, value in release_config.items():
                try:
                    widget.config(**{key: value})
                except: 
                    pass
        
        widget.bind("<ButtonPress-1>", on_press)
        widget.bind("<ButtonRelease-1>", on_release)


# ============================================
# ANIMATED COMPONENTS
# ============================================
class AnimatedButton(Button):
    """Button with CSS-like hover and click animations"""
    
    def __init__(self, parent, text="", command=None, variant="primary", theme="light", **kwargs):
        style = StyleConfig.get_button_style(theme, variant)
        
        config = {**style, **kwargs}
        config. pop('hover_bg', None)
        config.pop('active_bg', None)
        
        super().__init__(parent, text=text, command=command, **config)
        
        self.default_bg = style. get('bg')
        self.hover_bg = style.get('hover_bg')
        self.active_bg = style.get('active_bg')
        
        EventHandler.on_hover(
            self,
            enter_config={"bg": self.hover_bg},
            leave_config={"bg": self.default_bg}
        )
        
        EventHandler.on_click_animation(
            self,
            press_config={"bg": self.active_bg, "relief": SUNKEN},
            release_config={"bg": self.hover_bg, "relief": FLAT}
        )


class AnimatedCard(Frame):
    """Card component with shadow and hover effects"""
    
    def __init__(self, parent, bg="#ffffff", hover_lift=True, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        
        self. default_relief = kwargs.get('relief', FLAT)
        self.hover_lift = hover_lift
        
        if hover_lift:
            EventHandler.on_hover(
                self,
                enter_config={"relief": RAISED, "borderwidth": 1},
                leave_config={"relief": self.default_relief, "borderwidth": 0}
            )


# ============================================
# ENHANCED RIDER DASHBOARD
# ============================================
class RiderDashboard: 
    def __init__(self, root, username, logout_callback=None):
        self.root = root
        self.username = username
        self. logout_callback = logout_callback

        # Initialize service layer
        try:
            self.service = RiderService(username)
            self.driver_id = self.service.driver_id
            self.driver_email = self.service.driver_email
            self.driver_name = self.service.driver_name
            # Load photo path from profile
            try:
                profile = self.service.get_profile()
                self.photo_path = profile[5] if profile and len(profile) > 5 else None
            except Exception:
                self.photo_path = None
        except Exception as e:
            messagebox.showerror("Driver Error", f"Failed to resolve driver: {e}")
            self.driver_id = None
            self. driver_email = None
            self.driver_name = None
            self.photo_path = None

        # Cache for image reference
        self.profile_img_tk = None

        # Theme management
        self.current_theme = get_theme_preference()
        self.theme_colors = get_theme_colors(self.current_theme)
        self.theme_toggle_btn = None

        # Update colors
        self.update_theme_colors()

        # Window setup
        try:
            self.root.title(f"Driver Dashboard - {self.username}")
            self.root.geometry("950x765")
        except Exception:
            pass
        self.root.configure(bg=self.color_content_bg)

        # Configure styles
        self.configure_styles()

        # Sidebar
        self.sidebar_frame = Frame(self.root, bg=self.color_sidebar_bg, width=220)
        self.sidebar_frame.pack(side=LEFT, fill=Y)
        self._create_sidebar()

        # Main content
        self.main_frame = Frame(self.root, bg=self.color_content_bg)
        self.main_frame. pack(side=RIGHT, fill=BOTH, expand=True)

        # Menu bar
        self.setup_menubar()

        # Start on dashboard
        self.show_dashboard()

    def update_theme_colors(self):
        """Update all theme colors from theme_colors dict"""
        self.color_sidebar_bg = self.theme_colors. get("sidebar_bg", "#050816")
        self.color_sidebar_btn = self.theme_colors.get("sidebar_btn", "#111827")
        self.color_sidebar_btn_active = self.theme_colors.get("sidebar_btn_active", "#1f2937")
        self.color_content_bg = self.theme_colors.get("content_bg", "#f9fafb")
        self.color_accent = self.theme_colors.get("accent", "#2563eb")
        self.color_text_primary = self.theme_colors.get("text_primary", "#111827")
        self.color_text_secondary = self.theme_colors.get("text_secondary", "#6b7280")
        self.color_card_bg = self.theme_colors.get("card_bg", "#ffffff")

    def configure_styles(self):
        """Configure TTK styles with CSS-like approach"""
        try:
            style = ttk.Style(self.root)
            style.configure(
                "Rider. Treeview",
                background=self.theme_colors.get("treeview_bg", "#ffffff"),
                foreground=self.theme_colors.get("treeview_fg", "#111827"),
                fieldbackground=self.theme_colors.get("treeview_bg", "#ffffff"),
                rowheight=20,
                padding=(2, 1),
                font=("Arial", 9),
                borderwidth=0,
                relief="flat"
            )
            style.configure(
                "Rider. Treeview.Heading",
                background=self.color_sidebar_btn,
                foreground="#ffffff",
                padding=(4, 2),
                font=("Arial", 10, "bold"),
                borderwidth=0,
                relief="flat"
            )
            style.map(
                "Rider. Treeview",
                background=[("selected", self.theme_colors.get("treeview_selected_bg", "#2563eb"))],
                foreground=[("selected", self.theme_colors.get("treeview_selected_fg", "#ffffff"))]
            )
            style.layout("Rider.Treeview", [('Rider.Treeview.treearea', {'sticky': 'nswe'})])
        except Exception: 
            pass

    def setup_menubar(self):
        """Setup menu bar with organized structure"""
        self.mainmenu = Menu(self.root)

        # File Menu
        filemenu = Menu(self.mainmenu, tearoff=0)
        filemenu.add_command(label='New', command=self._do_nothing)
        filemenu.add_command(label='Open', command=self._do_nothing)
        filemenu.add_command(label='Save', command=self._do_nothing)
        filemenu.add_command(label='Close', command=self._do_nothing)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self._on_logout)
        self.mainmenu.add_cascade(label='File', menu=filemenu)

        # Edit Menu
        editmenu = Menu(self.mainmenu, tearoff=0)
        editmenu.add_command(label='Undo', command=self._do_nothing)
        editmenu.add_command(label='Redo', command=self._do_nothing)
        editmenu.add_separator()
        editmenu.add_command(label='Cut', command=self._do_nothing)
        editmenu.add_command(label='Copy', command=self._do_nothing)
        editmenu.add_command(label='Paste', command=self._do_nothing)
        self.mainmenu.add_cascade(label='Edit', menu=editmenu)

        # View Menu
        viewmenu = Menu(self.mainmenu, tearoff=0)
        viewmenu.add_command(label='Dashboard', command=self.show_dashboard)
        viewmenu.add_command(label='My Trips', command=self.show_trips)
        viewmenu.add_command(label='Profile', command=self.show_profile)
        self.mainmenu. add_cascade(label='View', menu=viewmenu)

        # Tools Menu
        toolsmenu = Menu(self.mainmenu, tearoff=0)
        toolsmenu.add_command(label='Settings', command=self.show_settings)
        toolsmenu.add_command(label='Support', command=self.show_support)
        toolsmenu.add_command(label='Toggle Theme', command=self.toggle_theme)
        self.mainmenu.add_cascade(label='Tools', menu=toolsmenu)

        # Help Menu
        helpmenu = Menu(self.mainmenu, tearoff=0)
        helpmenu.add_command(label='User Guide', command=self._do_nothing)
        helpmenu.add_command(label='About', command=self._do_nothing)
        helpmenu.add_command(label='Contact Support', command=self._show_support_popup)
        self.mainmenu.add_cascade(label='Help', menu=helpmenu)

        self.root.config(menu=self.mainmenu)

    # ------------- THEME TOGGLE -------------
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        save_theme_preference(self.current_theme)
        self.theme_colors = get_theme_colors(self.current_theme)
        
        self.update_theme_colors()
        self.root.config(bg=self.color_content_bg)
        self.configure_styles()
        
        # Rebuild UI
        self.sidebar_frame.destroy()
        self.main_frame.destroy()
        
        self.sidebar_frame = Frame(self.root, bg=self.color_sidebar_bg, width=220)
        self.sidebar_frame.pack(side=LEFT, fill=Y)
        self._create_sidebar()

        self.main_frame = Frame(self.root, bg=self. color_content_bg)
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        self.show_dashboard()

    # ------------- IMAGE UTIL -------------
    def _load_circular_image(self, path, size=(100, 100)):
        """Load image from path, crop to circle, return PhotoImage."""
        try:
            img = Image.open(path).convert("RGBA")
            img = img.resize(size, Image. LANCZOS)

            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size[0], size[1]), fill=255)
            
            # Add soft shadow
            shadow = Image.new("RGBA", size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_draw.ellipse((2, 2, size[0] - 2, size[1] - 2), fill=(0, 0, 0, 50))
            shadow = shadow.filter(ImageFilter.GaussianBlur(3))
            
            img.putalpha(mask)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"[DEBUG] _load_circular_image error: {e}")
            return None

    # ---------------- ENHANCED SIDEBAR ----------------
    def _create_sidebar(self):
        # Theme toggle button
        toggle_bg = "#f0f0f0" if self.current_theme == "light" else "#2d3748"
        toggle_fg = "#333333" if self.current_theme == "light" else "#e2e8f0"
        toggle_text = "Dark" if self.current_theme == "light" else "Light"
        
        self.theme_toggle_btn = Button(
            self.sidebar_frame,
            text=toggle_text,
            font=("Arial", 10, "bold"),
            bg=toggle_bg,
            fg=toggle_fg,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            command=self.toggle_theme,
            width=8,
            height=1
        )
        self.theme_toggle_btn.pack(pady=(10, 0))
        
        hover_bg = "#e5e5e5" if self.current_theme == "light" else "#374151"
        EventHandler.on_hover(
            self.theme_toggle_btn,
            enter_config={"bg": hover_bg},
            leave_config={"bg": toggle_bg}
        )
        
        Label(
            self.sidebar_frame,
            text="Driver Menu",
            fg="white",
            bg=self. color_sidebar_bg,
            font=("Arial", 16, "bold"),
            pady=20
        ).pack()

        options = [
            ("Dashboard", self.show_dashboard),
            ("My Trips", self.show_trips),
            ("Profile", self.show_profile),
            ("Settings", self.show_settings),
            ("Support", self. show_support),
        ]
        
        for text, command in options:
            self.create_sidebar_button(text, command)

        # Logout button
        logout_btn = AnimatedButton(
            self.sidebar_frame,
            text="Logout",
            command=self._on_logout,
            variant="danger",
            theme=self.current_theme,
            width=20,
            height=2
        )
        logout_btn.pack(side=BOTTOM, pady=20)

    def create_sidebar_button(self, text, command):
        """Create an animated sidebar button"""
        btn = Button(
            self.sidebar_frame,
            text=text,
            command=command,
            font=("Arial", 12),
            fg="white",
            bg=self.color_sidebar_btn,
            bd=0,
            relief="flat",
            activebackground=self.color_sidebar_btn_active,
            cursor="hand2",
            width=20,
            height=2,
            anchor="center"
        )
        btn.pack(pady=5)
        
        EventHandler.on_hover(
            btn,
            enter_config={"bg": self. color_sidebar_btn_active},
            leave_config={"bg": self.color_sidebar_btn}
        )
        
        return btn

    def clear_main(self):
        for widget in self.main_frame. winfo_children():
            widget.destroy()

    # ------------- Treeview helpers -------------
    def _make_treeview_sortable(self, tree, cols, numeric_cols=None):
        """Enable click-to-sort on ttk.Treeview headers"""
        if numeric_cols is None:
            numeric_cols = set()
        else:
            numeric_cols = set(numeric_cols)

        def _cast(val, col):
            if col in numeric_cols:
                try:
                    return int(val)
                except Exception:
                    return 0
            return val. lower() if isinstance(val, str) else val

        def _sort(col, reverse=False):
            data = [(tree.set(k, col), k) for k in tree.get_children("")]
            data.sort(key=lambda t: _cast(t[0], col), reverse=reverse)
            for idx, (_, k) in enumerate(data):
                tree.move(k, "", idx)
            tree.heading(col, command=lambda: _sort(col, not reverse))

        for c in cols:
            tree.heading(c, command=lambda col=c: _sort(col, False))

    # ------------------ ENHANCED DASHBOARD WITH ANIMATED CARDS ------------------
    def show_dashboard(self):
        self.clear_main()
        
        # Get driver display name
        display = self.driver_name or self.driver_email or self. username
        
        # Hero Section
        hero_frame = Frame(self.main_frame, bg=self.color_content_bg)
        hero_frame.pack(pady=(20, 8))
        
        Label(
            hero_frame,
            text=f"Welcome, {display}! ",
            font=("Arial", 26, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack()
        
        Label(
            hero_frame,
            text="Your ride statistics at a glance",
            font=("Arial", 12),
            bg=self.color_content_bg,
            fg=self.color_text_secondary
        ).pack(pady=(5, 0))

        # Stats Cards Container
        stats_container = Frame(self.main_frame, bg=self.color_content_bg)
        stats_container.pack(pady=20, padx=20, fill=X)

        try:
            stats = self.service.get_stats()
            total_assigned = stats.get("assigned", 0)
            total_active = stats.get("active", 0)
            total_completed = stats.get("completed", 0)
        except Exception:
            total_assigned = total_active = total_completed = 0

        self. create_stat_card(stats_container, total_assigned, "Assigned", "#2563eb")
        self.create_stat_card(stats_container, total_active, "Active / Accepted", "#f59e0b")
        self.create_stat_card(stats_container, total_completed, "Completed", "#16a34a")

        # Quick Actions
        actions_frame = Frame(self.main_frame, bg=self.color_content_bg)
        actions_frame.pack(pady=20)
        
        AnimatedButton(
            actions_frame,
            text="View All Trips",
            command=self.show_trips,
            variant="primary",
            theme=self.current_theme,
            width=18,
            height=2
        ).pack(side=LEFT, padx=5)
        
        AnimatedButton(
            actions_frame,
            text="Update Profile",
            command=self. show_profile,
            variant="success",
            theme=self.current_theme,
            width=18,
            height=2
        ).pack(side=LEFT, padx=5)

        # Hint text
        Label(
            self.main_frame,
            text="Use the menu to view trips or manage your profile",
            font=("Arial", 11),
            bg=self.color_content_bg,
            fg=self.color_text_secondary
        ).pack(pady=(10, 0))

    def create_stat_card(self, parent, value, label, color):
        """Create an animated stat card"""
        outer = AnimatedCard(parent, bg=self.color_card_bg, relief="flat", bd=1, hover_lift=True)
        outer.pack(side=LEFT, padx=10, fill=BOTH, expand=True)
        
        inner = Frame(outer, bg=self.color_card_bg)
        inner.pack(padx=20, pady=20, fill=BOTH)
        
        Label(inner, text=str(value), font=("Arial", 32, "bold"), bg=self.color_card_bg, fg=color).pack()
        Label(inner, text=label, font=("Arial", 11), bg=self.color_card_bg, fg=self.color_text_secondary).pack()

    # ------------------ MY TRIPS (CONTINUED IN NEXT MESSAGE DUE TO LENGTH) ------------------
    def show_trips(self):
        self.clear_main()
        
        Label(
            self.main_frame,
            text="My Assigned Trips",
            font=("Arial", 20, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=10)

        # Search / filter card
        search_card = AnimatedCard(self.main_frame, bg=self.color_card_bg, relief="flat", bd=1)
        search_card.pack(fill=X, padx=10, pady=(0, 5))
        
        search_frame = Frame(search_card, bg=self.color_card_bg)
        search_frame.pack(fill=X, padx=10, pady=8)

        entry_bg = self.theme_colors.get("entry_bg", "#ffffff")
        entry_fg = self.theme_colors.get("entry_fg", "#111827")

        Label(search_frame, text="Search:", bg=self.color_card_bg, fg=self.color_text_primary, font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 4))
        search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=search_var, width=22, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, font=("Arial", 9))
        search_entry.pack(side=LEFT, padx=(0, 10))

        Label(search_frame, text="Status:", bg=self.color_card_bg, fg=self.color_text_primary, font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 4))
        status_var = StringVar(value="All")
        status_cb = ttk.Combobox(
            search_frame,
            textvariable=status_var,
            values=["All", "Pending", "Accepted", "Completed", "Cancelled"],
            width=12,
            state="readonly",
            font=("Arial", 9)
        )
        status_cb.pack(side=LEFT)

        frame = Frame(self.main_frame, bg=self.color_content_bg)
        frame.pack(fill=BOTH, expand=True, pady=10, padx=10)

        cols = ("ID", "Customer", "Pickup", "Dropoff", "Date", "Time", "Status")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=20, style="Rider.Treeview")

        # Striped rows
        even_bg = self.theme_colors.get("treeview_even", "#ffffff")
        odd_bg = self.theme_colors.get("treeview_odd", "#f3f4f6")
        text_color = self.theme_colors.get("treeview_fg", "#111827")
        
        tree.tag_configure("evenrow", background=even_bg, foreground=text_color)
        tree.tag_configure("oddrow", background=odd_bg, foreground=text_color)

        for c in cols:
            tree.heading(c, text=c)
            if c == "ID":
                tree.column(c, width=50, anchor=CENTER, stretch=False)
            elif c in ("Date", "Time"):
                tree. column(c, width=80, anchor=CENTER, stretch=False)
            elif c == "Status":
                tree.column(c, width=85, anchor=CENTER, stretch=False)
            elif c == "Customer":
                tree.column(c, width=150, stretch=True)
            else:  # Pickup, Dropoff
                tree.column(c, width=150, stretch=True)

        tree.pack(fill=BOTH, expand=True, side=LEFT)

        scroll = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        tree.configure(yscrollcommand=scroll.set)

        self._make_treeview_sortable(tree, cols, numeric_cols={"ID"})

        # Button frame
        btn_frame = Frame(self.main_frame, bg=self.color_content_bg)
        btn_frame.pack(pady=8)
        
        AnimatedButton(
            btn_frame,
            text="Accept Ride",
            command=lambda: self.accept_ride(tree),
            variant="primary",
            theme=self.current_theme,
            width=12
        ).pack(side=LEFT, padx=6)
        
        AnimatedButton(
            btn_frame,
            text="Complete Ride",
            command=lambda: self.complete_ride(tree),
            variant="success",
            theme=self.current_theme,
            width=15
        ).pack(side=LEFT, padx=6)

        # Load data
        self._trips_cache = []
        try:
            trips = self.service.get_trips()
            self._trips_cache = [
                {
                    "ID": r["id"],
                    "Customer": r. get("customer_email", ""),
                    "Pickup": r.get("pickup", ""),
                    "Dropoff": r.get("dropoff", ""),
                    "Date": r.get("date", ""),
                    "Time": r.get("time", ""),
                    "Status": r.get("status", ""),
                }
                for r in trips
            ]
        except Exception as e:
            messagebox.showerror("Error", str(e))

        def _refresh_tree(filtered=None):
            for item in tree.get_children():
                tree.delete(item)
            data = filtered if filtered is not None else self._trips_cache
            for idx, r in enumerate(data):
                vals = [
                    r. get("ID"),
                    r.get("Customer"),
                    r.get("Pickup"),
                    r. get("Dropoff"),
                    r.get("Date"),
                    r.get("Time"),
                    r.get("Status"),
                ]
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree. insert("", END, values=vals, tags=(tag,))

        def _apply_filters(*_):
            text = (search_var.get() or "").strip().lower()
            status_filter = (status_var.get() or "All").strip().lower()

            filtered = []
            for r in self._trips_cache:
                rid = r. get("ID")
                customer = str(r.get("Customer", ""))
                pickup = str(r.get("Pickup", ""))
                dropoff = str(r.get("Dropoff", ""))
                date_str = str(r.get("Date", ""))
                time_str = str(r.get("Time", ""))
                status = str(r.get("Status", ""))

                if text: 
                    combined = " ".join([str(rid), customer, pickup, dropoff, date_str, time_str, status]).lower()
                    if text not in combined:
                        continue

                if status_filter and status_filter != "all":
                    if status. lower() != status_filter:
                        continue

                filtered.append(r)

            _refresh_tree(filtered)

        search_entry.bind("<KeyRelease>", _apply_filters)
        status_cb.bind("<<ComboboxSelected>>", _apply_filters)
        _refresh_tree()

    def accept_ride(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox. showwarning("Select", "Select a ride to accept.")
            return
        
        booking_id = tree.item(sel[0])["values"][0]
        
        try:
            self.service.accept_ride(booking_id)
            messagebox.showinfo("Success", "Ride accepted!")
            self. show_trips()
        except ValueError as e:
            messagebox. showinfo("Info", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def complete_ride(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a ride to complete.")
            return
        
        booking_id = tree.item(sel[0])["values"][0]
        
        if not messagebox.askyesno("Confirm", f"Mark ride {booking_id} as completed?"):
            return
        
        try:
            self.service.complete_ride(booking_id)
            messagebox.showinfo("Success", "Ride marked as completed!")
            self.show_trips()
        except Exception as e:
            messagebox. showerror("Error", str(e))

    # ------------------ PROFILE (same as before but with clear_main fix) ------------------
    def show_profile(self):
        self.clear_main()

        Label(
            self.main_frame,
            text="My Profile",
            font=("Arial", 18, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=20)

        if not self.driver_id:
            messagebox.showerror("Error", "Driver ID not resolved.  Cannot load profile.")
            return

        try:
            row = self.service.get_profile()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load driver profile: {e}")
            return

        if not row:
            messagebox. showerror("Error", "Driver not found!")
            return

        if len(row) >= 6:
            name, email, phone, address, status, db_photo_path = row[: 6]
            self.photo_path = db_photo_path
        else:
            name, email, phone = row[:3]
            address = row[3] if len(row) > 3 else ""
            status = row[4] if len(row) > 4 else ""

        # Photo + Upload
        photo_frame = Frame(self.main_frame, bg=self.color_content_bg)
        photo_frame.pack(pady=10)

        canvas_size = 120
        avatar_canvas = Canvas(
            photo_frame,
            width=canvas_size,
            height=canvas_size,
            bg=self.color_content_bg,
            highlightthickness=0
        )
        avatar_canvas.pack()

        radius = 50
        center_x = center_y = canvas_size // 2
        avatar_canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="#d1d5db",
            outline="#9ca3af",
            width=2,
            tags="avatar_bg"
        )

        def refresh_avatar():
            avatar_canvas.delete("avatar_img")
            avatar_canvas.delete("avatar_initial")
            if self.photo_path and os.path.isfile(self.photo_path):
                img_tk = self._load_circular_image(self.photo_path, size=(100, 100))
                if img_tk:
                    self.profile_img_tk = img_tk
                    avatar_canvas.create_image(
                        center_x,
                        center_y,
                        image=self.profile_img_tk,
                        tags="avatar_img"
                    )
                    return
            avatar_canvas.create_text(
                center_x,
                center_y,
                text=(name[: 1]. upper() if name else "?"),
                font=("Arial", 32, "bold"),
                fill="#4b5563",
                tags="avatar_initial"
            )

        refresh_avatar()

        def upload_photo():
            filetypes = [
                ("Image files", "*.png *.jpg *.jpeg *. gif *.bmp"),
                ("All files", "*.*"),
            ]
            filepath = filedialog.askopenfilename(
                title="Select Profile Photo",
                filetypes=filetypes
            )
            if not filepath:
                return

            try:
                photos_dir = "profile_photos"
                os.makedirs(photos_dir, exist_ok=True)
                ext = os.path.splitext(filepath)[1]
                filename = f"driver_{self.driver_id}{ext}"
                dest_path = os.path.join(photos_dir, filename)

                with open(filepath, "rb") as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())

                self.photo_path = dest_path
                self.service.update_photo_path(dest_path)
                messagebox.showinfo("Success", "Profile photo updated.")
            except Exception as e: 
                messagebox.showerror("Error", f"Failed to update photo: {e}")
                return

            refresh_avatar()

        AnimatedButton(
            photo_frame,
            text="Upload Photo",
            command=upload_photo,
            variant="primary",
            theme=self.current_theme,
            width=15,
            height=1
        ).pack(pady=5)

        # Form card
        form_card = AnimatedCard(self.main_frame, bg=self.color_card_bg, relief="flat", bd=1)
        form_card.pack(pady=10, padx=20, fill=BOTH)

        frame = Frame(form_card, bg=self.color_card_bg)
        frame.pack(pady=20, padx=20)

        labels = ["Name", "Email", "Phone", "Address", "Status"]
        values = [name, email, phone, address, status]
        entries = {}

        entry_bg = self.theme_colors.get("entry_bg", "#ffffff")
        entry_fg = self. theme_colors.get("entry_fg", "#111827")

        for i, lab in enumerate(labels):
            Label(
                frame,
                text=lab,
                bg=self.color_card_bg,
                fg=self.color_text_primary,
                font=("Arial", 11, "bold")
            ).grid(row=i, column=0, padx=10, pady=7, sticky="w")

            ent = Entry(frame, width=30, font=("Arial", 11), bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
            ent.insert(0, values[i] if values[i] is not None else "")
            if lab in ["Email", "Status"]:
                ent.config(state="disabled", disabledbackground=self.color_content_bg)
            ent.grid(row=i, column=1, padx=10, pady=7)
            entries[lab] = ent

        def update():
            new_name = entries["Name"].get()
            new_phone = entries["Phone"].get()
            new_address = entries["Address"].get()

            try:
                self.service.update_profile(new_name, new_phone, new_address)
                self.driver_name = new_name
                messagebox.showinfo("Success", "Profile updated successfully!")
            except ValueError as e:
                messagebox. showwarning("Warning", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {e}")

        AnimatedButton(
            self.main_frame,
            text="Save Changes",
            command=update,
            variant="success",
            theme=self.current_theme,
            width=20,
            height=2
        ).pack(pady=20)

    # ------------------ SETTINGS & SUPPORT ------------------
    def show_settings(self):
        self.clear_main()
        
        Label(
            self.main_frame,
            text="Settings",
            font=("Arial", 18, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=20)

        settings_card = AnimatedCard(self.main_frame, bg=self.color_card_bg, relief="flat", bd=1)
        settings_card.pack(pady=10, padx=20, fill=BOTH)

        frame = Frame(settings_card, bg=self.color_card_bg)
        frame.pack(pady=20, padx=20)

        Label(
            frame,
            text="Notification Preferences",
            bg=self.color_card_bg,
            fg=self.color_text_primary,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.email_notif_var = BooleanVar(value=True)
        self.sms_notif_var = BooleanVar(value=True)

        Checkbutton(
            frame,
            text="Email notifications",
            variable=self.email_notif_var,
            bg=self.color_card_bg,
            fg=self. color_text_primary,
            selectcolor=self.color_card_bg,
            font=("Arial", 11)
        ).grid(row=1, column=0, sticky="w", padx=20, pady=5)
        
        Checkbutton(
            frame,
            text="SMS notifications",
            variable=self.sms_notif_var,
            bg=self.color_card_bg,
            fg=self.color_text_primary,
            selectcolor=self. color_card_bg,
            font=("Arial", 11)
        ).grid(row=2, column=0, sticky="w", padx=20, pady=5)

        Label(
            frame,
            text="(Placeholder settings — wire to DB if needed. )",
            bg=self.color_card_bg,
            fg=self.color_text_secondary,
            font=("Arial", 9, "italic")
        ).grid(row=3, column=0, sticky="w", padx=10, pady=10)

    def show_support(self):
        self.clear_main()

        Label(
            self.main_frame,
            text="Support",
            font=("Arial", 18, "bold"),
            bg=self.color_content_bg,
            fg=self. color_accent
        ).pack(pady=20)

        support_card = AnimatedCard(self. main_frame, bg=self. color_card_bg, relief="flat", bd=1)
        support_card.pack(pady=10, padx=20, fill=BOTH)

        Label(
            support_card,
            text="If you face any issue with your trips or profile,\nyou can contact our support team.",
            font=("Arial", 12),
            bg=self.color_card_bg,
            fg=self.color_text_primary,
            justify="center"
        ).pack(pady=20)

        def contact_support():
            messagebox.showinfo(
                "Contact Support",
                "Email: support@example.com\n"
                "Phone: +977-9810000000\n"
                "Hours: 24/7"
            )

        AnimatedButton(
            support_card,
            text="Contact Support",
            command=contact_support,
            variant="primary",
            theme=self.current_theme,
            width=20,
            height=2
        ).pack(pady=20)

    # ------------------ LOGOUT ------------------
    def _on_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            try:
                if self.logout_callback:
                    self.logout_callback()
                else:
                    self.root.destroy()
            except Exception: 
                try:
                    self.root. destroy()
                except Exception:
                    pass

    def _do_nothing(self):
        messagebox.showinfo("Coming Soon", "Feature not implemented yet")

    def _show_support_popup(self):
        messagebox.showinfo(
            "Contact Support",
            "Email: support@example.com\n"
            "Phone: +977-9810000000"
        )

    def destroy(self):
        """Remove dashboard UI when logging out / switching user."""
        try:
            self.sidebar_frame.destroy()
        except Exception:
            pass
        try: 
            self.main_frame. destroy()
        except Exception: 
            pass


if __name__ == "__main__": 
    root = Tk()
    RiderDashboard(root, username="rupak@gmail.com")
    root.mainloop()