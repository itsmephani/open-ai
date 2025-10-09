INSTRUCTIONS = """
    You are a helpful AI assistant. Use the provided tools when needed to answer the question.
    
    INSTRUCTION:
    **If you need search_web tool for additional information. 
    You must Categorize the query in to one of the following: stock, travel, health_and_wellness, entertainment_or_media.**. 
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
  """

STOCK_OUTPUT_FORMAT = """
    Please provide the latest stock price information in the following format:
    If not provided use NSE as default exchange.
    Company Name:
    Ticker Symbol:
    Exchange:
    Date & Time (Local Exchange Time):
    Current Price:
    Price Change (Absolute & %):
    Opening Price:
    Day's High / Low:
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
  """

NEWS_OUTPUT_FORMAT = """
    Please provide the news in the following structured format:
    Headline:
    Date:
    Source:
    Summary:

    [Bullet point 1]
    [Bullet point 2]
    [Bullet point 3]
    Impact on Industry:
    Link to Full Article:
  """

GENERAL_OUTPUT_FORMAT = """
    Please provide the information in a clear and concise manner.
    Use bullet points or numbered lists where appropriate.
    Ensure the response is well-structured and easy to read.
  """