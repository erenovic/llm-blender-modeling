# vllm-blender

An LLM project using VLLM and BlenderNet to generate 3D Assets for Three.JS development. This project is built upon the foundational work of [BlenderLLM](https://github.com/FreedomIntelligence/BlenderLLM) by FreedomIntelligence.

[![CI](https://github.com/erenovic/vllm_blender/workflows/CI/badge.svg)](https://github.com/erenovic/vllm_blender/actions)
[![Coverage](https://codecov.io/gh/erenovic/vllm_blender/branch/main/graph/badge.svg)](https://codecov.io/gh/erenovic/vllm_blender)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install vllm_blender
```

## Quick Start

### Python API

```python
from vllm_blender.main import hello_world

# Basic usage
result = hello_world()
print(result)  # "Hello from vllm-blender!"

# With a name
result = hello_world("Alice")
print(result)  # "Hello, Alice, from vllm-blender!"
```

### Command Line

```bash
python -m vllm_blender
```

## Development

### Setup

1. Clone the repository:

```bash
git clone https://github.com/erenovic/vllm_blender.git
cd vllm_blender
```

2. Set up development environment:

```bash
make all  # Install dependencies, pre-commit hooks, and run all checks
```

### Development Commands

```bash
make help          # Show all available commands
make install-dev   # Install development dependencies
make fmt           # Format code with ruff
make lint          # Lint code with ruff
make typecheck     # Type check with mypy
make test          # Run tests
make test-cov      # Run tests with coverage
make ci            # Run all CI checks locally
make clean         # Clean build artifacts
```

## Features

-   ✅ Modern Python packaging with `pyproject.toml`
-   ✅ Code formatting and linting with Ruff
-   ✅ Static type checking with mypy
-   ✅ Testing with pytest and coverage reporting
-   ✅ Pre-commit hooks for code quality
-   ✅ GitHub Actions CI/CD

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This project builds upon the work of [BlenderLLM](https://github.com/FreedomIntelligence/BlenderLLM) by FreedomIntelligence.

### Citation

If you use this project or find it helpful, please consider citing the original BlenderLLM work:

```bibtex
@misc{du2024blenderllmtraininglargelanguage,
      title={BlenderLLM: Training Large Language Models for Computer-Aided Design with Self-improvement},
      author={Yuhao Du and Shunian Chen and Wenbo Zan and Peizhao Li and Mingxuan Wang and Dingjie Song and Bo Li and Yan Hu and Benyou Wang},
      year={2024},
      eprint={2412.14203},
      archivePrefix={arXiv},
      primaryClass={cs.HC},
      url={https://arxiv.org/abs/2412.14203},
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
