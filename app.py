import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import sys
import re
import importlib.util
from pathlib import Path
__version__ = "1.0.0"

# Colors & Fonts
BG = "#151515"
CRIMSON = "#93032E"
CRIMSON_H = "#B8043A"
SURFACE = "#1E1E1E"
SURFACE2 = "#242424"
TEXT = "#F0EAE2"
MUTED = "#7A7068"
SUCCESS = "#4CAF72"
ERROR = "#E05A5A"
BAR_BG = "#2A2A2A"

FONT_TITLE = ("Georgia", 22, "bold")
FONT_LABEL = ("Courier New", 10)
FONT_ENTRY = ("Courier New", 11)
FONT_BTN = ("Courier New", 11, "bold")
FONT_STATUS = ("Courier New", 9)
FONT_SMALL = ("Times New Roman", 8)


def _pip_install(*packages):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", *packages]
    )


def ensure_dependencies():
    """Instala yt-dlp e imageio[ffmpeg] se necessario."""
    if importlib.util.find_spec("yt_dlp") is None:
        _pip_install("yt-dlp")
    if importlib.util.find_spec("imageio_ffmpeg") is None:
        _pip_install("imageio[ffmpeg]")


def get_ffmpeg_path() -> str:
    """Retorna o caminho do FFmpeg bundled via imageio-ffmpeg."""
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def get_downloads_dir() -> Path:
    home = Path.home()
    for name in ("Downloads", "download", "Transferencias"):
        d = home / name
        if d.exists():
            return d
    return home


