# Open finance

This project is a personal initiative to manage financial data securely and privately by hosting it on a local server (e.g., a Raspberry Pi) instead of a shared drive. The system categorizes financial transactions, with each category defined in a YAML file.

Sample YAML:
```yaml
category: E-commerce
regex:
- AMAZON
- DECATHLON
- 100KMPH
- AMAZFITINDIA
- AJIO
```

## Installation

I don't do well with frontend, so [streamlit](https://streamlit.io/) it is.

Currently only support
- HDFC bank

```bash
pip install streamlit
```

## Usage

Place your account statements in the appropriate folder. I automate the process of moving my account statements from email to a folder using a cron job.

Extension supported:
- xls

Folder structure
```
--- salaryslips (Monthly account statements)
--- output_json (Processed salary slips in JSON format)
--- cat_yaml (Categories stored in YAML format)
```
Note: Instead of storing data in flat files, using a NoSQL database (such as Redis or MongoDB) is preferred. 
```bash
streamlit run .\main.py
```
## Screenshots

