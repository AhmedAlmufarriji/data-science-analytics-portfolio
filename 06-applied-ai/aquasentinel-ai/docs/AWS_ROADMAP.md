# Optional future AWS architecture (NOT deployed)

AquaSentinel runs completely offline. These are **future engineering extensions**, not implemented features and not an AWS certification claim.

1. Store encrypted anonymized sensor files in Amazon S3 and publish data contracts through AWS Glue.
2. Use EventBridge or Kinesis for event ingestion; avoid identifiable utility coordinates in demonstration streams.
3. Containerize FastAPI behind authentication; consider ECS Fargate + Application Load Balancer or other supported hosting.
4. Experiment with Bedrock AgentCore Runtime for a model-driven copilot, with explicit tool allowlists and session-level identity.
5. Use Bedrock Knowledge Bases for versioned procedures, recording citations and resolving conflicts with primary operations manuals.
6. Use AgentCore Gateway for explicit API tool invocation with least-privilege permissions; protect with OAuth through Cognito.
7. Adopt Guardrails to moderate inputs, protect secrets and prevent unsupported operational advice, but preserve domain-specific control-plane safeguards.
8. Use CloudWatch tracing and Bedrock evaluation plus CI integration tests to measure correctness, grounding, latency and cost.
9. Private networking requires careful VPC endpoint coverage and connectivity tests; never assume it is functional purely because a runtime deploys.

**Cost / safety:** AWS services may incur charges. No AWS resources or API requests are made by this repository unless a developer separately implements this roadmap.
