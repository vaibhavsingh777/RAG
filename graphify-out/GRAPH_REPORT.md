# Graph Report - /Users/vaibhavsingh/Documents/RAG  (2026-07-13)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 25 nodes · 23 edges · 7 communities (4 shown, 3 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.5)
- Token cost: 197 input · 55 output

## Graph Freshness
- Built from commit: `06293d72`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- User Interface
- Question Answering Pipeline
- Rate Limiting
- Question Answering Pipeline
- User Interface

## God Nodes (most connected - your core abstractions)
1. `Human Readable Name` - 5 edges
2. `QAPipeline` - 4 edges
3. `rate_limit_handler()` - 3 edges
4. `Human Readable Name` - 3 edges
5. `QAPipeline` - 2 edges
6. `ask()` - 2 edges
7. `Human Readable Name` - 1 edges
8. `Human Readable Name` - 1 edges
9. `Human Readable Name` - 1 edges
10. `Human Readable Name` - 1 edges

## Surprising Connections (you probably didn't know these)
- `Human Readable Name` --conceptually_related_to--> `Human Readable Name`  [INFERRED]
  slowapi.py → data/my_docs.txt
- `Human Readable Name` --calls--> `Human Readable Name`  [EXTRACTED]
  requirements.txt → slowapi.py
- `Human Readable Name` --conceptually_related_to--> `Human Readable Name`  [INFERRED]
  requirements.txt → data/my_docs.txt
- `Human Readable Name` --conceptually_related_to--> `Human Readable Name`  [EXTRACTED]
  requirements.txt → data/my_docs.txt
- `Human Readable Name` --conceptually_related_to--> `Human Readable Name`  [EXTRACTED]
  requirements.txt → data/my_docs.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Human Readable Label** — machine_learning, climate_change, electric_vehicles, great_wall_of_china [EXTRACTED 0.75]

## Communities (7 total, 3 thin omitted)

### Community 0 - "User Interface"
Cohesion: 0.33
Nodes (6): Human Readable Name, Human Readable Name, Human Readable Name, Human Readable Name, Human Readable Name, Human Readable Name

### Community 2 - "Rate Limiting"
Cohesion: 0.50
Nodes (4): ask(), rate_limit_handler(), RateLimitExceeded, Request

## Knowledge Gaps
- **5 isolated node(s):** `Human Readable Name`, `Human Readable Name`, `Human Readable Name`, `Human Readable Name`, `Human Readable Name`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Human Readable Name` connect `User Interface` to `Question Answering Pipeline`?**
  _High betweenness centrality (0.286) - this node is a cross-community bridge._
- **Why does `Human Readable Name` connect `User Interface` to `Caching`?**
  _High betweenness centrality (0.283) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Human Readable Name` (e.g. with `Human Readable Name` and `Human Readable Name`) actually correct?**
  _`Human Readable Name` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Human Readable Name`, `Human Readable Name`, `Human Readable Name` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._