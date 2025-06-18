#!/usr/bin/env python3
"""
Code generation helper that sends a prompt to OpenAI GPT-4o (or GPT-4-turbo)
and writes the result to stdout or a file.
"""

import argparse
import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def main() -> None:
    parser = argparse.ArgumentParser(description="Codegen using OpenAI GPT-4o")
    parser.add_argument(
        "--prompt",
        required=True,
        help="Prompt to send to the LLM",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output file (default: print to stdout)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="OpenAI model (default: gpt-4o)",
    )
    args = parser.parse_args()

    resp = openai.ChatCompletion.create(
        model=args.model,
        messages=[
            {
                "role": "system",
                "content": "You are a world-class AI code generator and documenter.",
            },
            {"role": "user", "content": args.prompt},
        ],
    )
    code = resp.choices[0].message.content.strip()

    if args.out:
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(code + "\n")
    else:
        print(code)

if __name__ == "__main__":
    main()
