import sys
import typer
import questionary
from rich.console import Console
from .core import load_config, save_config, process_last_command
from .api import get_available_models

console = Console()
app = typer.Typer()

@app.command()
def config():
    current_config = load_config()
    
    api_key = questionary.text("OpenRouter API Key:", default=current_config.get("api_key", "")).ask()
    
    if not api_key:
        console.print("[red]API key is required.[/red]")
        return
    
    console.print("[yellow]Fetching available models...[/yellow]")
    models = get_available_models(api_key, console)
    
    if models:
        model = questionary.select(
            "Select an LLM model:",
            choices=models,
            default=current_config.get("model") if current_config.get("model") in models else models[0]
        ).ask()
        
        new_config = {"api_key": api_key, "model": model}
        save_config(new_config)
        console.print("[green]Configuration saved successfully![/green]")
    else:
        console.print("[red]Failed to fetch models. Please check your API key and internet connection.[/red]")


@app.command()
def selected_model():
    current_config = load_config()
    
    if not current_config.get("api_key"):
        console.print("[red]API key not configured. Run 'debuginator config' first.[/red]")
        return
        
    model = current_config.get("model")
    if model:
        console.print(f"Currently selected model: [bold]{model}[/bold]")
    else:
        console.print("[yellow]No model currently selected. Run 'debuginator config' or 'debuginator change-model' to select a model.[/yellow]")


@app.command()
def change_model():
    current_config = load_config()
    
    if not current_config.get("api_key"):
        console.print("[red]API key not configured. Run 'debuginator config' first.[/red]")
        return
    
    console.print("[yellow]Fetching available models...[/yellow]")
    models = get_available_models(current_config["api_key"], console)
    
    if models:
        model = questionary.select(
            "Select an LLM model:",
            choices=models,
            default=current_config.get("model") if current_config.get("model") in models else models[0]
        ).ask()
        
        if model is not None:
            current_config["model"] = model
            save_config(current_config)
            console.print("[green]Model updated successfully![/green]")
        else:
            console.print("[yellow]Model selection cancelled. Keeping existing model.[/yellow]")
    else:
        console.print("[red]Failed to fetch models. Please check your API key and internet connection.[/red]")


@app.command()
def debug():
    config = load_config()
    
    if not config.get("api_key"):
        console.print("[red]API key not configured. Run 'debuginator config' first.[/red]")
        return
    
    process_last_command(console, config)


def main():
    if len(sys.argv) == 1:
        debug()
        return
        
    app()