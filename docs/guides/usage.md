---
title: "Usage"
schema_type: common
status: published
owner: core-maintainer
purpose: "Usage guide for Template Sample."
tags:
  - guide
  - usage
---

# Usage

This guide covers common usage patterns for Template Sample.

## Installation

### From PyPI

```bash
pip install template-sample
```

### From Source

```bash
git clone https://github.com/ByronWilliamsCPA/template-sample
cd template_sample
uv sync --all-extras
```

## Command Line Interface

### Available Commands

```bash
# Show help
template_sample --help

# Hello command
template_sample hello --name "World"

# Show configuration
template_sample config
```

### Debug Mode

Enable debug logging:

```bash
template_sample --debug hello --name "Test"
```
## Library Usage

### Basic Import

```python
from template_sample import __version__

print(f"Version: {__version__}")
```

### Logging

```python
from template_sample.utils.logging import get_logger, setup_logging

# Setup logging
setup_logging(level="DEBUG", json_logs=False)

# Get a logger
logger = get_logger(__name__)
logger.info("Hello from Template Sample")
```
