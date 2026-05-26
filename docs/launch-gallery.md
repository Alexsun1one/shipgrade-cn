# Launch Gallery

README images must explain what the tool does before they explain how it was distilled. Canonical concept images live in `assets/imagegen/` and are copied into the publishable repo by `scripts/build_github_repo.py`; the Pillow renderer is only a local fallback. Workflow, terminal, and demo animation assets are generated from local release facts.

| asset | purpose |
| --- | --- |
| `assets/shipgrade-hero-cn.png` | Image Gen README hero: product promise, workbench mockup, supported agents, quality-gate proof. |
| `assets/shipgrade-loop.png` | First-screen workflow card: request -> engineering loop -> verifiable delivery. |
| `assets/shipgrade-terminal-demo.png` | Terminal proof card showing the commands a new user can run immediately. |
| `assets/shipgrade-demo.gif` | Animated first-screen proof generated from the real `shipgrade_demo.py --clean` output. |
| `assets/shipgrade-proof-map-cn.png` | Image Gen seven-step pipeline card: repo -> knowledge -> task -> eval -> RAG/SFT/DPO. |
| `assets/shipgrade-audience-cn.png` | Image Gen four-asset card: Repo Card, Pattern Card, Task Card, Eval. |

## Image Gen Rule

Use Image Gen for README hero and concept diagrams by default. Assets should be white-background, text-bearing, and product-facing. The first README image must answer "what can this do for me?" before any internal distillation pipeline is shown. Do not replace Image Gen assets with generated dark gradients or quick Pillow diagrams unless concept assets are unavailable during a local emergency build.

The assets contain no private project screenshots, secrets, cookies, sessions, browser profiles, or local machine paths.
