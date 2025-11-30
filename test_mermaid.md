# Mermaid Diagram Test

This is a test file to verify Mermaid diagram conversion functionality.

## Flowchart Example

```mermaid
flowchart TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Process Diagram]
    B -->|No| D[Debug Issue]
    C --> E[Generate Image]
    D --> E
    E --> F[End]
```

## Sequence Diagram Example

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Database

    Client->>Server: Request
    Server->>Database: Query
    Database-->>Server: Results
    Server-->>Client: Response
```

## Regular Text Content

This is regular Markdown content that should remain unchanged.

* Item 1
* Item 2
* Item 3

## Another Flowchart

```mermaid
graph LR
    A-->B
    B-->C
    C-->D
    D-->A
```

This document contains multiple Mermaid diagrams that should be converted to images during the conversion process.