# baseball-mcp: An MLB Stats API Wrapper for MCP

This project provides an MCP (Model Context Protocol) that acts as a wrapper for the MLB Stats API.  It allows you to easily access and process various MLB data points, including schedules, game results, and team information.  This server is designed for efficient data retrieval and processing within an MCP framework.

## Demo Videos

Here are a couple of demo videos showcasing the capabilities of `mcp_mlb_statsapi`:
* **Demo 1:  MCP MLB Stats API - Quick Overview**
- [![Quick Overview](https://img.youtube.com/vi/cnqbcB8064k/0.jpg)](https://youtu.be/cnqbcB8064k "demo 1")
* **Demo 2:  MCP MLB Stats API - 輸入中文也可以**
- [![輸入中文也可以](https://img.youtube.com/vi/XhuyfIWKLjY/0.jpg)](https://youtu.be/XhuyfIWKLjY "demo 2")


## Features

* **Game Schedules:** Retrieve MLB game schedules for specified date ranges, optionally filtering by team.
* **Game Results:** Fetch daily game results, including scores, winning/losing teams, and winning pitcher.
* **Team Results:** Get detailed results for a specific team's most recent game, including scoring plays and highlights.
* **Player Lookup:** Look up player IDs using last name, first name, or a combination of both.  Supports fuzzy matching.

## Installation

#### Prerequisites
- Python 3.10 or newer
- uv package manager: 

**If you're on Mac, please install uv as**
```bash
brew install uv
```
**On Windows**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex" 
```
Otherwise installation instructions are on their website: [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

#### Install via PyPI
The `mcp_mlb_statsapi` package is available on PyPI and can be installed using `pip`:

```bash
pip install mcp_mlb_statsapi
```

#### Install via Github
or you can clone this repo, run it with soruce code.
```bash
uv venv
source .venv\Scripts\activate
uv pip install -r requirements.txt
```

#### Claude for Desktop Integration
Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json to include the following:

```json
    {
      "mcpServers": {
        "mcp_mlb_statsapi": {
           "command": "{YOUR_PYTHON_EXECUTABLE_PATH}/python",
            "args": ["-m",
            "mcp_mlb_statsapi"]
          }
        }
    }
```

If you install it via source code
```json
{
  "mcpServers": {
    "mcp_mlb_statsapi": {
        "command": "{YOUR_UV_EXECUTABLE_PATH}/uv",
        "args": [
            "--directory",
            "{YOUR_PROJECT_PATH}/src/mcp_mlb_statsapi",
            "run",
            "mcp_mlb_statsapi"
        ]
    }
  }
}
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.

## References

This project utilizes the following external libraries and resources:

* **MLB-StatsAPI:**  [https://github.com/toddrob99/MLB-StatsAPI](https://github.com/toddrob99/MLB-StatsAPI) -  A Python library providing access to the MLB Stats API.  This project relies heavily on `mlb-statsapi` for data retrieval.

[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/mpizza-mcp-mlb-statsapi-badge.png)](https://mseep.ai/app/mpizza-mcp-mlb-statsapi)
[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/45b7cf1b-10ee-4ba0-8bf5-90a464b0f860)
