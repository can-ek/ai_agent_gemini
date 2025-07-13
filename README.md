### Install pip
`sudo apt install python3-pip`

### Install UV with pip
`pip install uv`

### Create project with UV

```
uv init your-project-name
cd your-project-name
```

### Create Virtual environment

```
uv venv
```

### Activate Virtual environment

```
source .venv/bin/activate
```

### Add dependencies with UV

```
uv add google-genai==1.12.1
uv add python-dotenv==1.1.0
```

### Run project

```
uv run main.py
```
