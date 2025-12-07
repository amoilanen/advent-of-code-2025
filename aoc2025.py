#!/usr/bin/env python3
"""Advent of Code 2025 - Main Entry Point

Usage:
    python aoc2025.py           # Run all days
    python aoc2025.py 1         # Run day 1
    python aoc2025.py day01     # Run day 1
"""

import sys
from internal.days import day01, day02, day03, day04, day05, day06


def main():
    if len(sys.argv) > 1:
        run_specific_day(sys.argv[1])
    else:
        run_all_days()


def run_all_days():
    print("Advent of Code 2025 - Solutions")
    print("=" * 40)
    print()

    run_day01()
    run_day02()
    run_day03()
    run_day04()
    run_day05()
    run_day06()


def run_specific_day(day: str):
    """Run a specific day's solution."""
    day_map = {
        '1': run_day01,
        '2': run_day02,
        '3': run_day03,
        '4': run_day04,
        '5': run_day05,
        '6': run_day06
    }

    runner = day_map.get(day.lower())
    if runner:
        runner()
    else:
        print(f"Unknown day: {day}", file=sys.stderr)
        print("Usage: python aoc2025.py [day]", file=sys.stderr)
        print("Example: python aoc2025.py 1", file=sys.stderr)
        sys.exit(1)


def run_day01():
    """Run Day 1 solution."""
    print("Day 1:")
    parsed = day01.parse(day01.DAY_INPUT)
    print(f"  Part 1: {day01.part1(parsed)}")
    print(f"  Part 2: {day01.part2(parsed)}")
    print()


def run_day02():
    """Run Day 2 solution."""
    print("Day 2:")
    parsed = day02.parse(day02.DAY_INPUT)
    print(f"  Part 1: {day02.part1(parsed)}")
    print(f"  Part 2: {day02.part2(parsed)}")
    print()


def run_day03():
    """Run Day 3 solution."""
    print("Day 3:")
    parsed = day03.parse(day03.DAY_INPUT)
    print(f"  Part 1: {day03.part1(parsed)}")
    print(f"  Part 2: {day03.part2(parsed)}")
    print()


def run_day04():
    """Run Day 4 solution."""
    print("Day 4:")
    parsed = day04.parse(day04.DAY_INPUT)
    print(f"  Part 1: {day04.part1(parsed)}")
    print(f"  Part 2: {day04.part2(parsed)}")
    print()

def run_day05():
    """Run Day 5 solution."""
    print("Day 5:")
    parsed = day05.parse(day05.DAY_INPUT)
    print(f"  Part 1: {day05.part1(parsed)}")
    print(f"  Part 2: {day05.part2(parsed)}")
    print()


def run_day06():
    """Run Day 6 solution."""
    print("Day 6:")
    parsed_part1 = day06.parse_part1(day06.DAY_INPUT)
    parsed_part2 = day06.parse_part2(day06.DAY_INPUT)
    print(f"  Part 1: {day06.part1(parsed_part1)}")
    print(f"  Part 2: {day06.part2(parsed_part2)}")
    print()


if __name__ == "__main__":
    main()
