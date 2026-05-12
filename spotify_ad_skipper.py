#!/usr/bin/env python3
"""
Spotify Ad Skipper for macOS by nedathar
-----------------------------
Detects ads via Spotify's AppleScript API (track ID starts with 'spotify:ad:'),
instantly quits Spotify, reopens, and unpauses music

Usage:
  python3 spotify_ad_skipper.py

Stop with Ctrl+C.
"""

import subprocess
import time
import sys

POLL_INTERVAL = 0.8       # Seconds between checks while music is playing
AD_POLL_INTERVAL = 0.3    # Faster polling once we're in an ad cycle
SPOTIFY_LAUNCH_TIMEOUT = 8  # Max seconds to wait for Spotify to launch



def run_as(script: str) -> tuple[str, int]:
    r = subprocess.run(["osascript", "-e", script],
                       capture_output=True, text=True)
    return r.stdout.strip(), r.returncode


def is_spotify_running() -> bool:
    out, _ = run_as('application "Spotify" is running')
    return out == "true"


def spotify_state() -> str:
    out, code = run_as('tell application "Spotify" to return player state as string')
    return out if code == 0 else ""


def current_track_id() -> str | None:
    out, code = run_as('tell application "Spotify" to return id of current track')
    return out if code == 0 else None


def is_ad_playing() -> bool:
    track_id = current_track_id()
    return track_id is not None and track_id.startswith("spotify:ad:")



def quit_spotify() -> None:
    subprocess.run(["pkill", "-x", "Spotify"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.25)


def launch_spotify() -> bool:
    subprocess.Popen(["open", "-a", "Spotify"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    deadline = time.monotonic() + SPOTIFY_LAUNCH_TIMEOUT
    while time.monotonic() < deadline:
        time.sleep(0.2)
        if is_spotify_running():
            time.sleep(0.4)
            return True
    return False


def press_play() -> None:
    run_as('tell application "Spotify" to play')




def main() -> None:
    print("Spotify Ad Skipper 🎵 — running (Ctrl+C to stop)\n")

    skipped = 0
    handling_ad = False  # Debounce flag — don't re-trigger mid-restart

    while True:
        try:
            if not is_spotify_running():
                handling_ad = False
                time.sleep(1)
                continue

            if is_ad_playing():
                if not handling_ad:
                    handling_ad = True
                    skipped += 1
                    print(f" Ad detected — skipping... (#{skipped})")

                    t0 = time.monotonic()
                    quit_spotify()
                    launched = launch_spotify()
                    elapsed = time.monotonic() - t0

                    if launched:
                        press_play()
                        print(f" Resumed in {elapsed:.2f}s\n")
                    else:
                        print(" Spotify took too long to relaunch — retrying...")
                        handling_ad = False  # Allow retry

                time.sleep(AD_POLL_INTERVAL)
                continue
            handling_ad = False
            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print(f"\nStopped. Ads skipped this session: {skipped}")
            sys.exit(0)
        except Exception as e:
            time.sleep(1)


if __name__ == "__main__":
    main()
