# Launch Gallery

README images must explain what the tool does before they explain how it was distilled. The first image is a white-background function map. Pipeline and distilled-asset diagrams are white-background, text-bearing concept assets copied into the publishable repo by `scripts/build_github_repo.py`. Workflow, terminal, and demo animation assets are generated from local release facts.

| asset | purpose |
| --- | --- |
| `assets/shipgrade-hero-cn.png` | White-background function map: init workbench, wire agents, write brief, run doctor, hand off, preflight. |
| `assets/shipgrade-loop.png` | First-screen workflow card: request -> engineering loop -> verifiable delivery. |
| `assets/shipgrade-terminal-demo.png` | Terminal proof card showing the commands a new user can run immediately. |
| `assets/shipgrade-demo.gif` | Animated first-screen proof generated from the real `shipgrade_demo.py --clean` output. |
| `assets/shipgrade-proof-map-cn.png` | Image Gen seven-step pipeline card: repo -> knowledge -> task -> eval -> RAG/SFT/DPO. |
| `assets/shipgrade-audience-cn.png` | Image Gen four-asset card: Repo Card, Pattern Card, Task Card, Eval. |

## Image Gen Rule

Use white-background, text-bearing assets for README hero and concept diagrams. The first README image must answer "what can this do for me?" before any internal distillation pipeline is shown. Do not replace these with dark gradient placeholders unless concept assets are unavailable during a local emergency build.

The assets contain no private project screenshots, secrets, cookies, sessions, browser profiles, or local machine paths.
