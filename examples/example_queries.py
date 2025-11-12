"""
Example queries and usage scenarios for the E-Commerce Insights Agent
"""

# Sales and Revenue Analysis
SALES_QUERIES = [
    "What are the top 10 product categories by total revenue?",
    "Show me monthly sales trends for 2017",
    "Which product category has the highest average order value?",
    "What was the total revenue in Q1 2018?",
    "Compare revenue across different payment types",
    "Show me the distribution of order prices",
    "What percentage of total revenue comes from the top 5 categories?",
    "Which months had the highest sales volume?",
    "What is the average revenue per order?",
    "Show me revenue breakdown by payment installments",
]

# Customer Analysis
CUSTOMER_QUERIES = [
    "How many unique customers do we have?",
    "What is the geographic distribution of our customers?",
    "Which cities have the most customers?",
    "Show me customer distribution across Brazilian states",
    "What is the average number of orders per customer?",
    "Which state has customers with the highest average order value?",
    "How many customers are from São Paulo?",
    "Show me the top 20 cities by customer count",
    "What percentage of customers have made repeat purchases?",
    "Which ZIP codes have the most customers?",
]

# Product and Seller Analysis
PRODUCT_QUERIES = [
    "What are the most popular product categories?",
    "Which products have the highest review scores?",
    "Show me products with the most reviews",
    "What is the average price by product category?",
    "Which sellers have the highest number of orders?",
    "What categories have the best customer satisfaction?",
    "Show me the price range for electronics products",
    "Which product categories have the most items?",
    "What is the average product weight by category?",
    "Which sellers are in São Paulo?",
]

# Order and Delivery Analysis
ORDER_QUERIES = [
    "What is the average delivery time for orders?",
    "Show me order status distribution",
    "What percentage of orders were delivered on time?",
    "Which months have the longest delivery times?",
    "How many orders were delivered late?",
    "What is the average time between purchase and delivery?",
    "Show me orders by delivery status",
    "Which product categories have the fastest delivery?",
    "What percentage of orders are marked as delivered?",
    "Show me the distribution of order processing times",
]

# Review and Satisfaction Analysis
REVIEW_QUERIES = [
    "What is the overall average review score?",
    "Show me review score distribution",
    "Which product categories have the highest ratings?",
    "How many reviews have we received in total?",
    "What percentage of reviews are 5 stars?",
    "Show me products with review scores below 3",
    "Which categories have the most negative reviews?",
    "What is the correlation between price and review score?",
    "Show me review trends over time",
    "Which sellers have the best review scores?",
]

# Payment Analysis
PAYMENT_QUERIES = [
    "What are the most popular payment methods?",
    "Show me payment value distribution",
    "What is the average number of installments?",
    "Which payment type generates the highest revenue?",
    "How many orders use credit card payments?",
    "What percentage of orders are paid in installments?",
    "Show me payment methods by order value",
    "What is the average payment value?",
    "Which payment type has the highest average transaction value?",
    "Show me the distribution of payment installments",
]

# Advanced Multi-Table Queries
ADVANCED_QUERIES = [
    "Show me the top 5 product categories with their average delivery time and review score",
    "Which sellers in Rio de Janeiro have the highest revenue?",
    "What is the relationship between delivery time and customer satisfaction?",
    "Show me monthly revenue and order count trends together",
    "Which product categories are most popular in São Paulo vs Rio de Janeiro?",
    "What is the average order value for customers in each state?",
    "Show me sellers with above-average review scores and their total revenue",
    "Which payment methods are preferred for high-value orders (>R$500)?",
    "What is the customer lifetime value by state?",
    "Show me the correlation between product price and review score by category",
]

# Translation Queries
TRANSLATION_QUERIES = [
    "Translate 'beleza saude' to English",
    "What does 'cama mesa banho' mean in English?",
    "Translate the top product categories to Portuguese",
    "What is 'moveis decoracao' in English?",
    "Translate 'informatica acessorios' to English",
]

# Knowledge and Definition Queries
KNOWLEDGE_QUERIES = [
    "What is customer lifetime value?",
    "Explain what NPS score means",
    "What is a good conversion rate for e-commerce?",
    "Define average order value",
    "What does customer churn mean?",
    "Explain the importance of delivery time in e-commerce",
    "What is customer acquisition cost?",
    "Define product margin",
    "What are e-commerce KPIs?",
    "Explain what cohort analysis means",
]

