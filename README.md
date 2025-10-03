# Up2Date

This program detects the operating system from the machine on which it gets executed and retreives the End of Support (EOS) date from the official vendor website for the given version.

The main intention was to integrate it with an existing monitoring system which can run the script periodically and evaluate the reported EOS date. If the EOS date is close, the monitoring software can trigger a warning or alert, ensuring that administrators are notified in time to plan migrations or updates. 

Currently, the following operating systems are supported:
- Debian
- Ubuntu
- Windows (7, 8.1, 10, 11)

## Prerequisites

- Python >= 3.7
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)  
- [requests](https://pypi.org/project/requests/)  

## Installation

```bash
# Clone the repository
git clone https://github.com/l3fuex/up2date.git

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
python3 up2date.py
```

Example output:
```yaml
ubuntu 20.04 EOS date: 2025-05-31
```

## License
This software is provided under the [Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license.


## Acknowledgments
Lifecycle information is retrieved from:
- [Debian](https://www.debian.org/releases/)
- [Ubuntu](https://ubuntu.com/about/release-cycle)
- [Windows](https://learn.microsoft.com/en-us/lifecycle/products/)
