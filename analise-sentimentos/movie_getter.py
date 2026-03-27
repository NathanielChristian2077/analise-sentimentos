from __future__ import annotations

import re
import time
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup


def _extract_codes_from_soup(soup: BeautifulSoup) -> Iterable[str]:
    links = soup.find_all("a", class_="meta-title-link")
    for link in links:
        href = link.get("href", "")
        match = re.search(r"/filmes/filme-(\d+)/", href)
        if match:
            yield match.group(1)


def get_movie_codes(
    num_movies: int,
    num_pages: int,
    output_file: str | None = None,
    delay: float = 0.0,
) -> List[str]:
    codes: List[str] = []
    base_url = "https://www.adorocinema.com/filmes-todos/"

    for page in range(1, num_pages + 1):
        url = base_url if page == 1 else f"{base_url}?page={page}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        for code in _extract_codes_from_soup(soup):
            codes.append(code)
            if len(codes) >= num_movies:
                break
        if len(codes) >= num_movies:
            break
        if delay > 0:
            time.sleep(delay)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            for code in codes:
                f.write(f"{code}\n")
    return codes


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extrai códigos de filmes do AdoroCinema.",
    )
    parser.add_argument(
        "num_movies", type=int, help="número máximo de filmes a extrair"
    )
    parser.add_argument(
        "num_pages", type=int, help="número máximo de páginas a percorrer"
    )
    parser.add_argument(
        "--output", "-o", type=str, default="movie_code_inputs.txt", help="arquivo de saída"
    )

    args = parser.parse_args()
    codes = get_movie_codes(
        num_movies=args.num_movies,
        num_pages=args.num_pages,
        output_file=args.output,
    )
    print(f"Extraídos {len(codes)} códigos de filme.")
