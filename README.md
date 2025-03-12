# 🤖 DSA Quiz Bot

A Telegram bot that automatically sends challenging Data Structures and Algorithms quiz questions to keep your coding skills sharp!

![Bot Demo](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKcGqQoVYaW4I76YoiPqem1ysYuwiGMJ0uwXKRHV9CHn_xt06cc-yjoAzw1WZwwj52gOg&usqp=CAU)

## ✨ Features

- 🧠 Generates high-quality DSA quiz questions using Groq's AI API
- 📝 Multiple-choice format with immediate feedback
- 🔄 Automatic scheduling (sends quizzes every 2 hours)
- 📊 Includes explanations for correct answers
- 🌐 Covers a wide range of DSA topics:
  - Sorting and searching algorithms
  - Data structures (trees, heaps, graphs)
  - Dynamic programming
  - Time and space complexity
  - And more!

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Telegram account
- Groq API key
- A Telegram group where you'd like to send quizzes

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/dsa-quiz-bot.git
   cd dsa-quiz-bot
   ```

2. **Install dependencies**
   ```bash
   pip install "python-telegram-bot[job-queue]" python-dotenv requests
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```
   TOKEN=your_telegram_bot_token
   CHAT_ID=your_telegram_chat_id
   GROQ_API_KEY=your_groq_api_key
   ```

### Getting Required Values

#### Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the API token provided

#### Chat ID
1. Add your bot to the desired Telegram group
2. Send any message in the group
3. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Look for the "chat" object and find the "id" field

#### Groq API Key
1. Sign up at [Groq](https://console.groq.com/)
2. Navigate to API keys section
3. Create and copy your API key

### Running Locally

```bash
python dsa_quiz_bot.py
```

The bot will start sending quizzes to your specified chat every 2 hours.

## 🌩️ Deployment

### Deploy to Railway

1. **Prepare your project**
   - Make sure `requirements.txt`, `Procfile`, and `.gitignore` are set up
   - Push your code to GitHub

2. **Deploy on Railway**
   - Sign up on [Railway](https://railway.app/)
   - Create a new project and connect your GitHub repo
   - Add your environment variables
   - Railway will automatically deploy your bot

3. **Verify it's working**
   - Check the logs in Railway dashboard
   - You should see quiz messages appearing in your Telegram group

## ⚙️ Customization

### Changing Quiz Frequency

Edit the interval in `main()` function:
```python
job_queue.run_repeating(send_quiz, interval=7200, first=10)  # 7200 seconds = 2 hours
```

### Modifying Question Types

Adjust the prompt in the `generate_quiz_data()` function to focus on specific DSA areas.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 🙏 Acknowledgements

- [Groq](https://groq.com/) for providing the AI API
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library
- All DSA enthusiasts who help improve this project

---

Made with ❤️ by [Renu Vishwakarma](https://www.linkedin.com/in/renu-vishwakarma-464813225/)
