# Contributing to ADAC Blockchain

## Getting Started

1. Fork the repository
2. Create a new branch for your feature/fix
3. Write tests for your changes
4. Implement your changes
5. Run the test suite
6. Submit a pull request

## Code Style

We follow PEP 8 for Python code. Use `black` for formatting:

```bash
black src/ tests/
```

## Testing

All new features should include tests. Run the test suite:

```bash
pytest tests/
```

## Pull Request Process

1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Development Environment

Use the provided development container or set up your environment:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Documentation

Update documentation for any changes:

- API changes: Update `docs/api.md`
- Architecture changes: Update `docs/architecture.md`
- Deployment changes: Update `docs/deployment.md`

## Community

- Join our Discord server
- Subscribe to our mailing list
- Follow us on Twitter