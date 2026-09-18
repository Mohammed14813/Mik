#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║              MikroTik File Manager - Version 1.0                 ║
║                                                                  ║
║  الأقسام:                                                        ║
║  1. IMPORTS          - الاستيرادات                                ║
║  2. ARABIC SUPPORT   - دعم اللغة العربية                          ║
║  3. SETTINGS         - حفظ وتحميل الإعدادات                       ║
║  4. THEME            - الألوان والخطوط                            ║
║  5. WIDGETS          - الودجات المخصصة                            ║
║  6. CONNECTION       - إدارة الاتصال بالراوتر                     ║
║  7. UI HELPERS       - دوال مساعدة                                ║
║  8. ONBOARDING PAGE  - شاشة الترحيب                               ║
║  9. LOGIN PAGE       - شاشة تسجيل الدخول (كارت صغير + خلفية)      ║
║ 10. FILES PAGE       - شاشة إدارة الملفات                         ║
║ 11. MAIN APP         - التطبيق الرئيسي                            ║
║ 12. ENTRY POINT      - نقطة الدخول                                ║
╚══════════════════════════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════════════
# 1. IMPORTS - الاستيرادات
# ═══════════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import ssl
import ftplib
import os
import json
import random
import math
import io
import urllib.request

try:
    import librouteros
except ImportError:
    librouteros = None

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════
# 2. ARABIC SUPPORT - دعم اللغة العربية
# ═══════════════════════════════════════════════════════════════════

ARABIC_FORMS = {
    '\u0621': ('\u0621', '\u0621', '\u0621', '\u0621'),
    '\u0622': ('\u0622', '\u0622', '\u0622', '\u0622'),
    '\u0623': ('\u0623', '\u0623', '\u0623', '\u0623'),
    '\u0624': ('\u0624', '\u0624', '\u0624', '\u0624'),
    '\u0625': ('\u0625', '\u0625', '\u0625', '\u0625'),
    '\u0626': ('\u0626', '\uFE89', '\uFE8B', '\uFE8A'),
    '\u0627': ('\u0627', '\u0627', '\u0627', '\u0627'),
    '\u0628': ('\u0628', '\uFE91', '\uFE92', '\uFE90'),
    '\u0629': ('\u0629', '\uFE93', '\uFE94', '\uFE94'),
    '\u062A': ('\u062A', '\uFE97', '\uFE98', '\uFE96'),
    '\u062B': ('\u062B', '\uFE9B', '\uFE9C', '\uFE9A'),
    '\u062C': ('\u062C', '\uFE9F', '\uFEA0', '\uFE9E'),
    '\u062D': ('\u062D', '\uFEA3', '\uFEA4', '\uFEA2'),
    '\u062E': ('\u062E', '\uFEA7', '\uFEA8', '\uFEA6'),
    '\u062F': ('\u062F', '\uFEA9', '\uFEAA', '\uFEA9'),
    '\u0630': ('\u0630', '\uFEAB', '\uFEAC', '\uFEAB'),
    '\u0631': ('\u0631', '\uFEAD', '\uFEAE', '\uFEAD'),
    '\u0632': ('\u0632', '\uFEAF', '\uFEB0', '\uFEAF'),
    '\u0633': ('\u0633', '\uFEB3', '\uFEB4', '\uFEB2'),
    '\u0634': ('\u0634', '\uFEB7', '\uFEB8', '\uFEB6'),
    '\u0635': ('\u0635', '\uFEBB', '\uFEBC', '\uFEBA'),
    '\u0636': ('\u0636', '\uFEBF', '\uFEC0', '\uFEBE'),
    '\u0637': ('\u0637', '\uFEC3', '\uFEC4', '\uFEC2'),
    '\u0638': ('\u0638', '\uFEC7', '\uFEC8', '\uFEC6'),
    '\u0639': ('\u0639', '\uFECB', '\uFECC', '\uFECA'),
    '\u063A': ('\u063A', '\uFECF', '\uFED0', '\uFECE'),
    '\u0640': ('\u0640', '\u0640', '\u0640', '\u0640'),
    '\u0641': ('\u0641', '\uFED3', '\uFED4', '\uFED2'),
    '\u0642': ('\u0642', '\uFED7', '\uFED8', '\uFED6'),
    '\u0643': ('\u0643', '\uFEDB', '\uFEDC', '\uFEDA'),
    '\u0644': ('\u0644', '\uFEDF', '\uFEE0', '\uFEDE'),
    '\u0645': ('\u0645', '\uFEE3', '\uFEE4', '\uFEE2'),
    '\u0646': ('\u0646', '\uFEE7', '\uFEE8', '\uFEE6'),
    '\u0647': ('\u0647', '\uFEEB', '\uFEEC', '\uFEEA'),
    '\u0648': ('\u0648', '\uFEED', '\uFEEE', '\uFEED'),
    '\u0649': ('\u0649', '\uFEEF', '\uFEF0', '\uFEEF'),
    '\u064A': ('\u064A', '\uFEF3', '\uFEF4', '\uFEF2'),
    '\u0671': ('\u0671', '\u0671', '\u0671', '\u0671'),
    '\u067E': ('\u067E', '\uFB57', '\uFB58', '\uFB56'),
    '\u0686': ('\u0686', '\uFB7B', '\uFB7C', '\uFB7A'),
    '\u06A4': ('\u06A4', '\uFB6B', '\uFB6C', '\uFB6A'),
    '\u06AF': ('\u06AF', '\uFB93', '\uFB94', '\uFB92'),
}

NON_CONNECTING = set(
    '\u0621\u0622\u0623\u0624\u0625\u0627\u062F\u0630\u0631'
    '\u0632\u0648\u0649\u0671'
)


def _shape_arabic(text):
    """يعيد تشكيل الحروف العربية حسب موقعها."""
    if not text:
        return text
    result = []
    chars = list(text)
    n = len(chars)
    for i, ch in enumerate(chars):
        if ch not in ARABIC_FORMS:
            result.append(ch)
            continue
        prev_connected = False
        if i > 0:
            prev_ch = chars[i - 1]
            if prev_ch in ARABIC_FORMS and prev_ch not in NON_CONNECTING:
                prev_connected = True
        next_arabic = False
        if i < n - 1:
            next_ch = chars[i + 1]
            if next_ch in ARABIC_FORMS:
                next_arabic = True
        forms = ARABIC_FORMS[ch]
        if prev_connected and next_arabic:
            result.append(forms[2])
        elif prev_connected:
            result.append(forms[3])
        elif next_arabic and ch not in NON_CONNECTING:
            result.append(forms[1])
        else:
            result.append(forms[0])
    return ''.join(result)


def _reverse_arabic(text):
    """يعكس المقاطع العربية فقط."""
    if not text:
        return text

    def is_arabic(ch):
        return ('\u0600' <= ch <= '\u06FF'
                or '\u0750' <= ch <= '\u077F'
                or '\uFB50' <= ch <= '\uFEFF')

    segments = []
    current = ''
    current_is_ar = None
    for ch in text:
        a = is_arabic(ch)
        if current_is_ar is None:
            current_is_ar = a
            current = ch
        elif a == current_is_ar:
            current += ch
        else:
            segments.append((current, current_is_ar))
            current = ch
            current_is_ar = a
    if current:
        segments.append((current, current_is_ar))

    result_segments = []
    for seg, is_ar in segments:
        result_segments.append(seg[::-1] if is_ar else seg)

    result_segments.reverse()
    return ''.join(result_segments)


