import typer
from core.graph_controller import run_agent

app = typer.Typer()


@app.command()
def build(prompt: str):

    print("🚀 Starting AI Software Engineer Agent...")

    result = run_agent(prompt)

    print("\n✅ Agent finished\n")
    print(result)


if __name__ == "__main__":
    app()