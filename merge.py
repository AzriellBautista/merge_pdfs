from PyPDF2 import PdfMerger
import click

from glob import glob
import os

def merge_pdfs(files: list[str], output: str) -> None:
    """Merges a list of PDF files into one PDF file."""

    merger = PdfMerger()
    for file in files:
        try:
            merger.append(file)
            click.echo(click.style(f"Appended `{file}`", fg="green"))
        except FileNotFoundError:
            click.echo(click.style(f"File `{file}` not found. Skipping", fg="red"))
            continue
        except Exception as e:
            click.echo(click.style(f"Error appending `{file}: {e}`. Skipping", fg="red"))
            continue
            
    if merger.pages:
        click.style(f"Merging PDFs...")
        merger.write(output)
        merger.close()
        click.echo(click.style(f"Merged PDFs to `{output}`.", fg="blue"))
    else:
        click.echo(click.style("No valid PDFs found to merge.", fg="red"))

def sort_pdfs(files: list[str], sort_option: str) -> list[str]:
    """Sorts a list of PDF files based on a given option."""

    sort_key = None
    reverse_order = False

    if sort_option:
        if sort_option.startswith("^"):
            reverse_order = True
            sort_option = sort_option[1:]

        if sort_option == 'name':
            sort_key = lambda name: name.lower()
        elif sort_option == 'date':
            sort_key = os.path.getmtime
        elif sort_option == 'size':
            sort_key = os.path.getsize

        if sort_key:
            click.echo(click.style(f"Sorting PDFs by {sort_option} in " \
                f"{'descending' if reverse_order else 'ascending'} order.", 
                fg="yellow"))
            files.sort(key=sort_key, reverse=reverse_order)

    return files

@click.command()
@click.argument(
    "files",
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--dir", "-d", 
    help="Directory containing PDF files to merge. " \
         "Defaults to current working directory.",
    default=os.getcwd(), 
    type=click.Path(exists=True, dir_okay=True), 
)
@click.option(
    "--pattern", "-p",
    help="Filename pattern to match. Wildcards (*, ?, [ranges]) are accepted.",
    default="*.pdf",
    show_default=True,
)
@click.option(
    "--from-list", "-L",
    help="File containing a list of PDF files to merge.",
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--sort", "-s",
    help="Sort PDFs by a given option.",
    type=click.Choice([
        'name', 'date', 'size',
        '^name', '^date', '^size'
    ], 
    case_sensitive=False),
)
@click.option(
    "--output", "-o", 
    help="Output filename.",
    default="merged.pdf", 
    show_default=True, 
)
@click.option(
    "--yes", "-y",
    is_flag=True,
    help="Skip confirmation prompt."
)
def main(yes, files, dir, pattern, from_list, sort, output) -> None:
    """
    Merges a list of PDF files into one PDF file.
    """

    if files:
        pdfs = [ os.path.join(dir, file) for file in files ]
    elif from_list:
        with open(from_list, "r") as f:
            pdfs = [ 
                line.strip() 
                for line in f.readlines() 
                if line.strip().endswith(".pdf")
            ]
    else:
        pdfs = glob(os.path.join(dir, pattern))

    if sort:
        pdfs = sort_pdfs(pdfs, sort)

    if not pdfs:
        click.echo(click.style("No PDFs found.", fg="red"))
        return
    
    click.echo(click.style(f"Found {len(pdfs)} PDFs to merge:", fg="blue"))
    [click.echo(f"{index+1:>3} {pdf}") for index, pdf in enumerate(pdfs)]

    if not yes:
        click.confirm(click.style("Are you sure you want to merge these PDFs?", 
            fg="yellow"), abort=True)

    merge_pdfs(pdfs, output)

if __name__ == "__main__":
    main()