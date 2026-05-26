# Launch Gallery

Text-bearing hero, pipeline, and distilled-asset images are generated with Image Gen and then copied into the publishable repo by `scripts/build_github_repo.py`. Workflow, terminal, and demo animation assets are generated from local release facts.

| asset | purpose |
| --- | --- |
| `assets/shipgrade-hero-cn.png` | Image Gen white-background hero card for the repository engineering distillation pipeline. |
| `assets/shipgrade-loop.png` | First-screen workflow card: request -> engineering loop -> verifiable delivery. |
| `assets/shipgrade-terminal-demo.png` | Terminal proof card showing the commands a new user can run immediately. |
| `assets/shipgrade-demo.gif` | Animated first-screen proof generated from the real `shipgrade_demo.py --clean` output. |
| `assets/shipgrade-proof-map-cn.png` | Image Gen seven-step pipeline card: repo -> knowledge -> task -> eval -> RAG/SFT/DPO. |
| `assets/shipgrade-audience-cn.png` | Image Gen four-asset card: Repo Card, Pattern Card, Task Card, Eval. |

The assets contain no private project screenshots, secrets, cookies, sessions, browser profiles, or local machine paths.
