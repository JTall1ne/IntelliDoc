"""
IntelliDoc Command-Line Interface

A powerful CLI for generating documentation using multiple AI models working in collaboration.
"""

import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint
import asyncio

from intellidoc.core import (
    load_config,
    create_default_config,
    validate_config,
    MultiModelOrchestrator,
    DocumentationTask,
    CodeParser,
    detect_language,
    CollaborationStrategy
)

app = typer.Typer(
    name="intellidoc",
    help="IntelliDoc - Multi-Model AI Documentation Generator",
    add_completion=False
)
console = Console()


@app.command()
def init(
    path: str = typer.Option(".", help="Directory to initialize IntelliDoc in")
):
    """Initialize IntelliDoc in a directory."""
    config_path = Path(path) / ".intellidoc.yml"
    
    if config_path.exists():
        console.print(f"[yellow]Configuration already exists at {config_path}[/yellow]")
        overwrite = typer.confirm("Overwrite?")
        if not overwrite:
            raise typer.Abort()
    
    create_default_config(str(config_path))
    console.print(f"[green]✓[/green] Initialized IntelliDoc at {config_path}")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("1. Set your API keys in environment variables:")
    console.print("   export OPENAI_API_KEY=your_key_here")
    console.print("   export ANTHROPIC_API_KEY=your_key_here")
    console.print("2. Edit .intellidoc.yml to customize settings")
    console.print("3. Run: intellidoc generate <file>")


