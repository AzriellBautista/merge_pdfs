# About

Merges a list of PDF files into one PDF file.

# Usage

`merge.py [OPTIONS] [FILES]...`

```
Options:
  -d, --dir PATH                  Directory containing PDF files to merge.
                                  Defaults to current working directory.
  -p, --pattern TEXT              Filename pattern to match. Wildcards (*, ?,
                                  [ranges]) are accepted.  [default: *.pdf]
  -L, --from-list FILE            File containing a list of PDF files to
                                  merge.
  -s, --sort [name|date|size|^name|^date|^size]
                                  Sort PDFs by a given option.
  -o, --output TEXT               Output filename.  [default: merged.pdf]
  -y, --yes                       Skip confirmation prompt.
  --help                          Show this message and exit.
```

# Example

Merge `file1.pdf`, `file2.pdf`, and `file3.pdf` immediately.

```
merge file1.pdf file2.pdf file.pdf -y
```

Merge PDFs with the filename pattern of `file*.pdf`.

```
merge --pattern file*.pdf
```
Merge from a list file names `list.txt` 

```
merge -L list.txt
```

# Dependencies

Requires `PyPDF2` and `click` modules.