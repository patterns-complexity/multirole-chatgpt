# MultiRole-ChatGPT

![Static Badge](https://img.shields.io/badge/MIT-blue?label=License&labelColor=black) ![Static Badge](https://img.shields.io/badge/3.11-blue?label=Python&labelColor=black)

## Description

Welcome to the **MultiRole-ChatGPT** repository! This project is a Python-based orchestration system designed to manage multiple GPT-based AI models with varying roles and intelligence levels. It's built to handle complex queries and make intelligent decisions through a multi-model approach.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [License](#license)

## Installation

To get started, you'll need to clone the repository:

```bash
git clone git@github.com:patterns-complexity/multirole-chatgpt.git
```

Then go to the project directory:

```bash
cd multirole-chatgpt
```

Then install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

### Provide your OpenAI API Key
- Rename `.env.example` to `.env`.
- Fill in your OpenAI API Key in `.env`.

```bash
# file: /.env
OPENAI_API_KEY=your_api_key_here
```

### Where to get the API key from?

You can get your OpenAI API Key here:
- [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).

### Warning
In order for this code to work, you need to have access to the following models:
- `gpt-3.5-turbo` - available by default at the time of writing this README.
- `gpt-4` - you have to top up your OpenAI account with at least $1 worth of prepaid credits to access this model. Doing it will immediately unlock the `gpt-4` model for you.

## Usage

To run the project, simply execute the following command:

```bash
python ./app.py
```

You'll be prompted to enter your query. The manager will then communicate with the designated models to provide you with a well-rounded answer.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).