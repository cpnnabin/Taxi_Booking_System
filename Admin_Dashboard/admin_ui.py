from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from datetime import datetime
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme_manager import get_theme_colors, save_theme_preference, get_theme_preference
from Admin_Dashboard. admin_service import AdminService


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
                    "bg":  "#2563eb",
                    "fg":  "white",
                    "active_bg": "#1d4ed8",
                    "hover_bg": "#1e40af",
                    "font": ("Arial", 12, "bold"),
                    "relief":  FLAT,
                    "cursor": "hand2",
                    "border": 0
                },
                "success": {
                    "bg":  "#16a34a",
                    "fg": "white",
                    "active_bg": "#15803d",
                    "hover_bg": "#166534",
                    "font":  ("Arial", 12, "bold"),
                    "relief":  FLAT,
                    "cursor":  "hand2",
                    "border": 0
                },
                "danger": {
                    "bg":  "#ef4444",
                    "fg": "white",
                    "active_bg": "#dc2626",
                    "hover_bg": "#b91c1c",
                    "font": ("Arial", 12, "bold"),
                    "relief": FLAT,
                    "cursor": "hand2",
                    "border":  0
                },
                "sidebar": {
                    "bg":  "#111827",
                    "fg":  "white",
                    "active_bg": "#1f2937",
                    "hover_bg": "#374151",
                    "font":  ("Arial", 12),
                    "relief": FLAT,
                    "cursor": "hand2",
                    "border": 0
                }
            },
            "dark":  {
                "primary": {
                    "bg": "#3b82f6",
                    "fg": "white",
                    "active_bg": "#2563eb",
                    "hover_bg": "#1d4ed8",
                    "font":  ("Arial", 12, "bold"),
                    "relief":  FLAT,
                    "cursor":  "hand2",
                    "border": 0
                },
                "success": {
                    "bg": "#22c55e",
                    "fg": "white",
                    "active_bg": "#16a34a",
                    "hover_bg": "#15803d",
                    "font": ("Arial", 12, "bold"),
                    "relief":  FLAT,
                    "cursor": "hand2",
                    "border": 0
                },
                "danger": {
                    "bg": "#f87171",
                    "fg":  "white",
                    "active_bg": "#ef4444",
                    "hover_bg": "#dc2626",
                    "font": ("Arial", 12, "bold"),
                    "relief": FLAT,
                    "cursor": "hand2",
                    "border":  0
                },
                "sidebar": {
                    "bg": "#1e293b",
                    "fg": "white",
                    "active_bg": "#334155",
                    "hover_bg": "#475569",
                    "font": ("Arial", 12),
                    "relief":  FLAT,
                    "cursor": "hand2",
                    "border": 0
                }
            }
        }
        return styles.get(theme, styles["light"]).get(variant, styles["light"]["primary"])

    @staticmethod
    def apply_shadow(widget, color="#000000", offset=2, opacity=0.1):
        """Simulate shadow effect (limited in Tkinter)"""
        try:
            widget.config(highlightthickness=1, highlightbackground=color)
        except:
            pass


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
            for key, value in press_config. items():
                try:
                    widget.config(**{key: value})
                except:
                    pass
        
        def on_release(e):
            for key, value in release_config. items():
                try:
                    widget.config(**{key: value})
                except:
                    pass
        
        widget. bind("<ButtonPress-1>", on_press)
        widget.bind("<ButtonRelease-1>", on_release)
    
    @staticmethod
    def smooth_scroll(canvas, delta):
        """Smooth scrolling effect"""
        canvas.yview_scroll(int(-1 * (delta / 120)), "units")
    
    @staticmethod
    def fade_in(widget, duration=300, steps=10):
        """Fade in animation (simulated)"""
        widget.update()
    
    @staticmethod
    def debounce(func, wait_ms=300):
        """Debounce function calls (like JavaScript debounce)"""
        timer = None
        def debounced(*args, **kwargs):
            nonlocal timer
            if timer: 
                try:
                    widget.after_cancel(timer)
                except:
                    pass
            widget = args[0] if args else None
            if widget and hasattr(widget, 'after'):
                timer = widget.after(wait_ms, lambda: func(*args, **kwargs))
        return debounced


# ============================================
# ANIMATED COMPONENTS
# ============================================
class AnimatedButton(Button):
    """Button with CSS-like hover and click animations"""
    
    def __init__(self, parent, text="", command=None, variant="primary", theme="light", **kwargs):
        style = StyleConfig.get_button_style(theme, variant)
        
        # Merge style with custom kwargs
        config = {**style, **kwargs}
        config.pop('hover_bg', None)
        config.pop('active_bg', None)
        
        super().__init__(parent, text=text, command=command, **config)
        
        # Store colors for animations
        self.default_bg = style. get('bg')
        self.hover_bg = style.get('hover_bg')
        self.active_bg = style.get('active_bg')
        
        # Apply hover effect
        EventHandler.on_hover(
            self,
            enter_config={"bg": self.hover_bg},
            leave_config={"bg": self.default_bg}
        )
        
        # Apply click animation
        EventHandler.on_click_animation(
            self,
            press_config={"bg": self.active_bg, "relief": SUNKEN},
            release_config={"bg": self. hover_bg, "relief": FLAT}
        )


