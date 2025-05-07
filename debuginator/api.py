import requests

def get_available_models(api_key, console):
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        model_ids = []
        for model in data["data"]:
            model_ids.append(model["id"])
        return model_ids
    except Exception as e:
        console.print(f"[red]Error fetching models: {str(e)}[/red]")
        return []
