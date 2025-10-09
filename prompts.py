INSTRUCTIONS = """
    You are a helpful AI assistant. Use the provided tools when needed to answer the question.
    INSTRUCTION:
    If you need search_web tool for additional information. Categorize the area in to following:
    stock, travel, health_and_wellness, entertainment_or_media. 
  """

WEATHER_OUTPUT_FORMAT = """
    Please provide the current weather in Hyderabad in the following structured format:
    Location:
    Date & Time:
    Temperature:
    Feels Like:
    Humidity:
    Wind Speed & Direction:
    Weather Condition:

    Format the response in Markdown for readability.
  """

STOCK_OUTPUT_FORMAT = """
    Please provide the latest stock price information in the following format:
    Company Name:
    Ticker Symbol:
    Exchange:
    Date & Time (Local Exchange Time):
    Current Price:
    Price Change (Absolute & %):
    Opening Price:
    Day's High / Low:
    Previous Close:
    Volume Traded:
    Market Cap:
    52-Week High / Low:
    P/E Ratio:
    Dividend Yield:
    Analyst Rating (if available):

    Format the response in Markdown for readability.
  """

AI_NEWS_OUTPUT_FORMAT = """
    Please provide the latest AI news in the following structured format:
    Headline:
    Date:
    Source:
    Summary:
    Key Developments:

    [Bullet point 1]
    [Bullet point 2]
    [Bullet point 3]
    Impact on Industry:
    Relevant Companies / Technologies:
    Link to Full Article:

    Format the response in Markdown for readability.
  """

TRAVEL_OUTPUT_FORMAT = """
    Please provide travel information in the following format:
    Destination:
    Best Time to Visit:
    Weather Overview:
    Top Attractions:

    [Attraction 1]
    [Attraction 2]
    [Attraction 3]
    Local Cuisine to Try:
    [Dish 1]
    [Dish 2]
    Cultural Tips / Etiquette:
    Safety & Health Advice:
    Transportation Options:
    Budget Estimate (Daily):
    Recommended Duration of Stay:
    Link to Travel Guide or Blog:

    Format the response in Markdown for readability.
  """

ENTERTAINMENT_MEDIA_OUTPUT_FORMAT = """
    Please provide entertainment and media updates in the following format:
    Title:
    Category: (e.g., Movie, TV Show, Music, Celebrity News, Gaming)
    Release Date / Event Date:
    Platform / Channel:
    Summary:
    Cast / Artists / Creators:
    Genre:
    Ratings / Reviews:
    Trending Status:
    Fun Fact or Behind-the-Scenes Info:
    Link to Trailer / Article / Official Page:
    
    Format the response in Markdown for readability.
  """

HEALTH_AND_WELLNESS_OUTPUT_FORMAT = """
    Please provide health and wellness information in the following format:
    Topic:
    Date:
    Source:
    Summary:
    Key Tips / Recommendations:

    [Tip 1]
    [Tip 2]
    [Tip 3]
    Benefits:
    Target Audience:
    Expert Insights (if available):
    Link to Full Article:

    Format the response in Markdown for readability.
  """
