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


def debug_error(error_message, api_key, model, console):
    if not error_message:
        console.print("[red]No error message provided.[/red]")
        return None
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    prompt = f"""
                You are a programming expert and debugger. 
                Please analyze the following error message:
                
                {error_message}
                
                Provide your response in markdown format with the following sections:
                
                ## Error Analysis
                A clear explanation of what caused this error
                
                ## Solution Steps
                Step-by-step solutions to fix it
                
                ## Additional Context
                Any additional context or information that might be helpful
            """
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert programming assistant. Format your response in markdown."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        console.print("[yellow]Analyzing error with AI...[/yellow]")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            analysis = result["choices"][0]["message"]["content"]
            return analysis
        else:
            console.print("[red]No analysis returned from the model.[/red]")
            return None
    except Exception as e:
        console.print(f"[red]Error during analysis: {str(e)}[/red]")
        return None
