# Day 11: Device Path Counting

## Problem Description

You need to help debug a communication issue between a server rack and a reactor. The issue is triggered by data following specific paths through devices.

Each device can have multiple outputs, and data flows forward only (no backwards flow). Given a device network where each line specifies:
```
device_name: output1 output2 ...
```

Find all possible paths from the device labeled `you` to the device labeled `out`.

### Example

```
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
```

In this example, there are **5** paths from `you` to `out`:
1. you → bbb → ddd → ggg → out
2. you → bbb → eee → out
3. you → ccc → ddd → ggg → out
4. you → ccc → eee → out
5. you → ccc → fff → out

## Solution Approach

### Data Structure
- Use a **directed graph** represented as an adjacency list (dictionary)
- Key: device name
- Value: list of output devices

### Algorithm
- **Depth-First Search (DFS)** with backtracking
- Track visited nodes in the current path to avoid cycles
- Count paths by:
  1. Starting from 'you'
  2. For each output device:
     - If it's 'out', increment counter
     - Otherwise, recursively explore its outputs
  3. Backtrack by removing nodes from visited set

### Time Complexity
- O(V + E) where V is vertices (devices) and E is edges (connections)
- In worst case with all paths, could be O(2^V) for fully connected graphs

### Space Complexity
- O(V) for the recursion stack and visited set

## Implementation Notes

- The algorithm properly handles cycles by tracking visited nodes per path
- Terminal node ('out') doesn't need to be in the graph as a key
- Empty inputs and disconnected components are handled gracefully
