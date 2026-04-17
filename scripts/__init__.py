"""VA-Agent package.

Bootstrap: stellt sicher, dass WeasyPrint unter Anaconda-Python auf macOS die
Homebrew-gelieferten Pango/Cairo/Gdk-Pixbuf Libraries findet. Muss laufen bevor
WeasyPrint importiert wird, weil dyld DYLD_LIBRARY_PATH beim dlopen konsultiert.
"""
from __future__ import annotations
import os
import sys

if sys.platform == "darwin":
    _hb = "/opt/homebrew/lib"
    _existing = os.environ.get("DYLD_LIBRARY_PATH", "")
    if _hb not in _existing.split(":"):
        os.environ["DYLD_LIBRARY_PATH"] = _hb + (":" + _existing if _existing else "")
