# CRIME Attack Challenge

## Understanding Compression Oracle Attacks

This challenge helps you understand and exploit the CRIME (Compression Ratio Info-leak Made Easy) attack, a vulnerability that can occur when compression is used before encryption. The attack leverages the fact that when similar strings are compressed together, the compressed output becomes smaller, creating an oracle that can leak information.

### Challenge Overview

The challenge includes three main components:

1. A compression oracle server (`organizer.py`)
2. A demonstration file (`oracle_demonstration.py`)
3. An exploit skeleton (`exploit.py`) for you to implement

### Challenge Modes

#### Mode 1: Basic Compression Oracle

- The server compresses your input along with a secret flag
- Your goal is to recover the flag by analyzing compression ratios
- Ideal for understanding the basic principles of CRIME attacks

#### Mode 2: Advanced - Compression + Encryption

- Adds an encryption layer after compression
- More realistic scenario, simulating real-world conditions (HTTPS)

### Getting Started

1. Run `oracle_demonstration.py` first - it contains examples showing:

- How compression ratios change with different inputs
- Basic patterns that indicate successful matches
  ```python
  # Basic test with the oracle
  python ./oracle_demonstration.py
  ```

2. Start implementing your solution in `exploit.py`:
   - The file contains a skeleton structure
   - Key function is marked for implementation
   - Comments guide you through the attack process

### Attack Strategy

1. **Understanding the Oracle**

   - Compression produces smaller output when similar patterns exist
   - The flag is concatenated with your input before compression
   - By guessing characters, you can detect matches through size changes

2. **Basic Approach**

   - Start by guessing one character at a time
   - When a guess is correct, the compressed size will be smaller
   - Build the flag progressively using this information

3. **Advanced Considerations**
   - In Mode 2, encryption obscures the compression size
   - However, the encrypted size still correlates with the compressed size
   - Additional techniques may be needed to filter out noise

### Example Usage

```python
# Basic test with the oracle
python exploit.py
```

Good luck!