def is_valid_youtube_url(url: str) -> bool:
    patterns = [
        r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w\-]+",
        r"(https?://)?(www\.)?youtube\.com/shorts/[\w\-]+",
        r"(https?://)?(www\.)?youtube\.com/playlist\?list=[\w\-]+",
    ]
    return any(re.search(p, url) for p in patterns)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ytdown")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._center(600, 560)
        self._status_label = None
        self._build_ui()
        self._animate_title(0)
        threading.Thread(target=self._preload_deps, daemon=True).start()

    def _center(self, w, h):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _preload_deps(self):
        try:
            self.after(0, self._set_status,
                       "Verificando dependencias...", MUTED)
            ensure_dependencies()
            self.after(0, self._set_status,
                       "Cole o link e clique em baixar.", MUTED)
        except Exception as e:
            self.after(0, self._set_status,
                       f"Aviso ao verificar deps: {e}", ERROR)

    def _build_ui(self):
        # Header bar
        tk.Frame(self, bg=CRIMSON, height=6).pack(fill="x")

        # Logo
        logo_frame = tk.Frame(self, bg=BG, pady=26)
        logo_frame.pack(fill="x")

        self._title_lbl = tk.Label(
            logo_frame, text="ytdown",
            font=FONT_TITLE, bg=BG, fg=TEXT
        )
        self._title_lbl.pack()

        tk.Label(
            logo_frame,
            text="youtube video downloader",
            font=FONT_SMALL, bg=BG, fg=MUTED
        ).pack(pady=(2, 0))

        # Signature
        tk.Label(
            logo_frame,
            text="By: Satheus",
            font=FONT_SMALL,
            bg=BG,
            fg=CRIMSON
        ).pack(pady=(5, 0))

        # Card
        card = tk.Frame(self, bg=SURFACE, padx=32, pady=26)
        card.pack(fill="both", padx=32, expand=True)

        # URL
        tk.Label(card, text="LINK DO VIDEO", font=FONT_LABEL,
                 bg=SURFACE, fg=MUTED).pack(anchor="w")

        # URL input crimson border
        border = tk.Frame(card, bg=CRIMSON, pady=1, padx=1)
        border.pack(fill="x", pady=(4, 4))
        inner = tk.Frame(border, bg=SURFACE2)
        inner.pack(fill="x")

        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(
            inner, textvariable=self.url_var,
            font=FONT_ENTRY, bg=SURFACE2, fg=TEXT,
            insertbackground=CRIMSON, relief="flat", bd=8
        )
        self.url_entry.pack(fill="x")
        self.url_entry.bind("<Return>", lambda _: self._start_download())

        # Paste & Clear
        btn_row = tk.Frame(card, bg=SURFACE)
        btn_row.pack(fill="x", pady=(2, 12))

        self._small_btn(btn_row, "COLAR LINK", self._paste_url).pack(
            side="left", padx=(0, 8))
        self._small_btn(btn_row, "LIMPAR", lambda: self.url_var.set("")).pack(
            side="left")

        # Quality
        tk.Label(card, text="QUALIDADE", font=FONT_LABEL,
                 bg=SURFACE, fg=MUTED).pack(anchor="w", pady=(4, 4))

        q_frame = tk.Frame(card, bg=SURFACE)
        q_frame.pack(fill="x", pady=(0, 18))

        self.quality_var = tk.StringVar(value="best")
        qualities = [
            ("Melhor Qualidade", "best"),
            ("1080p", "1080"),
            ("720p", "720"),
            ("480p", "480"),
            ("Apenas Audio (MP3)", "audio"),
        ]
        for i, (label, val) in enumerate(qualities):
            tk.Radiobutton(
                q_frame, text=label,
                variable=self.quality_var, value=val,
                bg=SURFACE, fg=TEXT, selectcolor=CRIMSON,
                activebackground=SURFACE, activeforeground=TEXT,
                font=FONT_SMALL, bd=0, highlightthickness=0, cursor="hand2"
            ).grid(row=i // 3, column=i % 3, sticky="w", padx=8, pady=2)

        # Button
        self.dl_btn = self._main_btn(
            card, "BAIXAR VIDEO", self._start_download
        )
        self.dl_btn.pack(fill="x", pady=(2, 14))

        # progress bar
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(
            "Red.Horizontal.TProgressbar",
            troughcolor=BAR_BG, background=CRIMSON,
            bordercolor=BG, lightcolor=CRIMSON, darkcolor=CRIMSON,
            thickness=5
        )
        self.progress = ttk.Progressbar(
            card, style="Red.Horizontal.TProgressbar",
            orient="horizontal", mode="indeterminate"
        )
        self.progress.pack(fill="x", pady=(0, 8))

        # Status
        self.status_var = tk.StringVar(value="Iniciando...")
        self._status_label = tk.Label(
            card, textvariable=self.status_var,
            font=FONT_STATUS, bg=SURFACE, fg=MUTED,
            wraplength=460, justify="left", anchor="w"
        )
        self._status_label.pack(fill="x")

        # Footer
        footer = tk.Frame(self, bg=BG, pady=10)
        footer.pack(fill="x")
        tk.Label(
            footer,
            text=f"downloads  {get_downloads_dir()}",
            font=FONT_SMALL, bg=BG, fg=MUTED
        ).pack()

        # Bottom
        tk.Frame(self, bg=CRIMSON, height=4).pack(fill="x", side="bottom")

    def _main_btn(self, parent, text, cmd):
        btn = tk.Button(
            parent, text=text, command=cmd,
            bg=CRIMSON, fg=TEXT,
            activebackground=CRIMSON_H, activeforeground=TEXT,
            font=FONT_BTN, relief="flat", bd=0,
            cursor="hand2", padx=12, pady=10
        )
        btn.bind("<Enter>", lambda _: btn.config(bg=CRIMSON_H))
        btn.bind("<Leave>", lambda _: btn.config(bg=CRIMSON))
        return btn

    def _small_btn(self, parent, text, cmd):
        btn = tk.Button(
            parent, text=text, command=cmd,
            bg=SURFACE2, fg=MUTED,
            activebackground=SURFACE, activeforeground=TEXT,
            font=FONT_SMALL, relief="flat", bd=0,
            cursor="hand2", padx=8, pady=4
        )
        btn.bind("<Enter>", lambda _: btn.config(fg=TEXT))
        btn.bind("<Leave>", lambda _: btn.config(fg=MUTED))
        return btn

    def _paste_url(self):
        try:
            self.url_var.set(self.clipboard_get().strip())
        except Exception:
            pass

    def _animate_title(self, frame):
        colors = [TEXT, CRIMSON, CRIMSON, CRIMSON, TEXT, TEXT]
        self._title_lbl.config(fg=colors[frame % len(colors)])
        self.after(700, lambda: self._animate_title(frame + 1))

    def _set_status(self, msg: str, color=MUTED):
        self.status_var.set(msg)
        if self._status_label:
            self._status_label.config(fg=color)

    def _start_download(self):
        url = self.url_var.get().strip()
        if not url:
            self._set_status("Cole um link antes de baixar.", ERROR)
            return
        if not is_valid_youtube_url(url):
            self._set_status("Link invalido. Use um URL do YouTube.", ERROR)
            return

        self.dl_btn.config(state="disabled", text="  BAIXANDO...")
        self.progress.start(12)
        self._set_status("Preparando download...", MUTED)

        threading.Thread(
            target=self._download_worker, args=(url,), daemon=True
        ).start()

    def _download_worker(self, url: str):
        try:
            # FFmpeg
            ensure_dependencies()
            ffmpeg_path = get_ffmpeg_path()

            import yt_dlp

            dl_dir = get_downloads_dir()
            quality = self.quality_var.get()

            if quality == "audio":
                fmt = "bestaudio/best"
                post = [{"key": "FFmpegExtractAudio",
                         "preferredcodec": "mp3", "preferredquality": "192"}]
                ydl_opts = {
                    "format": fmt,
                    "outtmpl": str(dl_dir / "%(title)s.%(ext)s"),
                    "postprocessors": post,
                    "progress_hooks": [self._progress_hook],
                    "ffmpeg_location": ffmpeg_path,
                    "quiet": True,
                    "no_warnings": True,
                }
            else:
                # Para vídeo: usar formato que já inclui áudio ou forçar merge
                if quality == "best":
                    # best* tenta formatos pré-mesclados primeiro, depois separados
                    fmt = "best*[vcodec!=none][acodec!=none]/bestvideo*+bestaudio/best"
                else:
                    # Para qualidade específica, tentar formato mesclado primeiro
                    fmt = (f"best[height<={quality}][vcodec!=none][acodec!=none]/"
                           f"bestvideo[height<={quality}]+bestaudio/best")

                ydl_opts = {
                    "format": fmt,
                    "outtmpl": str(dl_dir / "%(title)s.%(ext)s"),
                    "postprocessors": [],
                    "progress_hooks": [self._progress_hook],
                    "ffmpeg_location": ffmpeg_path,
                    "merge_output_format": "mp4",
                    "quiet": True,
                    "no_warnings": True,
                    # Garantir que FFmpeg seja usado para merge quando necessário
                    "postprocessor_args": {
                        "merger+ffmpeg": ["-c", "copy", "-movflags", "+faststart"],
                    },
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "video")

            self.after(0, self._on_success, title)

        except Exception as e:
            self.after(0, self._on_error, str(e))

    def _progress_hook(self, d):
        if d["status"] == "downloading":
            pct = d.get("_percent_str", "").strip()
            speed = d.get("_speed_str", "").strip()
            eta = d.get("_eta_str", "").strip()
            self.after(0, self._set_status,
                       f"{pct}  |  {speed}  |  ETA {eta}", MUTED)

    def _on_success(self, title: str):
        self._reset_btn()
        self._set_status(f'Download concluido: {title}', SUCCESS)
        self.url_var.set("")

    def _on_error(self, err: str):
        self._reset_btn()
        short = err[:140] + "..." if len(err) > 140 else err
        self._set_status(f"Erro: {short}", ERROR)

    def _reset_btn(self):
        self.progress.stop()
        self.dl_btn.config(state="normal", text="BAIXAR VIDEO")


if __name__ == "__main__":
    app = App()
    app.mainloop()
