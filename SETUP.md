# Setup Instructions

## Prerequisites

1. **Python**: Version 3.9 or higher
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **Git**: For cloning the repository
   - Download from [git-scm.com](https://git-scm.com/downloads)

3. **Google Gemini API Key**: Free API access
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated key

## Step-by-Step Setup

### 1. Clone or Download Repository

```bash
# Option A: Clone with Git
git clone https://github.com/your-username/ecommerce-insights-agent.git
cd ecommerce-insights-agent

# Option B: Download ZIP
# Extract the ZIP file and navigate to the directory
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required packages (~500MB download).

### 4. Configure Environment Variables

```bash
# Windows
copy .env.example .env

# Linux/MacOS
cp .env.example .env
```

Edit the `.env` file with your favorite text editor:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

Replace `your_actual_gemini_api_key_here` with your actual API key from Google AI Studio.

### 5. Download Dataset

1. Go to [Kaggle Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/)
2. Click "Download" (you'll need a Kaggle account - it's free)
3. Extract all CSV files from the ZIP
4. Create a `data` folder in the project directory if it doesn't exist
5. Move all CSV files to the `data` folder

Expected files:
- `olist_customers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

### 6. Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

## First Time Usage

1. **Load Data**: 
   - In the sidebar, verify the data directory path is correct
   - Click "🔄 Load Data"
   - Wait for all tables to load (~10 seconds)
   - You should see green success messages

2. **Test the System**:
   - Try an example query like: "What are the top 5 product categories?"
   - Wait for the response
   - You should see analysis, data table, and possibly a chart

3. **Explore Features**:
   - Try the example queries in the sidebar
   - Ask follow-up questions
   - Export your conversation
   - Check the metrics dashboard

## Troubleshooting

### Issue: "Gemini API Key not configured"

**Solution**: 
- Ensure you've created a `.env` file (not `.env.example`)
- Verify the API key is correct
- Make sure there are no extra spaces or quotes around the key
- Restart the Streamlit app

### Issue: "No data files found"

**Solution**:
- Verify CSV files are in the `data/` directory
- Check file names match exactly (case-sensitive on Linux/Mac)
- Ensure files are not in a subdirectory

### Issue: "Module not found" errors

**Solution**:
```bash
# Ensure virtual environment is activated
# You should see (venv) in your prompt

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: Port already in use

**Solution**:
```bash
# Run on a different port
streamlit run app.py --server.port 8502
```

### Issue: Slow performance

**Solution**:
- Ensure you're using a recent Python version (3.9+)
- Close other memory-intensive applications
- Reduce `max_conversation_history` in `.env`
- Limit query result size

## Updating the Application

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart Streamlit
streamlit run app.py
```

## Development Mode

For development with auto-reload:

```bash
streamlit run app.py --server.runOnSave true
```

## Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets in Streamlit Cloud dashboard:
   - `GEMINI_API_KEY = "your_key_here"`
5. Deploy!

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

## Additional Configuration

### Custom Settings

Edit `.env` to customize:

```env
# Application
APP_NAME=My E-Commerce AI
DEBUG_MODE=False
LOG_LEVEL=INFO

# Database
MAX_QUERY_RESULTS=1000
QUERY_TIMEOUT=30

# LLM
DEFAULT_MODEL=gemini-1.5-pro
TEMPERATURE=0.1
MAX_TOKENS=4096

# Memory
MAX_CONVERSATION_HISTORY=20
ENABLE_MEMORY_PERSISTENCE=True
```

## Support

If you encounter issues:

1. Check the logs in the `logs/` directory
2. Ensure all prerequisites are installed correctly
3. Try clearing cache: `streamlit cache clear`
4. Create an issue on GitHub with error details

## Next Steps

- Read the [README.md](README.md) for full documentation
- Try the example queries
- Explore the agent system architecture
- Customize for your use case
