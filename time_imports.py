"""
Timing script for Frosty AI initialization.
Mirrors exactly how main.py loads — uses src/ as the root, matching the real app.
Run from the frosty/ directory: python3.11 time_imports.py
"""
import sys
import time
import os

# Match the real app: add src/ so imports use 'src.frosty_ai.*' (same as main.py)
sys.path.insert(0, os.path.dirname(__file__))

def timed(label, fn):
    t0 = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - t0
    print(f"  {elapsed*1000:8.1f} ms  {label}")
    return result

print("\n=== Frosty AI Startup Timing (mirrors main.py load order) ===\n")

t_total = time.perf_counter()

print("[1] Heavy third-party libs (cold import, paid once):")
timed("google.genai",        lambda: __import__("google.genai"))
timed("google.adk.agents",   lambda: __import__("google.adk.agents"))
timed("google.adk.runners",  lambda: __import__("google.adk.runners"))
timed("google.adk.memory",   lambda: __import__("google.adk.memory"))

print("\n[2] Frosty core (config, tools, lazy_agent_tool):")
timed("src.frosty_ai.objagents.config",          lambda: __import__("src.frosty_ai.objagents.config", fromlist=["*"]))
timed("src.frosty_ai.objagents.tools",           lambda: __import__("src.frosty_ai.objagents.tools", fromlist=["*"]))
timed("src.frosty_ai.objagents.lazy_agent_tool", lambda: __import__("src.frosty_ai.objagents.lazy_agent_tool", fromlist=["*"]))

print("\n[3] Pillar prompt imports (no agent loading expected):")
timed("dataengineer.prompt",     lambda: __import__("src.frosty_ai.objagents.sub_agents.dataengineer.prompt", fromlist=["*"]))
timed("securityengineer.prompt", lambda: __import__("src.frosty_ai.objagents.sub_agents.securityengineer.prompt", fromlist=["*"]))
timed("administrator.prompt",    lambda: __import__("src.frosty_ai.objagents.sub_agents.administrator.prompt", fromlist=["*"]))
timed("governance.prompt",       lambda: __import__("src.frosty_ai.objagents.sub_agents.governance.prompt", fromlist=["*"]))
timed("inspector.prompt",        lambda: __import__("src.frosty_ai.objagents.sub_agents.inspector.prompt", fromlist=["*"]))
timed("research.prompt",         lambda: __import__("src.frosty_ai.objagents.sub_agents.research.prompt", fromlist=["*"]))
timed("accountmonitor.prompt",   lambda: __import__("src.frosty_ai.objagents.sub_agents.accountmonitor.prompt", fromlist=["*"]))

print("\n[4] Root agent construction (ag_sf_manager + 7 LazyAgentTools):")
t0 = time.perf_counter()
from src.frosty_ai.objagents.agent import ag_sf_manager
elapsed = time.perf_counter() - t0
print(f"  {elapsed*1000:8.1f} ms  src.frosty_ai.objagents.agent")

print("\n[5] Session/runner imports:")
timed("src.frosty_ai.adksession", lambda: __import__("src.frosty_ai.adksession", fromlist=["*"]))
timed("src.frosty_ai.adkstate",   lambda: __import__("src.frosty_ai.adkstate", fromlist=["*"]))
timed("src.frosty_ai.adkrunner",  lambda: __import__("src.frosty_ai.adkrunner", fromlist=["*"]))

print("\n[6] Warm-up timing (BFS — all nodes at each level in parallel):")
from concurrent.futures import ThreadPoolExecutor
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

def resolve_one_timed(tool):
    t0 = time.perf_counter()
    try:
        tool.warm_up()
    except Exception as e:
        return tool.name, time.perf_counter() - t0, str(e), tool.get_sub_tools()
    return tool.name, time.perf_counter() - t0, None, tool.get_sub_tools()

current_level = [
    t for t in (getattr(ag_sf_manager, "tools", None) or [])
    if isinstance(t, LazyAgentTool)
]

t_warmup = time.perf_counter()
all_results = []
level = 0
while current_level:
    level += 1
    t_level = time.perf_counter()
    with ThreadPoolExecutor(max_workers=len(current_level)) as executor:
        results = list(executor.map(resolve_one_timed, current_level))
    level_wall = time.perf_counter() - t_level
    print(f"\n  Level {level} ({len(current_level)} agents, wall-clock {level_wall*1000:.1f} ms):")
    for name, elapsed, err, _ in sorted(results, key=lambda r: r[1], reverse=True):
        status = f"  ⚠ {err}" if err else ""
        print(f"    {elapsed*1000:8.1f} ms  {name}{status}")
    all_results.extend(results)
    current_level = [t for _, _, _, children in results for t in children]

wall_clock = time.perf_counter() - t_warmup
print(f"\n  {'─'*40}")
print(f"  {wall_clock*1000:8.1f} ms  total wall-clock across all levels")
print(f"  {sum(r[1] for r in all_results)*1000:8.1f} ms  sum of all threads (sequential equivalent)")

total = time.perf_counter() - t_total
print(f"\n  {'─'*40}")
print(f"  {total*1000:8.1f} ms  TOTAL (includes all above)\n")
print("=== Done ===\n")
