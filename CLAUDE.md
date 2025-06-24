# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the `prae` project (v0.1.0), a Python-based AI agent for personalized apartment searching in NYC. The project uses Python 3.12 and focuses on building a multi-turn interaction agent with tool use capabilities.

## Development Commands

### Environment Setup
```bash
# Install dependencies using uv package manager
uv sync

# Or install in editable mode
uv pip install -e .
```

### Running Code
```bash
# Run the main entry point
python hello.py

# Start Jupyter for notebook development
jupyter notebook w1/broker.ipynb
```

## Architecture

### Core Structure
- **Utilities**: `helpers.py` - Reserved for shared helper functions
- **Agent Development**: `w1/broker.ipynb` - Jupyter notebook containing the apartment broker agent implementation

### Key Components to Implement
1. **Apartment Search Tools**: Functions to query apartment listings APIs
2. **Listing Parser**: Extract relevant details from apartment listings
3. **User Profile Analyzer**: Understand renter preferences from text/images
4. **Scheduling System**: Proactive viewing appointment scheduler
5. **LLM Judge**: Evaluate if a renter wants to schedule a viewing

### Dependencies
- **openai**: LLM API access for agent intelligence
- **jupyter**: Interactive development environment
- **uv**: Modern Python package manager (replaces pip/poetry)

## Project Goals

Build an apartment broker agent that:
- Searches beyond basic filters to find personalized matches
- Understands renters through multimodal inputs (text and images)
- Proactively suggests and schedules apartment viewings
- Uses an LLM judge to determine user intent

## Important Notes

- Python 3.12 is required (specified in `.python-version`)
- The project uses `uv` for dependency management - use `uv` commands instead of pip
- Primary development happens in the Jupyter notebook at `w1/broker.ipynb`
- The assignment guidelines are in `w1/guidelines.md`