# 🕵️‍♂️ VulnScanJs

**VulnScanJs** is a lightweight, multithreaded scanner for identifying potentially vulnerable JavaScript patterns in JS files from remote URLs. It’s designed for security researchers, bug bounty hunters, and developers who want to audit front-end code for risky functions.

---

## 🚀 Features

- ⚡ Multithreaded scanning for fast performance  
- 📜 Customizable wordlist to detect risky JavaScript function calls  
- 🌐 URL-based scanning  
- ⏱️ Configurable request timeout  
- 🎨 Colored terminal output for easy reading  

---

## 📦 Installation

```bash
git clone https://github.com/your-username/VulnScanJs.git
cd VulnScanJs
pip install -r requirements.txt
```

**Dependencies:**
- `requests`
- `colored`

---

## 🛠️ Usage

```bash
python vulnscanjs.py -w wordlist.txt 
cat wordlist.txt | python3  vulnscanjs.py 
```

### Command-line Arguments

| Argument             | Description                                         |
|----------------------|-----------------------------------------------------|
| `-u, --urls`         | File path to a list of URLs (one per line)          |
| `-w, --wordlist`     | Wordlist of JavaScript patterns to scan for         |
| `-t, --timeout`      | Timeout for HTTP requests (default: 15 seconds)     |
| `-m, --matching`     | Turns on regex compiling for wordlist file          |
---

## 📂 Example

**urls.txt**
```
https://example.com/js/main.js
https://anotherdomain.com/app.js
```

**wordlist.txt**
```
eval
document.write
innerHTML
```

**Run the scanner:**

```bash
python3 vulnscanjs.py -u urls.txt -w wordlist.txt
cat wordlist.txt | python3  vulnscanjs.py 
```

**Sample output:**

```
[*] Target: https://example.com/js/main.js
[*] Status: 200 OK
[+] Match found for 'eval': 3 times
[+] Match found for 'document.write': 1 time
```

---

## 🛡️ Disclaimer

This tool is intended **for educational and ethical security research purposes only**.  
Do not use VulnScanJs on systems without explicit permission.

---

## 📃 License

[MIT License](LICENSE)

---

## 👨‍💻 Author

Created by [TechDevRon](https://github.com/TechDevRon)