@app.command()
def generate(
    path: str = typer.Argument(..., help="File or directory to generate documentation for"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    strategy: Optional[str] = typer.Option(None, "--strategy", "-s", help="Collaboration strategy (consensus, specialization, review, voting)"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """Generate documentation for a file or directory."""
    asyncio.run(_generate_async(path, output, strategy, config, verbose))


async def _generate_async(path: str, output: Optional[str], strategy: Optional[str], config_path: Optional[str], verbose: bool):
    """Async implementation of generate command."""
    
    # Load configuration
    config = load_config(config_path)
    config.verbose = verbose or config.verbose
    
    # Override strategy if provided
    if strategy:
        try:
            config.strategy = CollaborationStrategy(strategy)
        except ValueError:
            console.print(f"[red]Invalid strategy: {strategy}[/red]")
            console.print("Valid strategies: consensus, specialization, review, voting")
            raise typer.Exit(1)
    
    # Validate configuration
    if not validate_config(config):
        raise typer.Exit(1)
    
    # Check if path exists
    file_path = Path(path)
    if not file_path.exists():
        console.print(f"[red]Error: {path} not found[/red]")
        raise typer.Exit(1)
    
    # Initialize orchestrator
    console.print(f"[cyan]Initializing {len(config.models)} AI model(s)...[/cyan]")
    orchestrator = MultiModelOrchestrator(config.models, config.strategy)
    
    if file_path.is_file():
        await _generate_for_file(file_path, orchestrator, output, config)
    else:
        await _generate_for_directory(file_path, orchestrator, config)


async def _generate_for_file(file_path: Path, orchestrator: MultiModelOrchestrator, output: Optional[str], config):
    """Generate documentation for a single file."""
    
    # Detect language
    language = detect_language(file_path.name)
    if not language:
        console.print(f"[yellow]Warning: Could not detect language for {file_path.name}[/yellow]")
        console.print("Generating generic documentation...")
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Parse code if language is detected
    elements = []
    if language:
        parser = CodeParser(language)
        elements = parser.parse_file(code)
        
        if config.verbose:
            console.print(f"[dim]Found {len(elements)} code element(s)[/dim]")
    
    # Generate documentation
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task_id = progress.add_task("Generating documentation with AI models...", total=None)
        
        if elements:
            # Generate documentation for each element
            all_docs = []
            for element in elements:
                doc_task = DocumentationTask(
                    code=element.code,
                    language=language.value if language else "unknown",
                    context=f"This is a {element.type} named '{element.name}'",
                    metadata={"element": element}
                )
                result = await orchestrator.generate_documentation(doc_task)
                all_docs.append({
                    "element": element,
                    "documentation": result.final_documentation,
                    "confidence": result.confidence_score
                })
        else:
            # Generate documentation for entire file
            doc_task = DocumentationTask(
                code=code,
                language=language.value if language else "unknown",
                context=f"This is source code from {file_path.name}"
            )
            result = await orchestrator.generate_documentation(doc_task)
            all_docs = [{"documentation": result.final_documentation, "confidence": result.confidence_score}]
        
        progress.remove_task(task_id)
    
    # Format output
    output_content = _format_documentation(file_path, all_docs, config)
    
    # Write output
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        console.print(f"[green]✓[/green] Documentation written to {output_path}")
    else:
        console.print("\n" + "="*80 + "\n")
        console.print(output_content)
        console.print("\n" + "="*80 + "\n")
    
    # Show summary
    _show_generation_summary(all_docs)


async def _generate_for_directory(dir_path: Path, orchestrator: MultiModelOrchestrator, config):
    """Generate documentation for all files in a directory."""
    console.print(f"[yellow]Directory processing not yet fully implemented[/yellow]")
    console.print(f"Scanning {dir_path}...")
    
    # Find all code files
    code_files = []
    for ext in ['.py', '.js', '.ts', '.java', '.cpp', '.go']:
        code_files.extend(dir_path.rglob(f"*{ext}"))
    
    console.print(f"Found {len(code_files)} code file(s)")
    
    # Process first few files as demo
    for file in code_files[:3]:
        console.print(f"\n[cyan]Processing {file.name}...[/cyan]")
        await _generate_for_file(file, orchestrator, None, config)


def _format_documentation(file_path: Path, docs: list, config) -> str:
    """Format documentation output."""
    lines = []
    
    lines.append(f"# Documentation for {file_path.name}\n")
    lines.append(f"*Generated by IntelliDoc using {config.strategy.value} strategy*\n")
    lines.append("---\n\n")
    
    for doc_info in docs:
        if "element" in doc_info:
            element = doc_info["element"]
            lines.append(f"## {element.type.title()}: `{element.name}`\n")
        
        lines.append(doc_info["documentation"])
        lines.append("\n\n")
    
    return "".join(lines)


def _show_generation_summary(docs: list):
    """Show summary of generated documentation."""
    table = Table(title="Generation Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    total_elements = len(docs)
    avg_confidence = sum(d["confidence"] for d in docs) / total_elements if total_elements > 0 else 0
    
    table.add_row("Elements Documented", str(total_elements))
    table.add_row("Avg. Confidence", f"{avg_confidence:.2%}")
    
    console.print("\n")
    console.print(table)


@app.command()
def info():
    """Show information about IntelliDoc and available models."""
    from intellidoc import __version__
    
    console.print(f"[bold]IntelliDoc v{__version__}[/bold]")
    console.print("Multi-Model AI Documentation Generator\n")
    
    # Load config to show available models
    config = load_config()
    
    if config.models:
        table = Table(title="Configured AI Models")
        table.add_column("Provider", style="cyan")
        table.add_column("Model", style="green")
        table.add_column("Status", style="yellow")
        
        for model_config in config.models:
            status = "✓ Available" if model_config.api_key else "✗ No API Key"
            table.add_row(
                model_config.provider.value,
                model_config.model_name,
                status
            )
        
        console.print(table)
    else:
        console.print("[yellow]No models configured. Run 'intellidoc init' to get started.[/yellow]")
    
    console.print(f"\n[dim]Strategy: {config.strategy.value}[/dim]")


@app.command()
def version():
    """Show IntelliDoc version."""
    from intellidoc import __version__
    console.print(f"IntelliDoc v{__version__}")


if __name__ == "__main__":
    app()
