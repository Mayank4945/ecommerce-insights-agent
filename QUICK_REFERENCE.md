# Quick Reference Guide

## 🚀 Quick Start Commands

```bash
# Setup
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your API key

# Run
streamlit run app.py

# Verify setup
python verify_setup.py

# Run tests
python tests/test_system.py
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `README.md` | Complete documentation |
| `SETUP.md` | Installation instructions |
| `requirements.txt` | Python dependencies |
| `.env.example` | Configuration template |
| `verify_setup.py` | Setup checker |

## 🔑 Configuration (.env)

```env
# Required
GEMINI_API_KEY=your_key_here

# Optional
TAVILY_API_KEY=your_key_here
MAX_CONVERSATION_HISTORY=20
DEFAULT_MODEL=gemini-1.5-pro
TEMPERATURE=0.1
```

## 📊 Data Files (data/ directory)

Required CSV files from Kaggle:
- `olist_customers_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `product_category_name_translation.csv`

## 🤖 Agents Overview

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| Orchestrator | Query routing | User query | Agent assignments |
| SQL Analyst | SQL generation | Question + schema | SQL + results |
| Data Analyst | Insights | Query results | Analysis |
| Knowledge Expert | Context | Topic | Information |
| Translator | Translation | Text + language | Translation |

## 💬 Example Queries

### Sales
```
"What are the top 10 product categories by revenue?"
"Show monthly sales trends"
"What's the average order value?"
```

### Customers
```
"How many customers are from São Paulo?"
"Show customer distribution by state"
"Which cities have the most customers?"
```

### Products
```
"Which categories have the best ratings?"
"Show price range for electronics"
"What's the most popular category?"
```

### Advanced
```
"Compare revenue between Q1 and Q2"
"What's the correlation between price and satisfaction?"
"Show sellers in Rio with highest revenue"
```

## 🎨 UI Features

- **Chat Interface**: Natural language Q&A
- **Metrics Dashboard**: Quick stats at top
- **Data Tables**: Expandable result tables
- **Visualizations**: Auto-generated charts
- **SQL Viewer**: See generated queries
- **Export**: Download conversations
- **Examples**: Pre-built queries in sidebar

## 🛠️ Troubleshooting

### "API Key not configured"
```bash
# Check .env file exists
# Verify GEMINI_API_KEY is set
# Restart Streamlit
```

### "No data files found"
```bash
# Check files are in data/ directory
# Verify file names match exactly
# Try loading again
```

### "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

## 📈 Performance Tips

- Limit conversation history for faster responses
- Use specific queries rather than broad ones
- Close unused browser tabs
- Clear Streamlit cache if needed:
  ```bash
  streamlit cache clear
  ```

## 🔒 Security Notes

- Never commit API keys
- Use `.env` for secrets
- Review `.gitignore` before pushing
- Database is read-only
- Queries are validated

## 📝 Code Structure

```
src/
├── agents/          # Multi-agent system
│   ├── base_agents.py
│   └── agent_system.py
├── database/        # Data layer
│   └── db_manager.py
├── memory/          # Conversation
│   └── memory_manager.py
└── utils/           # Helpers
    ├── visualizations.py
    └── knowledge.py
```

## 🎬 Video Demo Checklist

- [ ] Record in 1080p
- [ ] 5-7 minutes total
- [ ] Include pitch (30s)
- [ ] Show live demo (3-4 min)
- [ ] Explain tech (60s)
- [ ] Discuss future (30s)
- [ ] Upload to YouTube unlisted
- [ ] Test link works

## 📤 Submission Checklist

- [ ] Code complete and tested
- [ ] Documentation reviewed
- [ ] Video recorded
- [ ] GitHub repo public
- [ ] .env.example (not .env!)
- [ ] No API keys in code
- [ ] README displays correctly
- [ ] Links tested

## 🌟 Key Selling Points

1. **Multi-agent architecture** - Not just an LLM wrapper
2. **Context-aware** - True conversation, not Q&A
3. **Production-ready** - Security, logging, error handling
4. **Auto-visualization** - Intelligent chart selection
5. **Extensible** - Easy to add features

## 🔗 Useful Links

- **Gemini API**: https://aistudio.google.com/app/apikey
- **Dataset**: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/
- **Streamlit Docs**: https://docs.streamlit.io
- **DuckDB Docs**: https://duckdb.org/docs/

## 💡 Tips for Success

### Development
- Test frequently
- Use type hints
- Add docstrings
- Handle errors
- Log important events

### Documentation
- Be clear and concise
- Use examples
- Explain "why" not just "how"
- Include diagrams
- Keep it updated

### Presentation
- Show, don't just tell
- Highlight innovations
- Admit limitations
- Discuss trade-offs
- Be enthusiastic

## 🆘 Getting Help

1. Check logs in `logs/` directory
2. Run `python verify_setup.py`
3. Review error messages
4. Check documentation
5. Test with simple queries first

## 🎯 Success Metrics

Your project should:
- ✅ Run without errors
- ✅ Load data successfully
- ✅ Answer queries correctly
- ✅ Generate visualizations
- ✅ Maintain conversation context
- ✅ Handle errors gracefully
- ✅ Have complete documentation

## 📊 Project Stats

- **Files**: 25+
- **Code**: 3,500+ lines
- **Agents**: 5 specialized
- **Features**: 15+
- **Docs**: 6 guides
- **Examples**: 100+ queries
- **Time**: 7-day timeline

## 🏁 Final Steps

1. Run full test
2. Record video
3. Review README
4. Push to GitHub
5. Upload video
6. Submit links

**Good luck! 🚀**
