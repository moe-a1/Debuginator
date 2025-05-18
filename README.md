# Debuginator

An AI-powered command line tool for analyzing and debugging error messages using Large Language Models (LLMs).

## Overview

Debuginator is a simple yet powerful CLI tool that helps developers debug errors by leveraging the capabilities of Large Language Models through the OpenRouter API. When you encounter an error in your terminal, just type `debuginator` to get an AI-powered analysis and solution.

## Features

- **Automatic Error Detection**: Automatically captures the output of your last terminal command
- **AI-Powered Analysis**: Uses OpenRouter's LLM models to analyze and provide solutions for errors
- **Configurable**: Choose from multiple LLM models available through OpenRouter
- **Easy to Use**: Just run `debuginator` after encountering an error

## Installation

```bash
pip install -e .
```

## Setup

Before using Debuginator, you need to configure it with your OpenRouter API key:

```bash
debuginator config
```

This command will prompt you to enter your OpenRouter API key and select an LLM model to use.

## Usage

When you encounter an error in your terminal, simply run:

```bash
debuginator
```

Debuginator will automatically:
1. Detect the last command you ran
2. Capture its output
3. Send it to the AI for analysis

If Debuginator can't detect the last command or you want to analyze output from a specific command, it will prompt you to enter the command manually.

### Managing Models

To check which model is currently selected:

```bash
debuginator selected-model
```

To change the LLM model:

```bash
debuginator change-model
```

## Commands

- `debuginator` - Analyze the output of the last command
- `debuginator config` - Configure your OpenRouter API key and select a model
- `debuginator selected-model` - Display the currently selected model
- `debuginator change-model` - Change the LLM model used for analysis

## Requirements

- Python 3.6+
- OpenRouter API key

## Dependencies

- typer - For creating the command line interface
- requests - For making API calls to OpenRouter
- rich - For beautiful terminal formatting
- questionary - For interactive prompts