def ar(text):
    """يرجع النص العربي جاهزاً للعرض."""
    if not text:
        return text
    try:
        return _reverse_arabic(_shape_arabic(text))
    except Exception as e:
        print(f"ar() error: {e}")
        return text


# ═══════════════════════════════════════════════════════════════════
# 3. SETTINGS - حفظ وتحميل الإعدادات
# ═══════════════════════════════════════════════════════════════════

SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".mikrotik_manager.json")


def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_settings(data):
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════
# 4. THEME - الألوان والخطوط
# ═══════════════════════════════════════════════════════════════════

class Theme:
    BG_MAIN = "#f0f2f5"
    BG_CARD = "#ffffff"
    BG_DARK = "#1e293b"
    BG_INPUT = "#f1f5f9"
    BG_CHAT = "#efeae2"

    PRIMARY = "#2563eb"
    PRIMARY_HOVER = "#1d4ed8"
    SUCCESS = "#25d366"
    ERROR = "#dc2626"
    WARNING = "#d97706"

    TEXT_MAIN = "#0f172a"
    TEXT_SUB = "#475569"
    TEXT_WHITE = "#ffffff"

    BORDER = "#e5e7eb"
    HOVER = "#f3f4f6"
    SELECTED = "#dbeafe"

    FONT_TITLE = ("Arial", 22, "bold")
    FONT_HEADING = ("Arial", 14, "bold")
    FONT_BODY = ("Arial", 11)
    FONT_SMALL = ("Arial", 10)
    FONT_BUTTON = ("Arial", 11, "bold")


# ═══════════════════════════════════════════════════════════════════
# 5. WIDGETS - الودجات المخصصة
# ═══════════════════════════════════════════════════════════════════

class ModernButton(tk.Frame):
    """زرّ عصري مع تأثير hover وحالة disabled."""

    def __init__(self, parent, text, command, bg=Theme.PRIMARY,
                 fg=Theme.TEXT_WHITE, hover=Theme.PRIMARY_HOVER, font=None,
                 padx=20, pady=10):
        super().__init__(parent, bg=bg, cursor="hand2")
        self.command = command
        self.default_bg = bg
        self.hover_bg = hover
        self.enabled = True

        self.label = tk.Label(
            self, text=text, bg=bg, fg=fg,
            font=font or Theme.FONT_BUTTON,
            padx=padx, pady=pady, cursor="hand2"
        )
        self.label.pack(fill=tk.BOTH, expand=True)

        for w in (self, self.label):
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)
            w.bind("<Button-1>", self._on_click)

    def _on_enter(self, e):
        if self.enabled:
            self.configure(bg=self.hover_bg)
            self.label.configure(bg=self.hover_bg)

    def _on_leave(self, e):
        if self.enabled:
            self.configure(bg=self.default_bg)
            self.label.configure(bg=self.default_bg)

    def _on_click(self, e):
        if self.enabled and self.command:
            self.command()

    def set_state(self, state):
        if state == "disabled":
            self.enabled = False
            self.configure(bg="#94a3b8", cursor="")
            self.label.configure(bg="#94a3b8", cursor="")
        else:
            self.enabled = True
            self.configure(bg=self.default_bg, cursor="hand2")
            self.label.configure(bg=self.default_bg, cursor="hand2")


# ═══════════════════════════════════════════════════════════════════
# 6. CONNECTION - إدارة الاتصال بالراوتر
# ═══════════════════════════════════════════════════════════════════

