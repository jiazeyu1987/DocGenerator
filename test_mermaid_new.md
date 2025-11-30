# Mermaid Diagram Test - New Configuration

This test will verify that images are saved to the project images directory.

## Simple Flowchart

```mermaid
flowchart LR
    Start --> Process
    Process --> End
```

## Decision Tree

```mermaid
flowchart TD
    A{Is it working?} -->|Yes| B[Success]
    A -->|No| C[Debug]
    C --> A
```