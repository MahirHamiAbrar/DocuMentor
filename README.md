# DocuMentor
A RAG implementation to chat with documents!

## Running DocuMentor

### Installation
#### Step #1: Clone the repo
```bash
git clone https://github.com/MahirHamiAbrar/DocuMentor.git
```

#### Step #2: Install `uv`
```bash
# On Linux & macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```
For other installation methods check [uv's website.](https://docs.astral.sh/uv/getting-started/installation/)

#### Step #3: Prepare the dev environment
```bash
cd DocuMentor
uv sync
```

### Running
To run DocuMentor, first cd into the project directory (eg: `cd DocuMentor`) and run:
```bash
uv run documentor
```