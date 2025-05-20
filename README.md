# Social Media Reply Generator

A FastAPI-based backend application that generates human-like replies to social media posts. The project supports multiple platforms (e.g., Twitter, LinkedIn), analyzes post content, and stores/retrieves generated replies using MongoDB.

---

## 🚀 Features

- **Generate Replies:** Create context-aware, human-like replies for social media posts.
- **Post Analysis:** Detects intent, sentiment, and topics in posts.
- **Platform Support:** Easily extendable to support various social media platforms.
- **Database Integration:** Stores and retrieves replies from MongoDB.
- **Async & Fast:** Built with FastAPI and async MongoDB operations.
- **CORS Enabled:** Ready for frontend integration.
- **Robust Error Handling:** Consistent error responses and logging.

---

## 🗂️ Project Structure

```
Social_Media_Reply_Generator/
│
├── app/
│   ├── api/
│   │   └── routes.py         # API endpoints
│   ├── db/
│   │   └── database.py       # Database logic
│   ├── schemas/
│   │   └── schema.py         # Pydantic models
│   ├── main.py               # FastAPI app entry point
│   ├── logic.py              # Core reply generation logic
│   └── config.py             # App configuration
│
├── .env                      # Environment variables (not committed)
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/<your-username>/Social_Media_Reply_Generator.git
   cd Social_Media_Reply_Generator
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` (if provided) or create a `.env` file.
   - Add your MongoDB URI and any required API keys.

---

## 🏃‍♂️ Running the Application

Start the FastAPI server:
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- API root: [http://localhost:8000/](http://localhost:8000/)
- Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠️ API Usage

### **Generate a Reply**
**POST** `/api/reply`

**Request Example:**
```json
{
  "platform": "twitter",
  "post_text": "What are the best practices for Python development?",
  "context": "Looking for advice on Python development.",
  "include_analysis": true
}
```

**Response Example:**
```json
{
  "reply_text": "Here are some best practices for Python development: ...",
  "platform": "twitter",
  "post_text": "What are the best practices for Python development?",
  "created_at": "2025-05-19T12:34:56.789Z",
  "analysis": {
    "intent": "question",
    "sentiment": "neutral",
    "topics": ["Python", "best practices"],
    "response_type": "informative"
  },
  "metadata": {}
}
```

### **Get Recent Replies**
**GET** `/api/replies/recent?platform=twitter&limit=5`

---

## 🧩 Extending the Project

- **Add new platforms:** Update `SUPPORTED_PLATFORMS` in `config.py` and extend logic in `logic.py`.
- **Improve analysis:** Enhance the `analyze_post` function for better intent/sentiment detection.
- **Frontend:** Build a frontend to interact with this API.

---

## 📝 License

MIT License

---

## 🙋‍♂️ Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📞 Contact

For questions or support, open an issue on GitHub.
