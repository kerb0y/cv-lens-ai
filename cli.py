"""Command line interface for CV Lens AI.

Examples:
    python cli.py analyze --cv examples/sample_cv.txt --job examples/sample_job.txt
    python cli.py keywords --file examples/sample_cv.txt --top 10
    python cli.py summarize --file examples/sample_job.txt
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.analyzer import analyze_cv
from app.services.keywords import extract_keywords
from app.services.summarizer import summarize


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(prog="cv-lens", description="CV Lens AI CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub.add_parser("analyze", help="Analyze a CV against a job description")
    p_analyze.add_argument("--cv", required=True)
    p_analyze.add_argument("--job", required=True)

    p_keywords = sub.add_parser("keywords", help="Extract keywords from a text file")
    p_keywords.add_argument("--file", required=True)
    p_keywords.add_argument("--top", type=int, default=10)

    p_summarize = sub.add_parser("summarize", help="Summarize a text file")
    p_summarize.add_argument("--file", required=True)
    p_summarize.add_argument("--sentences", type=int, default=3)

    args = parser.parse_args()

    if args.command == "analyze":
        result = analyze_cv(read(args.cv), read(args.job))
    elif args.command == "keywords":
        result = {"keywords": extract_keywords(read(args.file), top_n=args.top)}
    else:
        result = summarize(read(args.file), max_sentences=args.sentences)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
