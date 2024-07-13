# DEUTSCHIFAI

![image](data/images/logo.png)

## Overview
Welcome to DeutschifAI! This interactive application is designed to help you enhance your German vocabulary through personalized word descriptions generated by GPT-3.5. The app allows you to input German words, receive detailed descriptions, and store these entries in a SQLite database for future reference. Moreover, it includes sections to practice words.

## Installation

**Activate environment:**
```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```
**Install Required Packages:**
```
pip install -r requirements.txt
```

**Set Environment Variable:**

1. Create a `.env` file in the root directory of the project.
2. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

**Run the App:**
```bash
stremlit run src/main.py
```

**Contributing**
Contributions are welcome! If you have suggestions for improvements or new features, please:
* Open an issue to discuss your ideas
* Submit a pull request to contribute code

**License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

**Contact**
For any questions or feedback, feel free to reach out to [zumaquerodavid@gmail.com](zumaquerodavid@gmail.com)
