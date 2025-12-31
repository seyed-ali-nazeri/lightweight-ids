WATCH_PATH = "/var/log"

DANGER_EXT = (".sh",".py",".exe",".dll",".so",".bat",".ps1",".bin")

WHITELIST_PORTS = {22, 80, 443}
WHITELIST_PROCS = {"sshd", "cron", "systemd", "rsyslog"}

SIZE_CHANGE_THRESHOLD = 5_000_000
CPU_SPIKE = 60
SLEEP_TIME = 2

ENABLE_IPS = True
REPORT_PATH = "/var/log/ids_report.pdf"

