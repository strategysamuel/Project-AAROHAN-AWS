# AAR-DATA-DEPENDENCY-GRAPH

## Strict Hierarchical Data Dependencies

```text
Customer
    │
    ├── Persona (Mapped)
    ├── GST
    ├── CKYC
    ├── AA
    ├── EPFO
    ├── MCA
    ├── Financial Health Card
    ├── Credit Engine
    ├── CAM
    ├── Executive Dashboard
    └── Reports
```

## Validation
- **Customer** acts as the root node for all generated data.
- Every child node references the Customer ID directly or via application context.
- All edges have been verified to hold strict referential integrity under the shared `aarohan_local.db` architecture.
