---
title: "Configuration"
schema_type: common
status: published
owner: core-maintainer
purpose: "Configuration guide for Template Sample."
tags:
  - guide
  - configuration
---

# Configuration

This guide covers all configuration options for Template Sample.

## Environment Variables

Template Sample uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `JSON_LOGS` | Enable JSON log format | `false` |

## Configuration File

Create a `.env` file in your project root:

```bash
# Logging
LOG_LEVEL=INFO
JSON_LOGS=false

# Add your configuration here
```

## Pydantic Settings

Configuration is managed via Pydantic Settings for type safety:

```python
from template_sample.core.config import settings

# Access settings
print(settings.log_level)
```

## Development vs Production

### Development

```bash
LOG_LEVEL=DEBUG
JSON_LOGS=false
```

### Production

```bash
LOG_LEVEL=INFO
JSON_LOGS=true
```
