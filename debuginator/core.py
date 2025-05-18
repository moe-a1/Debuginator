import json
import subprocess
from pathlib import Path
from rich.panel import Panel
from rich.markdown import Markdown
import questionary
from .api import debug_error

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config" / "config.json"

def load_config():
    if not CONFIG_FILE.exists():
        return {"api_key": "", "model": ""}
    
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=2)


def get_last_terminal_output():
    history_process = subprocess.run('doskey /history', shell=True, capture_output=True, text=True)

    if not history_process.stdout.strip():
        history_process = subprocess.run('Get-History | Select-Object -Property CommandLine | ForEach-Object { $_.CommandLine }', shell=True, capture_output=True, text=True)
    
    history = history_process.stdout.strip().split('\n')

    if not history:
        return None, None
    
    last_cmd = None
    for cmd in reversed(history):
        cmd = cmd.strip()
        if not cmd.startswith("debuginator"):
            last_cmd = cmd
            break
    
    if not last_cmd:
        return None, None
    
    cmd_process = subprocess.run(last_cmd, shell=True, capture_output=True, text=True)
    output = cmd_process.stderr.strip() if cmd_process.stderr else cmd_process.stdout.strip()
    
    return output, last_cmd


def run_user_command(command):
    cmd_process = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = cmd_process.stderr.strip() if cmd_process.stderr else cmd_process.stdout.strip()
    return output, command


def format_and_print_response(console, text):
    md = Markdown(text)

    panel = Panel(md, border_style="green", expand=False, padding=(1, 2))
    console.print(panel)


def process_last_command(console, config):    
    output, last_cmd = get_last_terminal_output()
    
    if not output:
        console.print("[yellow]No output detected from the last command.[/yellow]")
        console.print("[blue]Please enter the command that caused the error you want to debug:[/blue]")
        
        user_command = questionary.text("Command:").ask()
        if not user_command:
            console.print("[red]No command provided. Exiting.[/red]")
            return None
            
        output, last_cmd = run_user_command(user_command)
        
        if not output:
            console.print("[yellow]No output detected from the provided command.[/yellow]")
            return None
    
    analysis = debug_error(output, config["api_key"], config["model"], console)
    
    if analysis:
        console.print("\n[bold green]AI Analysis:[/bold green]")
        format_and_print_response(console, analysis)
    
    return analysis