# Conversational Context Examples
CONVERSATIONAL_EXAMPLES = [
    # Example 1
    [
        "What are the top 5 product categories?",
        "Show me their average prices",
        "Which of these have the best review scores?",
        "What's the delivery time for the top one?",
    ],
    # Example 2
    [
        "How many customers are in São Paulo?",
        "What's their average order value?",
        "Compare this to Rio de Janeiro",
        "Which city has higher customer satisfaction?",
    ],
    # Example 3
    [
        "Show me orders from January 2018",
        "What was the total revenue?",
        "How does this compare to February?",
        "Show me the trend for the first quarter",
    ],
    # Example 4
    [
        "Which sellers have the most orders?",
        "Show me their locations",
        "What are their average review scores?",
        "Which one has the highest revenue?",
    ],
]

# Data Exploration Queries
EXPLORATION_QUERIES = [
    "What tables are available in the database?",
    "Show me a sample of the orders table",
    "What columns does the products table have?",
    "How many records are in the customers table?",
    "Show me the schema of the order_items table",
    "What is the date range of our data?",
    "How many unique sellers do we have?",
    "What product categories exist in the data?",
    "Show me the first few customer records",
    "What states are represented in our customer base?",
]

# Visualization-Friendly Queries
VISUALIZATION_QUERIES = [
    "Show me revenue by month as a line chart",
    "Create a pie chart of payment methods",
    "Show customer distribution by state as a bar chart",
    "Plot order count trends over time",
    "Show me a heatmap of orders by day of week and hour",
    "Create a distribution chart of review scores",
    "Show revenue comparison across top 10 categories",
    "Plot delivery time distribution",
    "Show seasonal trends in order volume",
    "Create a scatter plot of price vs review score",
]

# Business Intelligence Queries
BUSINESS_QUERIES = [
    "What is our customer retention rate?",
    "Calculate the cart abandonment rate",
    "What is the average customer acquisition cost by channel?",
    "Show me the revenue growth rate month-over-month",
    "What percentage of orders result in repeat purchases?",
    "Calculate gross merchandise value (GMV) for each month",
    "What is the average time to first purchase?",
    "Show me the conversion funnel from browse to purchase",
    "What is our customer churn rate?",
    "Calculate revenue per customer by segment",
]

# Comparison Queries
COMPARISON_QUERIES = [
    "Compare sales between 2017 and 2018",
    "How do delivery times differ by product category?",
    "Compare customer satisfaction across payment methods",
    "Show me revenue differences between states",
    "Compare average order values across quarters",
    "How do review scores differ between price ranges?",
    "Compare seller performance in different cities",
    "Show me seasonal differences in product category popularity",
    "Compare payment preferences between high and low value orders",
    "How do delivery times compare between states?",
]

# Trend Analysis Queries
TREND_QUERIES = [
    "Show me sales trends over the past year",
    "What is the trend in average order value?",
    "Show customer acquisition trends by month",
    "How has customer satisfaction changed over time?",
    "Show me delivery time trends",
    "What is the trend in payment installments usage?",
    "Show me review score trends by category",
    "How has order volume changed month-over-month?",
    "Show me the trend in repeat purchase rate",
    "What is the trend in average product prices?",
]

# Example Usage
if __name__ == "__main__":
    print("E-Commerce Insights Agent - Example Queries\n")
    print("=" * 60)
    
    print("\n📊 SALES & REVENUE")
    for q in SALES_QUERIES[:5]:
        print(f"  • {q}")
    
    print("\n👥 CUSTOMER ANALYSIS")
    for q in CUSTOMER_QUERIES[:5]:
        print(f"  • {q}")
    
    print("\n📦 PRODUCT & SELLER")
    for q in PRODUCT_QUERIES[:5]:
        print(f"  • {q}")
    
    print("\n⭐ REVIEWS & SATISFACTION")
    for q in REVIEW_QUERIES[:5]:
        print(f"  • {q}")
    
    print("\n💡 KNOWLEDGE & DEFINITIONS")
    for q in KNOWLEDGE_QUERIES[:5]:
        print(f"  • {q}")
    
    print("\n🌐 TRANSLATION")
    for q in TRANSLATION_QUERIES[:3]:
        print(f"  • {q}")
    
    print("\n💬 CONVERSATIONAL EXAMPLE")
    print("  Example conversation flow:")
    for q in CONVERSATIONAL_EXAMPLES[0]:
        print(f"    → {q}")
    
    print("\n" + "=" * 60)
    print(f"Total example queries: {sum([
        len(SALES_QUERIES),
        len(CUSTOMER_QUERIES),
        len(PRODUCT_QUERIES),
        len(ORDER_QUERIES),
        len(REVIEW_QUERIES),
        len(PAYMENT_QUERIES),
        len(ADVANCED_QUERIES),
        len(TRANSLATION_QUERIES),
        len(KNOWLEDGE_QUERIES),
    ])}")