class MikroTikConnection:
    """يدير اتصال librouteros + رفع الملفات عبر FTP."""

    def __init__(self, info):
        self.info = info
        self.connection = None

    def connect(self):
        if librouteros is None:
            raise RuntimeError("librouteros not installed")
        info = self.info
        if info['api_type'] == "api-ssl":
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            self.connection = librouteros.connect(
                host=info['ip'], port=info['port'],
                username=info['username'], password=info['password'],
                ssl_wrapper=ctx.wrap_socket
            )
        else:
            self.connection = librouteros.connect(
                host=info['ip'], port=info['port'],
                username=info['username'], password=info['password']
            )

    def list_files(self):
        if not self.connection:
            raise RuntimeError("Not connected")
        return list(self.connection('/file/print'))

    def file_exists(self, path):
        target = path.lstrip('/')
        try:
            for f in self.list_files():
                if f.get('name', '') == target:
                    return True
        except Exception:
            pass
        return False

    def upload_via_ftp(self, local_path, remote_path):
        info = self.info
        ftp = ftplib.FTP()
        ftp.connect(info['ip'], 21, timeout=15)
        ftp.login(info['username'], info['password'])
        ftp.set_pasv(True)
        try:
            ftp.cwd('/')
        except Exception:
            pass
        remote = remote_path.lstrip('/')
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote}', f)
        ftp.quit()

    def close(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass
            self.connection = None


# ═══════════════════════════════════════════════════════════════════
# 7. UI HELPERS - دوال مساعدة
# ═══════════════════════════════════════════════════════════════════

def format_size(size):
    try:
        size = float(size)
    except (TypeError, ValueError):
        size = 0
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def maximize_window(root):
    try:
        root.state('zoomed')
    except Exception:
        try:
            root.attributes('-zoomed', True)
        except Exception:
            sw = root.winfo_screenwidth()
            sh = root.winfo_screenheight()
            root.geometry(f"{sw}x{sh}+0+0")


# رابط الشعار
LOGO_URL = (
    "https://files.manuscdn.com/user_upload_by_module/session_file/"
    "310519663856733618/qbFMwbXzyOgicGZL.png"
)

# رابط صورة الخلفية
BG_IMAGE_URL = (
    "https://files.manuscdn.com/user_upload_by_module/session_file/"
    "310519663856733618/VEhJebXWqykagHlJ.jpg"
)


# ═══════════════════════════════════════════════════════════════════
# 8. ONBOARDING PAGE - شاشة الترحيب
# ═══════════════════════════════════════════════════════════════════

class OnboardingPage(tk.Frame):
    """شاشة ترحيبية مع أنيميشن + تعليمات تفعيل FTP."""

    def __init__(self, parent, on_complete, settings):
        super().__init__(parent, bg="#0f172a")
        self.on_complete = on_complete
        self.settings = settings

        self.onboarding_scale = settings.get("onboarding_scale", 1.0)
        self.shapes = []
        self.anim_schedule_id = None
        self._fade_in_step = 0
        self.zoomable_widgets = []
        self.step_labels = []
        self.step_canvases = []

        self._build()
        self._apply_zoom(initial=True)
        self._fade_in_schedule()
        self._animate_shapes()

    def _build(self):
        self.anim_canvas = tk.Canvas(
            self, bg="#0f172a", highlightthickness=0
        )
        self.anim_canvas.pack(fill=tk.BOTH, expand=True)
        self.update_idletasks()

        W = self.anim_canvas.winfo_width() or 1400
        H = self.anim_canvas.winfo_height() or 800

        self._create_shapes(W, H)
        self._create_card(W, H)
        self._create_zoom_controls()
        self._bind_events()

    def _create_shapes(self, W, H):
        colors = [
            "#1e3a8a", "#1e40af", "#2563eb", "#3b82f6",
            "#4f46e5", "#6366f1", "#8b5cf6", "#7c3aed",
            "#1e293b", "#334155",
        ]

        for _ in range(12):
            x = random.randint(-100, W + 100)
            y = random.randint(-100, H + 100)
            r = random.randint(80, 250)
            color = random.choice(colors)
            item = self.anim_canvas.create_oval(
                x - r, y - r, x + r, y + r, fill=color, outline=""
            )
            self.shapes.append({
                'id': item, 'x': x, 'y': y, 'r': r,
                'dx': random.uniform(-0.4, 0.4),
                'dy': random.uniform(-0.4, 0.4),
                'type': 'circle'
            })

        for _ in range(8):
            x = random.randint(0, W)
            y = random.randint(0, H)
            size = random.randint(40, 100)
            color = random.choice(colors)
            item = self.anim_canvas.create_rectangle(
                x, y, x + size, y + size, fill=color, outline=""
            )
            self.shapes.append({
                'id': item, 'x': x, 'y': y, 'size': size,
                'dx': random.uniform(-0.6, 0.6),
                'dy': random.uniform(-0.6, 0.6),
                'angle': random.uniform(0, 360),
                'angle_speed': random.uniform(-0.5, 0.5),
                'type': 'square'
            })

    def _create_card(self, W, H):
        self.card_frame = tk.Frame(
            self.anim_canvas, bg="#ffffff", highlightthickness=0
        )
        self.card_window = self.anim_canvas.create_window(
            W // 2, H // 2, window=self.card_frame, anchor="center"
        )

        self.card_content = tk.Frame(self.card_frame, bg="#ffffff")
        self.card_content.pack(padx=40, pady=30)

        self.icon_canvas = tk.Canvas(
            self.card_content, width=56, height=56,
            bg="#ffffff", highlightthickness=0
        )
        self.icon_canvas.pack(pady=(0, 12))
        self.icon_canvas.create_oval(
            2, 2, 54, 54, fill="#e8f0fe", outline="", tags="bg_circle"
        )
        self.icon_canvas.create_text(
            28, 28, text="⚙", font=("Arial", 24),
            fill="#2563eb", tags="icon_text"
        )

        title = tk.Label(
            self.card_content, text="MikroTik File Manager",
            bg="#ffffff", fg="#202124", font=("Arial", 15, "bold")
        )
        title.pack()
        self.zoomable_widgets.append((title, 15, "bold"))

        version = tk.Label(
            self.card_content, text="Version 1.0",
            bg="#ffffff", fg="#5f6368", font=("Arial", 9)
        )
        version.pack(pady=(2, 0))
        self.zoomable_widgets.append((version, 9, "normal"))

        tk.Frame(self.card_content, bg="#e5e7eb", height=1).pack(
            fill=tk.X, pady=(14, 14)
        )

        intro = tk.Label(
            self.card_content,
            text=ar("لإتمام عملية رفع الملفات بنجاح، فعّل خدمة FTP:"),
            bg="#ffffff", fg="#202124",
            font=("Arial", 10), justify="center", wraplength=320
        )
        intro.pack(pady=(0, 12))
        self.zoomable_widgets.append((intro, 10, "normal"))

        self._create_steps()

        tk.Frame(self.card_content, bg="#e5e7eb", height=1).pack(
            fill=tk.X, pady=(4, 12)
        )

        self._create_bottom_row()

    def _create_steps(self):
        self.steps_frame = tk.Frame(self.card_content, bg="#ffffff")
        self.steps_frame.pack(fill=tk.X, pady=(0, 12))

        steps = [
            ar("افتح WinBox واتصل بالراوتر"),
            ar("اذهب إلى IP ثم Services"),
            ar("فعّل خدمة ftp على المنفذ 21"),
            ar("تأكد من تفعيل خدمة api"),
        ]

        for i, step in enumerate(steps, 1):
            row = tk.Frame(self.steps_frame, bg="#ffffff")
            row.pack(fill=tk.X, pady=3, anchor="w")

            num_canvas = tk.Canvas(
                row, width=20, height=20,
                bg="#ffffff", highlightthickness=0
            )
            num_canvas.pack(side=tk.LEFT, padx=(0, 10))
            num_canvas.create_oval(
                1, 1, 19, 19, fill="#e8f0fe", outline="", tags="num_circle"
            )
            num_canvas.create_text(
                10, 10, text=str(i), font=("Arial", 8, "bold"),
                fill="#2563eb", tags="num_text"
            )
            self.step_canvases.append(num_canvas)

            lbl = tk.Label(
                row, text=step, bg="#ffffff", fg="#3c4043",
                font=("Arial", 9), anchor="e", justify="right"
            )
            lbl.pack(side=tk.LEFT, anchor="e")
            self.step_labels.append(lbl)

    def _create_bottom_row(self):
        bottom_row = tk.Frame(self.card_content, bg="#ffffff")
        bottom_row.pack(fill=tk.X)

        self.hide_check = tk.BooleanVar(value=False)
        self.checkbox_widget = tk.Checkbutton(
            bottom_row, text=ar("لا تعرض مرة أخرى"),
            variable=self.hide_check,
            bg="#ffffff", fg="#5f6368",
            activebackground="#ffffff", activeforeground="#202124",
            selectcolor="#ffffff", font=("Arial", 8),
            cursor="hand2", bd=0, highlightthickness=0
        )
        self.checkbox_widget.pack(side=tk.LEFT)

        self.ok_btn_frame = tk.Frame(bottom_row, bg="#2563eb", cursor="hand2")
        self.ok_btn_frame.pack(side=tk.RIGHT)

        self.ok_label = tk.Label(
            self.ok_btn_frame, text=ar("حسناً"),
            bg="#2563eb", fg="#ffffff",
            font=("Arial", 9, "bold"),
            padx=18, pady=6, cursor="hand2"
        )
        self.ok_label.pack()

        def _enter(e):
            self.ok_btn_frame.configure(bg="#1d4ed8")
            self.ok_label.configure(bg="#1d4ed8")

        def _leave(e):
            self.ok_btn_frame.configure(bg="#2563eb")
            self.ok_label.configure(bg="#2563eb")

        for w in (self.ok_btn_frame, self.ok_label):
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)
            w.bind("<Button-1>", lambda e: self._on_ok())

    def _create_zoom_controls(self):
        zoom_frame = tk.Frame(self.anim_canvas, bg="#1e293b")
        self.anim_canvas.create_window(20, 20, window=zoom_frame, anchor="nw")

        zoom_out_btn = tk.Label(
            zoom_frame, text="−", bg="#1e293b", fg="#ffffff",
            font=("Arial", 16, "bold"), width=2, cursor="hand2"
        )
        zoom_out_btn.pack(side=tk.LEFT)

        self.zoom_label = tk.Label(
            zoom_frame, text=f"{int(self.onboarding_scale * 100)}%",
            bg="#1e293b", fg="#94a3b8", font=("Arial", 10), width=5
        )
        self.zoom_label.pack(side=tk.LEFT)

        zoom_in_btn = tk.Label(
            zoom_frame, text="+", bg="#1e293b", fg="#ffffff",
            font=("Arial", 16, "bold"), width=2, cursor="hand2"
        )
        zoom_in_btn.pack(side=tk.LEFT)

        zoom_out_btn.bind("<Button-1>", lambda e: self._zoom(-0.1))
        zoom_in_btn.bind("<Button-1>", lambda e: self._zoom(+0.1))

        for btn in (zoom_out_btn, zoom_in_btn):
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#334155"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#1e293b"))

    def _bind_events(self):
        self.anim_canvas.bind(
            "<MouseWheel>",
            lambda e: self._zoom(0.1 if e.delta > 0 else -0.1)
        )
        self.anim_canvas.bind(
            "<Control-MouseWheel>",
            lambda e: self._zoom(0.1 if e.delta > 0 else -0.1)
        )

        try:
            self.winfo_toplevel().bind(
                "<Control-plus>", lambda e: self._zoom(+0.1)
            )
            self.winfo_toplevel().bind(
                "<Control-equal>", lambda e: self._zoom(+0.1)
            )
            self.winfo_toplevel().bind(
                "<Control-minus>", lambda e: self._zoom(-0.1)
            )
        except Exception:
            pass

        def _on_resize(event):
            try:
                self.anim_canvas.coords(
                    self.card_window, event.width // 2, event.height // 2
                )
            except Exception:
                pass

        self.anim_canvas.bind("<Configure>", _on_resize)

    def _zoom(self, delta):
        self.onboarding_scale = max(
            0.6, min(2.0, self.onboarding_scale + delta)
        )
        self._apply_zoom()

    def _apply_zoom(self, initial=False):
        try:
            s = self.onboarding_scale

            if hasattr(self, 'zoom_label'):
                try:
                    self.zoom_label.config(text=f"{int(s * 100)}%")
                except Exception:
                    pass

            for widget, base_size, weight in self.zoomable_widgets:
                try:
                    widget.configure(font=("Arial", max(6, int(base_size * s)), weight))
                except Exception:
                    pass

            for lbl in self.step_labels:
                try:
                    lbl.configure(font=("Arial", max(6, int(9 * s))))
                except Exception:
                    pass

            for c in self.step_canvases:
                try:
                    cs = int(20 * s)
                    c.configure(width=cs, height=cs)
                    c.coords("num_circle", 1, 1, cs - 1, cs - 1)
                    c.coords("num_text", cs / 2, cs / 2)
                    c.itemconfig("num_text", font=("Arial", max(6, int(8 * s)), "bold"))
                except Exception:
                    pass

            if hasattr(self, 'icon_canvas'):
                try:
                    ic = int(56 * s)
                    self.icon_canvas.configure(width=ic, height=ic)
                    self.icon_canvas.coords("bg_circle", 2, 2, ic - 2, ic - 2)
                    self.icon_canvas.coords("icon_text", ic / 2, ic / 2)
                    self.icon_canvas.itemconfig(
                        "icon_text", font=("Arial", max(10, int(24 * s)))
                    )
                except Exception:
                    pass

            if hasattr(self, 'checkbox_widget'):
                try:
                    self.checkbox_widget.configure(
                        font=("Arial", max(6, int(8 * s)))
                    )
                except Exception:
                    pass

            if hasattr(self, 'ok_label'):
                try:
                    self.ok_label.configure(
                        font=("Arial", max(6, int(9 * s)), "bold")
                    )
                except Exception:
                    pass

            if not initial:
                self.settings["onboarding_scale"] = s
                save_settings(self.settings)

        except Exception as e:
            print(f"Zoom error: {e}")

    def _fade_in_schedule(self):
        if not hasattr(self, 'card_frame') or not self.card_frame.winfo_exists():
            return
        total_steps = 15
        if self._fade_in_step > total_steps:
            return

        progress = self._fade_in_step / total_steps
        eased = 1 - (1 - progress) ** 3

        try:
            W = self.anim_canvas.winfo_width()
            H = self.anim_canvas.winfo_height()
            offset_y = int((1 - eased) * 30)
            self.anim_canvas.coords(self.card_window, W // 2, H // 2 + offset_y)
        except Exception:
            pass

        self._fade_in_step += 1
        self.after(20, self._fade_in_schedule)

    def _animate_shapes(self):
        if not self.shapes:
            return
        try:
            if not self.anim_canvas.winfo_exists():
                return

            W = self.anim_canvas.winfo_width()
            H = self.anim_canvas.winfo_height()

            for s in self.shapes:
                if s['type'] == 'circle':
                    s['x'] += s['dx']
                    s['y'] += s['dy']

                    if s['x'] - s['r'] < -200 or s['x'] + s['r'] > W + 200:
                        s['dx'] = -s['dx']
                    if s['y'] - s['r'] < -200 or s['y'] + s['r'] > H + 200:
                        s['dy'] = -s['dy']

                    self.anim_canvas.coords(
                        s['id'],
                        s['x'] - s['r'], s['y'] - s['r'],
                        s['x'] + s['r'], s['y'] + s['r']
                    )

                elif s['type'] == 'square':
                    s['x'] += s['dx']
                    s['y'] += s['dy']
                    s['angle'] += s['angle_speed']

                    if s['x'] < -200 or s['x'] > W + 200:
                        s['dx'] = -s['dx']
                    if s['y'] < -200 or s['y'] > H + 200:
                        s['dy'] = -s['dy']

                    cx = s['x'] + s['size'] / 2
                    cy = s['y'] + s['size'] / 2
                    half = s['size'] / 2
                    rad = math.radians(s['angle'])

                    points = []
                    for angle in [45, 135, 225, 315]:
                        a = math.radians(angle) + rad
                        points.extend([
                            cx + half * 1.414 * math.cos(a),
                            cy + half * 1.414 * math.sin(a)
                        ])

                    self.anim_canvas.coords(s['id'], *points)

        except Exception:
            return

        self.anim_schedule_id = self.after(30, self._animate_shapes)

    def _on_ok(self):
        if self.hide_check.get():
            self.settings["hide_onboarding"] = True
            save_settings(self.settings)
        self.on_complete(self.hide_check.get())

    def destroy(self):
        if self.anim_schedule_id:
            try:
                self.after_cancel(self.anim_schedule_id)
            except Exception:
                pass
            self.anim_schedule_id = None
        super().destroy()


# ═══════════════════════════════════════════════════════════════════
# 9. LOGIN PAGE - شاشة تسجيل الدخول (كارت صغير + خلفية صورة)
# ═══════════════════════════════════════════════════════════════════

class LoginPage(tk.Frame):
    """شاشة تسجيل الدخول — كارت صغير جداً + صورة خلفية ملء الشاشة."""

    def __init__(self, parent, on_connect, on_show_help):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.on_connect = on_connect
        self.on_show_help = on_show_help

        self._logo_photo = None
        self._bg_photo = None
        self._bg_original = None       # الصورة الأصلية لإعادة القياس
        self._resize_after_id = None

        self._build()
        self._load_images_async()

    # ---------- بناء الواجهة ----------
    def _build(self):
        # ─── 1) طبقة الخلفية ───
        self.bg_canvas = tk.Canvas(
            self, bg="#0f172a", highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # ─── 2) طبقة الكارت فوق الصورة ───
        wrapper = tk.Frame(self, bg=Theme.BG_MAIN)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(
            wrapper, bg=Theme.BG_CARD,
            bd=1, relief=tk.SOLID,
            highlightbackground=Theme.BORDER,
            highlightthickness=1
        )
        card.pack()

        # هامش صغير
        content = tk.Frame(card, bg=Theme.BG_CARD)
        content.pack(padx=14, pady=10)

        # الشعار
        self._build_logo(content)

        # العنوان
        tk.Label(
            content, text="MikroTik",
            bg=Theme.BG_CARD, fg=Theme.PRIMARY,
            font=("Arial", 11, "bold")
        ).pack(pady=(4, 0))

        # الحقول
        self._build_fields(content)

        # زر الاتصال + مساعدة
        self._build_buttons(content)

        # مراقبة تغيير الحجم
        self.bind("<Configure>", self._on_resize)

    def _build_logo(self, parent):
        self.logo_frame = tk.Frame(
            parent, bg=Theme.BG_CARD, width=52, height=52
        )
        self.logo_frame.pack(pady=(0, 2))
        self.logo_frame.pack_propagate(False)

        # أيقونة بديلة
        self.logo_fallback = tk.Label(
            self.logo_frame, text="⚙",
            bg="#e8f0fe", fg=Theme.PRIMARY,
            font=("Arial", 20, "bold")
        )
        self.logo_fallback.pack(fill=tk.BOTH, expand=True)

        self.logo_label = tk.Label(self.logo_frame, bg=Theme.BG_CARD)

    def _build_fields(self, parent):
        # IP
        tk.Label(parent, text="IP", bg=Theme.BG_CARD,
                 fg=Theme.TEXT_SUB, font=("Arial", 8)
                 ).pack(anchor="w", pady=(4, 1))
        self.ip_entry = self._make_entry(parent)
        self.ip_entry.insert(0, "192.168.88.1")
        self.ip_entry.pack(fill=tk.X, ipady=3)

        # Username
        tk.Label(parent, text="User", bg=Theme.BG_CARD,
                 fg=Theme.TEXT_SUB, font=("Arial", 8)
                 ).pack(anchor="w", pady=(4, 1))
        self.user_entry = self._make_entry(parent)
        self.user_entry.pack(fill=tk.X, ipady=3)

        # Password
        tk.Label(parent, text="Pass", bg=Theme.BG_CARD,
                 fg=Theme.TEXT_SUB, font=("Arial", 8)
                 ).pack(anchor="w", pady=(4, 1))
        self.pwd_entry = self._make_entry(parent, show="*")
        self.pwd_entry.pack(fill=tk.X, ipady=3)

        # Port + Type
        row = tk.Frame(parent, bg=Theme.BG_CARD)
        row.pack(fill=tk.X, pady=(4, 0))

        # Port
        port_frame = tk.Frame(row, bg=Theme.BG_CARD)
        port_frame.pack(side=tk.LEFT, padx=(0, 4))
        tk.Label(port_frame, text="Port", bg=Theme.BG_CARD,
                 fg=Theme.TEXT_SUB, font=("Arial", 8)
                 ).pack(anchor="w", pady=(0, 1))
        self.port_entry = self._make_entry(
            port_frame, justify=tk.CENTER, width=6
        )
        self.port_entry.insert(0, "8728")
        self.port_entry.pack(ipady=3)

        # Type
        type_frame = tk.Frame(row, bg=Theme.BG_CARD)
        type_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))
        tk.Label(type_frame, text="Type", bg=Theme.BG_CARD,
                 fg=Theme.TEXT_SUB, font=("Arial", 8)
                 ).pack(anchor="w", pady=(0, 1))
        self.api_type = tk.StringVar(value="api")
        radio_frame = tk.Frame(type_frame, bg=Theme.BG_CARD)
        radio_frame.pack(fill=tk.X)
        for text, value in [("API", "api"), ("SSL", "api-ssl")]:
            tk.Radiobutton(
                radio_frame, text=text, variable=self.api_type, value=value,
                bg=Theme.BG_CARD, fg=Theme.TEXT_MAIN, font=("Arial", 8),
                activebackground=Theme.BG_CARD,
                activeforeground=Theme.TEXT_MAIN,
                selectcolor=Theme.BG_CARD, cursor="hand2",
                command=self._update_port,
                bd=0, highlightthickness=0
            ).pack(side=tk.LEFT, padx=1)

    def _make_entry(self, parent, show=None, justify=tk.LEFT, width=18):
        return tk.Entry(
            parent, font=("Arial", 9), bg=Theme.BG_INPUT, fg=Theme.TEXT_MAIN,
            relief=tk.SOLID, bd=1, highlightthickness=1,
            highlightbackground=Theme.BORDER, highlightcolor=Theme.PRIMARY,
            show=show, justify=justify, width=width
        )

    def _build_buttons(self, parent):
        self.login_status = tk.Label(
            parent, text="", bg=Theme.BG_CARD, fg=Theme.ERROR,
            font=("Arial", 7), wraplength=200
        )
        self.login_status.pack(pady=(4, 0))

        self.connect_btn = ModernButton(
            parent, text="CONNECT",
            command=self._on_connect,
            padx=8, pady=3,
            font=("Arial", 9, "bold")
        )
        self.connect_btn.pack(fill=tk.X, pady=(6, 2))

        help_btn = tk.Label(
            parent, text=ar("تعليمات FTP"),
            bg=Theme.BG_CARD, fg=Theme.PRIMARY,
            font=("Arial", 7, "underline"), cursor="hand2"
        )
        help_btn.pack(pady=(2, 0))
        help_btn.bind("<Button-1>", lambda e: self.on_show_help())

    # ---------- تحميل الصور ----------
    def _load_images_async(self):
        if not PIL_AVAILABLE:
            print("Pillow غير مثبت — لا يمكن تحميل الصور")
            return
        threading.Thread(target=self._fetch_images_thread, daemon=True).start()

    def _fetch_images_thread(self):
        # 1) الشعار
        try:
            req = urllib.request.Request(
                LOGO_URL, headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
            logo = Image.open(io.BytesIO(data)).convert("RGBA")
            logo.thumbnail((48, 48), Image.LANCZOS)
            self.after(0, lambda: self._apply_logo(logo))
        except Exception as e:
            print(f"تعذّر تحميل الشعار: {e}")

        # 2) صورة الخلفية
        try:
            req = urllib.request.Request(
                BG_IMAGE_URL, headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            bg = Image.open(io.BytesIO(data)).convert("RGB")
            self._bg_original = bg
            self.after(0, self._render_background)
        except Exception as e:
            print(f"تعذّر تحميل صورة الخلفية: {e}")

    def _render_background(self):
        """يرسم الصورة لتغطي الشاشة (cover mode)."""
        if self._bg_original is None:
            return
        try:
            W = self.winfo_width()
            H = self.winfo_height()
            if W < 10 or H < 10:
                return

            img = self._bg_original.copy()
            iw, ih = img.size

            # القياس مع الحفاظ على النسبة (cover)
            scale = max(W / iw, H / ih)
            new_size = (int(iw * scale), int(ih * scale))
            img = img.resize(new_size, Image.LANCZOS)

            # قص الجزء المركزي
            left = (new_size[0] - W) // 2
            top = (new_size[1] - H) // 2
            img = img.crop((left, top, left + W, top + H))

            self._bg_photo = ImageTk.PhotoImage(img)
            self.bg_canvas.delete("all")
            self.bg_canvas.create_image(0, 0, image=self._bg_photo, anchor="nw")
        except Exception as e:
            print(f"خطأ في رسم الخلفية: {e}")

    def _on_resize(self, event):
        """إعادة رسم الخلفية عند تغيير حجم النافذة."""
        if self._bg_original is None:
            return
        if self._resize_after_id:
            try:
                self.after_cancel(self._resize_after_id)
            except Exception:
                pass
        self._resize_after_id = self.after(120, self._render_background)

    def _apply_logo(self, pil_image):
        try:
            self._logo_photo = ImageTk.PhotoImage(pil_image)
            self.logo_fallback.pack_forget()
            self.logo_label.configure(image=self._logo_photo)
            self.logo_label.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"خطأ في تطبيق الشعار: {e}")

    # ---------- أحداث ----------
    def _update_port(self):
        self.port_entry.delete(0, tk.END)
        self.port_entry.insert(
            0, "8729" if self.api_type.get() == "api-ssl" else "8728"
        )

    def _on_connect(self):
        ip = self.ip_entry.get().strip()
        user = self.user_entry.get().strip()
        pwd = self.pwd_entry.get()

        if not ip or not user or not pwd:
            self.set_status("Please fill all fields", Theme.ERROR)
            return

        if librouteros is None:
            self.set_status("librouteros not installed", Theme.ERROR)
            return

        try:
            port = int(self.port_entry.get())
        except ValueError:
            self.set_status("Port must be a number", Theme.ERROR)
            return

        info = {
            'ip': ip, 'port': port,
            'username': user, 'password': pwd,
            'api_type': self.api_type.get()
        }

        self.set_status("Connecting...", Theme.WARNING)
        self.connect_btn.set_state("disabled")
        self.on_connect(info)

    def set_status(self, text, color=Theme.ERROR):
        self.login_status.config(text=text, fg=color)

    def reset_connect_button(self):
        self.connect_btn.set_state("normal")

# ═══════════════════════════════════════════════════════════════════
# 10. FILES PAGE - شاشة إدارة الملفات (المحدث والمرتب)
# ═══════════════════════════════════════════════════════════════════

FILES_BG_URL = (
    "https://files.manuscdn.com/user_upload_by_module/session_file/"
    "310519663856733618/NvwJUKdYjLviZIHx.jpg"
)

_CARD_FONT_BASE = 9
_CARD_PADX_BASE = 8
_CARD_PADY_BASE = 6

_PANEL_W = 0.85
_PANEL_H = 0.72
_PANEL_X = 0.50
_PANEL_Y = 0.53


class FilesPage(tk.Frame):
    """شاشة إدارة ومستكشف الملفات المحدث والمرتب باحترافية."""

    def __init__(self, parent, connection, on_disconnect):
        super().__init__(parent, bg="#0f172a")
        self.connection = connection
        self.on_disconnect = on_disconnect

        self.current_path = "/"
        self.selected_file_path = None
        self.all_files = []
        self.selected_card = None
        self._loading = False

        self._bg_photo = None
        self._bg_original = None
        self._resize_after_id = None
        self._zoom = 1.0

        self._build()
        self._load_bg_async()
        self.refresh()

    def _build(self):
        # خلفية الشاشة
        self.bg_canvas = tk.Canvas(self, bg="#0f172a", highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # ─── الشريط العلوي (IP وزر الخروج) ───
        topbar = tk.Frame(self, bg="#0b1220", height=48)
        topbar.place(x=0, y=0, relwidth=1)
        topbar.pack_propagate(False)

        # زر الخروج
        logout = tk.Label(
            topbar, text="✕  خروج",
            bg="#dc2626", fg="#ffffff",
            font=("Arial", 10, "bold"),
            cursor="hand2", padx=12, pady=6,
            bd=1, relief=tk.RAISED
        )
        logout.pack(side=tk.RIGHT, padx=12, pady=8)
        logout.bind("<Button-1>", lambda e: self.on_disconnect())
        logout.bind("<Enter>", lambda e: logout.configure(bg="#b91c1c"))
        logout.bind("<Leave>", lambda e: logout.configure(bg="#dc2626"))

        # صندوق عنوان IP الراوتر
        ip_box = tk.Frame(topbar, bg="#14532d", bd=1, relief=tk.SUNKEN)
        ip_box.pack(side=tk.RIGHT, padx=6, pady=8)

        tk.Label(
            ip_box, text="IP:",
            bg="#14532d", fg="#86efac",
            font=("Arial", 9, "bold"),
            padx=4, pady=2
        ).pack(side=tk.LEFT)

        tk.Label(
            ip_box, text=self.connection.info['ip'],
            bg="#14532d", fg="#22c55e",
            font=("Consolas", 10, "bold"),
            padx=6, pady=2
        ).pack(side=tk.LEFT)

        # ─── شريط المسار الحالي ───
        self.path_frame = tk.Frame(self, bg="#0b1220")
        self.path_frame.place(x=0, y=48, relwidth=1, height=24)

        self.path_label = tk.Label(
            self.path_frame, text="/",
            bg="#0b1220", fg="#38bdf8",
            font=("Consolas", 10, "bold"), anchor="w"
        )
        self.path_label.pack(fill=tk.X, padx=12)

        # ─── شريط الأوامر (العمليات) ───
        self.action_bar = tk.Frame(self, bg="#0f172a")

        def mk_btn(parent, text, bg, hover, cmd, font_size=9):
            b = tk.Label(
                parent, text=text,
                bg=bg, fg="#ffffff",
                font=("Arial", font_size, "bold"),
                cursor="hand2", padx=10, pady=4
            )
            b.pack(side=tk.LEFT, padx=3)
            b.bind("<Button-1>", lambda e: cmd())
            b.bind("<Enter>", lambda e, x=b, h=hover: x.configure(bg=h))
            b.bind("<Leave>", lambda e, x=b, c=bg: x.configure(bg=c))
            return b

        mk_btn(self.action_bar, ar("📁 اختيار ملف"), "#2563eb", "#1d4ed8", self.select_file)
        self.upload_btn = mk_btn(self.action_bar, ar("⬆ رفع"), "#475569", "#334155", self.confirm_upload)
        mk_btn(self.action_bar, "الرئيسية", "#334155", "#1e293b", self.go_home)
        mk_btn(self.action_bar, "أعلى", "#334155", "#1e293b", self.go_up)
        mk_btn(self.action_bar, "⟳ تحديث", "#0891b2", "#0e7490", self.refresh)

        # أزرار التكبير والتصغير داخل شريط الأوامر
        zoom_frame = tk.Frame(self.action_bar, bg="#0f172a")
        zoom_frame.pack(side=tk.RIGHT, padx=4)

        zoom_out = tk.Label(zoom_frame, text="−", bg="#1e293b", fg="#ffffff", font=("Arial", 10, "bold"), width=2, cursor="hand2")
        zoom_out.pack(side=tk.LEFT, padx=1)
        self.zoom_lbl = tk.Label(zoom_frame, text=f"{int(self._zoom*100)}%", bg="#0f172a", fg="#94a3b8", font=("Arial", 9), width=4)
        self.zoom_lbl.pack(side=tk.LEFT, padx=2)
        zoom_in = tk.Label(zoom_frame, text="+", bg="#1e293b", fg="#ffffff", font=("Arial", 10, "bold"), width=2, cursor="hand2")
        zoom_in.pack(side=tk.LEFT, padx=1)

        zoom_in.bind("<Button-1>", lambda e: self._do_zoom(+0.15))
        zoom_out.bind("<Button-1>", lambda e: self._do_zoom(-0.15))
        for b in (zoom_in, zoom_out):
            b.bind("<Enter>", lambda e, w=b: w.configure(bg="#475569"))
            b.bind("<Leave>", lambda e, w=b: w.configure(bg="#1e293b"))

        # ─── اللوحة الرئيسية لعرض المستكشف ───
        self.panel = tk.Frame(
            self, bg="#111827",
            highlightthickness=2,
            highlightbackground="#334155"
        )
        self.panel.place(
            relx=_PANEL_X, rely=_PANEL_Y, anchor="center",
            relwidth=_PANEL_W, relheight=_PANEL_H
        )

        self._place_action_bar()

        # Canvas مع شريط تمرير عمودي منظم
        self.files_canvas = tk.Canvas(self.panel, bg="#111827", highlightthickness=0)
        sb = ttk.Scrollbar(self.panel, orient=tk.VERTICAL, command=self.files_canvas.yview)
        self.files_canvas.configure(yscrollcommand=sb.set)

        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.files_frame = tk.Frame(self.files_canvas, bg="#111827")
        self.files_window = self.files_canvas.create_window((0, 0), window=self.files_frame, anchor="nw")

        self.files_frame.bind(
            "<Configure>",
            lambda e: self.files_canvas.configure(scrollregion=self.files_canvas.bbox("all"))
        )
        self.files_canvas.bind(
            "<Configure>",
            lambda e: self.files_canvas.itemconfig(self.files_window, width=e.width)
        )
        self.files_canvas.bind(
            "<MouseWheel>",
            lambda e: self.files_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

        # ─── شريط معلومات الملف المحدد في الأسفل ───
        self.selected_file_label = tk.Label(
            self, text="",
            bg="#0b1220", fg="#facc15",
            font=("Consolas", 10), anchor="w"
        )
        self.selected_file_label.place(x=12, rely=1.0, y=-28, relwidth=0.96)

        self.bind("<Configure>", self._on_resize)

    def _place_action_bar(self):
        self.update_idletasks()
        W = self.winfo_width() or 400
        H = self.winfo_height() or 600

        panel_w = W * _PANEL_W
        panel_x = (W - panel_w) / 2
        panel_h = H * _PANEL_H
        panel_top = H * _PANEL_Y - panel_h / 2

        bar_h = 36
        bar_y = panel_top - bar_h - 8

        self.action_bar.place(
            x=int(panel_x), y=max(74, int(bar_y)),
            width=int(panel_w), height=bar_h
        )

    def _load_bg_async(self):
        if not PIL_AVAILABLE:
            return
        threading.Thread(target=self._fetch_bg_thread, daemon=True).start()

    def _fetch_bg_thread(self):
        try:
            req = urllib.request.Request(FILES_BG_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            bg = Image.open(io.BytesIO(data)).convert("RGB")
            self._bg_original = bg
            self.after(0, self._render_background)
        except Exception as e:
            print(f"BG error: {e}")

    def _render_background(self):
        if self._bg_original is None:
            return
        try:
            W = self.winfo_width()
            H = self.winfo_height()
            if W < 10 or H < 10:
                return
            img = self._bg_original.copy()
            iw, ih = img.size
            scale = max(W / iw, H / ih)
            ns = (int(iw * scale), int(ih * scale))
            img = img.resize(ns, Image.LANCZOS)
            left = (ns[0] - W) // 2
            top = (ns[1] - H) // 2
            img = img.crop((left, top, left + W, top + H))
            self._bg_photo = ImageTk.PhotoImage(img)
            self.bg_canvas.delete("all")
            self.bg_canvas.create_image(0, 0, image=self._bg_photo, anchor="nw")
        except Exception as e:
            print(f"BG render error: {e}")

    def _on_resize(self, event):
        self._place_action_bar()
        if self._bg_original is None:
            return
        if self._resize_after_id:
            try:
                self.after_cancel(self._resize_after_id)
            except Exception:
                pass
        self._resize_after_id = self.after(150, self._render_background)

    def _do_zoom(self, delta):
        self._zoom = max(0.7, min(2.5, self._zoom + delta))
        self.zoom_lbl.config(text=f"{int(self._zoom * 100)}%")
        self._redraw_cards()

    def _redraw_cards(self):
        for w in self.files_frame.winfo_children():
            w.destroy()
        self._render_items(
            self._last_ordered if hasattr(self, '_last_ordered') else []
        )

    def refresh(self):
        if self._loading:
            return
        self._loading = True
        for w in self.files_frame.winfo_children():
            w.destroy()
        self.path_label.config(text=self.current_path)
        threading.Thread(target=self._refresh_thread, daemon=True).str = None
        threading.Thread(target=self._refresh_thread, daemon=True).start()

    def _refresh_thread(self):
        try:
            files = self.connection.list_files()
            self.after(0, lambda: self._update_list(files))
        except Exception as e:
            self.after(0, lambda: self._on_err(str(e)))

    def _on_err(self, msg):
        self._loading = False
        for w in self.files_frame.winfo_children():
            w.destroy()
        tk.Label(
            self.files_frame, text=f"خطأ في الاتصال: {msg}",
            bg="#111827", fg="#ef4444", font=("Arial", 10, "bold")
        ).pack(padx=12, pady=16)

    def _update_list(self, files):
        self._loading = False
        for w in self.files_frame.winfo_children():
            w.destroy()

        self.all_files = files
        self.selected_card = None
        self.path_label.config(text=self.current_path)

        if not files:
            tk.Label(
                self.files_frame, text=ar("المجلد فارغ لا توجد ملفات"),
                bg="#111827", fg="#94a3b8", font=("Arial", 11)
            ).pack(pady=30)
            return

        # ترتيب منظم: المجلدات أولاً ثم الملفات
        folders = sorted(
            [f for f in files if f.get('type', '') == 'directory'],
            key=lambda x: x.get('name', '').lower()
        )
        regular = sorted(
            [f for f in files if f.get('type', '') != 'directory'],
            key=lambda x: x.get('name', '').lower()
        )
        ordered = folders + regular
        self._last_ordered = ordered
        self._render_items(ordered)

    def _render_items(self, ordered):
        """عرض البطاقات في عمودين متناسقين تماماً داخل المستكشف."""
        NUM_COLS = 1
        col_frames = []
        
        container = tk.Frame(self.files_frame, bg="#111827")
        container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        for _ in range(NUM_COLS):
            cf = tk.Frame(container, bg="#111827")
            cf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
            col_frames.append(cf)

        per_col = max(1, (len(ordered) + NUM_COLS - 1) // NUM_COLS)
        for idx, item in enumerate(ordered):
            ci = idx // per_col
            if ci >= NUM_COLS:
                ci = NUM_COLS - 1
            self._add_card(col_frames[ci], item)

    def _add_card(self, parent, file):
        name = file.get('name', '')
        size = file.get('size', '0')
        size_str = format_size(int(size) if size else 0)
        is_folder = (file.get('type', '') == 'directory')
        full_path = name if name.startswith('/') else f"/{name}"

        display_name = os.path.basename(name) or name
        max_chars = max(14, int(24 * self._zoom))
        if len(display_name) > max_chars:
            display_name = display_name[:max_chars - 3] + "..."
        display_name = ar(display_name)

        if is_folder:
            bg_normal = "#1e3a8a"
            bg_hover = "#1d4ed8"
            fg_color = "#eff6ff"
            icon = "📁 "
        else:
            bg_normal = "#1f2937"
            bg_hover = "#374151"
            fg_color = "#f3f4f6"
            icon = "📄 "

        font_size = max(8, int(_CARD_FONT_BASE * self._zoom))
        padx_val = max(6, int(_CARD_PADX_BASE * self._zoom))
        pady_val = max(4, int(_CARD_PADY_BASE * self._zoom))

        card = tk.Label(
            parent,
            text=f"{icon}{display_name}",
            bg=bg_normal, fg=fg_color,
            font=("Arial", font_size),
            anchor="w", cursor="hand2",
            padx=padx_val, pady=pady_val,
            highlightthickness=1,
            highlightbackground="#4b5563"
        )
        card.pack(fill=tk.X, pady=3, padx=2)

        card.file_data = {
            'name': os.path.basename(name),
            'path': full_path,
            'size': size_str,
            'is_folder': is_folder,
            'bg_normal': bg_normal,
            'bg_hover': bg_hover,
        }

        card.bind("<Button-1>", lambda e, c=card: self._select_card(c))
        if is_folder:
            card.bind("<Button-1>", lambda e, c=card: self._open_card(c), add="+")
        card.bind("<Enter>", lambda e, c=card: self._hover_card(c, True))
        card.bind("<Leave>", lambda e, c=card: self._hover_card(c, False))

    def _hover_card(self, card, entering):
        if card is self.selected_card:
            return
        d = card.file_data
        card.configure(bg=d['bg_hover'] if entering else d['bg_normal'])

    def _select_card(self, card):
        if self.selected_card and self.selected_card is not card:
            try:
                self.selected_card.configure(bg=self.selected_card.file_data['bg_normal'])
            except Exception:
                pass
        self.selected_card = card
        card.configure(bg="#2563eb")

        d = card.file_data
        icon = "📁" if d['is_folder'] else "📄"
        self.selected_file_label.config(
            text=f"  {icon} {ar(d['name'])}    [ الحجم: {d['size']} ]"
        )

    def _open_card(self, card):
        data = card.file_data
        if not data['is_folder']:
            return
        folder_path = data['path']
        if not folder_path.startswith('/'):
            if self.current_path == "/":
                self.current_path = "/" + folder_path
            else:
                self.current_path = self.current_path.rstrip('/') + '/' + folder_path
        else:
            self.current_path = folder_path
        self.refresh()

    def go_home(self):
        self.current_path = "/"
        self.refresh()

    def go_up(self):
        if self.current_path != "/":
            self.current_path = os.path.dirname(self.current_path.rstrip('/'))
            if not self.current_path:
                self.current_path = "/"
            self.refresh()

    def _open_file_picker(self):
        import subprocess, tempfile
        try:
            cmd = [
                "am", "start-activity",
                "--user", "0",
                "-a", "android.intent.action.GET_CONTENT",
                "-t", "*/*",
                "--ez", "android.intent.extra.LOCAL_ONLY", "false",
            ]
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                import android
                droid = android.Android()
                result = droid.startActivityForResult({
                    "action": "android.intent.action.GET_CONTENT",
                    "type": "*/*"
                })
                if result and result.result:
                    uri = result.result.get("data", "")
                    return uri
            except ImportError:
                pass
            raise RuntimeError("fallback")
        except Exception:
            try:
                path = filedialog.askopenfilename(title="اختر ملفاً", filetypes=[("All files", "*.*")])
                return path or None
            except Exception as e:
                messagebox.showerror("خطأ", str(e))
                return None

    def select_file(self):
        path = self._open_file_picker()
        if path:
            self.selected_file_path = path
            name = os.path.basename(path)
            size = os.path.getsize(path)
            self.selected_file_label.config(
                text=f"  📄 الملف المحدد: {ar(name)} ({format_size(size)})"
            )
            try:
                self.upload_btn.configure(bg="#16a34a")
            except Exception:
                pass

    def confirm_upload(self):
        if not self.selected_file_path:
            messagebox.showinfo("تنبيه", ar("الرجاء اختيار ملف أولاً للرفع."))
            return

        name = os.path.basename(self.selected_file_path)
        size = os.path.getsize(self.selected_file_path)
        target = f"{self.current_path}/{name}".replace("//", "/")

        if target.startswith("/flash/flash/"):
            target = target.replace("/flash/flash/", "/flash/", 1)

        exists = self._check_exists(target)
        warn = f"\n⚠ {ar('تحذير: الملف موجود مسبقاً وسيتم استبداله!')}" if exists else ""

        msg = (
            f"{ar('ملف:')} {name}\n"
            f"{ar('الحجم:')} {format_size(size)}\n"
            f"{ar('إلى المسار:')} {target}"
            f"{warn}\n\n"
            f"{ar('هل تريد متابعة الرفع؟')}"
        )

        if messagebox.askyesno(ar("تأكيد الرفع"), msg):
            self.selected_file_label.config(text=ar("  ⏳ جاري رفع الملف..."))
            threading.Thread(
                target=self._upload_thread, args=(target,), daemon=True
            ).start()

    def _check_exists(self, path):
        target = path.lstrip('/')
        return any(f.get('name', '') == target for f in self.all_files)

    def _upload_thread(self, target):
        try:
            self.connection.upload_via_ftp(self.selected_file_path, target)
            self.after(0, self._on_success)
        except Exception as e:
            self.after(0, lambda: self._on_fail(str(e)))

    def _on_success(self):
        self.selected_file_path = None
        self.selected_file_label.config(text=ar("  ✓ تم رفع الملف بنجاح!"))
        try:
            self.upload_btn.configure(bg="#475569")
        except Exception:
            pass
        self.refresh()

    def _on_fail(self, msg):
        self.selected_file_label.config(text=ar("  ✕ فشل الرفع"))
        messagebox.showerror("خطأ في الرفع", f"{ar('فشل رفع الملف:')}\n{msg}")

# ═══════════════════════════════════════════════════════════════════
# 11. MAIN APP - التطبيق الرئيسي
# ═══════════════════════════════════════════════════════════════════

class MikroTikApp:
    """المنسّق الرئيسي — يدير التنقّل بين الصفحات."""

    def __init__(self, root):
        self.root = root
        self.root.title("MikroTik Manager")
        maximize_window(self.root)
        self.root.configure(bg=Theme.BG_MAIN)

        self.settings = load_settings()
        self.connection = None
        self.connected = False
        self.current_page = None

        if not self.settings.get("hide_onboarding", False):
            self.show_onboarding()
        else:
            self.show_login()

    def _swap_page(self, page_factory):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = page_factory()
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_onboarding(self):
        self._swap_page(lambda: OnboardingPage(
            self.root,
            on_complete=self._on_onboarding_done,
            settings=self.settings
        ))

    def _on_onboarding_done(self, hidden):
        self.show_login()

    def show_login(self):
        self._swap_page(lambda: LoginPage(
            self.root,
            on_connect=self.do_connect,
            on_show_help=self.show_onboarding
        ))

    def show_files(self):
        self._swap_page(lambda: FilesPage(
            self.root,
            connection=self.connection,
            on_disconnect=self.do_disconnect
        ))

    def do_connect(self, info):
        self.connection = MikroTikConnection(info)
        threading.Thread(target=self._connect_thread, daemon=True).start()

    def _connect_thread(self):
        try:
            self.connection.connect()
            self.connected = True
            self.root.after(0, self.show_files)
        except Exception as e:
            msg = f"Connection failed: {str(e)}"
            self.root.after(0, lambda: self._on_connect_fail(msg))

    def _on_connect_fail(self, msg):
        if isinstance(self.current_page, LoginPage):
            self.current_page.set_status(msg, Theme.ERROR)
            self.current_page.reset_connect_button()

    def do_disconnect(self):
        if not messagebox.askyesno("Disconnect", "Do you want to disconnect?"):
            return
        if self.connection:
            self.connection.close()
        self.connection = None
        self.connected = False
        self.show_login()


# ═══════════════════════════════════════════════════════════════════
# 12. ENTRY POINT - نقطة الدخول
# ═══════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    try:
        root.option_add("*Font", ("Arial", 11))
    except Exception:
        pass
    MikroTikApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()