class AnimatedCard(Frame):
    """Card component with shadow and hover effects"""
    
    def __init__(self, parent, bg="#ffffff", hover_lift=True, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        
        self.default_relief = kwargs.get('relief', FLAT)
        self.hover_lift = hover_lift
        
        if hover_lift:
            EventHandler.on_hover(
                self,
                enter_config={"relief": RAISED, "borderwidth": 1},
                leave_config={"relief": self.default_relief, "borderwidth": 0}
            )


# ============================================
# ENHANCED ADMIN DASHBOARD
# ============================================
class AdminDashboard:
    def __init__(self, root, admin_id, logout_callback=None):
        self.root = root
        self. admin_id = admin_id
        self.logout_callback = logout_callback

        # Initialize service layer
        self.service = AdminService(admin_id)
        
        # Load photo path from profile
        try:
            profile = self.service.get_profile()
            self.photo_path = profile[6] if profile and len(profile) > 6 else None
        except Exception:
            self.photo_path = None

        # Cache for image reference
        self.profile_img_tk = None

        # Theme management
        self.current_theme = get_theme_preference()
        self.theme_colors = get_theme_colors(self.current_theme)
        self.theme_toggle_btn = None

        # Update theme colors
        self.update_theme_colors()

        # Window setup
        try:
            self.root.title("Admin Dashboard")
            self.root.geometry("950x765")
        except Exception:
            pass
        self.root.configure(bg=self.color_content_bg)

        # Configure styles
        self.configure_styles()

        # Setup menu bar
        self.setup_menubar()

        # Main layout
        self.sidebar = Frame(self.root, bg=self.color_sidebar_bg, width=240)
        self.sidebar.pack(side=LEFT, fill=Y)

        self.content = Frame(self.root, bg=self.color_content_bg)
        self.content.pack(side=RIGHT, fill=BOTH, expand=True)

        self._build_sidebar()
        self. show_home()

    def update_theme_colors(self):
        """Update all theme colors from theme_colors dict"""
        self.color_sidebar_bg = self.theme_colors.get("sidebar_bg", "#050816")
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
            
            # Compact Treeview with normal text
            style.configure(
                "Admin. Treeview",
                background=self.theme_colors.get("treeview_bg", "#1b1414"),
                foreground=self.theme_colors.get("treeview_fg", "#111827"),
                fieldbackground=self.theme_colors.get("treeview_bg", "#ffffff"),
                rowheight=20,
                padding=(2, 1),
                font=("Arial", 9),
                borderwidth=0,
                relief="flat"
            )
            style.configure(
                "Admin.Treeview.Heading",
                background=self.color_sidebar_btn,
                foreground="#130808",
                padding=(4, 2),
                font=("Arial", 10, "bold"),
                borderwidth=0,
                relief="flat"
            )
            style.map(
                "Admin.Treeview",
                background=[("selected", self.theme_colors. get("treeview_selected_bg", "#2563eb"))],
                foreground=[("selected", self.theme_colors.get("treeview_selected_fg", "#0b0b0b"))]
            )
            
            # Remove borders
            style.layout("Admin.Treeview", [('Admin.Treeview.treearea', {'sticky': 'nswe'})])
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
        filemenu.add_command(label='Save as... ', command=self._do_nothing)
        filemenu.add_command(label='Close', command=self._do_nothing)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self. root.quit)
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
        viewmenu.add_command(label='Home', command=self.show_home)
        viewmenu.add_command(label='All Bookings', command=self.show_all_bookings)
        viewmenu.add_command(label='Customers', command=self.show_customers)
        viewmenu.add_command(label='Assign Driver', command=self.show_assign_driver)
        viewmenu.add_command(label='Create Booking', command=self.show_create_booking)
        viewmenu.add_command(label='Create Driver', command=self.show_create_driver)
        viewmenu.add_command(label='Profile', command=self.show_profile)
        self.mainmenu.add_cascade(label='View', menu=viewmenu)

        # Tools Menu
        toolsmenu = Menu(self.mainmenu, tearoff=0)
        toolsmenu.add_command(label='Settings', command=self.show_settings)
        toolsmenu.add_command(label='Support', command=self.show_support)
        toolsmenu.add_command(label='Export Data', command=self._do_nothing)
        toolsmenu.add_command(label='Toggle Theme', command=self.toggle_theme)
        self.mainmenu.add_cascade(label='Tools', menu=toolsmenu)

        # Help Menu
        helpmenu = Menu(self.mainmenu, tearoff=0)
        helpmenu.add_command(label='User Guide', command=self._do_nothing)
        helpmenu.add_command(label='About', command=self._do_nothing)
        helpmenu.add_command(label='Contact Support', command=self._show_support_popup)
        self.mainmenu.add_cascade(label='Help', menu=helpmenu)

        self.root.config(menu=self.mainmenu)

    # ------------- THEME TOGGLE (NO POPUP) -------------
    def toggle_theme(self):
        """Toggle between light and dark theme with smooth transition"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        save_theme_preference(self.current_theme)
        self.theme_colors = get_theme_colors(self.current_theme)
        
        # Update colors
        self.update_theme_colors()
        
        # Update root background
        self.root.config(bg=self.color_content_bg)
        
        # Update styles
        self.configure_styles()
        
        # Rebuild UI (NO POPUP)
        self.sidebar.destroy()
        self.content.destroy()
        
        self.sidebar = Frame(self.root, bg=self.color_sidebar_bg, width=240)
        self.sidebar.pack(side=LEFT, fill=Y)

        self.content = Frame(self.root, bg=self.color_content_bg)
        self.content.pack(side=RIGHT, fill=BOTH, expand=True)
        
        self._build_sidebar()
        self.show_home()

    # ------------- IMAGE UTIL WITH EFFECTS -------------
    def _load_circular_image(self, path, size=(100, 100), add_shadow=True):
        """Load image from path, crop to circle, return PhotoImage with optional shadow"""
        try:
            img = Image.open(path).convert("RGBA")
            img = img.resize(size, Image. LANCZOS)

            # Create circular mask
            mask = Image. new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size[0], size[1]), fill=255)
            
            # Add soft shadow effect
            if add_shadow: 
                shadow = Image.new("RGBA", size, (0, 0, 0, 0))
                shadow_draw = ImageDraw.Draw(shadow)
                shadow_draw.ellipse((2, 2, size[0] - 2, size[1] - 2), fill=(0, 0, 0, 50))
                shadow = shadow.filter(ImageFilter.GaussianBlur(3))
            
            img.putalpha(mask)

            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"[DEBUG] _load_circular_image error: {e}")
            return None

    # ------------------ ENHANCED SIDEBAR ------------------
    def _build_sidebar(self):
        # Theme toggle button at the top with animation
        toggle_bg = "#f0f0f0" if self.current_theme == "light" else "#2d3748"
        toggle_fg = "#333333" if self.current_theme == "light" else "#e2e8f0"
        toggle_text = "Dark" if self.current_theme == "light" else "Light"
        
        self.theme_toggle_btn = Button(
            self.sidebar,
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
        
        # Add hover effect to theme toggle
        hover_bg = "#e5e5e5" if self.current_theme == "light" else "#374151"
        EventHandler.on_hover(
            self.theme_toggle_btn,
            enter_config={"bg": hover_bg},
            leave_config={"bg": toggle_bg}
        )
        
        Label(
            self.sidebar,
            text="Admin Menu",
            fg="white",
            bg=self. color_sidebar_bg,
            font=("Arial", 16, "bold"),
            pady=20
        ).pack()

        # Sidebar buttons with animations
        btns = [
            ("Home", self.show_home),
            ("View All Bookings", self.show_all_bookings),
            ("Assign Driver", self.show_assign_driver),
            ("View Customers", self.show_customers),
            ("Create Booking", self.show_create_booking),
            ("Create Driver", self.show_create_driver),
            ("Profile", self.show_profile),
            ("Settings", self.show_settings),
            ("Support", self.show_support),
        ]

        for text, cmd in btns:
            self.create_sidebar_button(text, cmd)

        # LOGOUT AT BOTTOM with animation
        logout_btn = AnimatedButton(
            self.sidebar,
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
            self.sidebar,
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
        btn.pack(pady=5, padx=5)
        
        # Add hover effect
        EventHandler.on_hover(
            btn,
            enter_config={"bg": self.color_sidebar_btn_active},
            leave_config={"bg": self.color_sidebar_btn}
        )
        
        return btn

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

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

    # ---------------- ENHANCED HOME ----------------
    def show_home(self):
        self.clear_content()
        
        # Hero Section
        hero_frame = Frame(self.content, bg=self. color_content_bg)
        hero_frame.pack(pady=(20, 30))
        
        Label(
            hero_frame,
            text="Welcome to Admin Dashboard",
            font=("Arial", 28, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack()
        
        Label(
            hero_frame,
            text="Manage your taxi booking system efficiently",
            font=("Arial", 12),
            bg=self.color_content_bg,
            fg=self.color_text_secondary
        ).pack(pady=(5, 0))

        # Stats Cards Container with AnimatedCard
        stats_container = Frame(self.content, bg=self.color_content_bg)
        stats_container.pack(pady=20, padx=20, fill=X)

        try:
            stats = self.service. get_stats()
            total_customers = stats.get("customers", 0)
            total_drivers = stats.get("drivers", 0)
            total_bookings = stats.get("bookings", 0)
        except Exception as e:
            total_customers = total_drivers = total_bookings = 0

        # Create stat cards with animations
        self. create_stat_card(stats_container, total_customers, "Customers", "👥", "#2563eb")
        self.create_stat_card(stats_container, total_drivers, "Drivers", "🚗", "#16a34a")
        self.create_stat_card(stats_container, total_bookings, "Total Bookings", "📋", "#dc2626")

        # Quick Actions
        quick_actions = Frame(self.content, bg=self.color_content_bg)
        quick_actions.pack(pady=30)
        
        AnimatedButton(
            quick_actions,
            text="View Bookings",
            command=self. show_all_bookings,
            variant="primary",
            theme=self.current_theme,
            width=18,
            height=2
        ).pack(side=LEFT, padx=5)
        
        AnimatedButton(
            quick_actions,
            text="Create Booking",
            command=self.show_create_booking,
            variant="success",
            theme=self.current_theme,
            width=18,
            height=2
        ).pack(side=LEFT, padx=5)
        
        AnimatedButton(
            quick_actions,
            text="Create Driver",
            command=self. show_create_driver,
            variant="primary",
            theme=self.current_theme,
            width=18,
            height=2
        ).pack(side=LEFT, padx=5)

    def create_stat_card(self, parent, value, label, emoji, color):
        """Create an animated stat card"""
        card = AnimatedCard(parent, bg=self.color_card_bg, relief="flat", bd=1, hover_lift=True)
        card.pack(side=LEFT, padx=10, fill=BOTH, expand=True)
        
        card_inner = Frame(card, bg=self.color_card_bg)
        card_inner.pack(padx=20, pady=20, fill=BOTH)
        
        Label(card_inner, text=emoji, font=("Arial", 32), bg=self.color_card_bg).pack()
        Label(card_inner, text=str(value), font=("Arial", 32, "bold"), bg=self.color_card_bg, fg=color).pack()
        Label(card_inner, text=label, font=("Arial", 12), bg=self.color_card_bg, fg=self.color_text_secondary).pack()

    # ---------------- ENHANCED ALL BOOKINGS ----------------
    def show_all_bookings(self):
        self.clear_content()
        Label(
            self.content,
            text="All Bookings",
            font=("Arial", 20, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=10)

        # Search / filter card
        search_card = AnimatedCard(self.content, bg=self.color_card_bg, relief="flat", bd=1)
        search_card.pack(fill=X, padx=10, pady=(0, 5))

        search_frame = Frame(search_card, bg=self.color_card_bg)
        search_frame.pack(fill=X, padx=10, pady=8)

        entry_bg = self.theme_colors.get("entry_bg", "#ffffff")
        entry_fg = self.theme_colors.get("entry_fg", "#111827")

        Label(search_frame, text="Search:", bg=self.color_card_bg, fg=self.color_text_primary, font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 4))
        search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=search_var, width=22, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, font=("Arial", 9))
        search_entry.pack(side=LEFT, padx=(0, 10))

        # Status filter
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
        status_cb.pack(side=LEFT, padx=(0, 10))

        # Customer filter
        Label(search_frame, text="Customer:", bg=self.color_card_bg, fg=self.color_text_primary, font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 4))
        customer_var = StringVar()
        customer_entry = Entry(search_frame, textvariable=customer_var, width=16, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, font=("Arial", 9))
        customer_entry.pack(side=LEFT, padx=(0, 10))

        # Driver filter
        Label(search_frame, text="Driver:", bg=self.color_card_bg, fg=self.color_text_primary, font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 4))
        driver_var = StringVar()
        driver_entry = Entry(search_frame, textvariable=driver_var, width=16, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, font=("Arial", 9))
        driver_entry.pack(side=LEFT, padx=(0, 10))

        frame = Frame(self.content, bg=self.color_content_bg)
        frame.pack(fill=BOTH, expand=True, pady=10, padx=10)

        cols = ("ID", "Customer", "Pickup", "Dropoff", "Date", "Time", "Status", "Driver", "Finished Time")
        self.bookings_tree = ttk. Treeview(frame, columns=cols, show="headings", height=18, style="Admin.Treeview")
        
        # row stripe tags
        even_bg = self.theme_colors.get("treeview_even", "#ffffff")
        odd_bg = self.theme_colors.get("treeview_odd", "#f3f4f6")
        text_color = self.theme_colors.get("treeview_fg", "#111827")
        
        self.bookings_tree. tag_configure("evenrow", background=even_bg, foreground=text_color)
        self.bookings_tree. tag_configure("oddrow", background=odd_bg, foreground=text_color)
        
        for c in cols:
            self.bookings_tree.heading(c, text=c)
            if c == "ID":
                self.bookings_tree.column(c, width=55, anchor=CENTER, stretch=False)
            elif c in ("Date", "Time"):
                self.bookings_tree.column(c, width=80, anchor=CENTER, stretch=False)
            elif c == "Status":
                self.bookings_tree.column(c, width=90, anchor=CENTER, stretch=False)
            elif c == "Finished Time":
                self.bookings_tree.column(c, width=130, anchor=CENTER, stretch=False)
            elif c == "Customer":
                self.bookings_tree.column(c, width=150, stretch=True)
            elif c == "Driver":
                self.bookings_tree.column(c, width=120, stretch=True)
            elif c == "Pickup":
                self.bookings_tree.column(c, width=140, stretch=True)
            elif c == "Dropoff": 
                self.bookings_tree. column(c, width=140, stretch=True)
        self.bookings_tree.pack(fill=BOTH, expand=True, side=LEFT)

        scroll = ttk.Scrollbar(frame, orient=VERTICAL, command=self.bookings_tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.bookings_tree. configure(yscrollcommand=scroll.set)

        # Make sortable
        self._make_treeview_sortable(self.bookings_tree, cols, numeric_cols={"ID"})

        btn_frame = Frame(self.content, bg=self.color_content_bg)
        btn_frame.pack(pady=8)
        
        AnimatedButton(
            btn_frame,
            text="Refresh",
            command=self. show_all_bookings,
            variant="primary",
            theme=self.current_theme,
            width=12
        ).pack(side=LEFT, padx=6)
        
        AnimatedButton(
            btn_frame,
            text="Cancel Booking",
            command=self.cancel_selected_booking,
            variant="danger",
            theme=self.current_theme,
            width=15
        ).pack(side=LEFT, padx=6)

        # Load data
        self._all_bookings_cache = []
        try:
            bookings = self.service.get_all_bookings()
            self._all_bookings_cache = bookings or []
        except Exception as e: 
            messagebox.showerror("Error", str(e))

        def _refresh_tree(filtered=None):
            for item in self.bookings_tree.get_children():
                self.bookings_tree.delete(item)
            data = filtered if filtered is not None else self._all_bookings_cache
            for idx, b in enumerate(data):
                vals = [
                    b.get("id"),
                    b.get("customer"),
                    b.get("pickup"),
                    b.get("dropoff"),
                    b.get("date"),
                    b.get("time"),
                    b.get("status"),
                    b.get("driver"),
                    b.get("finished_timestamp", ""),
                ]
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self. bookings_tree.insert("", END, values=vals, tags=(tag,))

        def _apply_filters(*_):
            text = (search_var.get() or "").strip().lower()
            status_filter = (status_var.get() or "All").strip().lower()
            cust_filter = (customer_var.get() or "").strip().lower()
            driver_filter = (driver_var. get() or "").strip().lower()

            filtered = []
            for b in self._all_bookings_cache:
                bid = b.get("id")
                customer = str(b.get("customer", ""))
                pickup = str(b. get("pickup", ""))
                dropoff = str(b.get("dropoff", ""))
                date_str = str(b.get("date", ""))
                time_str = str(b.get("time", ""))
                status = str(b.get("status", ""))
                driver = str(b.get("driver", ""))

                if text: 
                    finished_time = str(b.get("finished_timestamp", ""))
                    combined = " ".join(
                        [str(bid), customer, pickup, dropoff, date_str, time_str, status, driver, finished_time]
                    ).lower()
                    if text not in combined:
                        continue

                if status_filter and status_filter != "all":
                    if status. lower() != status_filter:
                        continue

                if cust_filter and cust_filter not in customer. lower():
                    continue

                if driver_filter and driver_filter not in driver.lower():
                    continue

                filtered.append(b)

            _refresh_tree(filtered)

        # Bind filters
        search_entry.bind("<KeyRelease>", _apply_filters)
        customer_entry.bind("<KeyRelease>", _apply_filters)
        driver_entry.bind("<KeyRelease>", _apply_filters)
        status_cb.bind("<<ComboboxSelected>>", _apply_filters)

        _refresh_tree()

    def cancel_selected_booking(self):
        sel = self.bookings_tree. selection()
        if not sel:
            messagebox.showwarning("Select", "Select a booking to cancel.")
            return
        booking_id = self.bookings_tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirm", f"Cancel booking {booking_id}?"):
            return
        try:
            self.service.cancel_booking(booking_id)
            messagebox.showinfo("Success", "Booking cancelled.")
            self. show_all_bookings()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- ENHANCED ASSIGN DRIVER ----------------
    def show_assign_driver(self):
        self.clear_content()
        Label(
            self.content,
            text="Assign Driver",
            font=("Arial", 20, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=10)

        # Form card
        form_card = AnimatedCard(self.content, bg=self.color_card_bg, relief="flat", bd=1)
        form_card.pack(pady=20, padx=16, fill=X)

        frame = Frame(form_card, bg=self.color_card_bg)
        frame.pack(pady=20, padx=16, fill=X)

        entry_bg = self.theme_colors.get("entry_bg", "#ffffff")
        entry_fg = self.theme_colors.get("entry_fg", "#111827")

        label_opts = {"bg": self.color_card_bg, "fg": self.color_text_primary, "anchor": "w", "font": ("Arial", 11, "bold"), "width": 16}
        entry_pad = {"padx": 8, "pady": 8, "sticky": "w"}

        Label(frame, text="Booking ID:", **label_opts).grid(row=0, column=0, **entry_pad)
        booking_id_entry = Entry(frame, width=24, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        booking_id_entry. grid(row=0, column=1, **entry_pad)

        Label(frame, text="Driver:", **label_opts).grid(row=1, column=0, **entry_pad)
        driver_cb = ttk.Combobox(frame, width=52, state="readonly")
        driver_cb.grid(row=1, column=1, **entry_pad)
        driver_cb._value_map = {}

        def load_driver_options():
            try:
                options, value_map = self.service.get_drivers_for_assignment()
                driver_cb["values"] = options
                driver_cb._value_map = value_map
            except Exception as e:
                messagebox.showerror("Error", str(e))

        load_driver_options()
        
        AnimatedButton(
            frame,
            text="Refresh Drivers",
            command=load_driver_options,
            variant="primary",
            theme=self. current_theme,
            width=15
        ).grid(row=1, column=2, padx=8)

        def assign():
            disp = driver_cb.get()
            bid = booking_id_entry.get().strip()
            if not bid: 
                return messagebox.showwarning("Error", "Enter booking id.")
            if not disp:
                return messagebox.showwarning("Error", "Select driver.")
            try:
                booking_id = int(bid)
            except: 
                return messagebox.showwarning("Error", "Invalid booking id.")
            sel = driver_cb._value_map.get(disp)
            if not sel: 
                return messagebox.showwarning("Error", "Invalid driver selected.")
            source, ident = sel

            try:
                self.service.assign_driver(booking_id, source, ident)
                messagebox.showinfo("Success", "Driver assigned successfully.")
                booking_id_entry.delete(0, END)
                driver_cb.set("")
            except ValueError as e:
                messagebox. showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        AnimatedButton(
            frame,
            text="Assign Driver",
            command=assign,
            variant="success",
            theme=self.current_theme,
            width=20,
            height=2
        ).grid(row=2, column=1, pady=14)

    # ---------------- ENHANCED CUSTOMERS ----------------
    def show_customers(self):
        self.clear_content()
        Label(
            self.content,
            text="Customers & Users",
            font=("Arial", 20, "bold"),
            bg=self.color_content_bg,
            fg=self. color_accent
        ).pack(pady=10)

        # Search / filters card
        search_card = AnimatedCard(self.content, bg=self.color_card_bg, relief="flat", bd=1)
        search_card.pack(fill=X, padx=10, pady=(0, 5))

        search_frame = Frame(search_card, bg=self.color_card_bg)
        search_frame.pack(fill=X, padx=10, pady=8)
        
        entry_bg = self.theme_colors.get("entry_bg", "#ffffff")
        entry_fg = self.theme_colors.get("entry_fg", "#111827")
        
        Label(search_frame, text="Search:", bg=self.color_card_bg, fg=self.color_text_primary, font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 4))
        search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=search_var, width=22, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, font=("Arial", 9))
        search_entry.pack(side=LEFT, padx=(0, 10))

        Label(search_frame, text="Role:", bg=self.color_card_bg, fg=self.color_text_primary, font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 4))
        role_var = StringVar(value="All")
        role_cb = ttk.Combobox(
            search_frame,
            textvariable=role_var,
            values=["All", "Admin", "Customer", "Driver"],
            width=12,
            state="readonly",
            font=("Arial", 9)
        )
        role_cb.pack(side=LEFT, padx=(0, 10))

        Label(search_frame, text="Phone:", bg=self.color_card_bg, fg=self.color_text_primary, font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 4))
        phone_var = StringVar()
        phone_entry = Entry(search_frame, textvariable=phone_var, width=16, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, font=("Arial", 9))
        phone_entry.pack(side=LEFT, padx=(0, 10))

        frame = Frame(self.content, bg=self.color_content_bg)
        frame.pack(fill=BOTH, expand=True, pady=10, padx=10)

        cols = ("ID", "Name", "Email", "Phone", "Address", "Role")
        self.customers_tree = ttk.Treeview(frame, columns=cols, show="headings", height=18, style="Admin.Treeview")
        
        # row stripe tags
        even_bg = self. theme_colors.get("treeview_even", "#ffffff")
        odd_bg = self.theme_colors.get("treeview_odd", "#f3f4f6")
        text_color = self.theme_colors.get("treeview_fg", "#111827")
        
        self.customers_tree.tag_configure("evenrow", background=even_bg, foreground=text_color)
        self.customers_tree.tag_configure("oddrow", background=odd_bg, foreground=text_color)
        
        for c in cols:
            self.customers_tree.heading(c, text=c)
            if c == "ID":
                self.customers_tree.column(c, width=55, anchor=CENTER, stretch=False)
            elif c == "Name":
                self.customers_tree.column(c, width=130, stretch=True)
            elif c == "Email":
                self.customers_tree.column(c, width=190, stretch=True)
            elif c == "Phone":
                self.customers_tree.column(c, width=105, anchor=CENTER, stretch=False)
            elif c == "Role":
                self.customers_tree.column(c, width=70, anchor=CENTER, stretch=False)
            else:  # Address
                self.customers_tree.column(c, width=190, stretch=True)
        self.customers_tree.pack(fill=BOTH, expand=True, side=LEFT)

        scroll = ttk.Scrollbar(frame, orient=VERTICAL, command=self.customers_tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.customers_tree.configure(yscrollcommand=scroll.set)

        # Make sortable
        self._make_treeview_sortable(self. customers_tree, cols, numeric_cols={"ID"})

        btn_frame = Frame(self. content, bg=self.color_content_bg)
        btn_frame.pack(pady=8)
        
        AnimatedButton(
            btn_frame,
            text="Refresh",
            command=self.show_customers,
            variant="primary",
            theme=self.current_theme,
            width=12
        ).pack(side=LEFT, padx=6)
        
        AnimatedButton(
            btn_frame,
            text="Edit",
            command=self.edit_selected_customer,
            variant="primary",
            theme=self.current_theme,
            width=12
        ).pack(side=LEFT, padx=6)
        
        AnimatedButton(
            btn_frame,
            text="Delete",
            command=self. delete_selected_customer,
            variant="danger",
            theme=self.current_theme,
            width=12
        ).pack(side=LEFT, padx=6)

        self._all_customers_cache = []
        try:
            rows = self.service.get_all_users()
            self._all_customers_cache = rows or []
        except Exception as e:
            messagebox.showerror("Error", str(e))

        def _refresh_tree(filtered=None):
            for item in self.customers_tree.get_children():
                self.customers_tree.delete(item)
            data = filtered if filtered is not None else self._all_customers_cache
            for idx, r in enumerate(data):
                vals = list(r)
                while len(vals) < 6:
                    vals.append("")
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self. customers_tree.insert("", END, values=vals[: 6], tags=(tag,))

        def _apply_filters(*_):
            text = (search_var.get() or "").strip().lower()
            role = (role_var.get() or "All").strip().lower()
            phone = (phone_var. get() or "").strip().lower()

            filtered = []
            for r in self._all_customers_cache:
                rid = r[0] if len(r) > 0 else ""
                name = r[1] if len(r) > 1 else ""
                email = r[2] if len(r) > 2 else ""
                phone_val = r[3] if len(r) > 3 else ""
                address = r[4] if len(r) > 4 else ""
                role_val = r[5] if len(r) > 5 else ""

                if text:
                    combined = " ".join(str(v) for v in (rid, name, email, phone_val, address, role_val)).lower()
                    if text not in combined:
                        continue

                if role and role != "all":
                    if str(role_val).lower() != role:
                        continue

                if phone and phone not in str(phone_val).lower():
                    continue

                filtered.append(r)

            _refresh_tree(filtered)

        search_entry.bind("<KeyRelease>", _apply_filters)
        phone_entry.bind("<KeyRelease>", _apply_filters)
        role_cb.bind("<<ComboboxSelected>>", _apply_filters)

        _refresh_tree()

    def edit_selected_customer(self):
        sel = self.customers_tree.selection()
        if not sel: 
            messagebox.showwarning("Select", "Select a customer to edit.")
            return
        customer_id = self.customers_tree. item(sel[0])["values"][0]
        self.edit_customer_form(customer_id, refresh_func=self.show_customers)

    def edit_customer_form(self, customer_id, refresh_func=None):
        try:
            row = self.service.get_user(customer_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if not row:
            messagebox. showerror("Error", "Customer not found.")
            return

        form = Toplevel(self.root)
        form.title("Edit User")
        form.configure(bg=self.color_card_bg)
        
        fields = ["Full Name", "Email", "Phone", "Address", "Role"]
        entries = {}
        
        entry_bg = self.theme_colors.get("entry_bg", "#ffffff")
        entry_fg = self. theme_colors.get("entry_fg", "#111827")
        
        for i, f in enumerate(fields):
            Label(form, text=f, bg=self.color_card_bg, fg=self.color_text_primary, font=("Arial", 11)).grid(row=i, column=0, padx=10, pady=6, sticky=E)
            ent = Entry(form, width=40, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
            ent.grid(row=i, column=1, padx=10, pady=6)
            entries[f] = ent
            
        ent_vals = [row[1], row[2], row[3], row[4], row[5]]
        for i, v in enumerate(ent_vals):
            entries[fields[i]].insert(0, v if v is not None else "")
            if fields[i] == "Email":
                entries[fields[i]].config(state="disabled")

        def save():
            new_name = entries["Full Name"]. get().strip()
            new_phone = entries["Phone"].get().strip()
            new_address = entries["Address"].get().strip()
            new_role = entries["Role"].get().strip() or "Customer"
            try:
                self.service.update_user(customer_id, new_name, new_phone, new_address, new_role)
                messagebox. showinfo("Success", "User updated.")
                form.destroy()
                if refresh_func:
                    refresh_func()
            except ValueError as e:
                messagebox. showwarning("Validation", str(e))
            except Exception as e:
                messagebox. showerror("Error", str(e))

        AnimatedButton(
            form,
            text="Save Changes",
            command=save,
            variant="success",
            theme=self.current_theme,
            width=20
        ).grid(row=len(fields), column=0, columnspan=2, pady=12)

    def delete_selected_customer(self):
        sel = self.customers_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a customer to delete.")
            return
        customer_id = self.customers_tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirm", f"Delete user {customer_id}?"):
            return
        try:
            self.service.delete_user(customer_id)
            messagebox.showinfo("Success", "User deleted.")
            self. show_customers()
        except Exception as e:
            messagebox. showerror("Error", str(e))

    # ---------------- ENHANCED CREATE BOOKING ----------------
    def show_create_booking(self):
        self.clear_content()
        Label(
            self.content,
            text="Create Booking (On Behalf of Customer)",
            font=("Arial", 18, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=10)

        # Form card
        form_card = AnimatedCard(self.content, bg=self.color_card_bg, relief="flat", bd=1)
        form_card.pack(pady=10, padx=16, fill=X)

        frame = Frame(form_card, bg=self.color_card_bg)
        frame.pack(pady=20, padx=16, fill=X)

        entry_bg = self.theme_colors.get("entry_bg", "#ffffff")
        entry_fg = self.theme_colors.get("entry_fg", "#111827")

        label_opts = {"bg": self.color_card_bg, "fg": self.color_text_primary, "anchor": "w", "font": ("Arial", 11, "bold"), "width": 18}
        entry_pad = {"padx": 8, "pady": 8, "sticky": "w"}

        Label(frame, text="Customer:", **label_opts).grid(row=0, column=0, **entry_pad)
        customer_cb = ttk.Combobox(frame, width=46, state="readonly")
        customer_cb.grid(row=0, column=1, **entry_pad)

        try:
            customers = self.service.get_customers_for_booking()
            options = [f"{c[0]} - {c[1]} ({c[2]})" for c in customers]
            customer_cb["values"] = options
            customer_map = {options[i]: customers[i][0] for i in range(len(options))}
        except Exception as e:
            messagebox.showerror("Error", str(e))
            customer_map = {}

        Label(frame, text="Pickup:", **label_opts).grid(row=1, column=0, **entry_pad)
        pickup_ent = Entry(frame, width=48, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        pickup_ent.grid(row=1, column=1, **entry_pad)

        Label(frame, text="Dropoff:", **label_opts).grid(row=2, column=0, **entry_pad)
        drop_ent = Entry(frame, width=48, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        drop_ent.grid(row=2, column=1, **entry_pad)

        Label(frame, text="Date (YYYY-MM-DD):", **label_opts).grid(row=3, column=0, **entry_pad)
        
        today = datetime.now().date()
        date_entry = DateEntry(
            frame,
            width=22,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            mindate=today
        )
        date_entry. set_date(today)
        date_entry.grid(row=3, column=1, sticky="w", padx=8, pady=8)

        Label(frame, text="Time (HH: MM):", **label_opts).grid(row=4, column=0, **entry_pad)
        
        time_container = Frame(frame, bg=self.color_card_bg)
        time_container. grid(row=4, column=1, sticky="w", padx=8, pady=8)
        
        time_ent = Entry(time_container, width=18, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        time_ent.insert(0, datetime.now().strftime("%H:%M"))
        time_ent.pack(side=LEFT, padx=(0, 5))
        
        def set_current_time():
            now_str = datetime.now().strftime("%H:%M")
            time_ent.delete(0, END)
            time_ent. insert(0, now_str)
        
        ttk.Button(time_container, text="Now", command=set_current_time).pack(side=LEFT)

        Label(frame, text="Taxi Type (optional):", **label_opts).grid(row=5, column=0, **entry_pad)
        taxi_ent = Entry(frame, width=48, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        taxi_ent.grid(row=5, column=1, **entry_pad)

        def submit_booking():
            sel = customer_cb.get()
            if not sel:  
                return messagebox.showwarning("Error", "Select a customer.")
            customer_id = customer_map. get(sel)
            pickup = pickup_ent.get().strip()
            dropoff = drop_ent.get().strip()
            date_str = date_entry.get().strip()
            time_str = time_ent. get().strip()
            taxi_type = taxi_ent.get().strip() or None

            try:
                self.service.create_booking(customer_id, pickup, dropoff, date_str, time_str, taxi_type)
                messagebox.showinfo("Success", "Booking created.")
                customer_cb.set("")
                pickup_ent.delete(0, END)
                drop_ent.delete(0, END)
                taxi_ent.delete(0, END)
                date_entry. set_date(today)
                time_ent.delete(0, END)
                time_ent.insert(0, datetime.now().strftime("%H:%M"))
            except ValueError as e:
                messagebox.showwarning("Validation", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        AnimatedButton(
            self.content,
            text="Create Booking",
            command=submit_booking,
            variant="success",
            theme=self.current_theme,
            width=20,
            height=2
        ).pack(pady=14)

    # ---------------- ENHANCED CREATE DRIVER ----------------
    def show_create_driver(self):
        self.clear_content()
        Label(
            self.content,
            text="Create Driver",
            font=("Arial", 18, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=10)

        # Form card
        form_card = AnimatedCard(self.content, bg=self.color_card_bg, relief="flat", bd=1)
        form_card.pack(pady=10, padx=16, fill=X)

        frame = Frame(form_card, bg=self.color_card_bg)
        frame.pack(pady=20, padx=16, fill=X)

        entry_bg = self.theme_colors. get("entry_bg", "#ffffff")
        entry_fg = self.theme_colors.get("entry_fg", "#111827")

        label_opts = {"bg":  self.color_card_bg, "fg": self.color_text_primary, "anchor": "w", "font": ("Arial", 11, "bold"), "width": 18}
        entry_pad = {"padx": 8, "pady": 8, "sticky": "w"}

        Label(frame, text="Full Name:", **label_opts).grid(row=0, column=0, **entry_pad)
        name_ent = Entry(frame, width=44, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        name_ent.grid(row=0, column=1, **entry_pad)

        Label(frame, text="Email:", **label_opts).grid(row=1, column=0, **entry_pad)
        email_ent = Entry(frame, width=44, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        email_ent.grid(row=1, column=1, **entry_pad)

        Label(frame, text="Phone:", **label_opts).grid(row=2, column=0, **entry_pad)
        phone_ent = Entry(frame, width=44, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        phone_ent.grid(row=2, column=1, **entry_pad)

        Label(frame, text="License Num:", **label_opts).grid(row=3, column=0, **entry_pad)
        lic_ent = Entry(frame, width=44, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        lic_ent.grid(row=3, column=1, **entry_pad)

        Label(frame, text="Registration Num:", **label_opts).grid(row=4, column=0, **entry_pad)
        reg_ent = Entry(frame, width=44, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        reg_ent.grid(row=4, column=1, **entry_pad)

        Label(frame, text="Password:", **label_opts).grid(row=5, column=0, **entry_pad)
        pass_ent = Entry(frame, width=44, show="*", bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        pass_ent.grid(row=5, column=1, **entry_pad)

        def submit_driver():
            name = name_ent.get().strip()
            email = email_ent.get().strip()
            phone = phone_ent.get().strip()
            lic = lic_ent.get().strip()
            reg = reg_ent.get().strip()
            pwd = pass_ent.get().strip()
            try:
                self.service.create_or_update_driver(name, email, phone, lic, reg, pwd)
                messagebox.showinfo("Success", "Driver created/updated.")
                name_ent.delete(0, END)
                email_ent.delete(0, END)
                phone_ent.delete(0, END)
                lic_ent.delete(0, END)
                reg_ent.delete(0, END)
                pass_ent.delete(0, END)
            except ValueError as e:  
                messagebox.showwarning("Validation", str(e))
            except Exception as e:  
                messagebox.showerror("Error", str(e))

        AnimatedButton(
            self.content,
            text="Create Driver",
            command=submit_driver,
            variant="success",
            theme=self.current_theme,
            width=20,
            height=2
        ).pack(pady=12)

    # ---------------- ENHANCED PROFILE ----------------
    def show_profile(self):
        self.clear_content()

        Label(
            self.content,
            text="My Profile",
            font=("Arial", 18, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=20)

        if not self.admin_id:
            messagebox.showerror("Error", "Admin ID not available.  Cannot load profile.")
            return

        try:
            row = self.service.get_profile()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch profile: {e}")
            return

        if not row:
            messagebox.showerror("Error", "Admin not found!")
            return

        if len(row) == 7:
            full_name, email, phone, address, gender, role, db_photo_path = row
            self.photo_path = db_photo_path
        else:
            full_name, email, phone, address, gender, role = row

        # ---------- Photo + Upload ----------
        photo_frame = Frame(self.content, bg=self.color_content_bg)
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
            # fallback:  first letter
            avatar_canvas.create_text(
                center_x,
                center_y,
                text=(full_name[: 1].upper() if full_name else "?"),
                font=("Arial", 32, "bold"),
                fill="#4b5563",
                tags="avatar_initial"
            )

        refresh_avatar()

        def upload_photo():
            filetypes = [
                ("Image files", "*.png *.jpg *. jpeg *.gif *.bmp"),
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
                filename = f"admin_{self.admin_id}{ext}"
                dest_path = os.path.join(photos_dir, filename)

                with open(filepath, "rb") as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())

                self.photo_path = dest_path
                self.service.update_photo_path(dest_path)
                messagebox. showinfo("Success", "Profile photo updated.")
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

        # ---------- Text fields in a card ----------
        form_card = AnimatedCard(self.content, bg=self.color_card_bg, relief="flat", bd=1)
        form_card.pack(pady=10, padx=20, fill=BOTH)

        frame = Frame(form_card, bg=self.color_card_bg)
        frame.pack(pady=20, padx=20)

        entry_bg = self. theme_colors.get("entry_bg", "#ffffff")
        entry_fg = self.theme_colors.get("entry_fg", "#111827")

        labels = ["Full Name", "Email", "Phone", "Address", "Gender", "Role"]
        values = [full_name, email, phone, address, gender, role]
        entries = {}

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

            if lab in ["Email", "Gender", "Role"]:
                ent.config(state="disabled", disabledbackground=self.color_content_bg)

            ent.grid(row=i, column=1, padx=10, pady=7)
            entries[lab] = ent

        def update():
            new_name = entries["Full Name"].get()
            new_phone = entries["Phone"].get()
            new_address = entries["Address"].get()

            if not new_name or not new_phone or not new_address:
                messagebox.showwarning("Warning", "All fields are required!")
                return

            try: 
                self.service.update_profile(new_name, new_phone, new_address)
                messagebox. showinfo("Success", "Profile updated successfully!")
            except ValueError as e:
                messagebox. showwarning("Warning", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {e}")

        AnimatedButton(
            self.content,
            text="Save Changes",
            command=update,
            variant="success",
            theme=self.current_theme,
            width=20,
            height=2
        ).pack(pady=20)

    # ---------------- ENHANCED SETTINGS ----------------
    def show_settings(self):
        self.clear_content()
        Label(
            self.content,
            text="Settings",
            font=("Arial", 18, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=20)

        # Settings card
        settings_card = AnimatedCard(self.content, bg=self.color_card_bg, relief="flat", bd=1)
        settings_card.pack(pady=10, padx=20, fill=BOTH)

        frame = Frame(settings_card, bg=self. color_card_bg)
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
            selectcolor=self.color_card_bg,
            font=("Arial", 11)
        ).grid(row=2, column=0, sticky="w", padx=20, pady=5)

        Label(
            frame,
            text="(These settings are placeholders – connect them to DB later. )",
            bg=self.color_card_bg,
            fg=self.color_text_secondary,
            font=("Arial", 9, "italic")
        ).grid(row=3, column=0, sticky="w", padx=10, pady=10)

    # ---------------- ENHANCED SUPPORT ----------------
    def show_support(self):
        self.clear_content()

        Label(
            self.content,
            text="Support",
            font=("Arial", 18, "bold"),
            bg=self.color_content_bg,
            fg=self.color_accent
        ).pack(pady=20)

        # Support card
        support_card = AnimatedCard(self.content, bg=self.color_card_bg, relief="flat", bd=1)
        support_card.pack(pady=10, padx=20, fill=BOTH)

        Label(
            support_card,
            text="If you face any issue with bookings, drivers, or users,\nyou can contact our support team.",
            font=("Arial", 12),
            bg=self.color_card_bg,
            fg=self.color_text_primary,
            justify="center"
        ).pack(pady=20)

        AnimatedButton(
            support_card,
            text="Contact Support",
            command=self._show_support_popup,
            variant="primary",
            theme=self.current_theme,
            width=20,
            height=2
        ).pack(pady=20)

    # ------------------ LOGOUT & MISC ------------------
    def logout(self):
        self._on_logout()

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

    def destroy(self):
        """Remove dashboard UI when logging out / switching user."""
        try:
            self.sidebar.destroy()
        except Exception:
            pass
        try: 
            self.content.destroy()
        except Exception:
            pass

    def _do_nothing(self):
        messagebox.showinfo("Coming Soon", "Feature not implemented yet ✨")

    def _show_support_popup(self):
        messagebox.showinfo(
            "Contact Support",
            "You can contact support at:  support@example.com\n"
            "Or call: +977-9810000000"
        )


if __name__ == "__main__": 
    from tkinter import Tk
    root = Tk()
    AdminDashboard(root, admin_id="admin@example.com")
    root.mainloop()