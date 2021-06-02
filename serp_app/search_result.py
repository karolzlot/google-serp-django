from dataclasses import dataclass
from typing import List


@dataclass
class PopularWordDataclass:
    word: str
    occurances: int

@dataclass
class LinkDataclass:
    link: str
    position: int

@dataclass
class SearchResultDataclass:
    query: str
    results_total: int
    most_popular_words: List[PopularWordDataclass]
    links: List[LinkDataclass]

