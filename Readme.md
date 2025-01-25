# Micro-Tokenizer with BPE and Regex Splitting

This is a mini-project for a micro-tokenizer inspired by OpenAI's GPT-2 tokenizer. It uses Byte Pair Encoding (BPE) and forced regex splitting for tokenization. The project is designed for educational purposes and has significant potential for improvements. Contributions are welcomed!

---

## Features
- **Byte Pair Encoding (BPE)**: Efficient subword tokenization technique.
- **Forced Regex Splitting**: Custom splitting based on regular expressions.
- **Customizable Configuration**: Easily adapt for training or inference with your own datasets.

---

## Getting Started

### Prerequisites
- Python 3.8 or higher.

### Installation
1. Clone the repository:
```bash
git clone https://github.com/SurAyush/micro-tokenizer.git
cd micro-tokenizer
```
2. Create and Activate Virtual Environment:
```bash
python -m venv my_bpe
my_bpe\Scripts\activate  # On Windows
source my_bpe/bin/activate  # On macOS/Linux
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

### Usage
1. Training
If you want to train the tokenizer on your own dataset:
- Replace the content of output.txt with your desired training data.

- Optionally, use extract_data.py to download data from Wikipedia
```bash
python extract_data.py
```

- Update the configuration in test.py:
Set the training_file and val_file variables to the paths of your training and validation files.
```bash
python test.py
```

2. Inference

If you just want to use the tokenizer without training:

Set the req_training parameter to False in test.py:

```bash
tokenizer = Tokenizer(req_training=False)
```
Run the file:
```bash
python test.py
```

### Notes

1. This project is primarily for educational purposes.
2. Many improvements can be made to the current implementation. Contributions, bug fixes, and suggestions are highly appreciated!


