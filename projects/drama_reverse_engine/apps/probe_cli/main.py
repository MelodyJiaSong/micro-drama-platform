from __future__ import annotations

import argparse

from apps.probe_cli.container import ProbeContainer

_CHOICES = ["all", "understand-connectivity"]


def main() -> None:
    parser = argparse.ArgumentParser(description="FR-13 PoC probes (live API; skipped without keys)")
    parser.add_argument("probes", nargs="+", choices=_CHOICES)
    args = parser.parse_args()

    command = ProbeContainer().probe_command()
    for result in command.run(args.probes if "all" not in args.probes else ["all"]):
        print(f"[{result.status:^7}] {result.name}: {result.detail}")
        for key, value in result.data.items():
            print(f"          {key} = {value}")


if __name__ == "__main__":
    main()
